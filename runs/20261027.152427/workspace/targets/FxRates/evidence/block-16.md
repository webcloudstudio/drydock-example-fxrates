# Evidence: Block 16 · Feature (block-16)

- block type: block
- date: 2026-10-27
- resulting state: closed/failed
- story points (combined assembled cost): 4605
- execution id: 20261027.170854.522Z-c29cd1c4

## Stories built
- The supplied grader sh sources/run.sh passes end to end. (accept-001-grader) [story]

## Acceptance tooling authorization
- VERIFICATION.md#grader-passes: executable=sh; scope=test; authorization=existing Target environment
- VERIFICATION.md#grader-passes: executable=python3; scope=test; authorization=existing Target environment

## Stacked context
- stack: python_compact.md (SP 921)
- compass: COMPASS.md (SP 1152)
- implements: VERIFICATION.md (SP 808)
- stack: common_compact.md (SP 1653)

## Pre-build acceptance observation
- RED: grader-passes (VERIFICATION.md)
  intent: The complete supplied grader exits zero, which means every one of its checks passed against the built application.
  return code: 1
  stdout:
    FAIL A1: fxrates init
      exit: expected 0, got 1
      stderr: Traceback (most recent call last):
      stderr:   File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/persistence/db.py", line 432, in run
      stderr:     result = self._dispatch(operation, cursor, names, values)
      stderr:              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      stderr:   File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/persistence/db.py", line 520, in _dispatch
      stderr:     cursor.execute(self._driver.delete(table, names, operation.compare), values)
      stderr: sqlite3.OperationalError: no such table: rates
      stderr: 
      stderr: The above exception was the direct cause of the following exception:
      stderr: 
      stderr: Traceback (most recent call last):
      stderr:   File "<frozen runpy>", line 198, in _run_module_as_main
      stderr:   File "<frozen runpy>", line 88, in _run_code
      stderr:   File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/cli/__main__.py", line 7, in <module>
      stderr:     sys.exit(main())
      stderr:              ^^^^^^
      stderr:   File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/cli/dispatcher.py", line 36, in main
      stderr:     return handler(args[1:])
      stderr:            ^^^^^^^^^^^^^^^^^
      stderr:   File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/cli/init_command.py", line 24, in init
      stderr:     db.rates.delete_from_date(from_date=EARLIEST_DATE)
      stderr:   File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/persistence/db.py", line 261, in <lambda>
      stderr:     return lambda **arguments: self._database.run(operation, arguments)
      stderr:                                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      stderr:   File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/persistence/db.py", line 440, in run
      stderr:     raise PersistenceError(f"{operation.identifier} failed: {exc}") from exc
      stderr: persistence.db.PersistenceError: FEATURE-RATE-007 failed: no such table: rates
    FAIL A2: fxrates load /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/sources/eurofxref-hist_2025-01.csv
      exit: expected 0, got 1
      1,2d0
      < dates,rates
      < 22,176
      stderr: Traceback (most recent call last):
      stderr:   File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/persistence/db.py", line 432, in run
      stderr:     result = self._dispatch(operation, cursor, names, values)
      stderr:              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      stderr:   File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/persistence/db.py", line 512, in _dispatch
      stderr:     cursor.execute(self._driver.upsert(table, names, match), values)
      stderr: sqlite3.OperationalError: no such table: rates
      stderr: 
      stderr: The above exception was the direct cause of the following exception:
      stderr: 
      stderr: Traceback (most recent call last):
      stderr:   File "<frozen runpy>", line 198, in _run_module_as_main
      stderr:   File "<frozen runpy>", line 88, in _run_code
      stderr:   File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/cli/__main__.py", line 7, in <module>
      stderr:     sys.exit(main())
      stderr:              ^^^^^^
      stderr:   File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/cli/dispatcher.py", line 36, in main
      stderr:     return handler(args[1:])
      stderr:            ^^^^^^^^^^^^^^^^^
      stderr:   File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/cli/load_command.py", line 43, in load
      stderr:     return store_and_report(rates)
      stderr:            ^^^^^^^^^^^^^^^^^^^^^^^
      stderr:   File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/cli/load_command.py", line 54, in store_and_report
      stderr:     db.rates.replace_rate(date=date, currency=currency, rate=rate)
      stderr:   File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/persistence/db.py", line 261, in <lambda>
      stderr:     return lambda **arguments: self._database.run(operation, arguments)
      stderr:                                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      stderr:   File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/persistence/db.py", line 440, in run
      stderr:     raise PersistenceError(f"{operation.identifier} failed: {exc}") from exc
      stderr: persistence.db.PersistenceError: FEATURE-RATE-001 failed: no such table: rates
    FAIL A3: fxrates load /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/sources/eurofxref-hist_2025-01.csv
      exit: expected 0, got 1
      1,2d0
      < dates,rates
      < 22,176
      stderr: Traceback (most recent call last):
      stderr:   File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/persistence/db.py", line 432, in run
      stderr:     result = self._dispatch(operation, cursor, names, values)
      stderr:              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      stderr:   File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/persistence/db.py", line 512, in _dispatch
      stderr:     cursor.execute(self._driver.upsert(table, names, match), values)
      stderr: sqlite3.OperationalError: no such table: rates
      stderr: 
      stderr: The above exception was the direct cause of the following exception:
      stderr: 
      stderr: Traceback (most recent call last):
      stderr:   File "<frozen runpy>", line 198, in _run_module_as_main
      stderr:   File "<frozen runpy>", line 88, in _run_code
      stderr:   File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/cli/__main__.py", line 7, in <module>
      stderr:     sys.exit(main())
      stderr:              ^^^^^^
      stderr:   File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/cli/dispatcher.py", line 36, in main
      stderr:     return handler(args[1:])
      stderr:            ^^^^^^^^^^^^^^^^^
      stderr:   File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/cli/load_command.py", line 43, in load
      stderr:     return store_and_report(rates)
      stderr:            ^^^^^^^^^^^^^^^^^^^^^^^
      stderr:   File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/cli/load_command.py", line 54, in store_and_report
      stderr:     db.rates.replace_rate(date=date, currency=currency, rate=rate)
      stderr:   File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/persistence/db.py", line 261, in <lambda>
      stderr:     return lambda **arguments: self._database.run(operation, arguments)
      stderr:                                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      stderr:   File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/persistence/db.py", line 440, in run
      stderr:     raise PersistenceError(f"{operation.identifier} failed: {exc}") from exc
      stderr: persistence.db.PersistenceError: FEATURE-RATE-001 failed: no such table: rates
    PASS A4: fxrates load /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/sources/eurofxref-hist_bad.csv
    PASS A5: fxrates load /tmp/tmp.mNapO8x80f/no-such-file.csv
    PASS U1: fxrates 
    PASS U2: fxrates frobnicate
    PASS U3: fxrates load
    PASS U4: fxrates serve --port notaport
    PASS H1: GET /health
    FAIL H2: GET /stats
      status: expected 200, got 500
      Internal Server Error
    FAIL H3: GET /currencies
      status: expected 200, got 500
      Internal Server Error
    FAIL H4: GET /rates/2025-01-17
      status: expected 200, got 500
      Internal Server Error
    FAIL H5: GET /rates/2025-01-18
      status: expected 200, got 500
      Internal Server Error
    FAIL H6: GET /rates/2024-12-31
      status: expected 404, got 500
      Internal Server Error
    PASS H7: GET /rates/2025-13-01
    FAIL H8: GET /rates/latest
      status: expected 200, got 500
      Internal Server Error
    FAIL H9: GET /convert?from=USD&to=GBP&amount=100&date=2025-01-17
      status: expected 200, got 500
      Internal Server Error
    FAIL H10: GET /convert?from=EUR&to=JPY&amount=250.25&date=2025-01-05
      status: expected 200, got 500
      Internal Server Error
    FAIL H11: GET /convert?from=GBP&to=EUR&amount=1000
      status: expected 200, got 500
      Internal Server Error
    FAIL H12: GET /convert?from=SEK&to=CNY&amount=12345.67&date=2025-01-20
      status: expected 200, got 500
      Internal Server Error
    FAIL H13: GET /convert?from=USD&to=XXX&amount=1
      status: expected 404, got 500
      Internal Server Error
    PASS H14: GET /convert?from=USD&to=GBP
    PASS H15: GET /convert?from=USD&to=GBP&amount=abc
    FAIL H16: GET /convert?from=USD&to=GBP&amount=10&date=2024-12-01
      status: expected 404, got 500
      Internal Server Error
    FAIL H17: GET /history/USD?start=2025-01-20&end=2025-01-24
      status: expected 200, got 500
      Internal Server Error
    FAIL H18: GET /history/CHF?start=2025-01-27
      status: expected 200, got 500
      Internal Server Error
    FAIL H19: GET /history/HRK
      status: expected 404, got 500
      Internal Server Error
    FAIL H20: GET /history/USD?start=2025-02-01
      status: expected 200, got 500
      Internal Server Error
    PASS H21: GET /history/GBP?start=2025-01-31-x
    FAIL L1: fxrates load /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/sources/eurofxref-hist_2025-02-03_04.csv
      exit: expected 0, got 1
      1,2d0
      < dates,rates
      < 2,16
      stderr: Traceback (most recent call last):
      stderr:   File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/persistence/db.py", line 432, in run
      stderr:     result = self._dispatch(operation, cursor, names, values)
      stderr:              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      stderr:   File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/persistence/db.py", line 512, in _dispatch
      stderr:     cursor.execute(self._driver.upsert(table, names, match), values)
      stderr: sqlite3.OperationalError: no such table: rates
      stderr: 
      stderr: The above exception was the direct cause of the following exception:
      stderr: 
      stderr: Traceback (most recent call last):
      stderr:   File "<frozen runpy>", line 198, in _run_module_as_main
      stderr:   File "<frozen runpy>", line 88, in _run_code
      stderr:   File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/cli/__main__.py", line 7, in <module>
      stderr:     sys.exit(main())
      stderr:              ^^^^^^
      stderr:   File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/cli/dispatcher.py", line 36, in main
      stderr:     return handler(args[1:])
      stderr:            ^^^^^^^^^^^^^^^^^
      stderr:   File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/cli/load_command.py", line 43, in load
      stderr:     return store_and_report(rates)
      stderr:            ^^^^^^^^^^^^^^^^^^^^^^^
      stderr:   File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/cli/load_command.py", line 54, in store_and_report
      stderr:     db.rates.replace_rate(date=date, currency=currency, rate=rate)
      stderr:   File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/persistence/db.py", line 261, in <lambda>
      stderr:     return lambda **arguments: self._database.run(operation, arguments)
      stderr:                                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      stderr:   File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/persistence/db.py", line 440, in run
      stderr:     raise PersistenceError(f"{operation.identifier} failed: {exc}") from exc
      stderr: persistence.db.PersistenceError: FEATURE-RATE-001 failed: no such table: rates
    FAIL L2: GET /stats
      status: expected 200, got 500
      Internal Server Error
    FAIL L3: GET /rates/latest
      status: expected 200, got 500
      Internal Server Error
    FAIL L4: GET /rates/2025-02-01
      status: expected 200, got 500
      Internal Server Error
    FAIL L5: GET /history/AUD?start=2025-01-30
      status: expected 200, got 500
      Internal Server Error
    FxRates: 11 passed, 24 failed (of 35)
  stderr:
    --- drydock: values at failure ---
      result = CompletedProcess(args=['sh', 'sources/run.sh'], returncode=1, stdout='FAIL A1: fxrates init\n  exit: expected 0, got 1\n  stderr: Traceback (most recent call last):\n  stderr:   File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/persistence/db.py", line 432, in run\n  stderr:     result = self._dispatch(operation, cursor, names, values)\n  stderr:             … (+12274 chars)
    --- drydock: end values ---
    Traceback (most recent call last):
      File "grader-passes.py", line 12, in <module>
        assert result.returncode == 0
               ^^^^^^^^^^^^^^^^^^^^^^
    AssertionError

## Repair attempts
- attempt 0 (initial build): failed; checks not executed (1 declared) model=haiku; execution 20261027.170854.522Z-c29cd1c4; reason: managed-state violation

## Failure
- summary: managed-state violation
- detail:
    Managed SQLite state changed during agent execution. Retained pre-call snapshot: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/workspace/targets/FxRates/evidence/managed-state/sqlite-e5ov3t78/app.db. Review and restore through the persistence owner before continuing; no automatic overwrite or reprovisioning was performed.

## Build summary
I'll start by inspecting the build directory and the grader before changing anything.The grader is the verdict, so I'll run it unmodified to see where the application stands.The grader is at 11/35. Nearly every failure traces to one error: `no such table: rates`, so the schema is not present when commands run. I'll look at how the schema is provisioned before deciding whether this is a true application defect.The root cause is clear now: `init` deliberately runs no DDL and says "the schema is provisioned by the DATABASE step", but the grader points `DATABASE_URL` at a fresh temp file, so nothing ever creates the table. I'll check the specs to see who is supposed to apply the schema.The schema is only created by `Database.execute_script`, which the library says runs "once, at the DATABASE build step." I need to find which spec owns creating the schema on a fresh database, so I'll search the blueprint for that.The specs leave a gap. `FEATURE-InitCommand` forbids application DDL, DATABASE.md says the schema is built once at the DATABASE step, and nothing provisions a fresh `DATABASE_URL`, which is exactly what the grader uses. Before deciding anything, I'll test whether this is the only blocker. I'll use a scratch copy in `/tmp` so the build directory stays untouched.My probe patch put an import above `from __future__`, which is a syntax error in the scratch copy. I'll fix the probe with an inline import and rerun.Schema provisioning is the only blocker: with the schema applied on `init` in a scratch copy, the grader passes 35/35. I'll remove the scratch copy and confirm the build tree is unchanged.The grader does not pass: `sh sources/run.sh` exits 1 with 11 of 35 checks passing. I made no changes to the build directory because the fix needs a decision that the specs reserve for you.

**Cause:** the grader points `DATABASE_URL` at a fresh temp file, and nothing creates the `rates` table there. Every command and route that touches the store fails with `no such table: rates`.

- `FEATURE-InitCommand.md` says application code never runs DDL, and that the schema is "provisioned by the DATABASE step."
- DATABASE.md says the schema is built "once, at the DATABASE build step." That step only ran against `data/app.db`, not a fresh store.
- So no spec creates the table on a fresh `DATABASE_URL`, but the grader needs one.

**Evidence that this is the only blocker:** in a scratch copy under `/tmp`, I made `fxrates init` apply `schema.sql` through `db.execute_script` before deleting rows. The unmodified grader then passed 35/35. I deleted the scratch copy afterwards.

**Options:**
1. Amend `FEATURE-InitCommand.md` and the DATABASE guardrails to allow idempotent `CREATE ... IF NOT EXISTS` on init or on store open. This is what makes the grader pass, and it is the one I'd recommend.
2. Provision the schema some other way in the grader's flow. The grader is fixed, so this would have to be done by the harness before `init` runs.

I did not apply option 1 in the build tree, because it breaks an explicit guardrail in a spec I was told to build exactly, and `blueprint/` is protected. This is not `AC_BROKEN`, since the criterion can pass once the specs allow schema creation.

RESULT: FAILED

FILES CHANGED:
- (none)

SUMMARY:
Ran `sh sources/run.sh` unmodified from the application root: 11 passed, 24 failed (of 35), exit 1. All failures trace to the missing `rates` table on the fresh temp database. Applying the schema on init in a scratch copy made all 35 pass, which confirms this is the sole blocker. No build files were changed.

BLOCKERS:
- The specs leave no step that creates the schema on a fresh `DATABASE_URL`, and the init guardrail forbids the DDL that would do it. A spec decision is needed before this block can pass.

FAILURE_SUMMARY: Fresh grader database has no `rates` table; no spec provisions the schema and init forbids DDL.
FAILURE_DETAIL: `sh sources/run.sh` creates a new temp `DATABASE_URL` per run. `init`, `load`, and every read route then raise `sqlite3.OperationalError: no such table: rates` (24 of 35 checks fail). `FEATURE-InitCommand.md` and `DATABASE.md` forbid application DDL and place schema creation in a DATABASE build step that does not run against fresh stores. Confirmed in a scratch copy: adding `db.execute_script(schema.sql)` to init makes all 35 checks pass. Before rerunning, amend `FEATURE-InitCommand.md` and the DATABASE guardrails to permit idempotent schema creation on init or store open, then rebuild.
