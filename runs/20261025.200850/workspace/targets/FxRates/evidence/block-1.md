# Evidence: Block 1 · Foundational (block-1)

- block type: block
- date: 2026-10-25
- resulting state: closed/verified
- story points (combined assembled cost): 4094
- execution id: 20261025.201419.952Z-67f61b7b

## Stories built
- Establish the Python application structure and module boundaries. (architecture-foundation) [story]

## Stacked context
- implements: python.md (SP 761)
- compass: COMPASS.md (SP 752)
- implements: ARCHITECTURE.md (SP 732)
- stack: common.md (SP 1812)

## Build directory changes
- app_server/__init__.py
- bin/test.sh
- cli/__init__.py
- cli/main.py
- docs/architecture.md
- fxrates
- tests/test_architecture.py

## Pre-build acceptance observation
- RED: python-structure (ARCHITECTURE.md)
  intent: The application exposes its CLI and HTTP foundation packages.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "python-structure.py", line 3, in <module>
        assert importlib.util.find_spec("cli") is not None
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: root-entrypoint (ARCHITECTURE.md)
  intent: The application root contains the declared executable entry point.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      entrypoint = PosixPath('fxrates')
    --- drydock: end values ---
    Traceback (most recent call last):
      File "root-entrypoint.py", line 4, in <module>
        assert entrypoint.is_file()
               ^^^^^^^^^^^^^^^^^^^^
    AssertionError

## Post-build programmatic acceptance
- PASS: python-structure (ARCHITECTURE.md)
  intent: The application exposes its CLI and HTTP foundation packages.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: root-entrypoint (ARCHITECTURE.md)
  intent: The application root contains the declared executable entry point.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0

## Build summary
RESULT: SUCCESS

FILES CHANGED:

- `cli/__init__.py`
- `cli/main.py`
- `app_server/__init__.py`
- `fxrates`
- `docs/architecture.md`
- `tests/test_architecture.py`
- `bin/test.sh`

SUMMARY:

Established the CLI and HTTP service package boundaries, added the root executable and documented module ownership. The declared structure and entrypoint assertions passed. `sh bin/test.sh` passed: 4 tests.

BLOCKERS:
- None.
