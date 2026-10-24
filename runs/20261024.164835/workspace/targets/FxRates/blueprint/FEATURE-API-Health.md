# FEATURE: API Health

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Provides a JSON health response for the service. |
| Depends On  | FEATURE-API-Foundation.md |
| Provides    | GET /health |

## Purpose

Provide a lightweight health endpoint for the local JSON API.

## Route

### `GET /health`

Return status 200 and a JSON object whose `status` value is `ok`.

## Programmatic Acceptance

=== AC health-route ===
Intent: The health route answers successfully with the declared JSON status.

from app_server.testing import web_client

response = web_client().get("/health")
assert response.status_code == 200
assert response.json()["status"] == "ok"
=== END AC health-route ===

## User Acceptance

- None.

## Guardrails

- The health response is JSON.
