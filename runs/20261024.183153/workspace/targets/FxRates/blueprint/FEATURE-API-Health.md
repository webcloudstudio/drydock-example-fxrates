# FEATURE: API Health

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Exposes a health endpoint for the FxRates service. |
| Depends On  | ARCHITECTURE.md |
| Provides    | GET /health |

## Purpose

Provide `GET /health` as a lightweight service health check.

## Route

`GET /health` returns status `200` and the JSON object `{"status": "ok"}`.

## Programmatic Acceptance

=== AC health-endpoint ===
Intent: The health route is reachable and returns success.

from app_server.testing import web_client

client = web_client()
response = client.get("/health")
assert response.status_code == 200
=== END AC health-endpoint ===

## User Acceptance

- None.

## Guardrails

- Return JSON from the HTTP API.
