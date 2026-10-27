# Evidence: Block 3 · Service (block-3)

- block type: block
- date: 2026-10-26
- resulting state: closed/verified
- story points (combined assembled cost): 14787
- execution id: 20261026.204750.616Z-f17235ce

## Stories built
- Validate and load ECB CSV history files atomically. (load) [story]
- Initialize an empty rates store. (init) [story]
- List currencies that have stored rates. (api_currencies) [story]
- Retrieve rates from the latest publication. (api_latest) [story]
- Report stored rate statistics. (api_stats) [story]
- Retrieve rates by effective date. (api_rates) [story]
- Retrieve currency history and summary statistics. (history) [story]
- Convert amounts between currencies. (convert) [story]
- Serve the health endpoint. (api_health) [story]
- Report CLI usage and operational errors. (cli_errors) [story]

## Acceptance tooling authorization
- FEATURE-Currencies.md#currencies-list-sorted: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-Currencies.md#currencies-list-sorted: python-package=httpx2; scope=test; authorization=existing Target environment
- FEATURE-Currencies.md#currencies-base: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-Currencies.md#currencies-base: python-package=httpx2; scope=test; authorization=existing Target environment
- FEATURE-LatestRates.md#latest-rates-response: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-LatestRates.md#latest-rates-response: python-package=httpx2; scope=test; authorization=existing Target environment
- FEATURE-LatestRates.md#latest-rates-empty: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-LatestRates.md#latest-rates-empty: python-package=httpx2; scope=test; authorization=existing Target environment
- FEATURE-Stats.md#stats-derive-from-store: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-Stats.md#stats-derive-from-store: python-package=httpx2; scope=test; authorization=existing Target environment
- FEATURE-Stats.md#stats-empty-store: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-Stats.md#stats-empty-store: python-package=httpx2; scope=test; authorization=existing Target environment
- FEATURE-Rates.md#rates-effective-date: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-Rates.md#rates-effective-date: python-package=httpx2; scope=test; authorization=existing Target environment
- FEATURE-Rates.md#rates-errors: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-Rates.md#rates-errors: python-package=httpx2; scope=test; authorization=existing Target environment
- FEATURE-History.md#history-range-and-statistics: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-History.md#history-range-and-statistics: python-package=httpx2; scope=test; authorization=existing Target environment
- FEATURE-History.md#history-empty-range-and-errors: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-History.md#history-empty-range-and-errors: python-package=httpx2; scope=test; authorization=existing Target environment
- FEATURE-Convert.md#convert-decimal-and-rounding: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-Convert.md#convert-decimal-and-rounding: python-package=httpx2; scope=test; authorization=existing Target environment
- FEATURE-Convert.md#convert-validation-and-unknown-currency: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-Convert.md#convert-validation-and-unknown-currency: python-package=httpx2; scope=test; authorization=existing Target environment
- FEATURE-Health.md#health-response: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-Health.md#health-response: python-package=httpx2; scope=test; authorization=existing Target environment
- FEATURE-Health.md#health-method: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-Health.md#health-method: python-package=httpx2; scope=test; authorization=existing Target environment

## Stacked context
- stack: python_compact.md (SP 601)
- compass: COMPASS.md (SP 752)
- implements: FEATURE-Load.md (SP 930)
- context: eurofxref-hist_2025-01.csv (SP 411)
- context: eurofxref-hist_2025-02-03_04.csv (SP 44)
- context: eurofxref-hist_bad.csv (SP 16)
- context: ARCHITECTURE_compact.md (SP 142)
- context: DATABASE_compact.md (SP 146)
- stack: common_compact.md (SP 1079)
- stack: sqlite_compact.md (SP 1943)
- implements: FEATURE-Init.md (SP 347)
- implements: FEATURE-Currencies.md (SP 514)
- stack: fastapi.md (SP 667)
- implements: FEATURE-LatestRates.md (SP 525)
- implements: FEATURE-Stats.md (SP 665)
- implements: FEATURE-Rates.md (SP 654)
- implements: FEATURE-History.md (SP 989)
- implements: FEATURE-Convert.md (SP 1016)
- implements: FEATURE-Health.md (SP 317)
- implements: FEATURE-CLI-Errors.md (SP 463)
- stack: cli.md (SP 1755)

## Build directory changes
- app_server/main.py
- cli/__init__.py
- cli/commands.py
- cli/parser.py
- config/__init__.py
- data/app.db-shm
- data/app.db-wal
- data/logs/test_2026-10-26_164812.log
- data/logs/test_2026-10-26_164838.log
- persistence/schema.py
- services/rates.py
- tests/test_foundations.py
- tests/test_rates_repository.py

## Pre-build acceptance observation
- RED: load-valid-file (FEATURE-Load.md)
  intent: Loading the supplied January history succeeds and reports the fixture-derived date and rate counts.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      code = 1
    --- drydock: end values ---
    Traceback (most recent call last):
      File "load-valid-file.py", line 7, in <module>
        assert code == 0
               ^^^^^^^^^
    AssertionError
- RED: load-rejects-atomically (FEATURE-Load.md)
  intent: A rejected CSV file leaves the rates it would otherwise have changed untouched.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      code = 1
    --- drydock: end values ---
    Traceback (most recent call last):
      File "load-rejects-atomically.py", line 13, in <module>
        assert code == 3
               ^^^^^^^^^
    AssertionError
- RED: load-replaces-published-text (FEATURE-Load.md)
  intent: Loading a valid file stores its rate text exactly and replaces a matching stored rate.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      code = 1
    --- drydock: end values ---
    Traceback (most recent call last):
      File "load-replaces-published-text.py", line 15, in <module>
        assert code == 0
               ^^^^^^^^^
    AssertionError
- RED: init-clears-store (FEATURE-Init.md)
  intent: The init command succeeds and leaves the rates repository empty.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      code = 1
    --- drydock: end values ---
    Traceback (most recent call last):
      File "init-clears-store.py", line 8, in <module>
        assert code == 0
               ^^^^^^^^^
    AssertionError
- RED: init-rejects-extra-arguments (FEATURE-Init.md)
  intent: The init command rejects an unexpected argument with the usage exit status.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      code = 1
    --- drydock: end values ---
    Traceback (most recent call last):
      File "init-rejects-extra-arguments.py", line 4, in <module>
        assert code == 2
               ^^^^^^^^^
    AssertionError
- RED: currencies-list-sorted (FEATURE-Currencies.md)
  intent: The endpoint lists currencies present in the store in ascending order.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      response = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "currencies-list-sorted.py", line 14, in <module>
        assert response.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: currencies-base (FEATURE-Currencies.md)
  intent: The endpoint identifies EUR as the base currency.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      response = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "currencies-base.py", line 5, in <module>
        assert response.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: latest-rates-response (FEATURE-LatestRates.md)
  intent: The latest-rates route returns the stored rates for the latest publication.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      response = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "latest-rates-response.py", line 13, in <module>
        assert response.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- GREEN (prepassed): latest-rates-empty (FEATURE-LatestRates.md)
  intent: The latest-rates route returns 404 when there is no publication.
  return code: 0
- RED: stats-derive-from-store (FEATURE-Stats.md)
  intent: The statistics endpoint reflects rates inserted through the repository.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      response = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "stats-derive-from-store.py", line 19, in <module>
        assert response.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: stats-empty-store (FEATURE-Stats.md)
  intent: The statistics endpoint reports null date bounds when the rates store is empty.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      response = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "stats-empty-store.py", line 13, in <module>
        assert response.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: rates-effective-date (FEATURE-Rates.md)
  intent: The route resolves a requested date to the latest available publication and returns its stored rates.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      response = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "rates-effective-date.py", line 15, in <module>
        assert response.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: rates-errors (FEATURE-Rates.md)
  intent: The route returns the declared errors for a missing effective publication and a malformed date.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      client = <starlette.testclient.TestClient object at 0x777d8a9cda00>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "rates-errors.py", line 5, in <module>
        assert client.get("/rates/2025-13-01").status_code == 422
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: history-range-and-statistics (FEATURE-History.md)
  intent: The history endpoint returns bounded points and statistics derived from the seeded rates.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      response = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "history-range-and-statistics.py", line 20, in <module>
        assert response.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: history-empty-range-and-errors (FEATURE-History.md)
  intent: The history endpoint distinguishes an empty range from a currency with no history and rejects malformed bounds.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      empty = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "history-empty-range-and-errors.py", line 13, in <module>
        assert empty.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: convert-decimal-and-rounding (FEATURE-Convert.md)
  intent: The conversion endpoint echoes its input amount and calculates its rate and result from the fixture rates with the specified rounding.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      response = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "convert-decimal-and-rounding.py", line 27, in <module>
        assert response.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: convert-validation-and-unknown-currency (FEATURE-Convert.md)
  intent: The conversion endpoint rejects missing or malformed inputs and returns 404 for a currency without a rate.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      client = <starlette.testclient.TestClient object at 0x7aaba5c419a0>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "convert-validation-and-unknown-currency.py", line 4, in <module>
        assert client.get("/convert", params={"from": "USD", "to": "EUR"}).status_code == 422
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: health-response (FEATURE-Health.md)
  intent: The health endpoint responds successfully with the documented JSON body.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      response = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "health-response.py", line 5, in <module>
        assert response.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: health-method (FEATURE-Health.md)
  intent: An unsupported method is refused by the health route.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      response = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "health-method.py", line 5, in <module>
        assert response.status_code == 405
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: cli-usage-errors (FEATURE-CLI-Errors.md)
  intent: Usage errors return status 2 and produce no standard output.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      code = 1
    --- drydock: end values ---
    Traceback (most recent call last):
      File "cli-usage-errors.py", line 5, in <module>
        assert code == 2
               ^^^^^^^^^
    AssertionError
- RED: cli-operational-errors (FEATURE-CLI-Errors.md)
  intent: File read failures return status 1 and rejected CSV files return status 3.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      code = 1
    --- drydock: end values ---
    Traceback (most recent call last):
      File "cli-operational-errors.py", line 10, in <module>
        assert code == 3
               ^^^^^^^^^
    AssertionError

## Post-build programmatic acceptance
- PASS: load-valid-file (FEATURE-Load.md)
  intent: Loading the supplied January history succeeds and reports the fixture-derived date and rate counts.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261026.202600/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: load-rejects-atomically (FEATURE-Load.md)
  intent: A rejected CSV file leaves the rates it would otherwise have changed untouched.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261026.202600/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: load-replaces-published-text (FEATURE-Load.md)
  intent: Loading a valid file stores its rate text exactly and replaces a matching stored rate.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261026.202600/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: init-clears-store (FEATURE-Init.md)
  intent: The init command succeeds and leaves the rates repository empty.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261026.202600/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: init-rejects-extra-arguments (FEATURE-Init.md)
  intent: The init command rejects an unexpected argument with the usage exit status.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261026.202600/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: currencies-list-sorted (FEATURE-Currencies.md)
  intent: The endpoint lists currencies present in the store in ascending order.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261026.202600/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: currencies-base (FEATURE-Currencies.md)
  intent: The endpoint identifies EUR as the base currency.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261026.202600/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: latest-rates-response (FEATURE-LatestRates.md)
  intent: The latest-rates route returns the stored rates for the latest publication.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261026.202600/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: latest-rates-empty (FEATURE-LatestRates.md)
  intent: The latest-rates route returns 404 when there is no publication.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261026.202600/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: stats-derive-from-store (FEATURE-Stats.md)
  intent: The statistics endpoint reflects rates inserted through the repository.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261026.202600/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: stats-empty-store (FEATURE-Stats.md)
  intent: The statistics endpoint reports null date bounds when the rates store is empty.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261026.202600/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: rates-effective-date (FEATURE-Rates.md)
  intent: The route resolves a requested date to the latest available publication and returns its stored rates.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261026.202600/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: rates-errors (FEATURE-Rates.md)
  intent: The route returns the declared errors for a missing effective publication and a malformed date.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261026.202600/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: history-range-and-statistics (FEATURE-History.md)
  intent: The history endpoint returns bounded points and statistics derived from the seeded rates.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261026.202600/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: history-empty-range-and-errors (FEATURE-History.md)
  intent: The history endpoint distinguishes an empty range from a currency with no history and rejects malformed bounds.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261026.202600/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: convert-decimal-and-rounding (FEATURE-Convert.md)
  intent: The conversion endpoint echoes its input amount and calculates its rate and result from the fixture rates with the specified rounding.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261026.202600/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: convert-validation-and-unknown-currency (FEATURE-Convert.md)
  intent: The conversion endpoint rejects missing or malformed inputs and returns 404 for a currency without a rate.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261026.202600/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: health-response (FEATURE-Health.md)
  intent: The health endpoint responds successfully with the documented JSON body.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261026.202600/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: health-method (FEATURE-Health.md)
  intent: An unsupported method is refused by the health route.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261026.202600/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: cli-usage-errors (FEATURE-CLI-Errors.md)
  intent: Usage errors return status 2 and produce no standard output.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261026.202600/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: cli-operational-errors (FEATURE-CLI-Errors.md)
  intent: File read failures return status 1 and rejected CSV files return status 3.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261026.202600/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0

## Repair attempts
- attempt 0 (initial build): failed; 18/21 checks model=gpt-6-luna; execution 20261026.203914.223Z-c325e8cf; reason: programmatic acceptance failed: init-clears-store, history-range-and-statistics, history-empty-range-and-errors
- attempt 1 (repair 1): failed; 20/21 checks model=gpt-6-luna; execution 20261026.204315.898Z-c5325729; reason: programmatic acceptance failed: init-clears-store
- attempt 2 (repair 2): built; 21/21 checks model=gpt-6-luna; execution 20261026.204750.616Z-f17235ce

## Build summary
RESULT: SUCCESS

FILES CHANGED:
- persistence/schema.py
- services/rates.py
- tests/test_rates_repository.py

SUMMARY:
Added a keyed rate delete operation and updated `init` to clear rows through the persistence boundary. Added a rollback-fixture test for initialization. The focused repository suite passed: 6 tests.

Restart required — run the start script or equivalent.

BLOCKERS:
- None
