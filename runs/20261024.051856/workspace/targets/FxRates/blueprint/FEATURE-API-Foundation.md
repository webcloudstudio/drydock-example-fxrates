# FEATURE: API Foundation

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Establishes the FastAPI application factory and published in-process test client. |
| Depends On  | ARCHITECTURE.md |
| Provides    | `app_server.main:create_app`, `app_server.main:app`, `app_server.testing:web_client` |

## Purpose

`app_server.main` exposes `create_app() -> FastAPI` and a module-level `app` suitable for uvicorn. `app_server.testing.web_client()` returns a test client created from the application factory.

## Programmatic Acceptance

Requires: python-package=httpx; scope=test

=== AC app-factory ===
Intent: The application factory returns a FastAPI application.

from fastapi import FastAPI
from app_server.main import create_app

assert isinstance(create_app(), FastAPI)
=== END AC app-factory ===

=== AC app-instance ===
Intent: The module exports an application instance usable by the server entry point.

from fastapi import FastAPI
from app_server.main import app

assert isinstance(app, FastAPI)
=== END AC app-instance ===

=== AC web-client ===
Intent: The published callable returns a client that can issue HTTP requests.

from fastapi.testclient import TestClient
from app_server.testing import web_client

client = web_client()
assert isinstance(client, TestClient)
response = client.get("/health")
assert response.status_code in (200, 404)
=== END AC web-client ===

## User Acceptance

- None.

## Guardrails

- The published test client is created by `app_server.testing.web_client()`.
- Route behavior is specified by the feature that owns each route.
