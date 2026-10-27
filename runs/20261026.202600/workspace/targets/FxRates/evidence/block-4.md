# Evidence: Block 4 · Service (block-4)

- block type: block
- date: 2026-10-26
- resulting state: closed/verified
- story points (combined assembled cost): 5396
- execution id: 20261026.205207.220Z-4de0908d

## Stories built
- Download and load the ECB history archive. (fetch) [story]

## Acceptance tooling authorization
- FEATURE-Fetch.md#fetch-stubbed-success: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-Fetch.md#fetch-stubbed-success: python-package=httpx2; scope=test; authorization=existing Target environment

## Stacked context
- stack: python_compact.md (SP 601)
- compass: COMPASS.md (SP 752)
- implements: FEATURE-Fetch.md (SP 645)
- context: ARCHITECTURE_compact.md (SP 142)
- context: DATABASE_compact.md (SP 146)
- stack: common_compact.md (SP 1079)
- stack: sqlite_compact.md (SP 1943)

## Build directory changes
- cli/__init__.py
- cli/commands.py
- data/app.db-shm
- data/app.db-wal
- data/logs/test_2026-10-26_165237.log
- services/rates.py
- tests/test_fetch.py

## Pre-build acceptance observation
- RED: fetch-stubbed-success (FEATURE-Fetch.md)
  intent: Fetch loads the CSV from a stubbed ECB archive and reports its fixture-derived counts.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      code = 2
    --- drydock: end values ---
    Traceback (most recent call last):
      File "fetch-stubbed-success.py", line 28, in <module>
        assert code == 0
               ^^^^^^^^^
    AssertionError
- RED: fetch-stubbed-failure (FEATURE-Fetch.md)
  intent: A failed stubbed download returns the operational failure status without standard output.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      code = 2
    --- drydock: end values ---
    Traceback (most recent call last):
      File "fetch-stubbed-failure.py", line 7, in <module>
        assert code == 1
               ^^^^^^^^^
    AssertionError

## Post-build programmatic acceptance
- PASS: fetch-stubbed-success (FEATURE-Fetch.md)
  intent: Fetch loads the CSV from a stubbed ECB archive and reports its fixture-derived counts.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261026.202600/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: fetch-stubbed-failure (FEATURE-Fetch.md)
  intent: A failed stubbed download returns the operational failure status without standard output.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261026.202600/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0

## Build summary
RESULT: SUCCESS

FILES CHANGED:
- cli/__init__.py
- cli/commands.py
- services/rates.py
- tests/test_fetch.py

SUMMARY:
Added `fxrates fetch` to download the ECB archive, extract `eurofxref-hist.csv`, and process it through the existing loader. Added offline tests for successful loading and download failure. `sh bin/test.sh` passed: 12 tests.

BLOCKERS:
- None
