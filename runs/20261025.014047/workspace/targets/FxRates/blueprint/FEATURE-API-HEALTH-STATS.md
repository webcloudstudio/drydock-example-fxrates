# FEATURE: API Health and Stats

| Field       | Value |
|-------------|-------|
| Version     | 20261025 V1 |
| Description | Provides health and database statistics endpoints. |
| Depends On  | DATABASE.md, ARCHITECTURE.md |
| Provides    | GET /health, GET /stats |
| Consumes    | rates.list |

## Purpose

Expose service health and counts and date bounds from stored rates. For an empty store, report zero counts and null date bounds.

## Routes

- `GET /health` returns JSON with the service status.
- `GET /stats` returns the number of publication dates with stored rates, total stored rate rows, and the earliest and latest publication dates. The date bounds are null when there are no rows.

## Programmatic Acceptance

=== AC health-route-responds ===
Intent: The health endpoint responds successfully with its declared status.
Suite: scoped

from app_server.testing import web_client

response = web_client().get("/health")
assert response.status_code == 200
assert response.json() == {"status": "ok"}
=== END AC health-route-responds ===

=== AC stats-route-responds ===
Intent: The statistics endpoint responds successfully and exposes its declared fields.
Suite: scoped

from app_server.testing import web_client

response = web_client().get("/stats")
assert response.status_code == 200
body = response.json()
assert set(body) == {"dates", "rates", "first", "last"}
assert isinstance(body["dates"], int)
assert isinstance(body["rates"], int)
=== END AC stats-route-responds ===

## User Acceptance

- None.

## Guardrails

- Derive statistics from database queries; do not hardcode counts or dates.
- All responses are JSON.
- Access persistent data only through the shipped persistence library.
