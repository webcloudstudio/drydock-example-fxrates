# Evidence: Block 6 · Service (block-6)

- block type: block
- date: 2026-10-27
- resulting state: closed/verified
- story points (combined assembled cost): 7305
- execution id: 20261027.155444.881Z-69d42135

## Stories built
- Validate a whole ECB history file before any write. (load-001-validate) [story]

## Acceptance tooling authorization
- FEATURE-LoadValidation.md#parse-valid-file: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-LoadValidation.md#parse-only-na: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-LoadValidation.md#parse-rejects-structure: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-LoadValidation.md#parse-rejects-dates: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-LoadValidation.md#parse-rejects-values: executable=python3; scope=test; authorization=existing Target environment

## Stacked context
- stack: python_compact.md (SP 921)
- compass: COMPASS.md (SP 1152)
- implements: FEATURE-LoadValidation.md (SP 2284)
- context: ARCHITECTURE_compact.md (SP 386)
- context: DATABASE_compact.md (SP 707)
- stack: common_compact.md (SP 1653)

## Build directory changes
- data/app.db-shm
- data/app.db-wal
- data/logs/test_2026-10-27_115531.log
- fxrates_app/ecb.py
- tests/test_ecb.py

## Pre-build acceptance observation
- RED: parse-valid-file (FEATURE-LoadValidation.md)
  intent: A valid file yields exactly its non-N/A cells as (date, currency, text) with the published text unchanged, ignoring the trailing comma.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "parse-valid-file.py", line 3, in <module>
        from fxrates_app.ecb import parse_history
    ModuleNotFoundError: No module named 'fxrates_app.ecb'
- RED: parse-only-na (FEATURE-LoadValidation.md)
  intent: A file whose values are all N/A is valid and yields no rates.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "parse-only-na.py", line 3, in <module>
        from fxrates_app.ecb import parse_history
    ModuleNotFoundError: No module named 'fxrates_app.ecb'
- RED: parse-rejects-structure (FEATURE-LoadValidation.md)
  intent: A wrong first header field, a malformed currency code, or a row with the wrong field count rejects the file.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "parse-rejects-structure.py", line 3, in <module>
        from fxrates_app.ecb import parse_history, RejectedFile
    ModuleNotFoundError: No module named 'fxrates_app.ecb'
- RED: parse-rejects-dates (FEATURE-LoadValidation.md)
  intent: A malformed, impossible, or repeated date rejects the whole file even when other rows are valid.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "parse-rejects-dates.py", line 3, in <module>
        from fxrates_app.ecb import parse_history, RejectedFile
    ModuleNotFoundError: No module named 'fxrates_app.ecb'
- RED: parse-rejects-values (FEATURE-LoadValidation.md)
  intent: Any value that is neither N/A nor a nonzero decimal matching the ECB pattern rejects the file, even when it is on a later row.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "parse-rejects-values.py", line 3, in <module>
        from fxrates_app.ecb import parse_history, RejectedFile
    ModuleNotFoundError: No module named 'fxrates_app.ecb'

## Post-build programmatic acceptance
- PASS: parse-valid-file (FEATURE-LoadValidation.md)
  intent: A valid file yields exactly its non-N/A cells as (date, currency, text) with the published text unchanged, ignoring the trailing comma.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: parse-only-na (FEATURE-LoadValidation.md)
  intent: A file whose values are all N/A is valid and yields no rates.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: parse-rejects-structure (FEATURE-LoadValidation.md)
  intent: A wrong first header field, a malformed currency code, or a row with the wrong field count rejects the file.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: parse-rejects-dates (FEATURE-LoadValidation.md)
  intent: A malformed, impossible, or repeated date rejects the whole file even when other rows are valid.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: parse-rejects-values (FEATURE-LoadValidation.md)
  intent: Any value that is neither N/A nor a nonzero decimal matching the ECB pattern rejects the file, even when it is on a later row.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0

## Build summary
Existing code is in place: `fxrates_app/` has only `config.py`, and there is no `ecb.py` yet. The spec is self-contained (pure parsing, no DB), so I'll write the module and its tests together.Now the test file. It mirrors the four declared acceptance checks and adds boundary and negative-path cases. Each test parses, then checks the returned values or the raised signal, never message text.Running the new tests, then the full project suite with the declared runner.The step is done and the full suite passes: 134 tests, including the 33 new ECB tests.

Implemented `fxrates_app.ecb.parse_history` and `RejectedFile` to validate a whole ECB history file before returning anything. The function is pure and does no database or file access. It returns `(date, currency, rate_text)` for each non-N/A value, with rates kept as published text.

I also wrote `tests/test_ecb.py`, which mirrors the four declared acceptance checks and adds boundary and negative cases. Each test parses the file and compares the returned tuples or the `RejectedFile` signal. I did not commit anything.

Two choices the spec did not settle:
- A repeated currency code in the header is rejected, because it would produce duplicate `(date, currency)` keys.
- Empty input is rejected as having no header. A header-only file is accepted and yields no rates.

RESULT: SUCCESS

FILES CHANGED:
- fxrates_app/ecb.py
- tests/test_ecb.py

SUMMARY:
- `parse_history(text)` checks the entire file before returning. It validates the header, field counts, dates, and values, and it ignores the ECB's trailing comma.
- Dates must match `YYYY-MM-DD`, be real calendar dates, and be unique within the file.
- Values must be `N/A` or match `[0-9]+(\.[0-9]+)?` and be nonzero. Zero is checked with `Decimal`.
- Checks run: `.venv/bin/pytest -q tests/test_ecb.py` gave 33 passed, and `sh bin/test.sh` gave 134 passed with exit 0.
- `sources/` was not touched, and `persistence/` was not imported.

<blueprint-decisions>
[{"spec":"FEATURE-LoadValidation.md","severity":"Low","subject":"Repeated currency code in the header","decision":"The spec does not cover duplicate header codes. I reject the file, because two columns with the same code would produce duplicate (date, currency) keys. Is that acceptable?"},{"spec":"FEATURE-LoadValidation.md","severity":"Low","subject":"Empty input and header-only files","decision":"The spec does not say how to treat empty input. I reject empty text as having no header. A header-only file with no data rows is accepted and yields an empty list. Is that acceptable?"}]
</blueprint-decisions>

FAILURE_SUMMARY: not applicable (step succeeded)
FAILURE_DETAIL: not applicable
