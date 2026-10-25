# FEATURE: Currency History

| Field       | Value |
|-------------|-------|
| Version     | 20261025 V1 |
| Description | Retrieves a currency's ordered rate points and exact summary statistics over optional date bounds. |
| Depends On  | FEATURE-API-Foundation.md, DATABASE.md |
| Provides    | GET /history/{code} |
| Consumes    | rates repository operations |

## Purpose

Return a currency's stored publication points in ascending date order, optionally restricted by inclusive `start` and `end` dates.

## Request and Response

For a currency with rates, return currency code, base `EUR`, point count, published-text minimum and maximum by numeric value, six-place half-even mean text, and ordered points. If filters select no points, return count zero with null min, max, and mean and an empty point list. A currency with no stored rate at all, including EUR, returns 404. Malformed date bounds return 422.

## Database Interface

- `FEATURE-RATE-003` — read: list stored rates - supplies: `currency`, `start_date`, `end_date` - returns: `date`, `currency`, `rate`

## Programmatic Acceptance

=== AC currency-history-bounds ===
Intent: History returns the selected points in ascending order with published text and exact summary values.

from app_server.testing import web_client
from persistence.testing import db_session

currency = "XTS"
first_day = "2099-01-02"
second_day = "2099-01-03"
third_day = "2099-01-04"
first_rate = "1.0"
second_rate = "2.00"
third_rate = "3"
with db_session() as db:
    db.rates.upsert(date=second_day, currency=currency, rate=second_rate)
    db.rates.upsert(date=first_day, currency=currency, rate=first_rate)
    db.rates.upsert(date=third_day, currency=currency, rate=third_rate)

response = web_client().get(
    "/history/" + currency,
    params={"start": first_day, "end": second_day},
)
assert response.status_code == 200
assert response.json() == {
    "currency": currency,
    "base": "EUR",
    "count": 2,
    "min": first_rate,
    "max": second_rate,
    "mean": "1.500000",
    "points": [
        {"date": first_day, "rate": first_rate},
        {"date": second_day, "rate": second_rate},
    ],
}
=== END AC currency-history-bounds ===

=== AC currency-history-empty-and-errors ===
Intent: Empty bounded history returns the declared empty result, and unknown currencies and malformed bounds return the declared statuses.

from app_server.testing import web_client
from persistence.testing import db_session

currency = "XTS"
day = "2099-01-02"
rate = "1.25"
with db_session() as db:
    db.rates.upsert(date=day, currency=currency, rate=rate)

client = web_client()
empty = client.get(
    "/history/" + currency,
    params={"start": "2100-01-01"},
)
assert empty.status_code == 200
assert empty.json() == {
    "currency": currency,
    "base": "EUR",
    "count": 0,
    "min": None,
    "max": None,
    "mean": None,
    "points": [],
}
assert client.get("/history/XXX").status_code == 404
assert client.get(
    "/history/" + currency,
    params={"start": "2099-13-01"},
).status_code == 422
=== END AC currency-history-empty-and-errors ===

## User Acceptance

- None.

## Guardrails

- Return points in ascending publication date order with inclusive bounds.
- Preserve stored text for points, minimum, and maximum; compare rate values numerically.
- Compute the mean exactly with decimal arithmetic and round half to even to six decimal places.
- Database access goes through the shipped persistence library.
