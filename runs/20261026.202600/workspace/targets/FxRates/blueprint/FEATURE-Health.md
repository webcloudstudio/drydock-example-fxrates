# FEATURE: Health Endpoint

| Field       | Value |
|-------------|-------|
| Version     | 20261026 V1 |
| Description | Defines the service health endpoint. |
| Depends On  | FEATURE-AppServer.md |
| Provides    | GET /health |
| Consumes    | create_app() |

## Purpose

`GET /health` provides a lightweight check that the API is responding.

## Programmatic Acceptance

=== AC health-response ===
Intent: The health endpoint responds successfully with the documented JSON body.
Cite: sources/INSTRUCTIONS.md:57-58
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client

client = web_client()
response = client.get("/health")
assert response.status_code == 200
assert response.json() == {"status": "ok"}
=== END AC health-response ===

=== AC health-method ===
Intent: An unsupported method is refused by the health route.
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client

client = web_client()
response = client.post("/health")
assert response.status_code == 405
=== END AC health-method ===

## User Acceptance

- None.

## Guardrails

- The endpoint returns JSON and does not depend on stored rates.
