# Evidence: Block 2 · Foundational (block-2)

- block type: block
- date: 2026-10-24
- resulting state: closed/verified
- story points (combined assembled cost): 12992
- execution id: 20261024.165747.279Z-17e50eb1

## Stories built
- Declare the rates store and generated persistence operations. (database-foundation) [story]
- Establish the FastAPI application and test client. (api-foundation) [story]
- Establish the fxrates command entry point. (cli-foundation) [story]

## Reusable compacts
- DATABASE_compact.md

## Missing context
- context: INSTRUCTIONS.md

## Stacked context
- stack: python_compact.md (SP 601)
- compass: COMPASS.md (SP 752)
- implements: DATABASE.md (SP 1968)
- stack: persistence.md (SP 4001)
- stack: sqlite.md (SP 2195)
- implements: FEATURE-API-Foundation.md (SP 496)
- context: ARCHITECTURE_compact.md (SP 180)
- context: DATABASE.md (SP 1968)
- stack: fastapi.md (SP 497)
- implements: FEATURE-CLI-Foundation.md (SP 405)
- stack: cli.md (SP 1755)

## Build directory changes
- app_server/main.py
- app_server/testing.py
- cli/__init__.py
- cli/__main__.py
- cli/testing.py
- fxrates
- pyproject.toml
- tests/test_foundations.py

## Pre-build acceptance observation
- RED: rates-replace-roundtrip (DATABASE.md)
  intent: Replacing a date and currency stores the supplied published text and reads the persisted row back.
  error: foundation not built: `persistence` is the package the database foundation (postgres.md, sqlite.md) builds, and the build directory has no `persistence/`. The criterion exercises the built application, so it was not run.
- RED: rates-date-queries (DATABASE.md)
  intent: Date queries return only the requested publication and effective-date queries order publications newest first.
  error: foundation not built: `persistence` is the package the database foundation (postgres.md, sqlite.md) builds, and the build directory has no `persistence/`. The criterion exercises the built application, so it was not run.
- RED: rates-history-and-list (DATABASE.md)
  intent: History applies inclusive bounds in ascending order and the unfiltered list exposes stored rates.
  error: foundation not built: `persistence` is the package the database foundation (postgres.md, sqlite.md) builds, and the build directory has no `persistence/`. The criterion exercises the built application, so it was not run.
- RED: api-factory (FEATURE-API-Foundation.md)
  intent: The application factory returns a FastAPI application and the module exposes its app instance.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "api-factory.py", line 2, in <module>
        from app_server.main import app, create_app
    ModuleNotFoundError: No module named 'app_server.main'
- RED: api-test-client (FEATURE-API-Foundation.md)
  intent: The published testing helper returns a client that can issue HTTP requests.
  return code: 1
  stderr:
    /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
    Traceback (most recent call last):
      File "api-test-client.py", line 2, in <module>
        from app_server.testing import web_client
    ModuleNotFoundError: No module named 'app_server.testing'
- RED: cli-entry-points (FEATURE-CLI-Foundation.md)
  intent: The CLI entry point and in-process runner are callable.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "cli-entry-points.py", line 1, in <module>
        from cli import main
    ImportError: cannot import name 'main' from 'cli' (/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261024.164835/build/FxRates/cli/__init__.py)
- RED: fxrates-executable (FEATURE-CLI-Foundation.md)
  intent: The application root contains an executable named fxrates.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      executable = PosixPath('fxrates')
    --- drydock: end values ---
    Traceback (most recent call last):
      File "fxrates-executable.py", line 5, in <module>
        assert executable.is_file()
               ^^^^^^^^^^^^^^^^^^^^
    AssertionError

## Post-build programmatic acceptance
- PASS: rates-replace-roundtrip (DATABASE.md)
  intent: Replacing a date and currency stores the supplied published text and reads the persisted row back.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: rates-date-queries (DATABASE.md)
  intent: Date queries return only the requested publication and effective-date queries order publications newest first.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: rates-history-and-list (DATABASE.md)
  intent: History applies inclusive bounds in ascending order and the unfiltered list exposes stored rates.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: api-factory (FEATURE-API-Foundation.md)
  intent: The application factory returns a FastAPI application and the module exposes its app instance.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: api-test-client (FEATURE-API-Foundation.md)
  intent: The published testing helper returns a client that can issue HTTP requests.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
  stderr:
    /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
- PASS: cli-entry-points (FEATURE-CLI-Foundation.md)
  intent: The CLI entry point and in-process runner are callable.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: fxrates-executable (FEATURE-CLI-Foundation.md)
  intent: The application root contains an executable named fxrates.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0

## Build summary
<reusable-compact filename="DATABASE.md">
# DATABASE: FxRates — consumer contract

Store ECB rates in `rates(date, currency, rate, id)`, with unique `(date, currency)`. Keep rate values as published text. Resolve storage from `DATABASE_URL`, then `DATABASE_PATH`, then `data/app.db`. Only the generated `persistence/` package accesses the database.

Available operations:

- `rates.replace_rate(date, currency, rate)`: upsert by `(date, currency)`.
- `rates.for_date(date)`: list matching rates, ordered by currency ascending.
- `rates.latest_on_or_before(requested_date)`: list rates at the latest publication date on or before the requested date, ordered by date descending.
- `rates.latest()`: list rates at the latest publication date, ordered by date descending.
- `rates.history(currency, start_date, end_date)`: list rates in the inclusive date range, ordered by date ascending.
- `rates.all()`: list all rates, ordered by date ascending.

Each operation returns `StoredRate(date: str, currency: str, rate: str)` rows; list operations return lists. Use the generated persistence package and its configured-store rollback fixture for database access.
</reusable-compact>

RESULT: SUCCESS

FILES CHANGED:
- cli/__init__.py
- cli/testing.py
- cli/__main__.py
- fxrates
- app_server/main.py
- app_server/testing.py
- pyproject.toml
- tests/test_foundations.py

SUMMARY:
Implemented the FastAPI factory and test client, callable CLI runner and executable, and a `/health` endpoint for the foundation client check. The generated rates persistence operations were already present and passed their three acceptance checks. `uv run pytest -q`: 10 passed. Database acceptance: 3 passed. `sources/` was left untouched.

BLOCKERS:
- None
