# FEATURE: Web Foundation

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | The app_server package with the create_app factory, per-request database access and the web_client fixture. |
| Depends On | ARCHITECTURE.md, DATABASE.md |
| Provides | app_server.main.create_app, app_server.testing.web_client |
| Consumes | config.database_path |

## Purpose

Provide the FastAPI application every endpoint story registers a router with.

## Interface

| Symbol | Contract |
|--------|----------|
| `app_server.main.create_app() -> FastAPI` | Builds the application and includes the routers found in `app_server/routers`. |
| `app_server.main.app` | Module-level application for `uvicorn app_server.main:app`. |
| `app_server.testing.web_client()` | Returns `fastapi.testclient.TestClient(create_app())`. |
| `app_server.deps.get_db` | Request-scoped dependency: a generator that opens `persistence.open_database(config.database_path())` per request, yields it and closes it afterwards, so a load completed by another process is visible to the next request. |

Application startup never opens or initializes the store.

## Database Interface

- None — persistence is owned by DATABASE.md.

## Programmatic Acceptance

=== AC app-factory ===
Intent: create_app returns a FastAPI application, a module-level app exists, and web_client returns a working test client.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app_server.main import app, create_app
from app_server.testing import web_client

assert isinstance(create_app(), FastAPI)
assert isinstance(app, FastAPI)
client = web_client()
assert isinstance(client, TestClient)
assert isinstance(client.app, FastAPI)
=== END AC app-factory ===

=== AC unknown-path-404 ===
Intent: A path no router owns answers 404, showing the application serves requests.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client

client = web_client()
response = client.get("/zz-no-such-route-probe")
assert response.status_code == 404
=== END AC unknown-path-404 ===

=== AC request-scoped-db ===
Intent: get_db yields an opened database exposing the rates table operations and closes cleanly when the request ends.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test

from app_server.deps import get_db
from drydock_acceptance import database_environment

with database_environment(url="web.db") as root:
    gen = get_db()
    db = next(gen)
    assert hasattr(db, "rates")
    try:
        next(gen)
        raise AssertionError("dependency must finish after one yield")
    except StopIteration:
        pass
=== END AC request-scoped-db ===

=== AC startup-does-not-initialize ===
Intent: Starting the application opens no store: with no database configured, startup leaves data/app.db uncreated.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from fastapi.testclient import TestClient

from app_server.main import create_app
from drydock_acceptance import database_environment

with database_environment() as root:
    with TestClient(create_app()) as client:
        assert client.get("/zz-no-such-route-probe").status_code == 404
    assert not (root / "data" / "app.db").exists()
=== END AC startup-does-not-initialize ===

## User Acceptance

- None.

## Guardrails

- Application startup never initializes the schema.
- The web layer reaches the store only through `persistence.open_database`; it never imports a database driver.
- The server binds only to 127.0.0.1 (enforced by the serve command).
