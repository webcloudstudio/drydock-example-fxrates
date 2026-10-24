# FEATURE: Currency History

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Returns a currency's stored publication history and exact summary statistics. |
| Depends On  | ARCHITECTURE.md, DATABASE.md |
| Provides    | GET /history/{code} |
| Consumes    | rates.list |

## Purpose

Return the stored rates for a currency in ascending publication-date order, with optional inclusive `start` and `end` date bounds. Report count, minimum, maximum, and exact mean. The minimum and maximum are the stored text for the values selected by numeric value. The mean is rounded half to even to six decimal places and returned as a string with exactly six decimal places.

If the range has no points, return count zero, null statistics, and an empty points list. Return 404 if the currency has no stored rate at all, including EUR. Malformed date bounds return 422.

## Database Interface

- `FEATURE-RATE-002` — read: list rates for a publication date - supplies: `date` - returns: `date`, `currency`, `rate`

## Programmatic Acceptance

=== AC history-bounded-points ===
Intent: History returns stored points within inclusive date bounds, in ascending order, with summary values.

from app_server.testing import web_client
from persistence.testing import db_session

currency = "USD"
first_date = "2001-01-10"
second_date = "2001-01-11"
first_rate = "1"
second_rate = "3"

with db_session() as db:
    db.rates.upsert(date=first_date, currency=currency, rate=first_rate)
    db.rates.upsert(date=second_date, currency=currency, rate=second_rate)

response = web_client().get(
    f"/history/{currency}",
    params={"start": first_date, "end": second_date},
)
body = response.json()
assert response.status_code == 200
assert body["currency"] == currency
assert body["base"] == "EUR"
assert body["count"] == 2
assert body["min"] == first_rate
assert body["max"] == second_rate
assert body["points"] == [
    {"date": first_date, "rate": first_rate},
    {"date": second_date, "rate": second_rate},
]
=== END AC history-bounded-points ===

=== AC history-empty-range ===
Intent: An empty bounded history range returns empty points and null statistics.

from app_server.testing import web_client
from persistence.testing import db_session

currency = "CAD"
date = "2001-01-12"
rate = "1.4"

with db_session() as db:
    db.rates.upsert(date=date, currency=currency, rate=rate)

response = web_client().get(
    f"/history/{currency}",
    params={"start": "2001-01-13"},
)
body = response.json()
assert response.status_code == 200
assert body["count"] == 0
assert body["min"] is None
assert body["max"] is None
assert body["mean"] is None
assert body["points"] == []
=== END AC history-empty-range ===

=== AC history-unknown-currency ===
Intent: A currency with no stored history returns 404.

from app_server.testing import web_client

response = web_client().get("/history/XXX")
assert response.status_code == 404
=== END AC history-unknown-currency ===

=== AC history-malformed-bound ===
Intent: A malformed history date bound returns 422.

from app_server.testing import web_client

response = web_client().get("/history/USD", params={"start": "2025-01-31-x"})
assert response.status_code == 422
=== END AC history-malformed-bound ===

## User Acceptance

- None.

## Guardrails

- Preserve stored rate text in point, minimum, and maximum values.
- Calculate the mean with exact decimal arithmetic and half-to-even rounding.
- Apply date bounds inclusively and return points in ascending date order.
- Reach persistence only through the declared persistence library.
