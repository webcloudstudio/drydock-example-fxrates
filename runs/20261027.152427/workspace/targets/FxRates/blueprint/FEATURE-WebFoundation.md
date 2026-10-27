# FEATURE: Web Foundation

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | The app_server package with the application factory, module-level app, and web_client test callable. |
| Depends On | ARCHITECTURE.md, DATABASE.md |
| Provides | app_server.create_app, app_server.testing.web_client |

## Purpose

Provide the FastAPI application that feature stories add endpoints to, and the in-process client
used by acceptance and the pytest suite.

## Interface

```python
# app_server/main.py
def create_app() -> FastAPI: ...
app = create_app()

# app_server/routes.py
router: APIRouter   # shared registry; feature stories attach routes to it

# app_server/testing.py
def web_client() -> TestClient: ...
```

- `create_app()` builds a new `FastAPI` instance each call and includes the shared `router`.
  FastAPI's OpenAPI and docs endpoints stay enabled.
- `app` is the module-level instance for `uvicorn app_server.main:app`.
- `web_client()` returns `TestClient(create_app())`.
- Feature stories register routes on `app_server.routes.router`; static routes are registered
  before dynamic ones.

## Database Interface

- None — persistence is owned by DATABASE.md.

## Programmatic Acceptance

=== AC web-create-app ===
Intent: create_app returns a FastAPI instance each call, distinct per call, and app is a module-level FastAPI instance.
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from fastapi import FastAPI
from app_server.main import create_app, app

first = create_app()
second = create_app()
assert isinstance(first, FastAPI)
assert isinstance(second, FastAPI)
assert first is not second
assert isinstance(app, FastAPI)
=== END AC web-create-app ===

=== AC web-client-fixture ===
Intent: web_client returns a Starlette TestClient wrapping a FastAPI application.
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from fastapi import FastAPI
from fastapi.testclient import TestClient
from app_server.testing import web_client

client = web_client()
assert isinstance(client, TestClient)
assert isinstance(client.app, FastAPI)
=== END AC web-client-fixture ===

=== AC web-router-registry ===
Intent: The shared router registry exists so feature stories can attach routes to it.
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from fastapi import APIRouter
from app_server import routes

assert isinstance(routes.router, APIRouter)
=== END AC web-router-registry ===

## User Acceptance

- None.

## Guardrails

- This story invokes no endpoint owned by a later story.
- No database driver is imported in the `app_server` package.
- The server binds only to `127.0.0.1`; there is no authentication because only public ECB reference rates are served.
