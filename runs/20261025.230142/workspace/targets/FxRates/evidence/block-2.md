# Evidence: Block 2 · Foundational (block-2)

- block type: block
- date: 2026-10-25
- resulting state: closed/failed
- story points (combined assembled cost): 12796
- execution id: 20261025.231658.095Z-dfe7e129

## Stories built
- Declare the rates store and repository operations. (database) [story]
- Provide the FastAPI application foundation. (api-foundation) [story]
- Provide the executable command-line foundation. (cli-foundation) [story]

## Acceptance tooling authorization
- FEATURE-ApiFoundation.md#api_factory_and_app: python-package=httpx; scope=test; authorization=Drydock test environment
- FEATURE-ApiFoundation.md#api_test_client: python-package=httpx; scope=test; authorization=Drydock test environment

## Stacked context
- stack: python_compact.md (SP 601)
- compass: COMPASS.md (SP 752)
- implements: DATABASE.md (SP 1888)
- stack: persistence.md (SP 4001)
- stack: sqlite.md (SP 2195)
- implements: FEATURE-ApiFoundation.md (SP 407)
- context: ARCHITECTURE_compact.md (SP 256)
- context: DATABASE.md (SP 1888)
- stack: fastapi.md (SP 497)
- implements: FEATURE-CliFoundation.md (SP 340)
- stack: cli.md (SP 1755)

## Build directory changes
- app_server/testing.py
- cli/__init__.py
- cli/__main__.py
- cli/commands.py
- cli/parser.py
- cli/testing.py
- fxrates
- pyproject.toml
- tests/test_foundations.py
- uv.lock
- cli.py

## Pre-build acceptance observation
- RED: rates_get_round_trip (DATABASE.md)
  intent: Retrieve a stored rate by its date and currency through the declared repository operation.
  error: baseline unavailable: authorized Target tooling is not provisioned
- RED: rates_list_filters_and_order (DATABASE.md)
  intent: List stored rates in date and currency order and filter by currency and inclusive date bounds.
  error: baseline unavailable: authorized Target tooling is not provisioned
- RED: rates_upsert_replaces (DATABASE.md)
  intent: Upsert replaces an existing date and currency rate while preserving its published text.
  error: baseline unavailable: authorized Target tooling is not provisioned
- RED: rates_delete_round_trip (DATABASE.md)
  intent: Delete removes the selected date and currency rate from the repository.
  error: baseline unavailable: authorized Target tooling is not provisioned
- RED: api_factory_and_app (FEATURE-ApiFoundation.md)
  intent: The application factory returns a FastAPI application and the module exports its application instance.
  error: baseline unavailable: authorized Target tooling is not provisioned
- RED: api_test_client (FEATURE-ApiFoundation.md)
  intent: The published web client callable returns a client for the application.
  error: baseline unavailable: authorized Target tooling is not provisioned
- RED: cli_entry_point (FEATURE-CliFoundation.md)
  intent: The CLI foundation exposes a callable entry point returning an integer status.
  error: baseline unavailable: authorized Target tooling is not provisioned
- RED: cli_runner_contract (FEATURE-CliFoundation.md)
  intent: The published CLI runner returns an integer exit code and captured output strings.
  error: baseline unavailable: authorized Target tooling is not provisioned

## Post-build programmatic acceptance
- PASS: rates_get_round_trip (DATABASE.md)
  intent: Retrieve a stored rate by its date and currency through the declared repository operation.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.230142/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- FAIL: rates_list_filters_and_order (DATABASE.md)
  intent: List stored rates in date and currency order and filter by currency and inclusive date bounds.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.230142/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 1
  stderr:
    --- drydock: values at failure ---
      all_rows = [RatesListOutput(date='2099-01-01', currency='YYY', rate='8.00'), RatesListOutput(date='2099-01-01', currency='ZZZ', rate='1.00'), RatesListOutput(date='2099-01-02', currency='ZZZ', rate='2.00'), RatesListOutput(date='2099-01-03', currency='ZZZ', rate='3.00')]
      currency = 'ZZZ'
      other_currency = 'YYY'
      dates = ['2099-01-03', '2099-01-01', '2099-01-02']
    --- drydock: end values ---
    Traceback (most recent call last):
      File "rates_list_filters_and_order.py", line 20, in <module>
        assert [(row.date, row.currency, row.rate) for row in all_rows if row.date in dates] == [
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- PASS: rates_upsert_replaces (DATABASE.md)
  intent: Upsert replaces an existing date and currency rate while preserving its published text.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.230142/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: rates_delete_round_trip (DATABASE.md)
  intent: Delete removes the selected date and currency rate from the repository.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.230142/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: api_factory_and_app (FEATURE-ApiFoundation.md)
  intent: The application factory returns a FastAPI application and the module exports its application instance.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.230142/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: api_test_client (FEATURE-ApiFoundation.md)
  intent: The published web client callable returns a client for the application.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.230142/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
  stderr:
    /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.230142/build/FxRates/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
- PASS: cli_entry_point (FEATURE-CliFoundation.md)
  intent: The CLI foundation exposes a callable entry point returning an integer status.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.230142/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
  stderr:
    error: unknown command: __foundation_probe__
- PASS: cli_runner_contract (FEATURE-CliFoundation.md)
  intent: The published CLI runner returns an integer exit code and captured output strings.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.230142/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0

## Repair attempts
- attempt 0 (initial build): failed; 7/8 checks model=gpt-6-luna; execution 20261025.231217.506Z-4bb7d9e1; reason: programmatic acceptance failed: rates_list_filters_and_order
- attempt 1 (repair 1): failed; 7/8 checks model=gpt-6-luna; execution 20261025.231519.380Z-fc932b2e; reason: programmatic acceptance failed: rates_list_filters_and_order
- attempt 2 (repair 2): failed; 7/8 checks model=gpt-6-luna; execution 20261025.231658.095Z-dfe7e129; stopped: deterministic acceptance score did not improve on 2 consecutive calls; reason: programmatic acceptance failed: rates_list_filters_and_order

## Failure
- summary: programmatic acceptance failed: rates_list_filters_and_order
- detail:
    Block "Block 2 · Foundational" [block-2] failed its acceptance criteria.
      Story "Declare the rates store and repository operations." [database] does not meet its own acceptance criteria:
        - AC rates_list_filters_and_order — List stored rates in date and currency order and filter by currency and inclusive date bounds.
            assertion: assert [(row.date, row.currency, row.rate) for row in all_rows if row.date in dates] == [ → AssertionError
            raised at: rates_list_filters_and_order.py:20
            process exit code: 1
            values at failure:
              all_rows = [RatesListOutput(date='2099-01-01', currency='YYY', rate='8.00'), RatesListOutput(date='2099-01-01', currency='ZZZ', rate='1.00'), RatesListOutput(date='2099-01-02', currency='ZZZ', rate='2.00'), RatesListOutput(date='2099-01-03', currency='ZZZ', rate='3.00')]
              currency = 'ZZZ'
              other_currency = 'YYY'
              dates = ['2099-01-03', '2099-01-01', '2099-01-02']
            check stderr:
              Traceback (most recent call last):
                File "rates_list_filters_and_order.py", line 20, in <module>
                  assert [(row.date, row.currency, row.rate) for row in all_rows if row.date in dates] == [
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
              AssertionError

## Build summary
RESULT: SUCCESS

FILES CHANGED:
- None

SUMMARY:
The complete failure log confirms `rates.list()` returns the declared order: date ascending, then currency ascending. For 2099-01-01 that places `YYY` before `ZZZ`, while the acceptance assertion expects `ZZZ` first. The implementation matches the `DATABASE.md` order contract, so I left it unchanged.

AC_BROKEN: rates_list_filters_and_order

BLOCKERS:
- None

FAILURE_SUMMARY: Acceptance expectation conflicts with the declared list order
FAILURE_DETAIL: The assertion expects ZZZ before YYY for the same date, but the declared currency ascending order requires YYY before ZZZ. The implementation’s result matches the declaration; update the acceptance expectation or the declaration before rerunning.
