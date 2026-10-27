# Evidence: Block 11 · Service (block-11)

- block type: block
- date: 2026-10-27
- resulting state: closed/verified
- story points (combined assembled cost): 14462
- execution id: 20261027.162116.999Z-665549b5

## Stories built
- GET /stats reports dates, rates, first, and last. (rates-002-stats) [story]
- GET /currencies lists base EUR and stored currency codes ascending. (rates-003-currencies) [story]
- GET /rates/{date} resolves the effective publication date and lists its rates. (rates-004-rates-by-date) [story]
- Each command accepts --help, prints usage and a one-line summary to stdout, and exits 0. (cli-004-help) [story]

## Acceptance tooling authorization
- FEATURE-Stats.md#stats-reflects-store: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-Stats.md#stats-reflects-store: python-package=httpx2; scope=test; authorization=existing Target environment
- FEATURE-Stats.md#stats-body-shape: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-Stats.md#stats-body-shape: python-package=httpx2; scope=test; authorization=existing Target environment
- FEATURE-Currencies.md#currencies-lists-stored: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-Currencies.md#currencies-lists-stored: python-package=httpx2; scope=test; authorization=existing Target environment
- FEATURE-Currencies.md#currencies-body-shape: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-Currencies.md#currencies-body-shape: python-package=httpx2; scope=test; authorization=existing Target environment
- FEATURE-RatesByDate.md#rates-by-date-exact: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-RatesByDate.md#rates-by-date-exact: python-package=httpx2; scope=test; authorization=existing Target environment
- FEATURE-RatesByDate.md#rates-by-date-effective: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-RatesByDate.md#rates-by-date-effective: python-package=httpx2; scope=test; authorization=existing Target environment
- FEATURE-RatesByDate.md#rates-effective-date-function: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-RatesByDate.md#rates-by-date-errors: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-RatesByDate.md#rates-by-date-errors: python-package=httpx2; scope=test; authorization=existing Target environment
- FEATURE-CommandHelp.md#help-per-command: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-CommandHelp.md#help-has-usage-and-summary: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-CommandHelp.md#help-does-not-touch-rates: executable=python3; scope=test; authorization=existing Target environment

## Stacked context
- stack: python_compact.md (SP 921)
- compass: COMPASS.md (SP 1152)
- implements: FEATURE-Stats.md (SP 1274)
- context: ARCHITECTURE_compact.md (SP 386)
- context: DATABASE_compact.md (SP 707)
- stack: fastapi_compact.md (SP 1122)
- implements: FEATURE-Currencies.md (SP 1143)
- implements: FEATURE-RatesByDate.md (SP 2074)
- implements: FEATURE-CommandHelp.md (SP 1018)
- stack: common_compact.md (SP 1653)
- stack: cli.md (SP 2689)

## Build directory changes
- app_server/routes.py
- cli/fetch_command.py
- cli/help.py
- cli/init_command.py
- cli/load_command.py
- cli/serve_command.py
- data/app.db-shm
- data/app.db-wal
- data/logs/test_2026-10-27_122205.log
- data/logs/test_2026-10-27_122432.log
- fxrates_app/currencies.py
- fxrates_app/rates.py
- fxrates_app/stats.py
- tests/test_currencies.py
- tests/test_fetch.py
- tests/test_help.py
- tests/test_load.py
- tests/test_rates_by_date.py
- tests/test_serve.py
- tests/test_stats.py

## Pre-build acceptance observation
- RED: stats-reflects-store (FEATURE-Stats.md)
  intent: The stats body equals the counts, first date and last date derived from the stored keys read back through the repository, and includes the rows the criterion seeded.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      response = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "stats-reflects-store.py", line 15, in <module>
        assert response.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: stats-body-shape (FEATURE-Stats.md)
  intent: The stats body carries exactly the four declared keys, and first and last are null exactly when no rate is stored.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      response = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "stats-body-shape.py", line 8, in <module>
        assert response.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: currencies-lists-stored (FEATURE-Currencies.md)
  intent: The currency list equals the distinct stored codes read back through the repository, ascending, includes the seeded codes, and omits EUR.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      response = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "currencies-lists-stored.py", line 13, in <module>
        assert response.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: currencies-body-shape (FEATURE-Currencies.md)
  intent: The body carries exactly base and currencies, currencies is a list, and it is empty exactly when no rate is stored.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      response = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "currencies-body-shape.py", line 8, in <module>
        assert response.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: rates-by-date-exact (FEATURE-RatesByDate.md)
  intent: A request for a publication date returns that date as both date and requested, base EUR, and each stored rate text exactly as supplied.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      response = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "rates-by-date-exact.py", line 13, in <module>
        assert response.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: rates-by-date-effective (FEATURE-RatesByDate.md)
  intent: A request between two publications resolves to the earlier publication, keeps the requested date, and carries that earlier date's rates rather than the later ones.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      response = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "rates-by-date-effective.py", line 15, in <module>
        assert response.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: rates-effective-date-function (FEATURE-RatesByDate.md)
  intent: effective_date returns the latest publication date on or before its argument and None when none exists.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "rates-effective-date-function.py", line 1, in <module>
        from fxrates_app.rates import effective_date
    ModuleNotFoundError: No module named 'fxrates_app.rates'
- RED: rates-by-date-errors (FEATURE-RatesByDate.md)
  intent: A date before every publication answers 404, and malformed or impossible dates answer 422.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      client = <starlette.testclient.TestClient object at 0x72d65a0c3380>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "rates-by-date-errors.py", line 6, in <module>
        assert client.get("/rates/2025-13-01").status_code == 422
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: help-per-command (FEATURE-CommandHelp.md)
  intent: Each of the four commands exits 0 with non-empty standard output and empty standard error when given --help, including load without its file argument.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      command = 'init'
      out = ''
    --- drydock: end values ---
    Traceback (most recent call last):
      File "help-per-command.py", line 6, in <module>
        assert out.strip() != "", command
               ^^^^^^^^^^^^^^^^^
    AssertionError: init
- RED: help-has-usage-and-summary (FEATURE-CommandHelp.md)
  intent: Help output has at least two non-blank lines: a usage line and a one-line summary.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      command = 'init'
      lines = []
    --- drydock: end values ---
    Traceback (most recent call last):
      File "help-has-usage-and-summary.py", line 7, in <module>
        assert len(lines) >= 2, command
               ^^^^^^^^^^^^^^^
    AssertionError: init
- RED: help-does-not-touch-rates (FEATURE-CommandHelp.md)
  intent: init --help must not reset the store: a seeded rate is still there afterwards.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      text = '6.5'
      rows = []
    --- drydock: end values ---
    Traceback (most recent call last):
      File "help-does-not-touch-rates.py", line 13, in <module>
        assert [r.rate for r in rows] == [text]
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError

## Post-build programmatic acceptance
- PASS: stats-reflects-store (FEATURE-Stats.md)
  intent: The stats body equals the counts, first date and last date derived from the stored keys read back through the repository, and includes the rows the criterion seeded.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: stats-body-shape (FEATURE-Stats.md)
  intent: The stats body carries exactly the four declared keys, and first and last are null exactly when no rate is stored.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: currencies-lists-stored (FEATURE-Currencies.md)
  intent: The currency list equals the distinct stored codes read back through the repository, ascending, includes the seeded codes, and omits EUR.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: currencies-body-shape (FEATURE-Currencies.md)
  intent: The body carries exactly base and currencies, currencies is a list, and it is empty exactly when no rate is stored.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: rates-by-date-exact (FEATURE-RatesByDate.md)
  intent: A request for a publication date returns that date as both date and requested, base EUR, and each stored rate text exactly as supplied.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: rates-by-date-effective (FEATURE-RatesByDate.md)
  intent: A request between two publications resolves to the earlier publication, keeps the requested date, and carries that earlier date's rates rather than the later ones.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: rates-effective-date-function (FEATURE-RatesByDate.md)
  intent: effective_date returns the latest publication date on or before its argument and None when none exists.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: rates-by-date-errors (FEATURE-RatesByDate.md)
  intent: A date before every publication answers 404, and malformed or impossible dates answer 422.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: help-per-command (FEATURE-CommandHelp.md)
  intent: Each of the four commands exits 0 with non-empty standard output and empty standard error when given --help, including load without its file argument.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: help-has-usage-and-summary (FEATURE-CommandHelp.md)
  intent: Help output has at least two non-blank lines: a usage line and a one-line summary.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: help-does-not-touch-rates (FEATURE-CommandHelp.md)
  intent: init --help must not reset the store: a seeded rate is still there afterwards.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0

## Build summary
Baseline is green (182 passed). Three older tests assert that `--help` prints nothing for `load`, `serve`, and `fetch`, which conflicts with the stdout requirement in `cli-004-help`, so I'll update those assertions along with the code. Writing the help module and the command changes first.Now the service modules for the three routes.Before writing tests, I'll check how FastAPI's date validation treats the malformed inputs the spec names.The `datetime.date` annotation accepts `2025-01-31T00:00:00` and answers 404, but the spec defines the path as `YYYY-MM-DD` and says anything else is 422. I'll tighten it with a path pattern plus a calendar check.Now the tests. Each new file uses the same acceptance-transaction fixture the existing `init` and `load` tests use, so seeding and the routes share one connection and roll back at the end.Now I'll update the three older help assertions that expected silent `--help`.All 226 tests pass: the 182 baseline plus 44 new. I'll confirm the launcher's help output and then review the final route file.The four stories in block 11 are built and the full suite passes: 226 tests, up from 182, exit 0 (`sh bin/test.sh`). I did not run `sources/run.sh`, since COMPASS makes it a once-last terminal check.

**What I built**
- **`GET /stats`** (`fxrates_app/stats.py`): counts dates and rates from `db.rates.list_all_keys()`, with first and last dates, or `null` when the store is empty.
- **`GET /currencies`** (`fxrates_app/currencies.py`): returns `{"base": "EUR", "currencies": [...]}` from `db.rates.list_currencies()`, deduplicated and ascending.
- **`GET /rates/{date}`** (`fxrates_app/rates.py`): `effective_date(d)` picks the first row of `list_on_or_before`. The route returns 404 when no publication precedes the date, and 422 for anything not `YYYY-MM-DD` or not a real calendar date.
- **`--help` for init, load, fetch, serve** (`cli/help.py`): prints a usage line and a one-line summary to stdout, exits 0, and returns before any database or socket access.

**Things you should know**
- **`init --help` was destructive.** Before this change it fell through to the delete. It now returns before opening the store. Load, fetch, and serve printed nothing for `--help`, so they now print the help text too.
- **Three older tests asserted silent `--help`.** `test_load.py`, `test_serve.py`, and `test_fetch.py` each expected empty stdout. I changed those assertions to check the usage line, since the `cli-004-help` story requires stdout output. These are not declared acceptance assertions, but they are the only existing tests I edited.
- **EUR is filtered explicitly** from both `/currencies` and the `/rates` map, following the spec's "not listed" and "no EUR entry" rules. The ECB data carries no EUR column, so this only matters for hand-seeded rows.
- **Date validation** uses a `YYYY-MM-DD` path pattern plus `date.fromisoformat`. I checked that a bare `date` annotation would accept `2025-01-31T00:00:00` and answer 404, which the spec does not allow.

**Tests added** (`tests/test_stats.py`, `test_currencies.py`, `test_rates_by_date.py`, `test_help.py`): they follow the same acceptance-transaction fixture as the existing init and load tests, and read results back through `db.rates`. The declared acceptance assertions are covered by equivalent tests here; Drydock runs its own copies for the verdict.

Nothing was committed.

RESULT: SUCCESS

FILES CHANGED:
- app_server/routes.py
- cli/help.py
- cli/init_command.py
- cli/load_command.py
- cli/fetch_command.py
- cli/serve_command.py
- fxrates_app/rates.py
- fxrates_app/stats.py
- fxrates_app/currencies.py
- tests/test_stats.py
- tests/test_currencies.py
- tests/test_rates_by_date.py
- tests/test_help.py
- tests/test_load.py
- tests/test_serve.py
- tests/test_fetch.py

SUMMARY:
Implemented GET /stats, GET /currencies, GET /rates/{date} with effective-date resolution, and `--help` for init, load, fetch, and serve. `sh bin/test.sh` exits 0 with 226 passed (182 baseline + 44 new). The init `--help` path previously ran a store reset; it now returns before touching the database. Three older tests were updated to expect the new stdout help text. `sources/run.sh` was not run (terminal story, not this block).

BLOCKERS:
- none
