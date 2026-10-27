# FEATURE: Application Server Foundation

| Field       | Value |
|-------------|-------|
| Version     | 20261026 V1 |
| Description | Establishes the FastAPI application factory and its in-process test client. |
| Depends On  | ARCHITECTURE.md |

## Purpose

Provide the shared FastAPI application entry point used by `uvicorn app_server.main:app` and by in-process acceptance checks.

## Interface

- `app_server.main.create_app()` returns a FastAPI application.
- `app_server.main.app` is the module-level application used by uvicorn.
- `app_server.testing.web_client()` returns a `fastapi.testclient.TestClient` for a newly created application.

This foundation registers no feature endpoints. Endpoint behavior belongs to the stories that provide those routes.

## Programmatic Acceptance

=== AC app-server-factory ===
Intent: The application factory and published test client are importable and construct the declared FastAPI interfaces.
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from fastapi import FastAPI
from fastapi.testclient import TestClient
from app_server.main import app, create_app
from app_server.testing import web_client

created = create_app()
client = web_client()
assert isinstance(created, FastAPI)
assert isinstance(app, FastAPI)
assert isinstance(client, TestClient)
assert isinstance(client.app, FastAPI)
=== END AC app-server-factory ===

## User Acceptance

- None.

## Guardrails

- Do not implement or claim endpoints owned by later feature stories in this foundation.
- Expose `create_app()` and the module-level `app` from `app_server.main`.
- The published `web_client()` callable returns a TestClient built from `create_app()`.
