# Evidence: Block 2 · Foundational (block-2)

- block type: block
- date: 2026-10-24
- resulting state: closed/verified
- story points (combined assembled cost): 12403
- execution id: 20261024.052707.533Z-f67e7d93

## Stories built
- Declare the rates schema and generated persistence operations. (database) [story]
- Establish the FastAPI application and server test client. (app-server-foundation) [story]
- Establish the fxrates command entry point. (cli-foundation) [story]

## Reusable compacts
- DATABASE_compact.md
- ARCHITECTURE_compact.md

## Stacked context
- stack: python_compact.md (SP 601)
- compass: COMPASS.md (SP 752)
- implements: DATABASE.md (SP 1486)
- stack: persistence.md (SP 3834)
- stack: sqlite.md (SP 2160)
- implements: FEATURE-API-Foundation.md (SP 404)
- context: ARCHITECTURE.md (SP 494)
- context: DATABASE.md (SP 1486)
- stack: fastapi.md (SP 497)
- implements: FEATURE-CLI-Foundation.md (SP 324)
- stack: cli.md (SP 1755)

## Build directory changes
- app_server/__init__.py
- app_server/main.py
- app_server/testing.py
- bin/run.ps1
- bin/run.sh
- cli/__init__.py
- cli/__main__.py
- cli/commands.py
- cli/parser.py
- cli/testing.py
- config.py
- fxrates
- pyproject.toml
- tests/test_foundations.py
- app_server.py
- cli.py

## Pre-build acceptance observation
- RED: rates-get (DATABASE.md)
  intent: A rate can be retrieved by its unique publication date and currency key.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "rates-get.py", line 1, in <module>
        from persistence.testing import db_session
    ModuleNotFoundError: No module named 'persistence.testing'
- RED: rates-list (DATABASE.md)
  intent: Rate rows can be listed and filtered by declared equality fields.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "rates-list.py", line 1, in <module>
        from persistence.testing import db_session
    ModuleNotFoundError: No module named 'persistence.testing'
- RED: rates-upsert (DATABASE.md)
  intent: Storing a rate inserts it and replaces the value for the same date and currency.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "rates-upsert.py", line 1, in <module>
        from persistence.testing import db_session
    ModuleNotFoundError: No module named 'persistence.testing'
- RED: rates-delete (DATABASE.md)
  intent: A stored rate can be deleted by its unique publication date and currency key.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "rates-delete.py", line 1, in <module>
        from persistence.testing import db_session
    ModuleNotFoundError: No module named 'persistence.testing'
- RED: app-factory (FEATURE-API-Foundation.md)
  intent: The application factory returns a FastAPI application.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "app-factory.py", line 2, in <module>
        from app_server.main import create_app
    ModuleNotFoundError: No module named 'app_server.main'; 'app_server' is not a package
- RED: app-instance (FEATURE-API-Foundation.md)
  intent: The module exports an application instance usable by the server entry point.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "app-instance.py", line 2, in <module>
        from app_server.main import app
    ModuleNotFoundError: No module named 'app_server.main'; 'app_server' is not a package
- RED: web-client (FEATURE-API-Foundation.md)
  intent: The published callable returns a client that can issue HTTP requests.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "web-client.py", line 1, in <module>
        from fastapi.testclient import TestClient
      File "/mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py", line 1, in <module>
        from starlette.testclient import TestClient as TestClient  # noqa
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/starlette/testclient.py", line 35, in <module>
        raise RuntimeError(
    RuntimeError: The starlette.testclient module requires the httpx2 package to be installed.
    You can install this with:
        $ pip install httpx2
- RED: cli-main (FEATURE-CLI-Foundation.md)
  intent: The CLI exposes its documented callable entry point.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "cli-main.py", line 1, in <module>
        from cli import main
    ImportError: cannot import name 'main' from 'cli' (/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261024.051856/build/FxRates/cli.py)
- RED: cli-runner (FEATURE-CLI-Foundation.md)
  intent: The in-process CLI runner returns an exit code and captured output streams.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "cli-runner.py", line 1, in <module>
        from cli.testing import cli_runner
    ModuleNotFoundError: No module named 'cli.testing'; 'cli' is not a package

## Post-build programmatic acceptance
- PASS: rates-get (DATABASE.md)
  intent: A rate can be retrieved by its unique publication date and currency key.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: rates-list (DATABASE.md)
  intent: Rate rows can be listed and filtered by declared equality fields.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: rates-upsert (DATABASE.md)
  intent: Storing a rate inserts it and replaces the value for the same date and currency.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: rates-delete (DATABASE.md)
  intent: A stored rate can be deleted by its unique publication date and currency key.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: app-factory (FEATURE-API-Foundation.md)
  intent: The application factory returns a FastAPI application.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: app-instance (FEATURE-API-Foundation.md)
  intent: The module exports an application instance usable by the server entry point.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: web-client (FEATURE-API-Foundation.md)
  intent: The published callable returns a client that can issue HTTP requests.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
  stderr:
    /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
- PASS: cli-main (FEATURE-CLI-Foundation.md)
  intent: The CLI exposes its documented callable entry point.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
  stderr:
    error: a command is required
- PASS: cli-runner (FEATURE-CLI-Foundation.md)
  intent: The in-process CLI runner returns an exit code and captured output streams.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0

## Build summary
<reusable-compact filename="DATABASE.md">
# FxRates persistence contract

The generated `persistence` package is the only database access boundary. It exposes `open_database(dsn)`, `SCHEMA`, and `db.rates` operations. Rates retain ECB text exactly; arithmetic belongs in application services and uses `decimal`.

The `rates` table has `id INTEGER PRIMARY KEY`, `date TEXT NOT NULL`, `currency TEXT NOT NULL`, and `rate TEXT NOT NULL`, with a unique `(date, currency)` key.

- `rates.get(date: str, currency: str)` returns a rate row or `None`.
- `rates.list(date?: str, currency?: str)` returns rows filtered by supplied equality fields.
- `rates.upsert(date: str, currency: str, rate: str)` inserts or replaces a rate and returns its row.
- `rates.delete(date: str, currency: str)` deletes the matching row and returns its date and currency or `None`.

Resolve the database location from `DATABASE_URL`, then `DATABASE_PATH`, then `data/app.db`. `fxrates init` resets the rates store through the persistence boundary. Do not access the database driver outside `persistence/` or create schema at application startup.

Database criteria use `persistence.testing.db_session()` and its configured, provisioned store. Pass its yielded database through the operation and read back state in the same rollback transaction. Do not replace the configured store or delete unrelated records.
</reusable-compact>

<reusable-compact filename="ARCHITECTURE.md">
# FxRates module contract

- `cli` owns command dispatch and the root `./fxrates` entry point; it depends on application services and configuration.
- `app_server` owns the FastAPI factory, routes, and HTTP test client; it depends on application services.
- Application services own CSV validation, ingestion, rate lookup, conversion, and history calculations; they use only public `persistence` operations.
- `persistence` owns the database connection, schema, and generated repository operations.
- Configuration owns database location resolution from environment variables.

Python 3.11+, FastAPI, SQLite through the generated persistence library, pytest, and ECB CSV/ZIP inputs are the specified stack. Preserve published rate text and use `decimal` for calculations. The public packages `cli`, `app_server`, and `persistence` must be importable.
</reusable-compact>

RESULT: SUCCESS

FILES CHANGED:
- app_server.py (removed placeholder)
- app_server/__init__.py
- app_server/main.py
- app_server/testing.py
- bin/run.ps1
- bin/run.sh
- cli.py (removed placeholder)
- cli/__init__.py
- cli/__main__.py
- cli/commands.py
- cli/parser.py
- cli/testing.py
- config.py
- fxrates
- pyproject.toml
- tests/test_foundations.py

SUMMARY:
Implemented the FastAPI factory and test client, the `fxrates` CLI package and executable launchers, typed database configuration, and foundation tests. Preserved the already-present generated persistence package and schema. All declared foundation acceptance assertions passed; `python -m pytest -q` passed (13 tests). The executable also returned help when invoked outside the project directory.

BLOCKERS:
- None
