# Evidence: Block 14 · Service (block-14)

- block type: block
- date: 2026-10-27
- resulting state: closed/verified
- story points (combined assembled cost): 7993
- execution id: 20261027.164918.885Z-a8a38bcd

## Stories built
- /convert refuses unknown currencies and bad inputs with 404 and 422. (convert-002-convert-errors) [story]
- /history reports count, min, max, and mean. (hist-002-summary) [story]

## Acceptance tooling authorization
- FEATURE-ConvertErrors.md#convert-unknown-currency-404: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-ConvertErrors.md#convert-unknown-currency-404: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-ConvertErrors.md#convert-unknown-currency-404: python-package=httpx2; scope=test; authorization=existing Target environment
- FEATURE-ConvertErrors.md#convert-no-publication-404: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-ConvertErrors.md#convert-no-publication-404: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-ConvertErrors.md#convert-no-publication-404: python-package=httpx2; scope=test; authorization=existing Target environment
- FEATURE-ConvertErrors.md#convert-validation-422: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-ConvertErrors.md#convert-validation-422: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-ConvertErrors.md#convert-validation-422: python-package=httpx2; scope=test; authorization=existing Target environment
- FEATURE-HistoryStats.md#history-stats-min-max-count: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-HistoryStats.md#history-stats-min-max-count: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-HistoryStats.md#history-stats-min-max-count: python-package=httpx2; scope=test; authorization=existing Target environment
- FEATURE-HistoryStats.md#history-stats-mean-half-even: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-HistoryStats.md#history-stats-mean-half-even: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-HistoryStats.md#history-stats-mean-half-even: python-package=httpx2; scope=test; authorization=existing Target environment
- FEATURE-HistoryStats.md#history-stats-bounded: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-HistoryStats.md#history-stats-bounded: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-HistoryStats.md#history-stats-bounded: python-package=httpx2; scope=test; authorization=existing Target environment
- FEATURE-HistoryStats.md#history-stats-empty: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-HistoryStats.md#history-stats-empty: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-HistoryStats.md#history-stats-empty: python-package=httpx2; scope=test; authorization=existing Target environment

## Stacked context
- stack: python_compact.md (SP 921)
- compass: COMPASS.md (SP 1152)
- implements: FEATURE-ConvertErrors.md (SP 1307)
- context: ARCHITECTURE_compact.md (SP 386)
- context: DATABASE_compact.md (SP 707)
- stack: fastapi_compact.md (SP 1122)
- implements: FEATURE-HistoryStats.md (SP 2222)

## Build directory changes
- app_server/routes.py
- data/app.db-shm
- data/app.db-wal
- data/logs/test_2026-10-27_124938.log
- data/logs/test_2026-10-27_125059.log
- fxrates_app/history.py
- tests/test_convert_errors.py
- tests/test_history_stats.py

## Pre-build acceptance observation
- GREEN (prepassed): convert-unknown-currency-404 (FEATURE-ConvertErrors.md)
  intent: A currency with no stored rate on the effective date answers 404, whichever side it is on.
  return code: 0
- GREEN (prepassed): convert-no-publication-404 (FEATURE-ConvertErrors.md)
  intent: A date earlier than every publication answers 404 even for stored currencies.
  return code: 0
- GREEN (prepassed): convert-validation-422 (FEATURE-ConvertErrors.md)
  intent: Missing parameters, a malformed amount, and malformed or impossible dates are all refused with 422.
  return code: 0
- RED: history-stats-min-max-count (FEATURE-HistoryStats.md)
  intent: Count, min, and max are derived from the seeded rate texts by Decimal value, and min and max keep the stored text unchanged.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      body = {'currency': 'ZZH', 'base': 'EUR', 'count': 5, 'points': [{'date': '1900-12-01', 'rate': '0.9453'}, {'date': '1900-12-02', 'rate': '0.943'}, {'date': '1900-12-03', 'rate': '0.9441'}, {'date': '1900-12-04', 'rate': '10.5'}, {'date': '1900-12-05', 'rate': '9.75'}]}
      texts = ['0.9453', '0.943', '0.9441', '10.5', '9.75']
    --- drydock: end values ---
    Traceback (most recent call last):
      File "history-stats-min-max-count.py", line 24, in <module>
        assert body["min"] == min(texts, key=Decimal)
               ~~~~^^^^^^^
    KeyError: 'min'
- RED: history-stats-mean-half-even (FEATURE-HistoryStats.md)
  intent: Mean is the exact mean rounded half to even at six decimals and printed with six decimals; the two cases are exact ties at the seventh decimal, so they distinguish half-even from half-up.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      body = {'currency': 'ZZM', 'base': 'EUR', 'count': 2, 'points': [{'date': '1901-01-01', 'rate': '1.000000'}, {'date': '1901-01-02', 'rate': '1.000001'}]}
      mean = Decimal('1.000000')
    --- drydock: end values ---
    Traceback (most recent call last):
      File "history-stats-mean-half-even.py", line 22, in <module>
        assert body["mean"] == f"{mean:.6f}"
               ~~~~^^^^^^^^
    KeyError: 'mean'
- RED: history-stats-bounded (FEATURE-HistoryStats.md)
  intent: Statistics cover only the points inside the requested bounds, not the whole stored history.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      body = {'currency': 'ZZH', 'base': 'EUR', 'count': 2, 'points': [{'date': '1901-02-02', 'rate': '1.5'}, {'date': '1901-02-03', 'rate': '2.25'}]}
      inside = ['1.5', '2.25']
    --- drydock: end values ---
    Traceback (most recent call last):
      File "history-stats-bounded.py", line 25, in <module>
        assert body["min"] == min(inside, key=Decimal)
               ~~~~^^^^^^^
    KeyError: 'min'
- RED: history-stats-empty (FEATURE-HistoryStats.md)
  intent: A history with no points in range reports count 0 and null statistics with an empty points list, still as a 200.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      body = {'currency': 'ZZH', 'base': 'EUR', 'count': 0, 'points': []}
    --- drydock: end values ---
    Traceback (most recent call last):
      File "history-stats-empty.py", line 15, in <module>
        assert body["min"] is None
               ~~~~^^^^^^^
    KeyError: 'min'

## Post-build programmatic acceptance
- PASS: convert-unknown-currency-404 (FEATURE-ConvertErrors.md)
  intent: A currency with no stored rate on the effective date answers 404, whichever side it is on.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: convert-no-publication-404 (FEATURE-ConvertErrors.md)
  intent: A date earlier than every publication answers 404 even for stored currencies.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: convert-validation-422 (FEATURE-ConvertErrors.md)
  intent: Missing parameters, a malformed amount, and malformed or impossible dates are all refused with 422.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: history-stats-min-max-count (FEATURE-HistoryStats.md)
  intent: Count, min, and max are derived from the seeded rate texts by Decimal value, and min and max keep the stored text unchanged.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: history-stats-mean-half-even (FEATURE-HistoryStats.md)
  intent: Mean is the exact mean rounded half to even at six decimals and printed with six decimals; the two cases are exact ties at the seventh decimal, so they distinguish half-even from half-up.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: history-stats-bounded (FEATURE-HistoryStats.md)
  intent: Statistics cover only the points inside the requested bounds, not the whole stored history.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: history-stats-empty (FEATURE-HistoryStats.md)
  intent: A history with no points in range reports count 0 and null statistics with an empty points list, still as a 200.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0

## Build summary
I'll start by inspecting the build directory and the current state of the code.The convert error paths already exist, so this block is mostly the history summary. Before editing, I'll establish a baseline by running the existing suite through the declared runner.Baseline is green: 285 passed. The convert error contract is already implemented, and the history route lacks `min`, `max`, and `mean`. I'll add the statistics as a service function over the returned points, so the route only parses input and calls the service.The tuple handling in `history_summary` is more awkward than it needs to be. I'll simplify it to key on the points directly.Now the tests. The four history-statistics acceptance checks become named tests, plus boundary cases (empty, one point, a bound-filtered set). I'll follow the existing fixture pattern in `test_history_points.py`.Next, a convert-error file that mirrors the declared checks. The existing `test_convert.py` covers the `to`-side and most validation cases; this adds the `from`-side unknown-currency check and the publication-before-date check using the spec's exact inputs.Now I'll run the two new test files and the existing history and convert suites, then the full suite through the declared runner.Both stories are implemented and the full suite passes: 313 tests, up from 285, with the runner exiting 0.

I did not run `sh sources/run.sh`; it is the terminal story and this block is not the last one.

RESULT: SUCCESS

FILES CHANGED:
- fxrates_app/history.py
- app_server/routes.py
- tests/test_history_stats.py
- tests/test_convert_errors.py

SUMMARY:
- **convert-002-convert-errors:** The `/convert` error paths were already in place: 404 for unknown currencies and missing publications, and 422 for missing parameters, a bad amount, or a bad date. I added `tests/test_convert_errors.py` to cover the declared checks, including the `from`-side unknown-currency case that the existing tests did not exercise. No application code changed for this story.
- **hist-002-summary:** `fxrates_app/history.py` gains `history_summary(points)`, which returns `count`, `min`, `max`, and `mean`. Min and max compare as `Decimal` and return the stored text unchanged. Mean is quantized half-even to six decimals and written with six decimals. With no points, count is 0 and the other three are `None`. `app_server/routes.py` merges that summary into the `/history/{code}` response; `points` is unchanged.
- **Tests:** `tests/test_history_stats.py` contains named tests for the four declared AC cases (count, min/max, half-even ties at both seventh-decimal cases, and the bounded and empty cases). It also covers trailing zeros in stored text, a single point, and the response key set.
- **Choices I made:** The statistics are a service function over the returned points rather than inline in the route, so the route only parses input and calls services. The tests compute expected values with `Decimal` from the seeded texts and also hardcode the two tie results.

Checks run:
- Targeted: `.venv/bin/pytest -q` on the four files covering history and convert: 75 passed.
- Full: `sh bin/test.sh`: 313 passed, exit 0.
