# FEATURE: API Foundation

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Provides the shared FastAPI application factory and in-process test client. |
| Depends On  | ARCHITECTURE.md |
| Provides    | app_server.main:create_app, app_server.main:app, app_server.testing:web_client |

## Purpose

Provide the reusable FastAPI application foundation used by the HTTP feature modules. The application factory returns a FastAPI application, and the module exposes an application instance for uvicorn. The testing helper returns a FastAPI `TestClient` built from the factory.

## Interfaces

- `app_server.main.create_app() -> FastAPI`
- `app_server.main.app`: module-level FastAPI instance created by `create_app()`.
- `app_server.testing.web_client()`: returns a `fastapi.testclient.TestClient` built from `create_app()`.

HTTP feature stories register their routes with the application. This foundation does not define endpoint behavior.

## Programmatic Acceptance

=== AC api-factory ===
Intent: The application factory returns a FastAPI application and the module exposes its app instance.

from fastapi import FastAPI
from app_server.main import app, create_app

created = create_app()
assert isinstance(created, FastAPI)
assert isinstance(app, FastAPI)
=== END AC api-factory ===

=== AC api-test-client ===
Intent: The published testing helper returns a client that can issue HTTP requests.

from fastapi.testclient import TestClient
from app_server.testing import web_client

client = web_client()
assert isinstance(client, TestClient)
response = client.get("/health")
assert response.status_code != 404
=== END AC api-test-client ===

## User Acceptance

- None.

## Guardrails

- Keep the shared application factory in `app_server.main` and expose its module-level `app`.
- Use the published `app_server.testing.web_client()` helper for in-process API acceptance.
- This foundation does not replace endpoint-specific acceptance.
