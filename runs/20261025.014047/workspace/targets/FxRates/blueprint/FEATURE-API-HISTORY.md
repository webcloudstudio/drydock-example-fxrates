# FEATURE: Currency History

| Field       | Value |
|-------------|-------|
| Version     | 20261025 V1 |
| Description | Retrieves bounded currency publication history with exact summary statistics. |
| Depends On  | ARCHITECTURE.md, DATABASE.md |
| Provides    | GET /history/{code} |
| Consumes    | rates.list |

## Purpose

Return a currency's ECB publication history, optionally bounded by inclusive `start` and `end` dates. Points are ordered by ascending publication date and retain the rate text stored in the database.

The response contains `currency`, `base`, `count`, `min`, `max`, `mean`, and `points`. Calculate minimum and maximum by numeric value while returning their stored rate text. Calculate the mean using `Decimal`, rounded half to even to six decimal places and formatted with exactly six decimals.

When the requested currency has stored rates but the selected bounds contain no points, return count zero, null statistics, and an empty points list. Return 404 when the currency has no stored rates at all, including EUR. Malformed date bounds return 422.

## Programmatic Acceptance

=== AC history-bounded-points ===
Intent: The history endpoint returns stored points in ascending date order and calculates summary fields from the supplied rates.

from decimal import Decimal, ROUND_HALF_EVEN
from app_server.testing import web_client
from persistence.testing import db_session

currency = "ZZZ"
first_date = "2099-12-30"
second_date = "2099-12-31"
first_rate = "1.2"
second_rate = "1.4"
mean = (
    (Decimal(first_rate) + Decimal(second_rate)) / Decimal(2)
).quantize(Decimal("0.000001"), rounding=ROUND_HALF_EVEN)
expected_mean = format(mean, ".6f")

with db_session() as db:
    db.rates.upsert(date=second_date, currency=currency, rate=second_rate)
    db.rates.upsert(date=first_date, currency=currency, rate=first_rate)

response = web_client().get(
    f"/history/{currency}",
    params={"start": first_date, "end": second_date},
)
assert response.status_code == 200
body = response.json()
assert body["currency"] == currency
assert body["base"] == "EUR"
assert body["count"] == 2
assert body["min"] == first_rate
assert body["max"] == second_rate
assert body["mean"] == expected_mean
assert body["points"] == [
    {"date": first_date, "rate": first_rate},
    {"date": second_date, "rate": second_rate},
]
=== END AC history-bounded-points ===

=== AC history-empty-and-unknown ===
Intent: The history endpoint distinguishes an empty bounded result from a currency with no stored rates and rejects malformed bounds.

from app_server.testing import web_client
from persistence.testing import db_session

currency = "ZZZ"
stored_date = "2099-12-30"
stored_rate = "1.2"

with db_session() as db:
    db.rates.upsert(date=stored_date, currency=currency, rate=stored_rate)

client = web_client()
empty = client.get(
    f"/history/{currency}",
    params={"start": "2099-12-31"},
)
assert empty.status_code == 200
assert empty.json()["count"] == 0
assert empty.json()["min"] is None
assert empty.json()["max"] is None
assert empty.json()["mean"] is None
assert empty.json()["points"] == []

assert client.get("/history/QQQ").status_code == 404
assert client.get(
    f"/history/{currency}",
    params={"start": "2099-13-01"},
).status_code == 422
=== END AC history-empty-and-unknown ===

## User Acceptance

- None.

## Guardrails

- Include publication dates within the supplied bounds, inclusive, in ascending order.
- Preserve stored rate text in points and in minimum and maximum fields.
- Use exact decimal arithmetic and half-even rounding for the six-decimal mean.
- Return the specified empty bounded result for a currency with stored history; return 404 when that currency has no stored rates.
