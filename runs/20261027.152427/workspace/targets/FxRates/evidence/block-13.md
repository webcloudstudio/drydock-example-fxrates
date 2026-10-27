# Evidence: Block 13 · Service (block-13)

- block type: block
- date: 2026-10-27
- resulting state: closed/verified
- story points (combined assembled cost): 9810
- execution id: 20261027.163945.512Z-b207149b

## Stories built
- GET /convert computes exact, half-even rounded conversions. (convert-001-convert) [story]
- GET /history/{code} lists ascending points between optional bounds. (hist-001-points) [story]

## Acceptance tooling authorization
- FEATURE-Convert.md#convert-two-currencies: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-Convert.md#convert-two-currencies: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-Convert.md#convert-two-currencies: python-package=httpx2; scope=test; authorization=existing Target environment
- FEATURE-Convert.md#convert-eur-implicit-rate: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-Convert.md#convert-eur-implicit-rate: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-Convert.md#convert-eur-implicit-rate: python-package=httpx2; scope=test; authorization=existing Target environment
- FEATURE-Convert.md#convert-default-latest: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-Convert.md#convert-default-latest: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-Convert.md#convert-default-latest: python-package=httpx2; scope=test; authorization=existing Target environment
- FEATURE-Convert.md#convert-same-currency-and-zero: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-Convert.md#convert-same-currency-and-zero: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-Convert.md#convert-same-currency-and-zero: python-package=httpx2; scope=test; authorization=existing Target environment
- FEATURE-HistoryPoints.md#history-points-range: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-HistoryPoints.md#history-points-range: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-HistoryPoints.md#history-points-range: python-package=httpx2; scope=test; authorization=existing Target environment
- FEATURE-HistoryPoints.md#history-points-optional-bounds: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-HistoryPoints.md#history-points-optional-bounds: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-HistoryPoints.md#history-points-optional-bounds: python-package=httpx2; scope=test; authorization=existing Target environment
- FEATURE-HistoryPoints.md#history-points-start-after-end: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-HistoryPoints.md#history-points-start-after-end: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-HistoryPoints.md#history-points-start-after-end: python-package=httpx2; scope=test; authorization=existing Target environment
- FEATURE-HistoryPoints.md#history-points-round-trip: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-HistoryPoints.md#history-points-round-trip: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-HistoryPoints.md#history-points-round-trip: python-package=httpx2; scope=test; authorization=existing Target environment

## Stacked context
- stack: python_compact.md (SP 921)
- compass: COMPASS.md (SP 1152)
- implements: FEATURE-Convert.md (SP 2821)
- context: ARCHITECTURE_compact.md (SP 386)
- context: DATABASE_compact.md (SP 707)
- stack: fastapi_compact.md (SP 1122)
- implements: FEATURE-HistoryPoints.md (SP 2460)

## Build directory changes
- app_server/routes.py
- data/app.db-shm
- data/app.db-wal
- data/logs/test_2026-10-27_124142.log
- fxrates_app/convert.py
- fxrates_app/history.py
- tests/test_convert.py
- tests/test_history_points.py

## Pre-build acceptance observation
- RED: convert-two-currencies (FEATURE-Convert.md)
  intent: Converting ZZA to ZZB on a seeded date returns the effective date, a six-decimal rate and a two-decimal result derived with Decimal from the seeded rates, rounded half to even.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      response = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "convert-two-currencies.py", line 15, in <module>
        assert response.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: convert-eur-implicit-rate (FEATURE-Convert.md)
  intent: EUR to a stored currency uses rate 1 for EUR, and a stored currency to EUR divides by the stored rate; the effective date is the latest publication on or before a weekend-style gap date.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      out = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "convert-eur-implicit-rate.py", line 14, in <module>
        assert out.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: convert-default-latest (FEATURE-Convert.md)
  intent: Without date the latest publication date is used: a seeded date later than any real one is the effective date.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      response = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "convert-default-latest.py", line 14, in <module>
        assert response.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: convert-same-currency-and-zero (FEATURE-Convert.md)
  intent: Same from and to gives rate 1.000000 and the amount rounded half to even (derived with Decimal from a tie amount); amount 0 gives 0.00.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      same = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "convert-same-currency-and-zero.py", line 13, in <module>
        assert same.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: history-points-range (FEATURE-HistoryPoints.md)
  intent: Points between inclusive bounds come back ascending with the stored rate text, derived from the seeded inputs by sorting on date.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      resp = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "history-points-range.py", line 19, in <module>
        assert resp.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: history-points-optional-bounds (FEATURE-HistoryPoints.md)
  intent: Each bound is optional on its own; omitting both returns every stored point, and text such as 0.943 is returned exactly as stored.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      resp = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "history-points-optional-bounds.py", line 19, in <module>
        assert resp.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: history-points-start-after-end (FEATURE-HistoryPoints.md)
  intent: A start later than end is not an error; the response is 200 with no points even though the currency has stored rates.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      resp = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "history-points-start-after-end.py", line 14, in <module>
        assert resp.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: history-points-round-trip (FEATURE-HistoryPoints.md)
  intent: A replaced rate is what the next request returns, proving history is read from the store on each request and holds one point per date.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      resp = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "history-points-round-trip.py", line 13, in <module>
        assert resp.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError

## Post-build programmatic acceptance
- PASS: convert-two-currencies (FEATURE-Convert.md)
  intent: Converting ZZA to ZZB on a seeded date returns the effective date, a six-decimal rate and a two-decimal result derived with Decimal from the seeded rates, rounded half to even.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: convert-eur-implicit-rate (FEATURE-Convert.md)
  intent: EUR to a stored currency uses rate 1 for EUR, and a stored currency to EUR divides by the stored rate; the effective date is the latest publication on or before a weekend-style gap date.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: convert-default-latest (FEATURE-Convert.md)
  intent: Without date the latest publication date is used: a seeded date later than any real one is the effective date.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: convert-same-currency-and-zero (FEATURE-Convert.md)
  intent: Same from and to gives rate 1.000000 and the amount rounded half to even (derived with Decimal from a tie amount); amount 0 gives 0.00.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: history-points-range (FEATURE-HistoryPoints.md)
  intent: Points between inclusive bounds come back ascending with the stored rate text, derived from the seeded inputs by sorting on date.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: history-points-optional-bounds (FEATURE-HistoryPoints.md)
  intent: Each bound is optional on its own; omitting both returns every stored point, and text such as 0.943 is returned exactly as stored.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: history-points-start-after-end (FEATURE-HistoryPoints.md)
  intent: A start later than end is not an error; the response is 200 with no points even though the currency has stored rates.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: history-points-round-trip (FEATURE-HistoryPoints.md)
  intent: A replaced rate is what the next request returns, proving history is read from the store on each request and holds one point per date.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0

## Build summary
The block needs two new routes, `/convert` and `/history/{code}`, backed by two small services over the existing rates and persistence layers. I'll write the services first.Now the routes. I'll add them to the shared router, leaving the existing handlers untouched.Next, tests in the project's existing style: act through the client, read back the store, compare.I made an arithmetic slip in one expected value: 250.25 × 161.77 is 40482.9425, not 40472.94. Fixing that and tidying the long assertion lines.Both test files are written. Running the new tests first, then the full suite through the declared command.Block 13 is implemented and the full suite passes: `sh bin/test.sh` exited 0 with 285 passed. Nothing was committed.

- **`/convert`** computes the pair rate and the result with `Decimal`, rounded half to even to six and two decimals. The result comes from the stored rates, not the rounded rate. EUR has an implicit rate of 1. Without `date`, it uses the latest publication.
- **`/history/{code}`** returns `currency`, `base`, `count`, and `points` in ascending order between optional inclusive bounds. Rates come back as stored text.

The convert-related and history-related acceptance criteria are reproduced as tests in the project suite, along with boundary and error-path tests. Drydock runs the criteria themselves, so its verdict is separate from this run.

Choices I made where the spec was silent:
- An unknown currency returns 404.
- A stored rate of zero returns 422, since it cannot be a divisor.
- A malformed or impossible `date` or bound returns 422.
- A history request for a currency with no stored rates returns 200 with empty `points`.
- `count` is included because the history criterion asserts it. `min`, `max`, and `mean` are left for the later statistics story.

RESULT: SUCCESS

FILES CHANGED:
- app_server/routes.py
- fxrates_app/convert.py
- fxrates_app/history.py
- tests/test_convert.py
- tests/test_history_points.py

SUMMARY:
Added `GET /convert` (service `fxrates_app/convert.py`, reading via `rates.latest_rates` and `rates.rates_on`) and `GET /history/{code}` (service `fxrates_app/history.py`, one `db.rates.list_currency_history` call per request) to the shared router. Added 47 new tests across `tests/test_convert.py` and `tests/test_history_points.py`, which cover all declared acceptance assertions for both stories plus rounding, boundary, and error paths. Verification run: `.venv/bin/pytest -q` on the two new files, 47 passed; then `sh bin/test.sh`, exit 0, 285 passed. The terminal `sources/run.sh` check was not run because it belongs to the final block.

<blueprint-decisions>
[{"spec":"FEATURE-Convert.md","severity":"Low","subject":"Unknown currency and zero stored rate","decision":"A currency with no stored rate on the effective date (not EUR) returns 404. A stored rate of zero returns 422 instead of a 500 from division by zero. The spec did not name either status. Is that acceptable?"},{"spec":"FEATURE-HistoryPoints.md","severity":"Low","subject":"Response fields for this block","decision":"The response carries currency, base, count, and points. count is included because the history acceptance criterion asserts it. min, max, and mean are omitted and left for FEATURE-HistoryStats. Is that acceptable?"}]
</blueprint-decisions>
