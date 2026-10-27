# Evidence: Block 1 · Foundational (block-1)

- block type: block
- date: 2026-10-26
- resulting state: closed/verified
- story points (combined assembled cost): 4097
- execution id: 20261026.203238.059Z-80768e74

## Stories built
- Define application modules and their ownership boundaries. (architecture) [story]

## Stacked context
- implements: python.md (SP 761)
- compass: COMPASS.md (SP 752)
- implements: ARCHITECTURE.md (SP 661)
- stack: common.md (SP 1812)

## Build directory changes
- app_server/__init__.py
- cli/__init__.py
- config/__init__.py
- docs/ARCHITECTURE.md
- services/__init__.py
- tests/test_architecture.py

## Pre-build acceptance observation
- RED: architecture-service-boundary (ARCHITECTURE.md)
  intent: The application provides an importable services boundary for shared CLI and API behavior.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      services_spec = None
    --- drydock: end values ---
    Traceback (most recent call last):
      File "architecture-service-boundary.py", line 4, in <module>
        assert services_spec is not None
               ^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError

## Post-build programmatic acceptance
- PASS: architecture-service-boundary (ARCHITECTURE.md)
  intent: The application provides an importable services boundary for shared CLI and API behavior.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0

## Build summary
RESULT: SUCCESS

FILES CHANGED:
- services/__init__.py
- config/__init__.py
- cli/__init__.py
- app_server/__init__.py
- docs/ARCHITECTURE.md
- tests/test_architecture.py

SUMMARY:
Created the application boundary packages and documented module ownership, database configuration precedence, and technology roles. The focused test passed with `PYTHONPATH=.`. A plain `pytest -q` could not run because the parent Drydock pytest configuration requests an unavailable `--maxprocesses` option.

BLOCKERS:
- None
