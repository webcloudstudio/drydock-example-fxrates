# Evidence: Block 1 · Foundational (block-1)

- block type: block
- date: 2026-10-24
- resulting state: closed/verified
- story points (combined assembled cost): 6813
- execution id: 20261024.173604.926Z-afb15dff

## Stories built
- Establish the application structure and module boundaries. (architecture) [story]

## Reusable compacts
- ARCHITECTURE_compact.md

## Stacked context
- implements: python.md (SP 761)
- compass: COMPASS.md (SP 752)
- implements: ARCHITECTURE.md (SP 812)
- stack: fastapi.md (SP 497)
- stack: sqlite.md (SP 2195)
- stack: cli.md (SP 1755)

## Build directory changes
- app_server/__init__.py
- app_server/main.py
- app_server/testing.py
- bin/test.sh
- cli/__init__.py
- cli/__main__.py
- cli/commands.py
- cli/parser.py
- cli/testing.py
- fxrates
- pyproject.toml
- tests/test_architecture_imports.py
- uv.lock

## Pre-build acceptance observation
- RED: architecture-imports (ARCHITECTURE.md)
  intent: The declared application entry points and test clients are importable.
  error: foundation not built: `app_server` is the package the web-server foundation (django.md, fastapi.md, flask.md) builds, and the build directory has no `app_server/`; `cli` is the package the cli foundation (cli.md) builds, and the build directory has no `cli/`. The criterion exercises the built application, so it was not run.

## Post-build programmatic acceptance
- PASS: architecture-imports (ARCHITECTURE.md)
  intent: The declared application entry points and test clients are importable.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
  stderr:
    /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa

## Build summary
<reusable-compact filename="ARCHITECTURE.md">
# FxRates Architecture Contract

- Python 3.11+, FastAPI, SQLite through the generated persistence package, CLI executable `./fxrates`, and pytest.
- Boundaries: `app_server` registers routes and calls services; `services` owns rate behavior and calls declared persistence operations; `cli` parses and dispatches to services or the server runner; `persistence` owns database access; `bin` provides the POSIX test launcher.
- Interfaces: `app_server.main:create_app() -> FastAPI`, module-level `app`; `cli.main(argv: list[str] | None = None) -> int`; `persistence.open_database(dsn)` and `db.rates`; `app_server.testing.web_client()`; `cli.testing.cli_runner(*args) -> (exit_code, stdout, stderr)`.
- Database location precedence: `DATABASE_URL`, then `DATABASE_PATH`, then `data/app.db`. Store published rates as text and use `decimal` for arithmetic.
- CLI commands: `init`, `load`, `fetch`, `serve`. The root executable is `fxrates`.
- Acceptance contract `architecture-imports`: the app factory, app, web client, CLI entry point, and CLI runner must be importable and callable as applicable.
- Do not access SQLite directly from the CLI or API, and do not read grader scripts or supplied data from application code.
</reusable-compact>

RESULT: SUCCESS

FILES CHANGED:
- app_server/__init__.py
- app_server/main.py
- app_server/testing.py
- bin/test.sh
- cli/__init__.py
- cli/__main__.py
- cli/commands.py
- cli/parser.py
- cli/testing.py
- fxrates
- pyproject.toml
- tests/test_architecture_imports.py
- uv.lock

SUMMARY:
Created the application and CLI module boundaries, root executable, test launcher, Python dependency metadata, and the importability test. `bin/test.sh` passed (1 test), and the declared `architecture-imports` assertions passed.

BLOCKERS:
- None.
