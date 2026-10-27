# Evidence: Block 15 · Service (block-15)

- block type: block
- date: 2026-10-27
- resulting state: closed/verified
- story points (combined assembled cost): 5821
- execution id: 20261027.165850.342Z-9b040970

## Stories built
- /history refuses unknown currencies and malformed bounds. (hist-003-errors) [story]

## Acceptance tooling authorization
- FEATURE-HistoryErrors.md#history-errors-unknown-currency: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-HistoryErrors.md#history-errors-unknown-currency: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-HistoryErrors.md#history-errors-unknown-currency: python-package=httpx2; scope=test; authorization=existing Target environment
- FEATURE-HistoryErrors.md#history-errors-empty-range-is-not-404: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-HistoryErrors.md#history-errors-empty-range-is-not-404: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-HistoryErrors.md#history-errors-empty-range-is-not-404: python-package=httpx2; scope=test; authorization=existing Target environment
- FEATURE-HistoryErrors.md#history-errors-malformed-bounds: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-HistoryErrors.md#history-errors-malformed-bounds: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-HistoryErrors.md#history-errors-malformed-bounds: python-package=httpx2; scope=test; authorization=existing Target environment

## Stacked context
- stack: python_compact.md (SP 921)
- compass: COMPASS.md (SP 1152)
- implements: FEATURE-HistoryErrors.md (SP 1482)
- context: ARCHITECTURE_compact.md (SP 386)
- context: DATABASE_compact.md (SP 707)
- stack: fastapi_compact.md (SP 1122)

## Build directory changes
- app_server/routes.py
- data/app.db-shm
- data/app.db-wal
- data/logs/test_2026-10-27_130134.log
- fxrates_app/history.py
- tests/test_history_errors.py
- tests/test_history_points.py

## Pre-build acceptance observation
- RED: history-errors-unknown-currency (FEATURE-HistoryErrors.md)
  intent: A currency with no stored rate answers 404, including EUR; neither code is seeded by this criterion.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      client = <starlette.testclient.TestClient object at 0x72e078708f20>
      unknown = 'ZZX'
    --- drydock: end values ---
    Traceback (most recent call last):
      File "history-errors-unknown-currency.py", line 11, in <module>
        assert client.get(f"/history/{unknown}").status_code == 404
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- GREEN (prepassed): history-errors-empty-range-is-not-404 (FEATURE-HistoryErrors.md)
  intent: A known currency whose bounds exclude every point answers 200, so 404 is reserved for a currency with no stored rate at all.
  return code: 0
- GREEN (prepassed): history-errors-malformed-bounds (FEATURE-HistoryErrors.md)
  intent: A malformed start or end is refused with 422 for a stored currency, whether the text is a bad shape or an impossible calendar date.
  return code: 0

## Post-build programmatic acceptance
- PASS: history-errors-unknown-currency (FEATURE-HistoryErrors.md)
  intent: A currency with no stored rate answers 404, including EUR; neither code is seeded by this criterion.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: history-errors-empty-range-is-not-404 (FEATURE-HistoryErrors.md)
  intent: A known currency whose bounds exclude every point answers 200, so 404 is reserved for a currency with no stored rate at all.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: history-errors-malformed-bounds (FEATURE-HistoryErrors.md)
  intent: A malformed start or end is refused with 422 for a stored currency, whether the text is a bad shape or an impossible calendar date.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0

## Build summary
Baseline first, so I know which failures predate my change.Baseline is green (313 passed). The route already returns 422 for malformed bounds through FastAPI pattern validation and `_calendar_date`. What's missing is the 404 for a currency with no stored rate at all. I'll add that in the service, since the service owns the business rule, and map it in the route.The existing `test_unknown_currency_has_no_points_but_is_ok` asserts 200 for an unknown currency, which this spec reverses. I'll update that test to the new contract rather than keep a contradicting one. First I'll check the style of the sibling error test file.Now a dedicated test file covering the spec's acceptance cases plus the boundaries the spec names.The name `..._is_ok_not_not_found` reads badly; I'll fix it, then run the history tests and the full suite.All 329 tests pass. The protocol for a behavioral story is `sh bin/test.sh`, so I'll run that exact entry point too.`/history` now answers 404 for a currency with no stored rate at all (including `EUR`), and 422 for a malformed `start` or `end`. The project's `sh bin/test.sh` exits 0 with 329 tests passing, up from 313 before the change.

- **Unknown currency (404):** `fxrates_app/history.py` now raises `UnknownCurrency` when the bounded query is empty and the unbounded history for the code is also empty. A currency with stored rates outside the bounds still returns 200 with `count` 0. `app_server/routes.py` maps the error to 404.
- **Malformed bounds (422):** already handled by the route's existing FastAPI pattern check and `_calendar_date`, so I left that path alone.
- **Existing test changed:** `tests/test_history_points.py::test_unknown_currency_has_no_points_but_is_ok` asserted 200 for an unknown currency. This spec reverses that, so I rewrote it as `test_unknown_currency_is_not_found` expecting 404. This is the only pre-existing test whose expectation I changed.
- **New tests:** `tests/test_history_errors.py` covers the unknown and base-currency 404s, the 404 flipping to 200 once a rate is stored, the out-of-bounds 200, parametrized malformed `start` and `end` values returning 422, and the service-level exception.

I did not run the spec's three `AC` blocks as standalone criteria. Their assertions are covered by the new and updated tests above, which pass.

Decision for you: when a currency is unknown and a bound is also malformed, the 422 wins, because validation runs before the lookup. The spec doesn't settle that ordering. Say if you want 404 to take precedence instead.

RESULT: SUCCESS

FILES CHANGED:
- fxrates_app/history.py
- app_server/routes.py
- tests/test_history_points.py
- tests/test_history_errors.py

SUMMARY:
Added the 404 for a currency with no stored rate at all, including `EUR`, and kept the existing 422 for malformed bounds. Updated the one contradicting pre-existing test and added focused error tests. `sh bin/test.sh` exits 0 with 329 passed.

<blueprint-decisions>
[{"spec":"FEATURE-HistoryErrors.md","severity":"Low","subject":"Check order for an unknown currency combined with a malformed bound","decision":"Bound validation (422) runs before the currency lookup (404), so a request with both an unknown code and a malformed bound answers 422. The spec does not state which applies first. Is that acceptable, or should unknown currency take precedence?"}]
</blueprint-decisions>
