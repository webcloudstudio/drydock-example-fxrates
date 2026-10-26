# Evidence: Block 1 · Foundational (block-1)

- block type: block
- date: 2026-10-25
- resulting state: closed/verified
- story points (combined assembled cost): 4366
- execution id: 20261026.012435.745Z-4ccf5533

## Stories built
- Define the application boundaries and runtime structure. (architecture) [story]

## Stacked context
- implements: python.md (SP 761)
- compass: COMPASS.md (SP 752)
- implements: ARCHITECTURE.md (SP 990)
- stack: common.md (SP 1812)

## Build directory changes
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
  intent: The application factory and CLI entry point are importable.
  error: foundation not built: `app_server` is the package the web-server foundation (django.md, fastapi.md, flask.md) builds, and the build directory has no `app_server/`; `cli` is the package the cli foundation (cli.md) builds, and the build directory has no `cli/`. The criterion exercises the built application, so it was not run.

## Post-build programmatic acceptance
- PASS: architecture-imports (ARCHITECTURE.md)
  intent: The application factory and CLI entry point are importable.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261026.011843/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0

## Build summary
RESULT: SUCCESS

FILES CHANGED:
- pyproject.toml
- uv.lock
- config.py
- cli.py
- app_server/__init__.py
- app_server/main.py
- fxrates
- tests/test_architecture_imports.py

SUMMARY:
Added the configuration boundary, importable CLI and FastAPI application factory, and executable root launcher. Declared FastAPI, uvicorn, and pytest dependencies. The architecture import assertion and project test passed: 1 passed.

BLOCKERS:
- `pytest -q` could not run as written because pytest picked up parent-directory configuration. Running the project test with an explicit config and collection boundary passed.
