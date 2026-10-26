# FEATURE: API Foundation

| Field       | Value |
|-------------|-------|
| Version     | 20261025 V1 |
| Description | Provides the FastAPI application factory and module-level application. |
| Depends On  | ARCHITECTURE.md, DATABASE.md |
| Provides    | `app_server.main:create_app`, `app_server.main:app`, `app_server.testing:web_client` |
| Consumes    | rates repository operations |

## Purpose

`app_server.main.create_app()` constructs the service application, and `app_server.main.app` is the module-level ASGI application used by uvicorn. `app_server.testing.web_client()` returns a TestClient for the application so API behavior can be exercised in-process.

## Programmatic Acceptance

=== AC api_factory_and_app ===
Intent: The application factory returns a FastAPI application and the module exports its application instance.
Requires: python-package=httpx; scope=test

from fastapi import FastAPI
from app_server.main import app, create_app

created = create_app()
assert isinstance(created, FastAPI)
assert isinstance(app, FastAPI)
=== END AC api_factory_and_app ===

=== AC api_test_client ===
Intent: The published web client callable returns a client for the application.
Requires: python-package=httpx; scope=test

from fastapi.testclient import TestClient
from app_server.testing import web_client

client = web_client()
assert isinstance(client, TestClient)
client.close()
=== END AC api_test_client ===

## User Acceptance

- None.

## Guardrails

- Bind the API to `127.0.0.1` when serving.
- Application database access goes through the generated persistence package.
- The API returns JSON responses.
