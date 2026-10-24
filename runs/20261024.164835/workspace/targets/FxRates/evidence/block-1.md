# Evidence: Block 1 · Foundational (block-1)

- block type: block
- date: 2026-10-24
- resulting state: closed/verified
- story points (combined assembled cost): 2533
- execution id: 20261024.165527.067Z-b312190b

## Stories built
- Establish the Python application structure and boundary ownership. (architecture-foundation) [story]

## Reusable compacts
- ARCHITECTURE_compact.md

## Stacked context
- implements: python.md (SP 761)
- compass: COMPASS.md (SP 752)
- implements: ARCHITECTURE.md (SP 951)

## Build directory changes
- .env.example
- app_server/__init__.py
- cli/__init__.py
- config.py
- pyproject.toml
- services/__init__.py
- tests/test_architecture_imports.py
- tests/test_config.py

## Pre-build acceptance observation
- RED: architecture-imports (ARCHITECTURE.md)
  intent: The application configuration and service boundary modules import successfully.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "architecture-imports.py", line 4, in <module>
        module = importlib.import_module(module_name)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/barlo/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/importlib/__init__.py", line 90, in import_module
        return _bootstrap._gcd_import(name[level:], package, level)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
      File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
      File "<frozen importlib._bootstrap>", line 1324, in _find_and_load_unlocked
    ModuleNotFoundError: No module named 'config'
- RED: database-dsn-precedence (ARCHITECTURE.md)
  intent: Database configuration resolves DATABASE_URL before DATABASE_PATH and the default path.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "database-dsn-precedence.py", line 1, in <module>
        import config
    ModuleNotFoundError: No module named 'config'

## Post-build programmatic acceptance
- PASS: architecture-imports (ARCHITECTURE.md)
  intent: The application configuration and service boundary modules import successfully.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: database-dsn-precedence (ARCHITECTURE.md)
  intent: Database configuration resolves DATABASE_URL before DATABASE_PATH and the default path.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0

## Build summary
<reusable-compact filename="ARCHITECTURE.md">
- `config.database_dsn()` resolves `DATABASE_URL`, then `DATABASE_PATH`, then `data/app.db`; runtime settings belong at the configuration boundary.
- `cli` owns command parsing and dispatch; `app_server` owns the FastAPI and HTTP boundary; `services` owns application behavior; `persistence` owns database access through the shipped persistence library.
- Application modules must not import database drivers or issue SQL. Store ECB rates as published text and use `decimal.Decimal` for arithmetic.
- Stack: Python 3.11+, FastAPI, uvicorn, SQLite, pytest, and POSIX sh.
</reusable-compact>

RESULT: SUCCESS

FILES CHANGED:
- `.env.example`
- `app_server/__init__.py`
- `cli/__init__.py`
- `config.py`
- `pyproject.toml`
- `services/__init__.py`
- `tests/test_architecture_imports.py`
- `tests/test_config.py`

SUMMARY:
Added the configuration boundary, importable application boundary packages, environment-variable documentation, project dependencies, and focused tests. Verified the declared import and DSN precedence assertions; `uv run pytest -q` passed all 6 tests, and `uv lock --check` succeeded.

BLOCKERS:
- None
