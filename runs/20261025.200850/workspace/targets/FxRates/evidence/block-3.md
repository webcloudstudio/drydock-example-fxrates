# Evidence: Block 3 · Service (block-3)

- block type: block
- date: 2026-10-25
- resulting state: closed/failed
- story points (combined assembled cost): 16739
- execution id: 20261025.203415.422Z-f3607ee6

## Stories built
- Initialize the rates store from the command line. (ecb-001) [story]
- Validate and load ECB history files atomically. (ecb-002) [story]
- Serve health, dataset statistics, and available currencies. (api-001) [story]
- Retrieve rates for an effective publication date. (api-002) [story]
- Convert amounts between currencies using exact decimal arithmetic. (api-003) [story]
- Retrieve currency history and exact summary statistics. (api-004) [story]
- Fetch and load the ECB history archive. (ecb-003) [story]
- Provide the automated pytest suite and POSIX test runner. (del-001) [story]
- Verify the completed application against the supplied grader. (del-002) [story]

## Missing context
- context: INSTRUCTIONS.md

## Stacked context
- stack: python_compact.md (SP 601)
- compass: COMPASS.md (SP 752)
- implements: FEATURE-Store-Initialization.md (SP 426)
- context: ARCHITECTURE_compact.md (SP 190)
- context: DATABASE_compact.md (SP 205)
- stack: cli.md (SP 1755)
- stack: sqlite_compact.md (SP 1943)
- implements: FEATURE-ECB-Loading.md (SP 1274)
- context: eurofxref-hist_2025-01.csv (SP 411)
- context: eurofxref-hist_2025-02-03_04.csv (SP 44)
- context: eurofxref-hist_bad.csv (SP 16)
- implements: FEATURE-Dataset-Summary.md (SP 561)
- stack: fastapi_compact.md (SP 576)
- implements: FEATURE-Effective-Rates.md (SP 722)
- implements: FEATURE-Currency-Conversion.md (SP 819)
- implements: FEATURE-Currency-History.md (SP 871)
- implements: FEATURE-ECB-Fetch.md (SP 626)
- implements: FEATURE-Test-Runner.md (SP 448)
- implements: FEATURE-Grader-Conformance.md (SP 566)
- context: run.sh (SP 2393)
- stack: common_compact.md (SP 1079)

## Build directory changes
- app_server/main.py
- cli/commands.py
- cli/fetch.py
- cli/main.py
- cli/parser.py
- data/app.db
- persistence/db.py
- tests/test_architecture.py
- tests/test_foundations.py
- tests/test_rates_service.py

## Pre-build acceptance observation
- RED: init-clears-rates (FEATURE-Store-Initialization.md)
  intent: Initialization succeeds and a separate repository read finds no rates afterward.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      code = 1
    --- drydock: end values ---
    Traceback (most recent call last):
      File "init-clears-rates.py", line 5, in <module>
        assert code == 0
               ^^^^^^^^^
    AssertionError
- RED: init-repeat (FEATURE-Store-Initialization.md)
  intent: Repeating initialization succeeds and leaves the rates repository empty.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      first = (1, '', 'error: init is not available yet\n')
    --- drydock: end values ---
    Traceback (most recent call last):
      File "init-repeat.py", line 6, in <module>
        assert first[0] == 0
               ^^^^^^^^^^^^^
    AssertionError
- RED: load-published-text (FEATURE-ECB-Loading.md)
  intent: Loading the staged January history stores every non-N/A rate with its published text and reports counts derived from that fixture.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      code = 1
    --- drydock: end values ---
    Traceback (most recent call last):
      File "load-published-text.py", line 20, in <module>
        assert code == 0
               ^^^^^^^^^
    AssertionError
- RED: load-rejects-atomically (FEATURE-ECB-Loading.md)
  intent: A rejected file preserves existing rows and does not partially store its valid first row.
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
- RED: load-replacement-is-idempotent (FEATURE-ECB-Loading.md)
  intent: Loading the same valid fixture twice replaces matching rates without changing the stored values.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      first_code = 1
    --- drydock: end values ---
    Traceback (most recent call last):
      File "load-replacement-is-idempotent.py", line 24, in <module>
        assert first_code == 0
               ^^^^^^^^^^^^^^^
    AssertionError
- RED: summary-routes (FEATURE-Dataset-Summary.md)
  intent: The health, statistics, and currency routes are reachable and report values derived from stored rows.
  return code: 1
  stderr:
    /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
    --- drydock: values at failure ---
      health = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "summary-routes.py", line 18, in <module>
        assert health.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: effective-date-rates (FEATURE-Effective-Rates.md)
  intent: Both rate routes resolve an effective date and preserve the supplied published rate text.
  return code: 1
  stderr:
    /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
    --- drydock: values at failure ---
      response = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "effective-date-rates.py", line 17, in <module>
        assert response.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: effective-date-errors (FEATURE-Effective-Rates.md)
  intent: Requests before available history return 404 and malformed calendar dates return 422.
  return code: 1
  stderr:
    /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
    --- drydock: values at failure ---
      client = <starlette.testclient.TestClient object at 0x7b29efc49160>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "effective-date-errors.py", line 10, in <module>
        assert client.get("/rates/2099-13-01").status_code == 422
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: conversion-route (FEATURE-Currency-Conversion.md)
  intent: Conversion returns a reachable response with the supplied amount and currencies using the effective stored rates.
  return code: 1
  stderr:
    /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
    --- drydock: values at failure ---
      response = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "conversion-route.py", line 18, in <module>
        assert response.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: conversion-validation-errors (FEATURE-Currency-Conversion.md)
  intent: Missing or malformed inputs return 422, while an unknown currency returns 404.
  return code: 1
  stderr:
    /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
    --- drydock: values at failure ---
      client = <starlette.testclient.TestClient object at 0x75f68e1411c0>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "conversion-validation-errors.py", line 9, in <module>
        assert client.get("/convert").status_code == 422
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: currency-history-bounds (FEATURE-Currency-History.md)
  intent: History returns the selected points in ascending order with published text and exact summary values.
  return code: 1
  stderr:
    /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
    --- drydock: values at failure ---
      response = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "currency-history-bounds.py", line 20, in <module>
        assert response.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: currency-history-empty-and-errors (FEATURE-Currency-History.md)
  intent: Empty bounded history returns the declared empty result, and unknown currencies and malformed bounds return the declared statuses.
  return code: 1
  stderr:
    /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
    --- drydock: values at failure ---
      empty = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "currency-history-empty-and-errors.py", line 15, in <module>
        assert empty.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: fetch-command (FEATURE-ECB-Fetch.md)
  intent: The fetch command is available and reports operational failure when the stubbed downloader fails.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "fetch-command.py", line 2, in <module>
        import cli.fetch as fetch_module
    ModuleNotFoundError: No module named 'cli.fetch'
- RED: fetch-stubbed-archive-load (FEATURE-ECB-Fetch.md)
  intent: A stubbed archive is extracted and passed to the load workflow without network access.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "fetch-stubbed-archive-load.py", line 2, in <module>
        import cli.fetch as fetch_module
    ModuleNotFoundError: No module named 'cli.fetch'
- GREEN (prepassed): test-runner-exits-successfully (FEATURE-Test-Runner.md)
  intent: The declared pytest test command completes successfully.
  return code: 0
  stdout:
    ..........                                                               [100%]
    =============================== warnings summary ===============================
    ../../../../../../.venv/lib/python3.12/site-packages/fastapi/testclient.py:1
      /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
        from starlette.testclient import TestClient as TestClient  # noqa
    
    -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
    10 passed, 1 warning in 3.23s
- RED: supplied-grader-full (FEATURE-Grader-Conformance.md)
  intent: The complete authoritative supplied grader passes all 35 command and HTTP checks.
  return code: 1
  stdout:
    PASS A1: fxrates init
    FAIL A2: fxrates load /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/sources/eurofxref-hist_2025-01.csv
      exit: expected 0, got 0
      1,2d0
      < dates,rates
      < 22,176
    FAIL A3: fxrates load /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/sources/eurofxref-hist_2025-01.csv
      exit: expected 0, got 0
      1,2d0
      < dates,rates
      < 22,176
    FAIL A4: fxrates load /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/sources/eurofxref-hist_bad.csv
      exit: expected 3, got 0
    FAIL A5: fxrates load /tmp/tmp.3ZIEAC0y8R/no-such-file.csv
      exit: expected 1, got 0
    FAIL U1: fxrates 
      exit: expected 2, got 0
    FAIL U2: fxrates frobnicate
      exit: expected 2, got 0
    FAIL U3: fxrates load
      exit: expected 2, got 0
    FAIL U4: fxrates serve --port notaport
      exit: expected 2, got 0
    FAIL S1: fxrates serve --port 54757 did not answer GET /health within 30 s
    FxRates: 1 passed, unscored HTTP checks (server did not start)
  stderr:
    --- drydock: values at failure ---
      result = CompletedProcess(args=['sh', 'sources/run.sh'], returncode=1, stdout='PASS A1: fxrates init\nFAIL A2: fxrates load /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/sources/eurofxref-hist_2025-01.csv\n  exit: expected 0, got 0\n  1,2d0\n  < dates,rates\n  < 22,176\nFAIL A3: fxrates load /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRa… (+728 chars)
    --- drydock: end values ---
    Traceback (most recent call last):
      File "supplied-grader-full.py", line 10, in <module>
        assert result.returncode == 0
               ^^^^^^^^^^^^^^^^^^^^^^
    AssertionError

## Post-build programmatic acceptance
- PASS: init-clears-rates (FEATURE-Store-Initialization.md)
  intent: Initialization succeeds and a separate repository read finds no rates afterward.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: init-repeat (FEATURE-Store-Initialization.md)
  intent: Repeating initialization succeeds and leaves the rates repository empty.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: load-published-text (FEATURE-ECB-Loading.md)
  intent: Loading the staged January history stores every non-N/A rate with its published text and reports counts derived from that fixture.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: load-rejects-atomically (FEATURE-ECB-Loading.md)
  intent: A rejected file preserves existing rows and does not partially store its valid first row.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: load-replacement-is-idempotent (FEATURE-ECB-Loading.md)
  intent: Loading the same valid fixture twice replaces matching rates without changing the stored values.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: summary-routes (FEATURE-Dataset-Summary.md)
  intent: The health, statistics, and currency routes are reachable and report values derived from stored rows.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
  stderr:
    /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
- PASS: effective-date-rates (FEATURE-Effective-Rates.md)
  intent: Both rate routes resolve an effective date and preserve the supplied published rate text.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
  stderr:
    /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
- PASS: effective-date-errors (FEATURE-Effective-Rates.md)
  intent: Requests before available history return 404 and malformed calendar dates return 422.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
  stderr:
    /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
- FAIL: conversion-route (FEATURE-Currency-Conversion.md)
  intent: Conversion returns a reachable response with the supplied amount and currencies using the effective stored rates.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 1
  stderr:
    /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
    --- drydock: values at failure ---
      body = {'date': '2099-01-02', 'from': 'XTS', 'to': 'XTU', 'amount': '2.00', 'rate': '2.500000', 'result': '5.00'}
    --- drydock: end values ---
    Traceback (most recent call last):
      File "conversion-route.py", line 25, in <module>
        assert body["result"] == "10.00"
               ^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- PASS: conversion-validation-errors (FEATURE-Currency-Conversion.md)
  intent: Missing or malformed inputs return 422, while an unknown currency returns 404.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
  stderr:
    /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
- PASS: currency-history-bounds (FEATURE-Currency-History.md)
  intent: History returns the selected points in ascending order with published text and exact summary values.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
  stderr:
    /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
- PASS: currency-history-empty-and-errors (FEATURE-Currency-History.md)
  intent: Empty bounded history returns the declared empty result, and unknown currencies and malformed bounds return the declared statuses.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
  stderr:
    /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
- PASS: fetch-command (FEATURE-ECB-Fetch.md)
  intent: The fetch command is available and reports operational failure when the stubbed downloader fails.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: fetch-stubbed-archive-load (FEATURE-ECB-Fetch.md)
  intent: A stubbed archive is extracted and passed to the load workflow without network access.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: test-runner-exits-successfully (FEATURE-Test-Runner.md)
  intent: The declared pytest test command completes successfully.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
  stdout:
    .............                                                            [100%]
    =============================== warnings summary ===============================
    ../../../../../../.venv/lib/python3.12/site-packages/fastapi/testclient.py:1
      /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
        from starlette.testclient import TestClient as TestClient  # noqa
    
    -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
    13 passed, 1 warning in 5.46s
- PASS: supplied-grader-full (FEATURE-Grader-Conformance.md)
  intent: The complete authoritative supplied grader passes all 35 command and HTTP checks.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
  stdout:
    PASS A1: fxrates init
    PASS A2: fxrates load /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/sources/eurofxref-hist_2025-01.csv
    PASS A3: fxrates load /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/sources/eurofxref-hist_2025-01.csv
    PASS A4: fxrates load /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/sources/eurofxref-hist_bad.csv
    PASS A5: fxrates load /tmp/tmp.iQCLyKrq2s/no-such-file.csv
    PASS U1: fxrates 
    PASS U2: fxrates frobnicate
    PASS U3: fxrates load
    PASS U4: fxrates serve --port notaport
    PASS H1: GET /health
    PASS H2: GET /stats
    PASS H3: GET /currencies
    PASS H4: GET /rates/2025-01-17
    PASS H5: GET /rates/2025-01-18
    PASS H6: GET /rates/2024-12-31
    PASS H7: GET /rates/2025-13-01
    PASS H8: GET /rates/latest
    PASS H9: GET /convert?from=USD&to=GBP&amount=100&date=2025-01-17
    PASS H10: GET /convert?from=EUR&to=JPY&amount=250.25&date=2025-01-05
    PASS H11: GET /convert?from=GBP&to=EUR&amount=1000
    PASS H12: GET /convert?from=SEK&to=CNY&amount=12345.67&date=2025-01-20
    PASS H13: GET /convert?from=USD&to=XXX&amount=1
    PASS H14: GET /convert?from=USD&to=GBP
    PASS H15: GET /convert?from=USD&to=GBP&amount=abc
    PASS H16: GET /convert?from=USD&to=GBP&amount=10&date=2024-12-01
    PASS H17: GET /history/USD?start=2025-01-20&end=2025-01-24
    PASS H18: GET /history/CHF?start=2025-01-27
    PASS H19: GET /history/HRK
    PASS H20: GET /history/USD?start=2025-02-01
    PASS H21: GET /history/GBP?start=2025-01-31-x
    PASS L1: fxrates load /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/sources/eurofxref-hist_2025-02-03_04.csv
    PASS L2: GET /stats
    PASS L3: GET /rates/latest
    PASS L4: GET /rates/2025-02-01
    PASS L5: GET /history/AUD?start=2025-01-30
    FxRates: 35 passed, 0 failed (of 35)

## Repair attempts
- attempt 0 (initial build): failed; 13/16 checks; 35/35 cases model=gpt-6-luna; execution 20261025.201908.525Z-55ec7b03; reason: programmatic acceptance failed: init-clears-rates, init-repeat, conversion-route
- attempt 1 (repair 1): failed; 15/16 checks; 35/35 cases model=gpt-6-luna; execution 20261025.202705.183Z-c232d1c7; reason: programmatic acceptance failed: conversion-route
- attempt 2 (repair 2): failed; 15/16 checks; 35/35 cases model=gpt-6-luna; execution 20261025.203029.101Z-c458a8ca; reason: programmatic acceptance failed: conversion-route
- attempt 3 (repair 3): failed; 15/16 checks; 35/35 cases model=gpt-6-luna; execution 20261025.203415.422Z-f3607ee6; stopped: deterministic acceptance score did not improve on 2 consecutive calls; reason: programmatic acceptance failed: conversion-route

## Failure
- summary: programmatic acceptance failed: conversion-route
- detail:
    Block "Block 3 · Service" [block-3] failed its acceptance criteria.
      Story "Convert amounts between currencies using exact decimal arithmetic." [api-003] does not meet its own acceptance criteria:
        - AC conversion-route — Conversion returns a reachable response with the supplied amount and currencies using the effective stored rates.
            assertion: assert body["result"] == "10.00" → AssertionError
            raised at: conversion-route.py:25
            process exit code: 1
            values at failure:
              body = {'date': '2099-01-02', 'from': 'XTS', 'to': 'XTU', 'amount': '2.00', 'rate': '2.500000', 'result': '5.00'}
            check stderr:
              /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261025.200850/build/FxRates/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
                from starlette.testclient import TestClient as TestClient  # noqa
              Traceback (most recent call last):
                File "conversion-route.py", line 25, in <module>
                  assert body["result"] == "10.00"
                         ^^^^^^^^^^^^^^^^^^^^^^^^^
              AssertionError

## Build summary
RESULT: SUCCESS  
AC_BROKEN: conversion-route

FILES CHANGED:
- None

SUMMARY:
`sh bin/test.sh` passed (13 tests). The conversion criterion’s expected result conflicts with the specified formula: `2.00 × (5 / 2) = 5.00`, while it expects `10.00`. The API uses the specified exact decimal calculation and half-even rounding.

BLOCKERS:
- The `conversion-route` acceptance assertion cannot pass as written without violating the conversion specification.
