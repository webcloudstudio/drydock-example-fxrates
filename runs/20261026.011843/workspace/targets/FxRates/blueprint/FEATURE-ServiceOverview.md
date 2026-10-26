# FEATURE: Service Overview

| Field       | Value |
|-------------|-------|
| Version     | 20261026 V1 |
| Description | Serves health, database statistics, and available currencies. |
| Depends On  | ARCHITECTURE.md, DATABASE.md |
| Provides    | GET /health, GET /stats, GET /currencies |

## Purpose

Expose basic service health and a summary of the rates currently stored.

## Routes

| Method and path | Behavior |
|-----------------|----------|
| GET `/health` | Always returns status 200 and `{"status":"ok"}`. |
| GET `/stats` | Returns distinct publication-date count, stored-rate count, and earliest/latest publication dates. Empty date bounds are null. |
| GET `/currencies` | Returns base `EUR` and the ascending codes with at least one stored rate. |

## Database Interface

- `FEATURE-RATE-005` — read: list all stored rates - supplies: — - returns: `date`, `currency`, `rate`

## Programmatic Acceptance

=== AC overview-routes ===
Intent: Health, statistics, and currencies routes are reachable and reflect persisted state.

Requires: python-package=httpx; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

with db_session() as db:
    date = "2096-08-01"
    rate = "1.75"
    db.rates.upsert(date=date, currency="ZZZ", rate=rate)

client = web_client()
health = client.get("/health")
stats = client.get("/stats")
currencies = client.get("/currencies")
assert health.status_code == 200
assert health.json()["status"] == "ok"
assert stats.status_code == 200
assert stats.json()["dates"] >= 1
assert stats.json()["rates"] >= 1
assert stats.json()["first"] is not None
assert stats.json()["last"] is not None
assert currencies.status_code == 200
assert "ZZZ" in currencies.json()["currencies"]
=== END AC overview-routes ===

=== AC stats-empty-contract ===
Intent: Statistics expose the declared null bounds when the rates table is empty.

Requires: python-package=httpx; scope=test

from app_server.testing import web_client

client = web_client()
response = client.get("/stats")
assert response.status_code == 200
body = response.json()
assert body["first"] is None or isinstance(body["first"], str)
assert body["last"] is None or isinstance(body["last"], str)
=== END AC stats-empty-contract ===

## User Acceptance

- None.

## Guardrails

- Totals, currencies, and date bounds come from persisted rate records; do not hardcode them.
- Currency codes are returned in ascending order.
- EUR remains the API base currency with implicit rate one.
