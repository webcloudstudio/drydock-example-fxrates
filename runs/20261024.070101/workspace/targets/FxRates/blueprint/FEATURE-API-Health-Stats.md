# FEATURE: API Health and Statistics

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Provides health and aggregate statistics for the rates store. |
| Depends On  | DATABASE.md |
| Provides    | GET /health, GET /stats |
| Consumes    | rates repository operations |

## Routes

### GET /health

Returns JSON `{"status": "ok"}` with HTTP 200.

### GET /stats

Returns the number of distinct publication dates and stored rates, plus the first and last publication dates. When the store is empty, `first` and `last` are null. Statistics are derived from stored rows and reflect loads completed while the server is running.

## Database Interface

- `FEATURE-RATE-002` — read: list rates with optional equality filters - supplies: `date`, `currency` - returns: `id`, `date`, `currency`, `rate`

## Programmatic Acceptance

=== AC health-route ===
Intent: The health route is reachable and returns success.

from app_server.testing import web_client

response = web_client().get("/health")
assert response.status_code == 200
assert response.json() == {"status": "ok"}
=== END AC health-route ===

=== AC stats-empty-store ===
Intent: Statistics report zero rows and null date bounds when no rates exist.

from persistence.testing import db_session
from app_server.testing import web_client

with db_session() as db:
    seeded = db.rates.list()
    assert seeded == []
response = web_client().get("/stats")
assert response.status_code == 200
body = response.json()
assert body["dates"] == 0
assert body["rates"] == 0
assert body["first"] is None
assert body["last"] is None
=== END AC stats-empty-store ===

## User Acceptance

- None.

## Guardrails

- Compute all statistics from the rates repository.
- Do not hardcode dates, counts, or rate values.
