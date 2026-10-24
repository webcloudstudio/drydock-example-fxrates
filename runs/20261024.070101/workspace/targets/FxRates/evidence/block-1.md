# Evidence: Block 1 · Foundational (block-1)

- block type: block
- date: 2026-10-24
- resulting state: closed/verified
- story points (combined assembled cost): 8411
- execution id: 20261024.070717.782Z-d3efcda1

## Stories built
- Define application modules and ownership boundaries. (architecture) [story]

## Stacked context
- implements: python.md (SP 761)
- compass: COMPASS.md (SP 752)
- implements: ARCHITECTURE.md (SP 595)
- stack: common.md (SP 1812)
- stack: fastapi.md (SP 497)
- stack: sqlite.md (SP 2195)
- stack: cli.md (SP 1755)

## Build directory changes
- app_server/__init__.py
- app_server/main.py
- cli/__init__.py
- persistence/__init__.py
- tests/test_architecture.py

## Pre-build acceptance observation
- RED: architecture-imports (ARCHITECTURE.md)
  intent: The application, CLI, and persistence entry points are importable.
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
      File "<frozen importlib._bootstrap>", line 1310, in _find_and_load_unlocked
      File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
      File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
      File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
      File "<frozen importlib._bootstrap>", line 1324, in _find_and_load_unlocked
    ModuleNotFoundError: No module named 'app_server'
- RED: architecture-application-entry (ARCHITECTURE.md)
  intent: The application exposes its factory and the CLI exposes its callable entry point.
  error: foundation not built: `app_server` is the package the web-server foundation (django.md, fastapi.md, flask.md) builds, and the build directory has no `app_server/`; `cli` is the package the cli foundation (cli.md) builds, and the build directory has no `cli/`. The criterion exercises the built application, so it was not run.

## Post-build programmatic acceptance
- PASS: architecture-imports (ARCHITECTURE.md)
  intent: The application, CLI, and persistence entry points are importable.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: architecture-application-entry (ARCHITECTURE.md)
  intent: The application exposes its factory and the CLI exposes its callable entry point.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0

## Build summary
RESULT: SUCCESS

FILES CHANGED:
- cli/__init__.py
- app_server/__init__.py
- app_server/main.py
- persistence/__init__.py
- tests/test_architecture.py

SUMMARY:
Added importable CLI, FastAPI, and persistence boundaries, with tests for the declared architecture entry points. `python -m pytest -q` passed (3 tests).

BLOCKERS:
- None.
