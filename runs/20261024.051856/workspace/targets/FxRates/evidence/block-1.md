# Evidence: Block 1 · Foundational (block-1)

- block type: block
- date: 2026-10-24
- resulting state: closed/verified
- story points (combined assembled cost): 3843
- execution id: 20261024.052600.827Z-fe3180dc

## Stories built
- Define application modules and their ownership boundaries. (architecture) [story]

## Stacked context
- implements: python.md (SP 761)
- compass: COMPASS.md (SP 752)
- implements: ARCHITECTURE.md (SP 494)
- stack: common.md (SP 1812)

## Build directory changes
- app_server.py
- cli.py
- config.py
- persistence/__init__.py
- tests/test_architecture.py

## Pre-build acceptance observation
- RED: architecture-boundaries (ARCHITECTURE.md)
  intent: The published application packages can be imported.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "architecture-boundaries.py", line 4, in <module>
        module = importlib.import_module(name)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/barlo/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/importlib/__init__.py", line 90, in import_module
        return _bootstrap._gcd_import(name[level:], package, level)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
      File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
      File "<frozen importlib._bootstrap>", line 1324, in _find_and_load_unlocked
    ModuleNotFoundError: No module named 'cli'

## Post-build programmatic acceptance
- PASS: architecture-boundaries (ARCHITECTURE.md)
  intent: The published application packages can be imported.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0

## Build summary
RESULT: SUCCESS

FILES CHANGED:
- cli.py
- app_server.py
- persistence/__init__.py
- config.py
- tests/test_architecture.py

SUMMARY:
Created importable module boundaries for CLI dispatch, the application server, configuration, and persistence. Added a test for the declared architecture import check; the check passed and `python -m pytest -q` passed (1 test).

BLOCKERS:
- None.
