# FEATURE: Health

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | Serves GET /health returning status ok without touching the database. |
| Depends On | FEATURE-WebFoundation.md |
| Provides | GET /health |
| Consumes | app_server.main.create_app |

## Purpose

A liveness endpoint. The grader waits for it before issuing any other request.

## Routes

| Route | Method | Status | Body |
|-------|--------|--------|------|
| `/health` | GET | 200 | `{"status": "ok"}` |

The handler lives in a health router included by `create_app()`. It does not open the database.

## Database Interface

- None — persistence is owned by DATABASE.md.

## Programmatic Acceptance

=== AC health-ok ===
Intent: GET /health answers 200 with a JSON body equal to the single key status set to ok.
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client

client = web_client()
response = client.get("/health")
assert response.status_code == 200
assert response.json() == {"status": "ok"}
=== END AC health-ok ===

=== AC health-json-content-type ===
Intent: The health response is served as JSON and repeated requests give the same answer.
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client

client = web_client()
first = client.get("/health")
second = client.get("/health")
assert first.status_code == 200
assert second.status_code == 200
assert first.headers["content-type"].startswith("application/json")
assert first.json() == second.json()
=== END AC health-json-content-type ===

=== AC health-method-restricted ===
Intent: POST to /health is refused with 405 because only GET is declared.
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client

client = web_client()
response = client.post("/health")
assert response.status_code == 405
=== END AC health-method-restricted ===

## User Acceptance

- None.

## Guardrails

- The health handler never opens the database.
- The health endpoint does not initialize the schema.
