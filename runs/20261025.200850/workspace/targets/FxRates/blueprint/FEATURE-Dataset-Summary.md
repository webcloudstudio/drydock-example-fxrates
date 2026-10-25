# FEATURE: Dataset Summary

| Field       | Value |
|-------------|-------|
| Version     | 20261025 V1 |
| Description | Serves health, dataset counts and bounds, and the sorted currencies present in stored rates. |
| Depends On  | FEATURE-API-Foundation.md, DATABASE.md |
| Provides    | GET /health, GET /stats, GET /currencies |
| Consumes    | rates repository operations |

## Purpose

Expose health and database-derived summaries through the JSON API.

## Routes

- `GET /health` returns status 200 and `{"status":"ok"}`.
- `GET /stats` returns the count of distinct publication dates, total stored rates, and earliest and latest dates. Empty date bounds are `null`.
- `GET /currencies` returns base `EUR` and every currency with at least one stored rate, sorted ascending.

## Database Interface

- `FEATURE-RATE-003` — read: list stored rates - supplies: `currency`, `start_date`, `end_date` - returns: `date`, `currency`, `rate`

## Programmatic Acceptance

=== AC summary-routes ===
Intent: The health, statistics, and currency routes are reachable and report values derived from stored rows.

from app_server.testing import web_client
from persistence.testing import db_session

day_one = "2099-01-02"
day_two = "2099-01-03"
currency_one = "XTS"
currency_two = "XTU"
rate_one = "1.2300"
rate_two = "2.5"
with db_session() as db:
    db.rates.upsert(date=day_one, currency=currency_one, rate=rate_one)
    db.rates.upsert(date=day_two, currency=currency_two, rate=rate_two)

client = web_client()
health = client.get("/health")
stats = client.get("/stats")
currencies = client.get("/currencies")
assert health.status_code == 200
assert health.json()["status"] == "ok"
assert stats.status_code == 200
assert stats.json() == {
    "dates": 2,
    "rates": 2,
    "first": day_one,
    "last": day_two,
}
assert currencies.status_code == 200
assert currencies.json() == {
    "base": "EUR",
    "currencies": sorted([currency_one, currency_two]),
}
=== END AC summary-routes ===

## User Acceptance

- None.

## Guardrails

- Derive counts, bounds, and currencies from database queries; do not hardcode data values.
- Rates are stored and returned as published text.
- Database access goes through the shipped persistence library.
