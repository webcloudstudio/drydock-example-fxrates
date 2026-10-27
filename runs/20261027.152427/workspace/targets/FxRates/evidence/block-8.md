# Evidence: Block 8 · Service (block-8)

- block type: block
- date: 2026-10-27
- resulting state: closed/verified
- story points (combined assembled cost): 8690
- execution id: 20261027.160325.188Z-36792b52

## Stories built
- A missing or unreadable file exits 1 with one stderr line and writes nothing. (load-003-unreadable) [story]

## Acceptance tooling authorization
- FEATURE-LoadUnreadable.md#load-missing-file: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-LoadUnreadable.md#load-directory-path: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-LoadUnreadable.md#load-undecodable-file: executable=python3; scope=test; authorization=existing Target environment

## Stacked context
- stack: python_compact.md (SP 921)
- compass: COMPASS.md (SP 1152)
- implements: FEATURE-LoadUnreadable.md (SP 1146)
- context: ARCHITECTURE_compact.md (SP 386)
- context: DATABASE_compact.md (SP 707)
- stack: common_compact.md (SP 1653)
- stack: cli.md (SP 2689)

## Build directory changes
- cli/load_command.py
- data/app.db-shm
- data/app.db-wal
- tests/test_load.py

## Pre-build acceptance observation
- RED: load-missing-file (FEATURE-LoadUnreadable.md)
  intent: Loading a path that does not exist exits 1 with empty stdout and one stderr line, and adds no rows.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      rest = ['/tmp/tmppav1u3an/no-such-file.csv']
    --- drydock: end values ---
    Traceback (most recent call last):
      File "load-missing-file.py", line 10, in <module>
        code, out, err = cli_runner("load", path)
                         ^^^^^^^^^^^^^^^^^^^^^^^^
      File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/cli/testing.py", line 13, in cli_runner
        code = main(list(args))
               ^^^^^^^^^^^^^^^^
      File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/cli/dispatcher.py", line 36, in main
        return handler(args[1:])
               ^^^^^^^^^^^^^^^^^
      File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/cli/load_command.py", line 29, in load
        with open(rest[0], encoding="utf-8", newline="") as handle:
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    FileNotFoundError: [Errno 2] No such file or directory: '/tmp/tmppav1u3an/no-such-file.csv'
- RED: load-directory-path (FEATURE-LoadUnreadable.md)
  intent: Loading a directory cannot be read as a file, so it exits 1 with empty stdout and one stderr line.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      rest = ['/tmp/tmpaswmqi5k']
    --- drydock: end values ---
    Traceback (most recent call last):
      File "load-directory-path.py", line 8, in <module>
        code, out, err = cli_runner("load", tmp)
                         ^^^^^^^^^^^^^^^^^^^^^^^
      File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/cli/testing.py", line 13, in cli_runner
        code = main(list(args))
               ^^^^^^^^^^^^^^^^
      File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/cli/dispatcher.py", line 36, in main
        return handler(args[1:])
               ^^^^^^^^^^^^^^^^^
      File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/cli/load_command.py", line 29, in load
        with open(rest[0], encoding="utf-8", newline="") as handle:
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    IsADirectoryError: [Errno 21] Is a directory: '/tmp/tmpaswmqi5k'
- RED: load-undecodable-file (FEATURE-LoadUnreadable.md)
  intent: A file whose bytes are not valid text exits 1 with empty stdout and one stderr line, and stores nothing.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "load-undecodable-file.py", line 12, in <module>
        code, out, err = cli_runner("load", path)
                         ^^^^^^^^^^^^^^^^^^^^^^^^
      File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/cli/testing.py", line 13, in cli_runner
        code = main(list(args))
               ^^^^^^^^^^^^^^^^
      File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/cli/dispatcher.py", line 36, in main
        return handler(args[1:])
               ^^^^^^^^^^^^^^^^^
      File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/cli/load_command.py", line 30, in load
        text = handle.read()
               ^^^^^^^^^^^^^
      File "<frozen codecs>", line 322, in decode
    UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte

## Post-build programmatic acceptance
- PASS: load-missing-file (FEATURE-LoadUnreadable.md)
  intent: Loading a path that does not exist exits 1 with empty stdout and one stderr line, and adds no rows.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: load-directory-path (FEATURE-LoadUnreadable.md)
  intent: Loading a directory cannot be read as a file, so it exits 1 with empty stdout and one stderr line.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: load-undecodable-file (FEATURE-LoadUnreadable.md)
  intent: A file whose bytes are not valid text exits 1 with empty stdout and one stderr line, and stores nothing.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0

## Build summary
Baseline is green (149 passed). The gap is in `load()`: `open()` and `read()` run outside any error handling, so a missing or directory path raises `OSError`, and undecodable bytes raise `UnicodeDecodeError`. I'll catch both there, returning exit 1 with one stderr line before any store access.Now I'll add tests for the three declared acceptance cases, in the existing `tests/test_load.py` style. Each one reads the store back to confirm nothing was written.Unreadable input now exits 1 with one stderr line and writes nothing. The full suite passes (154 tests, up from 149 with the five new ones).

- **`cli/load_command.py`:** the read happens inside a `try` that catches `OSError` (missing file, directory, permission) and `UnicodeDecodeError`. On either, it prints one `error: cannot read <path>: <reason>` line to stderr and returns 1. This happens before parsing and before the store is opened, so nothing is written.
- **`tests/test_load.py`:** five new tests cover the declared cases: missing file, directory path, and undecodable bytes. Each checks exit 1, empty stdout, and one stderr line. The missing-file and undecodable cases also read the store back and confirm no rows were added.

Checks run:
- `.venv/bin/pytest -q`: 154 passed.
- `./fxrates load /nonexistent/x.csv`: exit 1, one stderr line.
- `./fxrates load sources/eurofxref-hist_bad.csv`: exit 3, which is unchanged.

I did not run `sources/run.sh`, because this block is not the terminal story. I did not commit, per the build rules. No `sources/` files were touched.

RESULT: SUCCESS

FILES CHANGED:
- cli/load_command.py
- tests/test_load.py

SUMMARY:
`load` now treats an `OSError` or `UnicodeDecodeError` during the file read as an operational failure: exit 1, empty stdout, one stderr line, and no store access. Five tests cover the missing, directory, and undecodable cases, including store read-back for the write-nothing guarantee. Full suite: 154 passed.
