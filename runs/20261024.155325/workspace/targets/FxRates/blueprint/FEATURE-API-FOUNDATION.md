# FEATURE: API Foundation

| Field | Value |
|-------|-------|
| Version | 20261024 V1 |
| Description | Establishes the FastAPI application factory and in-process test client. |
| Depends On | ARCHITECTURE.md |
| Provides | app_server.main:create_app, app_server.testing:web_client |

## Purpose

Expose `app_server.main.create_app()` returning a FastAPI application, a module-level `app` for uvicorn, and `app_server.testing.web_client()` returning a FastAPI `TestClient`.

This foundation provides the application shell. Endpoint behavior belongs to the API feature specifications.

## Programmatic Acceptance

=== AC api-factory ===
Intent: The application factory returns a FastAPI application.

from fastapi import FastAPI
from app_server.main import create_app

app = create_app()
assert isinstance(app, FastAPI)
=== END AC api-factory ===

=== AC api-test-client ===
Intent: The published testing helper returns a client that can issue requests.

from fastapi.testclient import TestClient
from app_server.testing import web_client

client = web_client()
assert isinstance(client, TestClient)
=== END AC api-test-client ===

## User Acceptance

- None.

## Guardrails

- Keep endpoint behavior in the API feature specifications.
- The module-level application must be usable by `uvicorn app_server.main:app`.
