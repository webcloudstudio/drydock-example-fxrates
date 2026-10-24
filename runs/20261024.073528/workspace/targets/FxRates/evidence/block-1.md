# Evidence: Block 1 · Foundational (block-1)

- block type: block
- date: 2026-10-24
- resulting state: closed/failed
- story points (combined assembled cost): 8866
- execution id: 20261024.074110.972Z-9790f444

## Stories built
- Establish the Python application, FastAPI server, CLI, and generated SQLite persistence foundations. (foundation) [story]

## Acceptance tooling authorization
- ARCHITECTURE.md#app-factory: python-package=httpx; scope=test; authorization=existing Target environment

## Stacked context
- implements: python.md (SP 761)
- compass: COMPASS.md (SP 752)
- implements: ARCHITECTURE.md (SP 1008)
- stack: common.md (SP 1812)
- stack: fastapi.md (SP 497)
- stack: sqlite.md (SP 2195)
- stack: cli.md (SP 1755)

## Build directory changes
- .env.example
- .gitignore
- app_server/__init__.py
- app_server/main.py
- app_server/testing.py
- bin/run.sh
- bin/test.sh
- cli/__init__.py
- cli/__main__.py
- cli/testing.py
- config.py
- fxrates
- persistence/__init__.py
- persistence/db.py
- persistence/postgres.py
- persistence/schema.py
- persistence/sqlite.py
- pyproject.toml
- schema.sql
- tests/test_foundation.py

## Pre-build acceptance observation
- RED: app-factory (ARCHITECTURE.md)
  intent: The application factory creates a FastAPI app that answers the public health route.
  error: foundation not built: `app_server` is the package the web-server foundation (django.md, fastapi.md, flask.md) builds, and the build directory has no `app_server/`. The criterion exercises the built application, so it was not run.
- RED: architecture-boundary (ARCHITECTURE.md)
  intent: The generated persistence interface opens the configured database and exposes the declared rates operations.
  error: foundation not built: `persistence` is the package the database foundation (postgres.md, sqlite.md) builds, and the build directory has no `persistence/`. The criterion exercises the built application, so it was not run.

## Post-build programmatic acceptance
- FAIL: app-factory (ARCHITECTURE.md)
  intent: The application factory creates a FastAPI app that answers the public health route.
  provisioning: not required
  return code: 1
  error: persistence verification failed: persistence artifacts missing; rebuild the DATABASE step
  stderr:
    persistence artifacts missing; rebuild the DATABASE step
- FAIL: architecture-boundary (ARCHITECTURE.md)
  intent: The generated persistence interface opens the configured database and exposes the declared rates operations.
  provisioning: not required
  return code: 1
  error: persistence verification failed: persistence artifacts missing; rebuild the DATABASE step
  stderr:
    persistence artifacts missing; rebuild the DATABASE step

## Agent self-report (advisory)
The build agent declared a failure. This is advisory only; the programmatic acceptance above is the authority for this block's outcome.
- summary: Dependency locking blocked by duplicate parent-workspace member
- detail:
    `uv add` and `uv lock` detect another `fxrates` project in the enclosing workspace. Isolate this build from the parent workspace or resolve the duplicate workspace member, then generate `uv.lock` and rerun `bin/test.sh`.

## Failure
- summary: persistence verification failed
- detail:
    persistence artifacts missing; rebuild the DATABASE step

## Build summary
RESULT: FAILED

FILES CHANGED:
- `config.py`
- `app_server/__init__.py`
- `app_server/main.py`
- `app_server/testing.py`
- `persistence/__init__.py`
- `persistence/schema.py`
- `persistence/db.py`
- `persistence/sqlite.py`
- `persistence/postgres.py`
- `schema.sql`
- `cli/__init__.py`
- `cli/__main__.py`
- `cli/testing.py`
- `fxrates`
- `.env.example`
- `.gitignore`
- `pyproject.toml`
- `tests/test_foundation.py`
- `bin/test.sh`
- `bin/run.sh`

SUMMARY:
Implemented the foundational application, CLI, API health route, configuration, and persistence interfaces. The in-language checks pass (`2 passed` with `PYTHONPATH=. python -m pytest -q`).

BLOCKERS:
- `uv` could not resolve or lock dependencies: it detected another parent-workspace member with the same `fxrates` name. No `uv.lock` was produced, and `bin/test.sh` could not be validated using its declared command.
- `bin/test.sh` remains dependent on resolving that workspace issue before the project’s required test workflow can pass.

FAILURE_SUMMARY: Dependency locking blocked by duplicate parent-workspace member
FAILURE_DETAIL: `uv add` and `uv lock` detect another `fxrates` project in the enclosing workspace. Isolate this build from the parent workspace or resolve the duplicate workspace member, then generate `uv.lock` and rerun `bin/test.sh`.

## Diagnosis

CAUSE: `DATABASE` produced no persistence artifacts, so block-1 acceptance could not verify the app or database interface.
DO: Inspect `persistence/` and rebuild the `DATABASE` step to generate its artifacts.
DO: Run `drydock build FxRates --step block-1`.
