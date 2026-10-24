# Evidence: Block 1 · Foundational (block-1)

- block type: block
- date: 2026-10-24
- resulting state: closed/verified
- story points (combined assembled cost): 3959
- execution id: 20261024.145840.366Z-ba93a8f1

## Stories built
- Establish the Python application structure and module boundaries. (architecture-foundation) [story]

## Stacked context
- implements: python.md (SP 761)
- compass: COMPASS.md (SP 752)
- implements: ARCHITECTURE.md (SP 601)
- stack: common.md (SP 1812)

## Build directory changes
- ARCHITECTURE.md
- app_server/__init__.py
- app_server/main.py
- cli.py
- config.py
- fxrates
- pyproject.toml
- tests/test_architecture_imports.py
- uv.lock

## Pre-build acceptance observation
- RED: architecture-imports (ARCHITECTURE.md)
  intent: The application entry points import successfully.
  error: foundation not built: `cli` is the package the cli foundation (cli.md) builds, and the build directory has no `cli/`; `app_server` is the package the web-server foundation (django.md, fastapi.md, flask.md) builds, and the build directory has no `app_server/`. The criterion exercises the built application, so it was not run.

## Post-build programmatic acceptance
- PASS: architecture-imports (ARCHITECTURE.md)
  intent: The application entry points import successfully.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0

## Build summary
RESULT: SUCCESS

FILES CHANGED:
- `config.py`
- `cli.py`
- `app_server/__init__.py`
- `app_server/main.py`
- `fxrates`
- `ARCHITECTURE.md`
- `tests/test_architecture_imports.py`
- `pyproject.toml`
- `uv.lock`

SUMMARY:
Created the application module boundaries, documented their ownership, and added the root executable and import acceptance test. Verified FastAPI and uvicorn package names against PyPI and generated the lock with `uv`. `pytest -q` passed: 1 test.

BLOCKERS:
- None
