# Evidence: Block 7 · Service (block-7)

- block type: block
- date: 2026-10-27
- resulting state: closed/verified
- story points (combined assembled cost): 11452
- execution id: 20261027.155829.052Z-00c30e97

## Stories built
- `fxrates load <csv>` stores published rates as text, replacing existing rows, and reports dates,rates counts. (load-002-store) [story]

## Acceptance tooling authorization
- FEATURE-LoadStore.md#load-counts-and-text: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-LoadStore.md#load-reload-is-idempotent: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-LoadStore.md#load-replaces-existing-rate: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-LoadStore.md#load-rejected-file-changes-nothing: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-LoadStore.md#load-supplied-bad-file: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-LoadStore.md#load-only-na: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-LoadStore.md#load-supplied-january-file: executable=python3; scope=test; authorization=existing Target environment

## Stacked context
- stack: python_compact.md (SP 921)
- compass: COMPASS.md (SP 1152)
- implements: FEATURE-LoadStore.md (SP 3761)
- context: ARCHITECTURE_compact.md (SP 386)
- context: DATABASE_compact.md (SP 707)
- stack: common_compact.md (SP 1653)
- stack: cli.md (SP 2689)

## Build directory changes
- cli/__init__.py
- cli/load_command.py
- data/app.db-shm
- data/app.db-wal
- data/logs/test_2026-10-27_120016.log
- tests/test_load.py

## Pre-build acceptance observation
- RED: load-counts-and-text (FEATURE-LoadStore.md)
  intent: A valid file exits 0, reports the dates and rates counts derived from the fixture (an all-N/A date is not counted), and stores each rate as published text.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      code = 2
    --- drydock: end values ---
    Traceback (most recent call last):
      File "load-counts-and-text.py", line 26, in <module>
        assert code == 0
               ^^^^^^^^^
    AssertionError
- RED: load-reload-is-idempotent (FEATURE-LoadStore.md)
  intent: Loading the same file twice reports the same counts both times and leaves the stored rates unchanged.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      code = 2
    --- drydock: end values ---
    Traceback (most recent call last):
      File "load-reload-is-idempotent.py", line 19, in <module>
        assert code == 0
               ^^^^^^^^^
    AssertionError
- RED: load-replaces-existing-rate (FEATURE-LoadStore.md)
  intent: A later file replaces a stored rate for the same date and currency, leaves other dates alone, and does not add a row.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      code = 2
    --- drydock: end values ---
    Traceback (most recent call last):
      File "load-replaces-existing-rate.py", line 25, in <module>
        assert code == 0
               ^^^^^^^^^
    AssertionError
- RED: load-rejected-file-changes-nothing (FEATURE-LoadStore.md)
  intent: A file with a valid first row and an invalid later row exits 3 with empty stdout and one stderr line, and stores nothing, including the valid first row.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      code = 2
    --- drydock: end values ---
    Traceback (most recent call last):
      File "load-rejected-file-changes-nothing.py", line 20, in <module>
        assert code == 3
               ^^^^^^^^^
    AssertionError
- RED: load-supplied-bad-file (FEATURE-LoadStore.md)
  intent: The supplied bad ECB file is rejected with exit 3 and no rows are added.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      code = 2
    --- drydock: end values ---
    Traceback (most recent call last):
      File "load-supplied-bad-file.py", line 7, in <module>
        assert code == 3
               ^^^^^^^^^
    AssertionError
- RED: load-only-na (FEATURE-LoadStore.md)
  intent: A file holding only N/A rates exits 0, reports zero dates and zero rates, and stores nothing.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      code = 2
    --- drydock: end values ---
    Traceback (most recent call last):
      File "load-only-na.py", line 18, in <module>
        assert code == 0
               ^^^^^^^^^
    AssertionError
- RED: load-supplied-january-file (FEATURE-LoadStore.md)
  intent: The supplied January file loads with counts derived from its own cells, and every stored USD rate equals the published text.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      code = 2
    --- drydock: end values ---
    Traceback (most recent call last):
      File "load-supplied-january-file.py", line 19, in <module>
        assert code == 0
               ^^^^^^^^^
    AssertionError

## Post-build programmatic acceptance
- PASS: load-counts-and-text (FEATURE-LoadStore.md)
  intent: A valid file exits 0, reports the dates and rates counts derived from the fixture (an all-N/A date is not counted), and stores each rate as published text.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: load-reload-is-idempotent (FEATURE-LoadStore.md)
  intent: Loading the same file twice reports the same counts both times and leaves the stored rates unchanged.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: load-replaces-existing-rate (FEATURE-LoadStore.md)
  intent: A later file replaces a stored rate for the same date and currency, leaves other dates alone, and does not add a row.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: load-rejected-file-changes-nothing (FEATURE-LoadStore.md)
  intent: A file with a valid first row and an invalid later row exits 3 with empty stdout and one stderr line, and stores nothing, including the valid first row.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: load-supplied-bad-file (FEATURE-LoadStore.md)
  intent: The supplied bad ECB file is rejected with exit 3 and no rows are added.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: load-only-na (FEATURE-LoadStore.md)
  intent: A file holding only N/A rates exits 0, reports zero dates and zero rates, and stores nothing.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: load-supplied-january-file (FEATURE-LoadStore.md)
  intent: The supplied January file loads with counts derived from its own cells, and every stored USD rate equals the published text.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0

## Build summary
I'll start by inspecting the build directory and the current state of the project.The load command needs `rates.replace_rate` and a single transaction, so I need the generated schema and the Database transaction API. I'll also check how the init tests are written.I need to see how `Database` handles commits and transactions, since the load has to be all-or-nothing.The persistence library has no public transaction API. `Database` autocommits each declared operation, and the library forbids driver access inside the acceptance transaction. I'll check the usage tests for `load`, the staged sources, and the existing ECB tests before deciding how to write the load.I have what I need. Here is the plan before I write anything:

- **Validation first:** `parse_history` runs over the whole file before any write, so a rejected file stores nothing.
- **Transaction gap:** the persistence layer has no transaction operation, and driver access is blocked inside the acceptance transaction. The spec asks for one transaction, so I can't deliver that from `cli/` without reaching around the library. I'll write each rate through `rates.replace_rate`, note the gap in the code, and flag it as a Material decision.

Writing the command handler now, registered the same way as `init`.Now the test suite, following the `test_init.py` pattern: the autouse acceptance-transaction fixture, reads back through `db.rates`, and temp files via `tmp_path`.I left a syntax error in the January test's comprehension (a stray `->`). I also wrote two count assertions that assume an empty store, when the store may already hold rates. Fixing all three.The January round-trip test still counts rows in the whole store, which breaks if the store already holds overlapping January rates. I'll check each parsed rate against the store instead.Running the new tests first, then the full suite through the declared gate (`bin/test.sh`).One failure, and it's a bug in my test, not the command: I passed `""` as a header column, so the validator correctly rejected it as a currency code. Fixing the header.All 15 load tests pass, and the declared gate `bin/test.sh` passes with 149 tests and exit 0. As a last check I'll run the real launcher end to end against a copy of the store, so the shipped database isn't touched.`fxrates load` is implemented and the declared gate passes. One requirement is not met: the load is not a single transaction.

**What's not met:** FEATURE-LoadStore asks for all rates to be stored in one transaction. The persistence library has no transaction operation, and driver access is blocked inside the acceptance transaction, so `cli/` cannot open one without reaching around the library. Each `rates.replace_rate` commits on its own. The validation runs before the first write, so a rejected file still stores nothing. A database error part way through a valid file would leave a partial load. Fixing this needs a transaction operation in DATABASE.md or the shipped persistence layer, which are Drydock-owned.

RESULT: SUCCESS

FILES CHANGED:
- cli/load_command.py
- cli/__init__.py
- tests/test_load.py

SUMMARY:
- `cli/load_command.py` registers the `load` handler. It reads the file, runs `fxrates_app.ecb.parse_history` over the whole file, and returns exit 3 with one stderr line and empty stdout on `RejectedFile`. On success it writes each rate through `db.rates.replace_rate` and prints `dates,rates` then `<dates>,<rates>`.
- `cli/__init__.py` imports the new module, the same way `init` is registered.
- `tests/test_load.py` has 15 tests. They cover counts, all-N/A dates, text rate storage, reload idempotence, replacement without adding rows, rejected files storing nothing, and the supplied good and bad ECB files. Reads go back through `db.rates`, and each test runs in the rolled-back acceptance transaction.

Checks run:
- `.venv/bin/pytest -q tests/test_load.py`: 15 passed. One of my tests first failed because I wrote a bad header in it. I fixed the test, not the command.
- `sh bin/test.sh`: exit 0, 149 passed.
- End-to-end on a temp copy of the store (`DATABASE_PATH`): the January file gives `22,176` twice; the bad file gives exit 3 with `error: line 3 has a malformed rate: '1.0x'`; the Feb 3–4 file gives `2,16`; `load` with no argument gives exit 2. The shipped `data/app.db` was not touched.
- I did not run the acceptance assertions directly. Drydock runs them after this step.

Choices I made:
- `load --help` returns 0 with no output and does not read a file, matching how `init` treats its arguments. The spec does not cover it.
- A missing or unreadable file raises an `OSError` and is not caught. That belongs to FEATURE-LoadUnreadable, which is not in this block.

```blueprint-decisions
[{"spec":"FEATURE-LoadStore.md","severity":"Material","subject":"Single transaction for the load","decision":"The spec asks for all upserts in one transaction. The persistence library exposes no transaction operation, and driver access is forbidden inside the acceptance transaction, so cli/ cannot open one without bypassing the library. I wrote each rate through rates.replace_rate, which autocommits per row. Validation still runs over the whole file before the first write, so rejected files store nothing, but a database failure mid-load is not rolled back. Should a transaction operation be added to DATABASE.md, or is per-row commit acceptable?"},{"spec":"FEATURE-LoadStore.md","severity":"Low","subject":"load --help handling","decision":"load --help returns exit 0 with no output and does not read a file, matching init. The spec does not define it. Confirm or change on replan."}]
```

FAILURE_SUMMARY is not needed because the result is SUCCESS, with the atomicity gap reported above.
