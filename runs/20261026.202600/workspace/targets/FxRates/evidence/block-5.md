# Evidence: Block 5 · Service (block-5)

- block type: block
- date: 2026-10-26
- resulting state: closed/verified
- story points (combined assembled cost): 3316
- execution id: 20261026.210343.826Z-3df6a277

## Stories built
- Provide the offline pytest suite and test launcher. (tests) [story]

## Acceptance tooling authorization
- FEATURE-Tests.md#test-suite-passes: executable=sh; scope=test; authorization=existing Target environment

## Stacked context
- stack: python_compact.md (SP 601)
- compass: COMPASS.md (SP 752)
- implements: FEATURE-Tests.md (SP 496)
- context: ARCHITECTURE_compact.md (SP 142)
- context: DATABASE_compact.md (SP 146)
- stack: common_compact.md (SP 1079)

## Build directory changes
- bin/test.sh
- data/app.db
- data/app.db-shm
- data/app.db-wal
- data/logs/test_2026-10-26_165652.log
- data/logs/test_2026-10-26_165808.log
- data/logs/test_2026-10-26_165834.log
- data/logs/test_2026-10-26_165957.log
- data/logs/test_2026-10-26_170026.log
- data/logs/test_2026-10-26_170142.log
- data/logs/test_2026-10-26_170402.log
- tests/test_api.py
- tests/test_load.py

## Pre-build acceptance observation
- GREEN (prepassed): test-suite-passes (FEATURE-Tests.md)
  intent: The project's test launcher completes successfully.
  return code: 0
  stdout:
    timestamp=2026-10-26T16:55:37-04:00
    arguments=
    working_directory=/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261026.202600/build/FxRates
    ............                                                             [100%]
    12 passed in 5.83s
    completed=2026-10-26T16:55:52-04:00

## Post-build programmatic acceptance
- PASS: test-suite-passes (FEATURE-Tests.md)
  intent: The project's test launcher completes successfully.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261026.202600/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
  stdout:
    timestamp=2026-10-26T17:05:15-0400
    arguments=
    working_directory=/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261026.202600/build/FxRates
    .............................                                            [100%]
    29 passed in 11.48s
    completed=2026-10-26T17:05:35-0400

## Repair attempts
- attempt 0 (initial build): failed; 0/1 checks; 28/29 cases model=gpt-6-luna; execution 20261026.205620.188Z-e68d76e3; reason: programmatic acceptance failed: test-suite-passes
- attempt 1 (repair 1): failed; 1/1 checks model=gpt-6-luna; execution 20261026.205928.931Z-0de2b679; reason: acceptance regression: latest-rates-empty
- attempt 2 (repair 2): built; 1/1 checks model=gpt-6-luna; execution 20261026.210343.826Z-3df6a277

## Build summary
RESULT: SUCCESS

FILES CHANGED:
- None

SUMMARY:
The existing `/rates/latest` route returns 404 when the configured store is empty, and the store currently has zero rows. The offline suite passes: `sh bin/test.sh` completed with 29 tests passing. I made no changes.

BLOCKERS:
- None
