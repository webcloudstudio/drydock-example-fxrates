# FEATURE: API Foundation

| Field       | Value |
|-------------|-------|
| Version     | 20261025 V1 |
| Description | Establishes the FastAPI application factory and local uvicorn entry point. |
| Depends On  | ARCHITECTURE.md, DATABASE.md |
| Provides    | FastAPI application factory, uvicorn server entry point |
| Consumes    | rates repository operations |

## Purpose

Create `app_server.main.create_app() -> FastAPI` and expose the module-level `app` for `uvicorn app_server.main:app`. The service binds to `127.0.0.1`; the CLI `serve` command starts uvicorn in the foreground and supports clean termination by SIGTERM. Application code uses the generated persistence package and the configured database location.

## Configuration

Resolve the database location from `DATABASE_URL`, then `DATABASE_PATH`, then `data/app.db`. Do not open a database driver outside the generated persistence package.

## Programmatic Acceptance

Requires: python-package=httpx; scope=test

=== AC api-factory ===
Intent: The application factory returns a FastAPI application and the module exposes its application instance.

from fastapi import FastAPI
from app_server.main import app, create_app

created = create_app()
assert isinstance(created, FastAPI)
assert isinstance(app, FastAPI)
=== END AC api-factory ===

Requires: python-package=httpx; scope=test

=== AC api-test-client ===
Intent: The published web client constructs a client for the application factory.

from fastapi.testclient import TestClient
from app_server.testing import web_client

client = web_client()
assert isinstance(client, TestClient)
response = client.get("/health")
assert response.status_code in (200, 404)
=== END AC api-test-client ===

## User Acceptance

- None.

## Guardrails

- Bind the HTTP service to `127.0.0.1`.
- Use FastAPI served by uvicorn.
- Keep database access inside the generated persistence package.
- Support clean shutdown on SIGTERM.
