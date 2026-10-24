# FEATURE: API Health and Statistics

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Reports service health and statistics for stored rate publications. |
| Depends On  | FEATURE-API-FOUNDATION.md, DATABASE.md |
| Provides    | GET /health, GET /stats |
| Consumes    | rates repository operations |

## Purpose

Provide a health response and statistics computed from the rates store. Statistics include the number of publication dates, stored rates, and first and last publication dates; empty stores have null bounds.

## Database Interface

- `FEATURE-DATA-007` — read: find the latest publication date - supplies: `date` - returns: `date`
- `FEATURE-DATA-008` — read: enumerate publication dates for statistics - supplies: `date` - returns: `date`

## Routes

| Method | Path | Behavior |
|--------|------|----------|
| GET | `/health` | Returns `{"status":"ok"}`. |
| GET | `/stats` | Returns date and rate counts and publication bounds; bounds are null when no rates are stored. |

## Programmatic Acceptance

Requires: python-package=httpx; scope=test

=== AC status-health ===
Intent: The health route responds successfully with the declared status field.

from app_server.testing import web_client

client = web_client()
response = client.get("/health")
assert response.status_code == 200
body = response.json()
assert body["status"] == "ok"
=== END AC status-health ===

=== AC status-statistics ===
Intent: Statistics reflect a publication and rate added through the declared persistence interface.

from app_server.testing import web_client
from persistence.testing import db_session

date = "2099-03-01"
currency = "TST"
rate = "1.2300"
with db_session() as db:
    before = db.rates.publication_stats()
    db.rates.upsert(date=date, currency=currency, rate=rate)
    response = web_client().get("/stats")
assert response.status_code == 200
body = response.json()
assert body["dates"] == len(before) + 1
assert body["rates"] >= 1
assert body["first"] is not None
assert body["last"] is not None
=== END AC status-statistics ===

=== AC status-empty-bounds ===
Intent: An empty statistics result represents absent publication bounds as null.

from app_server.testing import web_client
from persistence.testing import db_session

with db_session() as db:
    before = db.rates.publication_stats()
    response = web_client().get("/stats")
assert response.status_code == 200
body = response.json()
if not before:
    assert body["first"] is None
    assert body["last"] is None
=== END AC status-empty-bounds ===

## User Acceptance

- None.

## Guardrails

- Counts and bounds come from stored data; do not hardcode them.
- The health route does not depend on database contents.
