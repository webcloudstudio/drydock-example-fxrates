# Evidence: Block 9 · Service (block-9)

- block type: block
- date: 2026-10-27
- resulting state: closed/verified
- story points (combined assembled cost): 10226
- execution id: 20261027.160740.974Z-48d43aa5

## Stories built
- `fxrates fetch` downloads the ECB zip, extracts eurofxref-hist.csv, and loads it. (load-005-fetch) [story]

## Acceptance tooling authorization
- FEATURE-Fetch.md#fetch-loads-archive: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-Fetch.md#fetch-download-failure: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-Fetch.md#fetch-bad-archive: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-Fetch.md#fetch-rejected-member: executable=python3; scope=test; authorization=existing Target environment

## Stacked context
- stack: python_compact.md (SP 921)
- compass: COMPASS.md (SP 1152)
- implements: FEATURE-Fetch.md (SP 2537)
- context: ARCHITECTURE_compact.md (SP 386)
- context: DATABASE_compact.md (SP 707)
- stack: common_compact.md (SP 1653)
- stack: cli.md (SP 2689)

## Build directory changes
- cli/__init__.py
- cli/fetch_command.py
- cli/load_command.py
- data/app.db-shm
- data/app.db-wal
- data/logs/test_2026-10-27_121049.log
- fxrates_app/fetch.py
- tests/test_fetch.py

## Pre-build acceptance observation
- RED: fetch-loads-archive (FEATURE-Fetch.md)
  intent: With the download stubbed to return a zip holding the CSV, fetch exits 0, reports the date and rate counts, and stores each published rate text exactly.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      p = 'fetch'
    --- drydock: end values ---
    Traceback (most recent call last):
      File "fetch-loads-archive.py", line 25, in <module>
        with mock.patch("fxrates_app.fetch.download_archive", return_value=data):
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/barlo/.drydock/claude-home/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/unittest/mock.py", line 1451, in __enter__
        self.target = self.getter()
                      ^^^^^^^^^^^^^
      File "/home/barlo/.drydock/claude-home/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/pkgutil.py", line 528, in resolve_name
        result = getattr(result, p)
                 ^^^^^^^^^^^^^^^^^^
    AttributeError: module 'fxrates_app' has no attribute 'fetch'
- RED: fetch-download-failure (FEATURE-Fetch.md)
  intent: A failed download exits 1 with empty stdout and one stderr line, and stores nothing.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      p = 'fetch'
    --- drydock: end values ---
    Traceback (most recent call last):
      File "fetch-download-failure.py", line 10, in <module>
        with mock.patch("fxrates_app.fetch.download_archive", side_effect=OSError("network down")):
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/barlo/.drydock/claude-home/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/unittest/mock.py", line 1451, in __enter__
        self.target = self.getter()
                      ^^^^^^^^^^^^^
      File "/home/barlo/.drydock/claude-home/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/pkgutil.py", line 528, in resolve_name
        result = getattr(result, p)
                 ^^^^^^^^^^^^^^^^^^
    AttributeError: module 'fxrates_app' has no attribute 'fetch'
- RED: fetch-bad-archive (FEATURE-Fetch.md)
  intent: Bytes that are not a zip archive, and a zip without eurofxref-hist.csv, each exit 1 with empty stdout and store nothing.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      p = 'fetch'
    --- drydock: end values ---
    Traceback (most recent call last):
      File "fetch-bad-archive.py", line 25, in <module>
        with mock.patch("fxrates_app.fetch.download_archive", return_value=payload):
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/barlo/.drydock/claude-home/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/unittest/mock.py", line 1451, in __enter__
        self.target = self.getter()
                      ^^^^^^^^^^^^^
      File "/home/barlo/.drydock/claude-home/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/pkgutil.py", line 528, in resolve_name
        result = getattr(result, p)
                 ^^^^^^^^^^^^^^^^^^
    AttributeError: module 'fxrates_app' has no attribute 'fetch'
- RED: fetch-rejected-member (FEATURE-Fetch.md)
  intent: A member that fails ECB validation exits 3 with empty stdout and writes nothing, even for rows preceding the invalid one.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      p = 'fetch'
    --- drydock: end values ---
    Traceback (most recent call last):
      File "fetch-rejected-member.py", line 24, in <module>
        with mock.patch("fxrates_app.fetch.download_archive", return_value=data):
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/barlo/.drydock/claude-home/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/unittest/mock.py", line 1451, in __enter__
        self.target = self.getter()
                      ^^^^^^^^^^^^^
      File "/home/barlo/.drydock/claude-home/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/pkgutil.py", line 528, in resolve_name
        result = getattr(result, p)
                 ^^^^^^^^^^^^^^^^^^
    AttributeError: module 'fxrates_app' has no attribute 'fetch'

## Post-build programmatic acceptance
- PASS: fetch-loads-archive (FEATURE-Fetch.md)
  intent: With the download stubbed to return a zip holding the CSV, fetch exits 0, reports the date and rate counts, and stores each published rate text exactly.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
  stdout:
    dates,rates
    1,2
- PASS: fetch-download-failure (FEATURE-Fetch.md)
  intent: A failed download exits 1 with empty stdout and one stderr line, and stores nothing.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: fetch-bad-archive (FEATURE-Fetch.md)
  intent: Bytes that are not a zip archive, and a zip without eurofxref-hist.csv, each exit 1 with empty stdout and store nothing.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: fetch-rejected-member (FEATURE-Fetch.md)
  intent: A member that fails ECB validation exits 3 with empty stdout and writes nothing, even for rows preceding the invalid one.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0

## Build summary
I'll start by inspecting the build directory and the current state of the project.The first dump was truncated, so I'll read the CLI, ECB, and test files individually.The fetch story needs a new `fxrates_app/fetch.py`, a `fetch` handler in `cli/`, and tests. Before writing, I'll check the persistence API for transaction and session support, and the git history for how earlier blocks were structured.The persistence library has no transaction operation, and `load` already documents that each replace commits on its own. I'll mirror `load`'s path and call that out. First, a baseline run of the existing suite:Baseline is 154 passing. Now I'll write the download seam, the handler, and the registration. To avoid duplicating `load`'s store-and-report code, I'll pull it into a shared function in `load_command.py`, which keeps `fetch` on the same path.Next, the tests. I'll include the four declared acceptance checks verbatim in behavior, plus tests for the error paths and idempotence the step requires. Each shares a rolled-back transaction, the same way `test_load.py` does, so no test commits to the store.Two failures, both from a bug in my test helper rather than the handler. `csv_text` already appends the trailing comma, and I also passed a `""` in the header, so the header got an extra empty currency and was correctly rejected (exit 3). I'll drop the stray `""` from those headers.All 167 tests pass, and `bin/test.sh` exits 0. I'll confirm the set of files I touched.RESULT: SUCCESS

FILES CHANGED:
- fxrates_app/fetch.py
- cli/fetch_command.py
- cli/__init__.py
- cli/load_command.py
- tests/test_fetch.py

SUMMARY:
- `fxrates_app/fetch.py` adds `download_archive(url)`, a `urllib` download with a 30-second timeout. It is the only network call, and tests replace it at `fxrates_app.fetch.download_archive`.
- `cli/fetch_command.py` registers `fetch`. It calls the download through the module attribute, opens the zip, reads `eurofxref-hist.csv`, and runs it through `parse_history`. Then it stores and reports through the same path as `load`.
- Exit codes: download failure (OSError, timeout, or HTTP protocol error) exits 1. Non-zip bytes or a missing member exits 1. A rejected member exits 3. Nothing is stored on any failure. `fetch --help` exits 0 without downloading, and extra arguments are a usage error (exit 2) from the existing validation.
- `cli/load_command.py`: the store-and-report code moved into `store_and_report(rates)` so `load` and `fetch` share it. Behavior of `load` is unchanged.
- `cli/__init__.py` imports `fetch_command` so the handler registers.
- `tests/test_fetch.py` contains the four declared acceptance checks (loads archive, download failure, bad archive, rejected member), plus tests for the ECB URL seam, timeout and protocol errors, non-UTF-8 member, idempotence, help, and usage. Every test uses the shared rolled-back transaction fixture, and the network stays blocked by the existing conftest.

Verification:
- `.venv/bin/pytest -q tests/test_fetch.py`: 13 passed.
- `.venv/bin/pytest -q` (full suite): 167 passed (baseline was 154).
- `sh bin/test.sh`: exit 0.

Decisions for you to review:
- Step 4 of the spec mentions "one transaction of upserts", but the persistence library has no transaction operation. `load` already documents that each replace commits on its own, so `fetch` does the same. A store failure partway through a valid file is not rolled back. Validation still runs before any write.
- The ECB URL and the 30-second timeout are constants in `fxrates_app/fetch.py`. The spec leaves the timeout to the builder.
- I did not run `sources/run.sh`. It is the terminal-story grader and runs once, last.
- I did not commit, per the build rules.
