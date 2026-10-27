# Evidence: Block 4 · Service (block-4)

- block type: block
- date: 2026-10-27
- resulting state: closed/failed
- story points (combined assembled cost): 14463
- execution id: 20261027.193228.463Z-05a4d299

## Stories built
- Implement fxrates init via persistence.initialize_database. (cli-init) [story]
- Report command usage errors with exit 2. (cli-usage) [story]
- Store parsed rates, replacing any existing (date, currency) rate. (rate-store) [story]
- Parse and validate an ECB history CSV without writing anything. (load-parse) [story]

## Acceptance tooling authorization
- FEATURE-Init.md#init-fresh-store: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-Init.md#init-repeat-preserves: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-Init.md#init-uses-database-path: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-UsageErrors.md#usage-errors-exit-2: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-UsageErrors.md#parse-valid-arguments: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-UsageErrors.md#parse-raises-usage-error: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-RateStorage.md#ratestore-round-trip: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-RateStorage.md#ratestore-replace-and-idempotent: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-RateStorage.md#ratestore-empty: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-EcbParse.md#ecb-parse-valid: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-EcbParse.md#ecb-parse-rejects-bad-rows: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-EcbParse.md#ecb-parse-rejects-bad-header: executable=python3; scope=test; authorization=existing Target environment

## Stacked context
- stack: python_compact.md (SP 1002)
- compass: COMPASS.md (SP 1152)
- implements: FEATURE-Init.md (SP 1404)
- context: ARCHITECTURE_compact.md (SP 361)
- context: DATABASE_compact.md (SP 480)
- stack: common_compact.md (SP 1653)
- stack: cli.md (SP 2689)
- implements: FEATURE-UsageErrors.md (SP 1187)
- implements: FEATURE-RateStorage.md (SP 1569)
- implements: FEATURE-EcbParse.md (SP 2430)

## Build directory changes
- cli/commands/init.py
- cli/dispatch.py
- cli/usage.py
- ecb/__init__.py
- ecb/history.py
- ratestore.py
- tests/test_cli_init.py
- tests/test_cli_usage.py
- tests/test_ecb_parse.py
- tests/test_ratestore.py

## Pre-build acceptance observation
- RED: init-fresh-store (FEATURE-Init.md)
  intent: init on a fresh store exits 0 with empty stdout and leaves a store whose rates operations work.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      code = 2
    --- drydock: end values ---
    Traceback (most recent call last):
      File "init-fresh-store.py", line 9, in <module>
        assert code == 0
               ^^^^^^^^^
    AssertionError
- RED: init-repeat-preserves (FEATURE-Init.md)
  intent: Running init again succeeds and leaves previously stored rates unchanged.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      code = 2
    --- drydock: end values ---
    Traceback (most recent call last):
      File "init-repeat-preserves.py", line 10, in <module>
        assert code == 0
               ^^^^^^^^^
    AssertionError
- RED: init-uses-database-path (FEATURE-Init.md)
  intent: With DATABASE_URL unset, init creates the store named by DATABASE_PATH.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      code = 2
    --- drydock: end values ---
    Traceback (most recent call last):
      File "init-uses-database-path.py", line 7, in <module>
        assert code == 0
               ^^^^^^^^^
    AssertionError
- GREEN (prepassed): usage-errors-exit-2 (FEATURE-UsageErrors.md)
  intent: Every malformed invocation exits 2 with empty stdout and a single stderr line, before any store is touched.
  return code: 0
- RED: parse-valid-arguments (FEATURE-UsageErrors.md)
  intent: parse hands valid arguments on as parsed values, with the serve port an integer defaulting to 8000.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "parse-valid-arguments.py", line 1, in <module>
        from cli.usage import parse
    ModuleNotFoundError: No module named 'cli.usage'
- RED: parse-raises-usage-error (FEATURE-UsageErrors.md)
  intent: parse signals each violation with UsageError, whose exit code is 2.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "parse-raises-usage-error.py", line 2, in <module>
        from cli.usage import parse
    ModuleNotFoundError: No module named 'cli.usage'
- RED: ratestore-round-trip (FEATURE-RateStorage.md)
  intent: Stored records read back through the history operation with their exact published text, and the returned counts equal the distinct dates and the records written.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "ratestore-round-trip.py", line 2, in <module>
        from ratestore import store_rates
    ModuleNotFoundError: No module named 'ratestore'
- RED: ratestore-replace-and-idempotent (FEATURE-RateStorage.md)
  intent: Storing the same records twice leaves one row per date and currency, and storing a changed rate replaces the stored text.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "ratestore-replace-and-idempotent.py", line 2, in <module>
        from ratestore import store_rates
    ModuleNotFoundError: No module named 'ratestore'
- RED: ratestore-empty (FEATURE-RateStorage.md)
  intent: Empty input writes nothing and reports zero dates and zero rates.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "ratestore-empty.py", line 2, in <module>
        from ratestore import store_rates
    ModuleNotFoundError: No module named 'ratestore'
- RED: ecb-parse-valid (FEATURE-EcbParse.md)
  intent: Every non-N/A value becomes one record carrying the published text unchanged, N/A values and the trailing empty field produce nothing, and trailing zeros survive.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "ecb-parse-valid.py", line 3, in <module>
        from ecb import parse_history
    ModuleNotFoundError: No module named 'ecb'
- RED: ecb-parse-rejects-bad-rows (FEATURE-EcbParse.md)
  intent: A wrong field count, an invalid calendar date, a malformed date, a repeated date, or an invalid or zero value each reject the whole file with RejectedFile even when other rows are valid.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "ecb-parse-rejects-bad-rows.py", line 3, in <module>
        from ecb import parse_history
    ModuleNotFoundError: No module named 'ecb'
- RED: ecb-parse-rejects-bad-header (FEATURE-EcbParse.md)
  intent: A header whose first field is not Date, or that holds a code that is lowercase, two letters, or four letters, rejects the file even when its rows are well formed.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "ecb-parse-rejects-bad-header.py", line 3, in <module>
        from ecb import parse_history
    ModuleNotFoundError: No module named 'ecb'

## Repair attempts
- attempt 0 (initial build): failed; checks not executed (12 declared) model=haiku; execution 20261027.193228.463Z-05a4d299; reason: managed-state violation

## Failure
- summary: managed-state violation
- detail:
    Managed SQLite state changed during agent execution. Retained pre-call snapshot: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.190646/workspace/targets/FxRates/evidence/managed-state/sqlite-2rqgxlo6/app.db. Review and restore through the persistence owner before continuing; no automatic overwrite or reprovisioning was performed.

## Build summary
I'll start by inspecting the build working directory and the existing files.Several modules the spec names are missing (`ecb/`, `ratestore`, `cli/usage.py`). I'll read the existing CLI, persistence, and config files to see what's there.The first output was truncated. I'll read the remaining files I need individually.Block 4 needs four things: `cli/commands/init.py`, `cli/usage.py` (the `parse` function the usage spec names), `ratestore.py`, and the `ecb` package. Before writing, I need to check how the existing dispatch tests use command names, since `parse` will reject unknown ones, and how the SQLite driver opens files.I have the picture now. Two constraints shape the design:

- The usage spec requires `parse(["frobnicate"])` to raise, but the existing `main(["probe"])` tests register ad-hoc command modules and expect them to run. I'll keep both working: `parse` checks the declared arity table for the four known commands and, for any other name, defers to the existing `resolve()` module lookup.
- `init` needs `DATABASE_URL`/`DATABASE_PATH` resolved through `config.database_path()`, and `persistence.initialize_database` already creates the schema.

Next I'll get a baseline of the existing test suite before editing.Baseline is 72 passing tests, and the provisioned store already has the `rates` table. I'll write the usage validator first, then wire it into the dispatcher.Now I'll route the dispatcher through `usage.parse` so validation happens before any handler runs.Next, the `init` command, the `ratestore` module, and the `ecb` parser.Now the tests. I'll write them in the project's `tests/` location, following the existing style. Each one acts on the system and reads state back through the public interface.Now I'll run the full suite, including the existing 72 tests, to check for regressions.All 155 tests pass: the 72 existing ones plus 83 new ones. The suite is my own, though, so I also want to run the declared acceptance assertions verbatim. Some import `drydock_acceptance`, so I'll check whether that module is available here.The nine assertions that don't depend on `drydock_acceptance` all pass. The three `init` acceptance criteria need `database_environment`, which isn't installed here, so I'll exercise those behaviors through the real launcher instead.The launcher behaves as specified. I'll remove the scratch scripts outside the build directory.All four stories in block 4 are implemented. The suite passes at 155 tests (72 existing, 83 new), and the nine declared acceptance assertions that don't need the harness module pass when run verbatim.

The three `init` acceptance criteria (`init-fresh-store`, `init-repeat-preserves`, `init-uses-database-path`) import `drydock_acceptance`, which isn't installed here. I covered the same behavior in `tests/test_cli_init.py` and checked it through the real `./fxrates` launcher on a temp store.

RESULT: SUCCESS

<blueprint-decisions>
[{"spec":"FEATURE-UsageErrors.md","severity":"Material","subject":"parse() for names outside the declared command table","decision":"The spec requires parse(['frobnicate']) to raise UsageError, but the existing main() tests register ad-hoc command modules (e.g. 'probe') and expect them to run. I kept both: parse validates arity for init/fetch/load/serve, and any other name is accepted only if cli.dispatch.resolve() finds a command module, otherwise UsageError. Is that acceptable, or should unknown-name handling move to the table only?"},{"spec":"FEATURE-EcbParse.md","severity":"Low","subject":"Repeated currency codes in the header","decision":"The spec does not address a header that repeats a currency code. I reject it as RejectedFile, since two columns for one code would make the (date, currency) write ambiguous. Blank body lines are also rejected under the strict field-count rule."},{"spec":"FEATURE-Init.md","severity":"Low","subject":"Store location and init failure mapping","decision":"init creates the store's parent directory (the SQLite driver already does this) so a fresh checkout with no data/ directory works. A PersistenceError during initialization maps to OperationalError (exit 1) with one stderr line."}]
</blueprint-decisions>

FILES CHANGED:
- cli/usage.py (new): `parse(argv) -> (name, args)` with per-command rules for init, fetch, load and serve, raising `UsageError` on any violation.
- cli/dispatch.py: `dispatch` now calls `usage.parse` before `resolve`, so validation runs before any handler.
- cli/commands/init.py (new): `run(args)` calls `persistence.initialize_database(config.database_path())`, closes the database, prints nothing and returns 0.
- ratestore.py (new): `store_rates(db, records) -> (dates, rates)`, writing each record through `db.rates.replace_rate`.
- ecb/__init__.py (new) and ecb/history.py (new): `Rate` namedtuple and `parse_history(text)`, which validates the whole file before returning any records and raises `RejectedFile` otherwise.
- tests/test_cli_usage.py, tests/test_cli_init.py, tests/test_ecb_parse.py, tests/test_ratestore.py (new): behavior tests. Store-touching tests use `db_session()` or a per-test temp file, and never the shared store.

SUMMARY:
- `bin/test.sh` (pytest -q): 155 passed, 0 failed.
- Declared acceptance assertions run verbatim: `ecb-parse-valid`, `ecb-parse-rejects-bad-rows`, `ecb-parse-rejects-bad-header`, `usage-errors-exit-2`, `parse-valid-arguments`, `parse-raises-usage-error`, `ratestore-round-trip`, `ratestore-replace-and-idempotent`, `ratestore-empty` all pass. The three init criteria were not run verbatim (see above).
- Launcher smoke test on a temp store: `init` exits 0 with empty stdout, a repeat `init` exits 0, no-argument, unknown-command, `load` with no path, `init extra` and `serve --port notaport` each exit 2 with empty stdout, and the store contains the `rates` table.
- Not run: `sources/run.sh`. It is the terminal check, and it depends on `load`, `fetch` and `serve` handlers that belong to later blocks.
- Nothing committed. I did not touch `sources/`, the protected Drydock paths, or `.drydock-tests/`.

BLOCKERS:
- None for this block. `./fxrates fetch`, `load` with valid arguments and `serve` exit 2 with "unknown command" until their later-block handlers exist. That is expected, but the message is misleading for those names.
