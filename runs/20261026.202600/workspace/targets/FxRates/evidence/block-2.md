# Evidence: Block 2 · Foundational (block-2)

- block type: block
- date: 2026-10-26
- resulting state: closed/verified
- story points (combined assembled cost): 14722
- execution id: 20261026.203315.586Z-eea2c9ed

## Stories built
- Declare the rates schema and generated repository contract. (database) [story]
- Establish the FastAPI application and test client. (app_server) [story]
- Establish the fxrates executable and CLI entry point. (cli) [story]

## Acceptance tooling authorization
- FEATURE-AppServer.md#app-server-factory: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-AppServer.md#app-server-factory: python-package=httpx2; scope=test; authorization=Drydock test environment

## Reusable compacts
- DATABASE_compact.md
- ARCHITECTURE_compact.md

## Stacked context
- stack: python_compact.md (SP 601)
- compass: COMPASS.md (SP 752)
- implements: DATABASE.md (SP 1930)
- stack: common_compact.md (SP 1079)
- stack: persistence.md (SP 4001)
- stack: sqlite.md (SP 2195)
- implements: FEATURE-AppServer.md (SP 429)
- context: ARCHITECTURE.md (SP 661)
- context: DATABASE.md (SP 1930)
- stack: fastapi.md (SP 667)
- implements: FEATURE-CLI.md (SP 366)
- stack: cli.md (SP 1755)

## Build directory changes
- app_server/main.py
- app_server/testing.py
- bin/test.sh
- cli/__init__.py
- cli/__main__.py
- cli/testing.py
- data/app.db-shm
- data/app.db-wal
- data/logs/test_2026-10-26_163552.log
- fxrates
- pyproject.toml
- tests/test_foundations.py
- tests/test_rates_repository.py
- uv.lock

## Pre-build acceptance observation
- RED: rates-upsert (DATABASE.md)
  intent: The repository stores a rate and replaces the value for the same date and currency.
  error: baseline unavailable: authorized Target tooling is not provisioned
- RED: rates-by-date (DATABASE.md)
  intent: The repository returns the stored rates for a requested publication date.
  error: baseline unavailable: authorized Target tooling is not provisioned
- RED: rates-publications-through (DATABASE.md)
  intent: The repository returns stored publications on or before the requested date in descending date order.
  error: baseline unavailable: authorized Target tooling is not provisioned
- RED: rates-history (DATABASE.md)
  intent: The repository returns a currency's rates within inclusive optional date bounds in ascending date order.
  error: baseline unavailable: authorized Target tooling is not provisioned
- RED: rates-list (DATABASE.md)
  intent: The repository lists stored rates with their published text.
  error: baseline unavailable: authorized Target tooling is not provisioned
- RED: app-server-factory (FEATURE-AppServer.md)
  intent: The application factory and published test client are importable and construct the declared FastAPI interfaces.
  error: baseline unavailable: authorized Target tooling is not provisioned
- RED: cli-foundation-interfaces (FEATURE-CLI.md)
  intent: The CLI entry point and in-process runner expose the published callable interfaces.
  error: baseline unavailable: authorized Target tooling is not provisioned

## Post-build programmatic acceptance
- PASS: rates-upsert (DATABASE.md)
  intent: The repository stores a rate and replaces the value for the same date and currency.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261026.202600/build/FxRates/.venv/bin/python
  provisioning: uv sync --locked succeeded
  return code: 0
- PASS: rates-by-date (DATABASE.md)
  intent: The repository returns the stored rates for a requested publication date.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261026.202600/build/FxRates/.venv/bin/python
  provisioning: uv sync --locked succeeded
  return code: 0
- PASS: rates-publications-through (DATABASE.md)
  intent: The repository returns stored publications on or before the requested date in descending date order.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261026.202600/build/FxRates/.venv/bin/python
  provisioning: uv sync --locked succeeded
  return code: 0
- PASS: rates-history (DATABASE.md)
  intent: The repository returns a currency's rates within inclusive optional date bounds in ascending date order.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261026.202600/build/FxRates/.venv/bin/python
  provisioning: uv sync --locked succeeded
  return code: 0
- PASS: rates-list (DATABASE.md)
  intent: The repository lists stored rates with their published text.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261026.202600/build/FxRates/.venv/bin/python
  provisioning: uv sync --locked succeeded
  return code: 0
- PASS: app-server-factory (FEATURE-AppServer.md)
  intent: The application factory and published test client are importable and construct the declared FastAPI interfaces.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261026.202600/build/FxRates/.venv/bin/python
  provisioning: uv sync --locked succeeded
  return code: 0
- PASS: cli-foundation-interfaces (FEATURE-CLI.md)
  intent: The CLI entry point and in-process runner expose the published callable interfaces.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261026.202600/build/FxRates/.venv/bin/python
  provisioning: uv sync --locked succeeded
  return code: 0

## Agent self-report (advisory)
The build agent declared a failure. This report is advisory; Drydock's execution and deterministic checks determine the block's outcome.
- summary: Required rates repository operations are missing
- detail:
    The available generated persistence contract lacks the requested count, currency-list, effective-date, and latest-publication operations. The persistence rules prohibit editing generated files, and no writable DATABASE.md source or generator was supplied. Provide the declaration and run the Drydock database generation step before rerunning.

## Build summary
<reusable-compact filename="DATABASE.md">
Rates are stored in `rates(id, date, currency, rate)`, with text values and a unique `(date, currency)` key. The generated repository currently exposes `upsert`, `by_date`, `publications_through`, `history`, and `list`; history bounds are inclusive and results use their declared ordering. Application code must use the generated persistence package and resolve the store from `DATABASE_URL`, then `DATABASE_PATH`, then `data/app.db`.
</reusable-compact>

<reusable-compact filename="ARCHITECTURE.md">
Python 3.11+, FastAPI, uvicorn, and SQLite. `cli` owns the root executable and dispatch, `app_server` owns the application factory and routes, `services` owns shared behavior, `persistence` owns generated storage access, and `config` owns database location resolution. HTTP handlers and CLI commands call services; only persistence accesses the database. Preserve ECB rates as text and use `Decimal` for arithmetic.
</reusable-compact>

RESULT: FAILED

FILES CHANGED:
- `pyproject.toml`
- `uv.lock`
- `cli/__init__.py`
- `cli/testing.py`
- `cli/__main__.py`
- `fxrates`
- `app_server/main.py`
- `app_server/testing.py`
- `bin/test.sh`
- `tests/test_foundations.py`
- `tests/test_rates_repository.py`
- `data/logs/test_2026-10-26_163552.log`

SUMMARY:
Implemented the FastAPI factory and test client, `fxrates` entry point and in-process CLI runner, dependency declarations, and tests for the available repository contract. `sh bin/test.sh` passed: 9 tests.

BLOCKERS:
- The build instructions require additional rates repository operations, but the persistence contract says its generated package must not be edited by the build agent. The writable `DATABASE.md` declaration and regeneration step are not available in this build directory, so those operations could not be declared or generated.

FAILURE_SUMMARY: Required rates repository operations are missing
FAILURE_DETAIL: The available generated persistence contract lacks the requested count, currency-list, effective-date, and latest-publication operations. The persistence rules prohibit editing generated files, and no writable DATABASE.md source or generator was supplied. Provide the declaration and run the Drydock database generation step before rerunning.
