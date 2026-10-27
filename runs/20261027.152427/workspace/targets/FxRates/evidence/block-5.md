# Evidence: Block 5 · Service (block-5)

- block type: block
- date: 2026-10-27
- resulting state: closed/verified
- story points (combined assembled cost): 8862
- execution id: 20261027.155024.560Z-6475a427

## Stories built
- `fxrates init` resets the rates table to empty, prints nothing, exits 0. (cli-002-init) [story]

## Acceptance tooling authorization
- FEATURE-InitCommand.md#init-empties-store: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-InitCommand.md#init-idempotent: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-InitCommand.md#init-rejects-extra-argument: executable=python3; scope=test; authorization=existing Target environment

## Stacked context
- stack: python_compact.md (SP 921)
- compass: COMPASS.md (SP 1152)
- implements: FEATURE-InitCommand.md (SP 1265)
- context: ARCHITECTURE_compact.md (SP 386)
- context: DATABASE_compact.md (SP 707)
- stack: common_compact.md (SP 1653)
- stack: cli.md (SP 2689)

## Build directory changes
- cli/__init__.py
- cli/init_command.py
- data/app.db-shm
- data/app.db-wal
- data/logs/test_2026-10-27_115234.log
- tests/test_init.py

## Pre-build acceptance observation
- RED: init-empties-store (FEATURE-InitCommand.md)
  intent: After init, rates seeded through the repository are gone, and init prints nothing and exits 0.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      code = 2
    --- drydock: end values ---
    Traceback (most recent call last):
      File "init-empties-store.py", line 11, in <module>
        assert code == 0
               ^^^^^^^^^
    AssertionError
- RED: init-idempotent (FEATURE-InitCommand.md)
  intent: Running init twice in a row exits 0 both times, prints nothing, and leaves the store empty.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      code = 2
    --- drydock: end values ---
    Traceback (most recent call last):
      File "init-idempotent.py", line 8, in <module>
        assert code == 0
               ^^^^^^^^^
    AssertionError
- GREEN (prepassed): init-rejects-extra-argument (FEATURE-InitCommand.md)
  intent: Init with an extra argument is a usage error that exits 2 and leaves stored rates untouched.
  return code: 0

## Post-build programmatic acceptance
- PASS: init-empties-store (FEATURE-InitCommand.md)
  intent: After init, rates seeded through the repository are gone, and init prints nothing and exits 0.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: init-idempotent (FEATURE-InitCommand.md)
  intent: Running init twice in a row exits 0 both times, prints nothing, and leaves the store empty.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: init-rejects-extra-argument (FEATURE-InitCommand.md)
  intent: Init with an extra argument is a usage error that exits 2 and leaves stored rates untouched.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0

## Build summary
Existing code is clear: `cli.main` dispatches to handlers registered with `register_command`, `fxrates_app.config.open_store()` opens the store, and `rates.delete_from_date` is the declared reset operation. I'll add the init handler in its own module, register it from the `cli` package, and add tests.Now I'll run the declared acceptance assertions for this story (the three `init` AC blocks) and the full project suite.The new tests fail with `database is locked`. `db_session()` holds a transaction on its own connection, and `init` opens a second connection to delete rows. I'll check how the persistence layer provisions schema and whether the acceptance harness path (single shared connection) is what makes the declared AC work.The rollback session holds a transaction on its own connection, so a second connection can't write. The declared AC avoids this by running under the acceptance harness, which joins every store to one shared transaction. I'll confirm that the declared AC passes under that harness, then give my tests the same isolation.All three declared assertions pass under the harness. Next I'll switch my tests to the same harness-owned transaction, so they roll back and don't wipe the configured store.Init is implemented, the three declared `init` assertions pass under the acceptance harness, and the full suite is green (101 passed).

RESULT: SUCCESS

FILES CHANGED:
- cli/init_command.py
- cli/__init__.py
- tests/test_init.py

SUMMARY:
- `cli/init_command.py` adds `init(rest) -> int`. It opens the store with `fxrates_app.config.open_store()`, calls `db.rates.delete_from_date(from_date="0000-01-01")` to remove every rate, closes the database in a `finally`, and returns 0. It prints nothing and does no DDL and no driver access. It registers itself as `init` on import.
- `cli/__init__.py` imports `init_command` so the handler is registered whenever the `cli` package loads.
- `tests/test_init.py` adds five tests, all run in one harness-owned transaction that rolls back:
  - seeded rates for a currency are removed;
  - rates across many dates (1900, 2025, 9999) are removed;
  - stdout and stderr are empty;
  - init on an empty store succeeds and leaves it empty;
  - init applied twice exits 0 both times and stays empty.
- Read-back goes through `db.rates`, not captured output.

Checks run:
- `.venv/bin/pytest -q tests/test_init.py`: 5 passed.
- `sh bin/test.sh` (full suite): exit 0, 101 passed.
- The three declared AC blocks (`init-empties-store`, `init-idempotent`, `init-rejects-extra-argument`) run under `persistence.db.begin_acceptance_transaction()`: all pass. The extra-argument case is rejected by the existing usage validation, which exits 2 and leaves rows intact.

Things to know:
- Under plain pytest without the harness, the first version of the tests failed with `database is locked`. The rollback session holds a write transaction on its own connection, so `init`'s second connection can't write. The declared AC avoids this only because the harness shares one connection. My tests now use the same harness transaction, so they don't wipe `data/app.db`.
- I did not run `./fxrates init` against the build's real store, since it would delete the rates in `data/app.db`. The in-process tests cover the behavior.
- Nothing was committed.
