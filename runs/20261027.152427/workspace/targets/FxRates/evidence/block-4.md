# Evidence: Block 4 · Service (block-4)

- block type: block
- date: 2026-10-27
- resulting state: closed/verified
- story points (combined assembled cost): 11282
- execution id: 20261027.154630.706Z-4d50c4a8

## Stories built
- Report usage errors with exit 2, empty stdout, and one stderr line. (cli-001-usage-errors) [story]
- Provide bin/test.sh running the pytest suite offline, exiting zero only when every test passes. (cli-005-offline-tests) [story]
- Resolve the database location from DATABASE_URL, then DATABASE_PATH, then data/app.db. (cli-003-database-selection) [story]

## Acceptance tooling authorization
- FEATURE-CliUsageErrors.md#usage-rejected-invocations: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-CliUsageErrors.md#usage-valid-ports-pass-validation: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-CliUsageErrors.md#usage-executable-exit-2: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-OfflineTestRun.md#test-script-syntax: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-OfflineTestRun.md#test-script-runs-from-any-directory: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-DatabaseSelection.md#dbsel-url-wins-with-prefix: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-DatabaseSelection.md#dbsel-url-without-prefix: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-DatabaseSelection.md#dbsel-path-fallback: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-DatabaseSelection.md#dbsel-default-path: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-DatabaseSelection.md#dbsel-open-store: executable=python3; scope=test; authorization=existing Target environment

## Stacked context
- stack: python_compact.md (SP 921)
- compass: COMPASS.md (SP 1152)
- implements: FEATURE-CliUsageErrors.md (SP 1257)
- context: ARCHITECTURE_compact.md (SP 386)
- context: DATABASE_compact.md (SP 707)
- stack: common_compact.md (SP 1653)
- stack: cli.md (SP 2689)
- implements: FEATURE-OfflineTestRun.md (SP 811)
- implements: FEATURE-DatabaseSelection.md (SP 1370)

## Build directory changes
- cli/dispatcher.py
- cli/usage.py
- data/app.db-shm
- data/app.db-wal
- data/logs/test_2026-10-27_114825.log
- fxrates_app/config.py
- tests/test_config.py
- tests/test_launcher.py
- tests/test_usage.py

## Pre-build acceptance observation
- GREEN (prepassed): usage-rejected-invocations (FEATURE-CliUsageErrors.md)
  intent: Each malformed invocation exits 2 with empty stdout and exactly one stderr line.
  return code: 0
- RED: usage-valid-ports-pass-validation (FEATURE-CliUsageErrors.md)
  intent: Boundary ports and no port are valid, and validation raises UsageError only for invalid input.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "usage-valid-ports-pass-validation.py", line 1, in <module>
        from cli.usage import UsageError, validate
    ModuleNotFoundError: No module named 'cli.usage'
- GREEN (prepassed): usage-executable-exit-2 (FEATURE-CliUsageErrors.md)
  intent: The fxrates executable itself exits 2 with empty stdout for an unknown command.
  return code: 0
  stdout:
    error: unknown command: frobnicate
- GREEN (prepassed): test-script-syntax (FEATURE-OfflineTestRun.md)
  intent: bin/test.sh exists and parses as POSIX sh without executing.
  return code: 0
- GREEN (prepassed): test-script-runs-from-any-directory (FEATURE-OfflineTestRun.md)
  intent: Run from an unrelated working directory, the script finds the application root and the suite passes, so its exit status is zero.
  return code: 0
  stdout:
    === test started at 2026-10-27 11:46:10 ===
    Arguments: 
    Working dir: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates
    ---
    .................................                                        [100%]
    33 passed in 0.42s
    === test finished at 2026-10-27 11:46:16 with status 0 ===
- RED: dbsel-url-wins-with-prefix (FEATURE-DatabaseSelection.md)
  intent: DATABASE_URL takes precedence over DATABASE_PATH and its sqlite:// prefix is removed.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "dbsel-url-wins-with-prefix.py", line 2, in <module>
        from fxrates_app.config import database_path
    ModuleNotFoundError: No module named 'fxrates_app.config'
- RED: dbsel-url-without-prefix (FEATURE-DatabaseSelection.md)
  intent: A DATABASE_URL without the prefix is used as the file name.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "dbsel-url-without-prefix.py", line 2, in <module>
        from fxrates_app.config import database_path
    ModuleNotFoundError: No module named 'fxrates_app.config'
- RED: dbsel-path-fallback (FEATURE-DatabaseSelection.md)
  intent: With DATABASE_URL unset or empty, DATABASE_PATH is used.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "dbsel-path-fallback.py", line 2, in <module>
        from fxrates_app.config import database_path
    ModuleNotFoundError: No module named 'fxrates_app.config'
- RED: dbsel-default-path (FEATURE-DatabaseSelection.md)
  intent: With both variables unset, or both empty, the default data/app.db applies.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "dbsel-default-path.py", line 2, in <module>
        from fxrates_app.config import database_path
    ModuleNotFoundError: No module named 'fxrates_app.config'
- RED: dbsel-open-store (FEATURE-DatabaseSelection.md)
  intent: open_store opens the selected file through the persistence library without error.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "dbsel-open-store.py", line 2, in <module>
        from fxrates_app.config import open_store
    ModuleNotFoundError: No module named 'fxrates_app.config'

## Post-build programmatic acceptance
- PASS: usage-rejected-invocations (FEATURE-CliUsageErrors.md)
  intent: Each malformed invocation exits 2 with empty stdout and exactly one stderr line.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: usage-valid-ports-pass-validation (FEATURE-CliUsageErrors.md)
  intent: Boundary ports and no port are valid, and validation raises UsageError only for invalid input.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: usage-executable-exit-2 (FEATURE-CliUsageErrors.md)
  intent: The fxrates executable itself exits 2 with empty stdout for an unknown command.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
  stdout:
    error: unknown command: frobnicate
- PASS: test-script-syntax (FEATURE-OfflineTestRun.md)
  intent: bin/test.sh exists and parses as POSIX sh without executing.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: test-script-runs-from-any-directory (FEATURE-OfflineTestRun.md)
  intent: Run from an unrelated working directory, the script finds the application root and the suite passes, so its exit status is zero.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
  stdout:
    === test started at 2026-10-27 11:49:21 ===
    Arguments: 
    Working dir: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates
    ---
    ........................................................................ [ 75%]
    ........................                                                 [100%]
    96 passed in 0.92s
    === test finished at 2026-10-27 11:49:31 with status 0 ===
- PASS: dbsel-url-wins-with-prefix (FEATURE-DatabaseSelection.md)
  intent: DATABASE_URL takes precedence over DATABASE_PATH and its sqlite:// prefix is removed.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: dbsel-url-without-prefix (FEATURE-DatabaseSelection.md)
  intent: A DATABASE_URL without the prefix is used as the file name.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: dbsel-path-fallback (FEATURE-DatabaseSelection.md)
  intent: With DATABASE_URL unset or empty, DATABASE_PATH is used.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: dbsel-default-path (FEATURE-DatabaseSelection.md)
  intent: With both variables unset, or both empty, the default data/app.db applies.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: dbsel-open-store (FEATURE-DatabaseSelection.md)
  intent: open_store opens the selected file through the persistence library without error.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0

## Build summary
Baseline is 33 passing. Two stories need new code (usage validation and database selection), and `bin/test.sh` already exists and follows the spec. I'll add `cli/usage.py` and wire it into the dispatcher before dispatch.Now the database selection module.Next, the tests: usage validation, database selection, and the executable check for an unknown command.The change on disk is the import removal I just made with `sed`, so the file is as intended. Next, the config tests and the executable check.All 96 tests pass. Now I'll run `bin/test.sh` itself, which is the declared gate for this block, and check the usage acceptance cases directly.The three stories for this block are implemented, and `bin/test.sh` exits 0 with all 96 tests passing.

**What changed**

- **cli-001 usage errors:** Added `cli/usage.py` with `UsageError` and `validate(argv, registered=())`. It covers no command, unknown command, arity for `init`/`load`/`fetch`, and `serve [--port n]` with ports 1–65535. A lone `--help` after a known command passes through. `cli/dispatcher.py` calls `validate` before dispatch and prints one `error:` line to stderr, returning 2.
- **cli-005 offline tests:** `bin/test.sh` already existed and matches the spec (POSIX `sh`, runs from any directory, propagates pytest's status). I ran it and left it unchanged.
- **cli-003 database selection:** Added `fxrates_app/config.py` with `database_path()` (URL, then path, then `data/app.db`, with `sqlite://` stripped) and `open_store()`, which calls `persistence.open_database`.

**Tests added:** `tests/test_usage.py`, `tests/test_config.py`, and one subprocess test in `tests/test_launcher.py` for the `./fxrates frobnicate` acceptance case.

**Decisions to review**

- `validate` takes the registry as an optional second argument. The spec gives `validate(argv)`, but a command with a registered handler must be accepted, and passing the registry in avoids a circular import. Calling `validate(argv)` alone behaves as the spec describes.
- A command in the table with no handler yet (`serve`, `init`) exits 2 with "command not available in this build". Those handlers belong to later stories.
- The port check accepts only digits, so `+80` is rejected.

**Not run:** The spec's `dbsel-*` acceptance checks import `drydock_acceptance.database_environment`, which is not on disk, so I did not run them. My config tests cover the same cases with `monkeypatch`. I did not run `sources/run.sh`, because it needs the init, load, and serve stories that are not in this block. Nothing has been committed.

RESULT: SUCCESS

FILES CHANGED:
- cli/usage.py
- cli/dispatcher.py
- fxrates_app/config.py
- tests/test_usage.py
- tests/test_config.py
- tests/test_launcher.py

SUMMARY:
Usage validation runs before dispatch and rejects malformed invocations with exit 2, empty stdout, and one stderr line. `bin/test.sh` runs the pytest suite offline and exits 0 (96 passed). Database location resolves from DATABASE_URL, then DATABASE_PATH, then data/app.db, and opens through `persistence.open_database`. The spec's `dbsel-*` acceptance checks use a harness module not on disk, so they were not run; equivalent monkeypatch tests cover them.

<blueprint-decisions>
[{"spec":"FEATURE-CliUsageErrors.md","severity":"Low","subject":"validate signature and registry check","decision":"validate takes an optional registered collection so commands with a handler are accepted without importing the dispatcher (avoids a circular import). With no argument it behaves as validate(argv) in the spec. Is that acceptable, or should the registry check move into dispatcher.main?"}]
</blueprint-decisions>
