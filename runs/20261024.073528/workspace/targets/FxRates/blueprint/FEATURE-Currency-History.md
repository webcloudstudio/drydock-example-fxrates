# FEATURE: Currency History

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Retrieves a currency's published rate history and summary statistics. |
| Depends On  | ARCHITECTURE.md, DATABASE.md |
| Provides    | GET /history/{code} |
| Consumes    | rates.list |

## Purpose

Return a currency's rates by publication date in ascending order. Optional `start` and `end` bounds are inclusive. Return the number of points, the stored text rates with their dates, minimum and maximum by numeric value, and the exact mean rounded half-even to six decimal places. When the range has no points for a currency that has stored rates, return count zero, null min, max, and mean, and an empty points list. A currency with no stored rates, including EUR, returns 404. Malformed or impossible bounds return 422.

## Database Interface


- None — persistence is owned by FEATURE-CLI.md, FEATURE-Rate-Loading.md.

## Programmatic Acceptance

=== AC history-points ===
Intent: History returns stored points in ascending order and reports their count.

from app_server.testing import web_client
from persistence.testing import db_session

with db_session() as db:
    first_date = "2099-01-02"
    second_date = "2099-01-03"
    currency = "QAZ"
    first_rate = "1.2"
    second_rate = "1.3"
    db.rates.upsert(date=second_date, currency=currency, rate=second_rate)
    db.rates.upsert(date=first_date, currency=currency, rate=first_rate)

client = web_client()
response = client.get(f"/history/{currency}")
assert response.status_code == 200
body = response.json()
assert body["currency"] == currency
assert body["base"] == "EUR"
assert body["count"] == 2
assert body["points"] == [
    {"date": first_date, "rate": first_rate},
    {"date": second_date, "rate": second_rate},
]
=== END AC history-points ===

=== AC history-statistics ===
Intent: History reports numeric extrema and the exact rounded mean for the selected points.

from app_server.testing import web_client
from persistence.testing import db_session

with db_session() as db:
    date_a = "2099-01-02"
    date_b = "2099-01-03"
    currency = "QAZ"
    rate_a = "1.2"
    rate_b = "1.3"
    db.rates.upsert(date=date_a, currency=currency, rate=rate_a)
    db.rates.upsert(date=date_b, currency=currency, rate=rate_b)

client = web_client()
response = client.get(f"/history/{currency}")
assert response.status_code == 200
body = response.json()
assert body["min"] == rate_a
assert body["max"] == rate_b
assert body["mean"] == "1.250000"
=== END AC history-statistics ===

=== AC empty-range ===
Intent: An empty date range for a known currency returns empty statistics.

from app_server.testing import web_client
from persistence.testing import db_session

with db_session() as db:
    date = "2099-01-02"
    currency = "QAZ"
    rate = "1.2"
    db.rates.upsert(date=date, currency=currency, rate=rate)

client = web_client()
response = client.get(f"/history/{currency}", params={"start": "2100-01-01"})
assert response.status_code == 200
body = response.json()
assert body["count"] == 0
assert body["min"] is None
assert body["max"] is None
assert body["mean"] is None
assert body["points"] == []
=== END AC empty-range ===

=== AC unknown-currency ===
Intent: A currency without stored history returns not found.

from app_server.testing import web_client

client = web_client()
response = client.get("/history/ZZZ")
assert response.status_code == 404
=== END AC unknown-currency ===

=== AC malformed-bound ===
Intent: A malformed history date bound returns the validation status.

from app_server.testing import web_client

client = web_client()
response = client.get("/history/GBP", params={"start": "2025-01-31-x"})
assert response.status_code == 422
=== END AC malformed-bound ===

## User Acceptance

- None.

## Guardrails

- Sort points by ascending publication date.
- Preserve stored rate text in points and extrema.
- Compute the mean from exact decimal values and round half-even to six decimal places.
