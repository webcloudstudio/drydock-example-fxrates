# Evidence: Block 2 · Foundational (block-2)

- block type: block
- date: 2026-10-25
- resulting state: closed/verified
- story points (combined assembled cost): 12965
- execution id: 20261025.201524.594Z-8d911462

## Stories built
- Declare the rates store and its repository operations. (database-foundation) [story]
- Establish the FastAPI application and local server entry point. (api-foundation) [story]
- Establish the fxrates command-line entry point. (cli-foundation) [story]

## Reusable compacts
- DATABASE_compact.md
- ARCHITECTURE_compact.md

## Missing context
- context: INSTRUCTIONS.md

## Stacked context
- stack: python_compact.md (SP 601)
- compass: COMPASS.md (SP 752)
- implements: DATABASE.md (SP 1455)
- stack: persistence.md (SP 4001)
- stack: sqlite.md (SP 2195)
- implements: FEATURE-API-Foundation.md (SP 484)
- context: ARCHITECTURE.md (SP 732)
- context: DATABASE.md (SP 1455)
- stack: fastapi.md (SP 497)
- implements: FEATURE-CLI-Foundation.md (SP 367)
- stack: cli.md (SP 1755)

## Build directory changes
- app_server/main.py
- app_server/testing.py
- bin/run.ps1
- bin/run.sh
- cli/__main__.py
- cli/commands.py
- cli/main.py
- cli/parser.py
- cli/testing.py
- pyproject.toml
- tests/test_foundations.py
- uv.lock

## Pre-build acceptance observation
- RED: rate-upsert-round-trip (DATABASE.md)
  intent: An upsert stores the supplied published rate text and a separate get reads it back.
  error: foundation not built: `persistence` is the package the database foundation (postgres.md, sqlite.md) builds, and the build directory has no `persistence/`. The criterion exercises the built application, so it was not run.
- RED: rate-list-filters-and-order (DATABASE.md)
  intent: The list operation returns supplied rows in ascending date and currency order and applies its declared filters.
  error: foundation not built: `persistence` is the package the database foundation (postgres.md, sqlite.md) builds, and the build directory has no `persistence/`. The criterion exercises the built application, so it was not run.
- RED: rate-delete-round-trip (DATABASE.md)
  intent: Deleting a rate removes the supplied date and currency record.
  error: foundation not built: `persistence` is the package the database foundation (postgres.md, sqlite.md) builds, and the build directory has no `persistence/`. The criterion exercises the built application, so it was not run.
- RED: api-factory (FEATURE-API-Foundation.md)
  intent: The application factory returns a FastAPI application and the module exposes its application instance.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "api-factory.py", line 2, in <module>
        from app_server.main import app, create_app
    ModuleNotFoundError: No module named 'app_server.main'
- RED: api-test-client (FEATURE-API-Foundation.md)
  intent: The published web client constructs a client for the application factory.
  return code: 1
  stderr:
    /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
    Traceback (most recent call last):
      File "api-test-client.py", line 2, in <module>
        from app_server.testing import web_client
    ModuleNotFoundError: No module named 'app_server.testing'
- RED: cli-entrypoint (FEATURE-CLI-Foundation.md)
  intent: The published CLI entry point is callable and returns a usage error for an unknown command.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "cli-entrypoint.py", line 4, in <module>
        assert main(["frobnicate"]) == 2
               ^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: cli-runner (FEATURE-CLI-Foundation.md)
  intent: The published CLI runner returns an exit code and captured output streams for a usage error.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "cli-runner.py", line 1, in <module>
        from cli.testing import cli_runner
    ModuleNotFoundError: No module named 'cli.testing'

## Post-build programmatic acceptance
- PASS: rate-upsert-round-trip (DATABASE.md)
  intent: An upsert stores the supplied published rate text and a separate get reads it back.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: rate-list-filters-and-order (DATABASE.md)
  intent: The list operation returns supplied rows in ascending date and currency order and applies its declared filters.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: rate-delete-round-trip (DATABASE.md)
  intent: Deleting a rate removes the supplied date and currency record.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: api-factory (FEATURE-API-Foundation.md)
  intent: The application factory returns a FastAPI application and the module exposes its application instance.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: api-test-client (FEATURE-API-Foundation.md)
  intent: The published web client constructs a client for the application factory.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
  stderr:
    /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
- PASS: cli-entrypoint (FEATURE-CLI-Foundation.md)
  intent: The published CLI entry point is callable and returns a usage error for an unknown command.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
  stderr:
    usage: fxrates [-h] {init,load,fetch,serve} ...
    fxrates: error: argument command: invalid choice: 'frobnicate' (choose from init, load, fetch, serve)
- PASS: cli-runner (FEATURE-CLI-Foundation.md)
  intent: The published CLI runner returns an exit code and captured output streams for a usage error.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0

## Build summary
<reusable-compact filename="DATABASE.md">
# FxRates Persistence Contract

- Use the generated `persistence` package as the only database access boundary. Resolve the store from `DATABASE_URL`, then `DATABASE_PATH`, then `data/app.db`.
- `rates` stores `date`, `currency`, and published `rate` as text, with a surrogate integer `id` and a unique `(date, currency)` key.
- Repository operations: `rates.upsert(date, currency, rate)`, `rates.get(date, currency)`, `rates.list(currency?, start_date?, end_date?)` ordered by date then currency ascending, and `rates.delete(date, currency)`.
- Preserve rate text exactly. Do not access the database driver outside `persistence/` or create schema at application startup.
</reusable-compact>

<reusable-compact filename="ARCHITECTURE.md">
# FxRates Architecture Contract

- Python 3.11+ application with a root `./fxrates` executable, `cli` package, and `app_server` FastAPI package.
- `app_server.main` provides `create_app() -> FastAPI` and module-level `app`; serve locally on `127.0.0.1` with uvicorn and support clean SIGTERM shutdown.
- Application code uses the generated `persistence` boundary and configured database location. Preserve rates as published text and use decimal arithmetic for calculations.
- Do not read `sources/run.sh` or supplied data files from application code. Validate a complete input file before its first write.
</reusable-compact>

RESULT: SUCCESS

FILES CHANGED:
- app_server/main.py
- app_server/testing.py
- bin/run.ps1
- bin/run.sh
- cli/__main__.py
- cli/commands.py
- cli/main.py
- cli/parser.py
- cli/testing.py
- pyproject.toml
- tests/test_foundations.py
- uv.lock

SUMMARY:
Implemented the FastAPI factory and test client, CLI dispatch and in-process runner, root command launch support, and declared FastAPI/uvicorn/httpx dependencies. The existing generated persistence outputs were already present and left unchanged. `sh bin/test.sh` passed (10 tests); the declared foundation acceptance assertions passed.

BLOCKERS:
- None
