# Evidence: Block 1 · Foundational (block-1)

- block type: block
- date: 2026-10-25
- resulting state: closed/verified
- story points (combined assembled cost): 2206
- execution id: 20261025.230904.114Z-2491ee4f

## Stories built
- Define application modules and their ownership boundaries. (architecture) [story]

## Reusable compacts
- ARCHITECTURE_compact.md

## Stacked context
- implements: python.md (SP 761)
- compass: COMPASS.md (SP 752)
- implements: ARCHITECTURE.md (SP 644)

## Build directory changes
- app_server/__init__.py
- app_server/main.py
- cli.py
- config.py
- persistence/__init__.py
- persistence/db.py
- pyproject.toml
- services/__init__.py
- tests/test_architecture_modules.py
- uv.lock

## Pre-build acceptance observation
- RED: architecture_modules_import (ARCHITECTURE.md)
  intent: The application module boundaries are importable and expose the declared API and CLI entry points.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "architecture_modules_import.py", line 3, in <module>
        cli = importlib.import_module("cli")
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/barlo/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/importlib/__init__.py", line 90, in import_module
        return _bootstrap._gcd_import(name[level:], package, level)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
      File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
      File "<frozen importlib._bootstrap>", line 1324, in _find_and_load_unlocked
    ModuleNotFoundError: No module named 'cli'

## Post-build programmatic acceptance
- PASS: architecture_modules_import (ARCHITECTURE.md)
  intent: The application module boundaries are importable and expose the declared API and CLI entry points.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.230142/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0

## Build summary
<reusable-compact filename="ARCHITECTURE.md">
- Python 3.11+; FastAPI and uvicorn; SQLite through the `persistence` package; pytest.
- Module ownership: `config` resolves runtime settings from environment variables; `cli` parses and dispatches commands; `app_server` owns the FastAPI factory and routes; `services` owns feature behavior; `persistence` owns database connections and repository operations.
- Routes delegate to services. Features call declared persistence operations and do not open a database driver or issue SQL directly.
- Export `cli.main`, `app_server.main.create_app`, `app_server.main.app`, and `persistence.open_database`.
- Database location precedence: `DATABASE_URL`, then `DATABASE_PATH`, then `data/app.db`.
- Store ECB rates as published text and use `Decimal` for arithmetic.
- Acceptance import check: the four declared entry points must import and be callable or non-null as specified.
</reusable-compact>

RESULT: SUCCESS

FILES CHANGED:
- pyproject.toml
- uv.lock
- config.py
- cli.py
- app_server/__init__.py
- app_server/main.py
- services/__init__.py
- persistence/__init__.py
- persistence/db.py
- tests/test_architecture_modules.py

SUMMARY:
Created the declared module boundaries, added the application import entry points, and configured database setting precedence. Added FastAPI, uvicorn, and pytest through `uv`. The architecture import check and two configuration checks passed: 3 tests.

BLOCKERS:
- Full pytest invocation inherits an unsupported `--maxprocesses=8` option from the parent project configuration. The targeted checks passed with that inherited `addopts` setting cleared.
