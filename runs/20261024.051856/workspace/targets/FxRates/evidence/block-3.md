# Evidence: Block 3 · Service (block-3)

- block type: block
- date: 2026-10-24
- resulting state: closed/failed
- story points (combined assembled cost): 18482
- execution id: 20261024.054026.852Z-038863a6

## Stories built
- Initialize the rates store from the CLI. (ingest_001) [story]
- Validate and load ECB history files. (ingest_002) [story]
- Reject invalid ECB history files atomically. (ingest_003) [story]
- Fetch and load the ECB history archive. (ingest_004) [story]
- List currencies available in stored rates. (api_002) [story]
- Serve health and rate-store statistics. (api_001) [story]
- Return bounded currency history and summary statistics. (api_005) [story]
- Resolve rates for requested and latest dates. (api_003) [story]
- Convert amounts between currencies. (api_004) [story]
- Run the HTTP service on the requested localhost port. (cli_002) [story]
- Return usage errors for invalid CLI invocations. (cli_001) [story]
- Validate API dates, amounts, and currencies. (api_006) [story]
- Verify the completed application with the supplied grader. (verify_001) [story]

## Missing context
- stack: pytest

## Stacked context
- stack: python_compact.md (SP 601)
- compass: COMPASS.md (SP 752)
- implements: FEATURE-Initialize-Store.md (SP 285)
- context: ARCHITECTURE_compact.md (SP 251)
- context: DATABASE_compact.md (SP 372)
- stack: cli.md (SP 1755)
- stack: sqlite_compact.md (SP 1848)
- implements: FEATURE-Load-History.md (SP 773)
- implements: FEATURE-Reject-History.md (SP 554)
- implements: FEATURE-Fetch-History.md (SP 736)
- implements: FEATURE-Currencies.md (SP 459)
- stack: fastapi.md (SP 497)
- implements: FEATURE-Health-Stats.md (SP 636)
- implements: FEATURE-History.md (SP 723)
- implements: FEATURE-Rates.md (SP 758)
- implements: FEATURE-Convert.md (SP 910)
- implements: FEATURE-Serve.md (SP 325)
- implements: FEATURE-CLI-Usage.md (SP 420)
- implements: FEATURE-API-Validation.md (SP 615)
- implements: VERIFICATION.md (SP 557)
- context: run.sh (SP 2393)
- stack: common.md (SP 1812)

## Build directory changes
- app_server/main.py
- bin/test.sh
- cli/commands.py
- cli/fetch.py
- cli/parser.py
- data/app.db
- services.py
- tests/test_services.py

## Pre-build acceptance observation
- RED: init-exit (FEATURE-Initialize-Store.md)
  intent: Initializing the store succeeds.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      code = 2
    --- drydock: end values ---
    Traceback (most recent call last):
      File "init-exit.py", line 4, in <module>
        assert code == 0
               ^^^^^^^^^
    AssertionError
- RED: init-repeat (FEATURE-Initialize-Store.md)
  intent: Store initialization can be repeated successfully.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      first = (2, '', "usage: fxrates [-h] {serve} ...\nfxrates: error: argument command: invalid choice: 'init' (choose from serve)\n")
    --- drydock: end values ---
    Traceback (most recent call last):
      File "init-repeat.py", line 5, in <module>
        assert first[0] == 0
               ^^^^^^^^^^^^^
    AssertionError
- RED: load-valid-file (FEATURE-Load-History.md)
  intent: A valid staged history file loads successfully.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      result = (2, '', "usage: fxrates [-h] {serve} ...\nfxrates: error: argument command: invalid choice: 'load' (choose from serve)\n")
    --- drydock: end values ---
    Traceback (most recent call last):
      File "load-valid-file.py", line 4, in <module>
        assert result[0] == 0
               ^^^^^^^^^^^^^^
    AssertionError
- RED: load-preserves-rate-text (FEATURE-Load-History.md)
  intent: Loaded rates are readable through the generated repository with their published text preserved.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      result = (2, '', "usage: fxrates [-h] {serve} ...\nfxrates: error: argument command: invalid choice: 'load' (choose from serve)\n")
    --- drydock: end values ---
    Traceback (most recent call last):
      File "load-preserves-rate-text.py", line 5, in <module>
        assert result[0] == 0
               ^^^^^^^^^^^^^^
    AssertionError
- RED: load-skips-na (FEATURE-Load-History.md)
  intent: Currency cells marked N/A do not create stored rate rows.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      result = (2, '', "usage: fxrates [-h] {serve} ...\nfxrates: error: argument command: invalid choice: 'load' (choose from serve)\n")
    --- drydock: end values ---
    Traceback (most recent call last):
      File "load-skips-na.py", line 5, in <module>
        assert result[0] == 0
               ^^^^^^^^^^^^^^
    AssertionError
- RED: load-replaces-existing (FEATURE-Load-History.md)
  intent: Loading a publication row stores or replaces its matching rate.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      result = (2, '', "usage: fxrates [-h] {serve} ...\nfxrates: error: argument command: invalid choice: 'load' (choose from serve)\n")
    --- drydock: end values ---
    Traceback (most recent call last):
      File "load-replaces-existing.py", line 7, in <module>
        assert result[0] == 0
               ^^^^^^^^^^^^^^
    AssertionError
- RED: reject-invalid-file (FEATURE-Reject-History.md)
  intent: The staged malformed history file is rejected with the specified exit status.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      code = 2
    --- drydock: end values ---
    Traceback (most recent call last):
      File "reject-invalid-file.py", line 4, in <module>
        assert code == 3
               ^^^^^^^^^
    AssertionError
- RED: reject-preserves-existing-rate (FEATURE-Reject-History.md)
  intent: Rejecting a file with a valid row before its invalid row leaves an existing rate unchanged.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      code = 2
    --- drydock: end values ---
    Traceback (most recent call last):
      File "reject-preserves-existing-rate.py", line 13, in <module>
        assert code == 3
               ^^^^^^^^^
    AssertionError
- RED: fetch-loads-stubbed-archive (FEATURE-Fetch-History.md)
  intent: Fetch loads an ECB-format CSV from a locally supplied archive without opening a network connection.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      p = 'fetch'
    --- drydock: end values ---
    Traceback (most recent call last):
      File "fetch-loads-stubbed-archive.py", line 25, in <module>
        with patch("cli.fetch.download_archive", side_effect=stub_download):
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/barlo/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/unittest/mock.py", line 1451, in __enter__
        self.target = self.getter()
                      ^^^^^^^^^^^^^
      File "/home/barlo/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/pkgutil.py", line 528, in resolve_name
        result = getattr(result, p)
                 ^^^^^^^^^^^^^^^^^^
    AttributeError: module 'cli' has no attribute 'fetch'
- RED: fetch-download-failure (FEATURE-Fetch-History.md)
  intent: A failed archive download returns the conventional operational failure exit code.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      p = 'fetch'
    --- drydock: end values ---
    Traceback (most recent call last):
      File "fetch-download-failure.py", line 5, in <module>
        with patch("cli.fetch.download_archive", side_effect=OSError):
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/home/barlo/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/unittest/mock.py", line 1451, in __enter__
        self.target = self.getter()
                      ^^^^^^^^^^^^^
      File "/home/barlo/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/lib/python3.12/pkgutil.py", line 528, in resolve_name
        result = getattr(result, p)
                 ^^^^^^^^^^^^^^^^^^
    AttributeError: module 'cli' has no attribute 'fetch'
- RED: currencies-route (FEATURE-Currencies.md)
  intent: The currencies route is reachable and identifies EUR as the base.
  return code: 1
  stderr:
    /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
    --- drydock: values at failure ---
      response = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "currencies-route.py", line 4, in <module>
        assert response.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: currencies-include-stored (FEATURE-Currencies.md)
  intent: A currency with a stored rate appears in the returned currency list.
  return code: 1
  stderr:
    /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
    --- drydock: values at failure ---
      response = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "currencies-include-stored.py", line 13, in <module>
        assert response.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: health-route (FEATURE-Health-Stats.md)
  intent: The health route is reachable and returns a successful response.
  return code: 1
  stderr:
    /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
    --- drydock: values at failure ---
      response = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "health-route.py", line 5, in <module>
        assert response.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: stats-route (FEATURE-Health-Stats.md)
  intent: The statistics route is reachable and returns the declared response fields.
  return code: 1
  stderr:
    /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
    --- drydock: values at failure ---
      response = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "stats-route.py", line 4, in <module>
        assert response.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: stats-reflects-stored-rates (FEATURE-Health-Stats.md)
  intent: Statistics reflect a rate inserted before the request.
  return code: 1
  stderr:
    /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
    --- drydock: values at failure ---
      response = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "stats-reflects-stored-rates.py", line 13, in <module>
        assert response.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: history-route-returns-bounded-summary (FEATURE-History.md)
  intent: The history route returns the supplied points and summary derived from their rates.
  return code: 1
  stderr:
    /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
    --- drydock: values at failure ---
      response = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "history-route-returns-bounded-summary.py", line 15, in <module>
        assert response.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: history-route-empty-range (FEATURE-History.md)
  intent: A currency with stored history returns the declared empty summary for a range with no points.
  return code: 1
  stderr:
    /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
    --- drydock: values at failure ---
      response = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "history-route-empty-range.py", line 11, in <module>
        assert response.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: date-resolves-to-effective-publication (FEATURE-Rates.md)
  intent: The requested-date route returns the effective stored publication and preserves the requested date.
  return code: 1
  stderr:
    /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
    --- drydock: values at failure ---
      response = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "date-resolves-to-effective-publication.py", line 13, in <module>
        assert response.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: latest-rates-route-works (FEATURE-Rates.md)
  intent: The latest route returns a successful response and the latest stored publication.
  return code: 1
  stderr:
    /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
    --- drydock: values at failure ---
      response = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "latest-rates-route-works.py", line 12, in <module>
        assert response.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- GREEN (prepassed): no-publication-before-date-is-not-found (FEATURE-Rates.md)
  intent: A date with no earlier stored publication returns 404.
  return code: 0
  stderr:
    /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
- RED: convert-route-returns-computed-values (FEATURE-Convert.md)
  intent: The conversion route returns the echoed inputs and values derived from the supplied rates.
  return code: 1
  stderr:
    /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
    --- drydock: values at failure ---
      response = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "convert-route-returns-computed-values.py", line 20, in <module>
        assert response.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: euro-conversion-uses-implicit-unit-rate (FEATURE-Convert.md)
  intent: EUR conversions use the implicit unit rate without requiring an EUR row.
  return code: 1
  stderr:
    /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
    --- drydock: values at failure ---
      response = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "euro-conversion-uses-implicit-unit-rate.py", line 14, in <module>
        assert response.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- GREEN (prepassed): serve-command-entry (FEATURE-Serve.md)
  intent: The CLI exposes the serve command.
  return code: 0
- GREEN (prepassed): serve-app-factory (FEATURE-Serve.md)
  intent: The server command's application factory is available.
  return code: 0
- GREEN (prepassed): usage-unknown-command (FEATURE-CLI-Usage.md)
  intent: An unknown command returns the usage exit status.
  return code: 0
- GREEN (prepassed): usage-wrong-arguments (FEATURE-CLI-Usage.md)
  intent: A command missing its required argument returns the usage exit status.
  return code: 0
- GREEN (prepassed): usage-invalid-port (FEATURE-CLI-Usage.md)
  intent: A non-integer port returns the usage exit status.
  return code: 0
- RED: malformed-date-is-unprocessable (FEATURE-API-Validation.md)
  intent: A malformed requested rate date returns 422.
  return code: 1
  stderr:
    /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
    --- drydock: values at failure ---
      response = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "malformed-date-is-unprocessable.py", line 4, in <module>
        assert response.status_code == 422
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: missing-conversion-amount-is-unprocessable (FEATURE-API-Validation.md)
  intent: A conversion missing its required amount returns 422.
  return code: 1
  stderr:
    /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
    --- drydock: values at failure ---
      response = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "missing-conversion-amount-is-unprocessable.py", line 4, in <module>
        assert response.status_code == 422
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: malformed-amount-is-unprocessable (FEATURE-API-Validation.md)
  intent: A malformed conversion amount returns 422.
  return code: 1
  stderr:
    /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
    --- drydock: values at failure ---
      response = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "malformed-amount-is-unprocessable.py", line 6, in <module>
        assert response.status_code == 422
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- GREEN (prepassed): unknown-currency-is-not-found (FEATURE-API-Validation.md)
  intent: A conversion naming an unknown currency returns 404.
  return code: 0
  stderr:
    /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
- RED: terminal-grader (VERIFICATION.md)
  intent: The supplied end-to-end grader passes against the completed application.
  return code: 1
  stdout:
    FAIL A1: fxrates init
      exit: expected 0, got 2
      stderr: usage: fxrates [-h] {serve} ...
      stderr: fxrates: error: argument command: invalid choice: 'init' (choose from serve)
    FAIL A2: fxrates load /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261024.051856/build/FxRates/sources/eurofxref-hist_2025-01.csv
      exit: expected 0, got 2
      1,2d0
      < dates,rates
      < 22,176
      stderr: usage: fxrates [-h] {serve} ...
      stderr: fxrates: error: argument command: invalid choice: 'load' (choose from serve)
    FAIL A3: fxrates load /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261024.051856/build/FxRates/sources/eurofxref-hist_2025-01.csv
      exit: expected 0, got 2
      1,2d0
      < dates,rates
      < 22,176
      stderr: usage: fxrates [-h] {serve} ...
      stderr: fxrates: error: argument command: invalid choice: 'load' (choose from serve)
    FAIL A4: fxrates load /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261024.051856/build/FxRates/sources/eurofxref-hist_bad.csv
      exit: expected 3, got 2
      stderr: usage: fxrates [-h] {serve} ...
      stderr: fxrates: error: argument command: invalid choice: 'load' (choose from serve)
    FAIL A5: fxrates load /tmp/tmp.jG0uJJtIgQ/no-such-file.csv
      exit: expected 1, got 2
      stderr: usage: fxrates [-h] {serve} ...
      stderr: fxrates: error: argument command: invalid choice: 'load' (choose from serve)
    PASS U1: fxrates 
    PASS U2: fxrates frobnicate
    PASS U3: fxrates load
    PASS U4: fxrates serve --port notaport
    FAIL S1: fxrates serve --port 52349 did not answer GET /health within 30 s
      server: INFO:     Started server process [1329968]
      server: INFO:     Waiting for application startup.
      server: INFO:     Application startup complete.
      server: INFO:     Uvicorn running on http://127.0.0.1:52349 (Press CTRL+C to quit)
      server: INFO:     127.0.0.1:41456 - "GET /health HTTP/1.1" 404 Not Found
      server: INFO:     127.0.0.1:34158 - "GET /health HTTP/1.1" 404 Not Found
      server: INFO:     127.0.0.1:34164 - "GET /health HTTP/1.1" 404 Not Found
      server: INFO:     127.0.0.1:34174 - "GET /health HTTP/1.1" 404 Not Found
      server: INFO:     127.0.0.1:34182 - "GET /health HTTP/1.1" 404 Not Found
      server: INFO:     127.0.0.1:34198 - "GET /health HTTP/1.1" 404 Not Found
      server: INFO:     127.0.0.1:34206 - "GET /health HTTP/1.1" 404 Not Found
      server: INFO:     127.0.0.1:34216 - "GET /health HTTP/1.1" 404 Not Found
      server: INFO:     127.0.0.1:34226 - "GET /health HTTP/1.1" 404 Not Found
      server: INFO:     127.0.0.1:37024 - "GET /health HTTP/1.1" 404 Not Found
      server: INFO:     127.0.0.1:37038 - "GET /health HTTP/1.1" 404 Not Found
      server: INFO:     127.0.0.1:37040 - "GET /health HTTP/1.1" 404 Not Found
      server: INFO:     127.0.0.1:37054 - "GET /health HTTP/1.1" 404 Not Found
      server: INFO:     127.0.0.1:37064 - "GET /health HTTP/1.1" 404 Not Found
      server: INFO:     127.0.0.1:37080 - "GET /health HTTP/1.1" 404 Not Found
      server: INFO:     127.0.0.1:37094 - "GET /health HTTP/1.1" 404 Not Found
      server: INFO:     127.0.0.1:37108 - "GET /health HTTP/1.1" 404 Not Found
      server: INFO:     127.0.0.1:37110 - "GET /health HTTP/1.1" 404 Not Found
      server: INFO:     127.0.0.1:48426 - "GET /health HTTP/1.1" 404 Not Found
      server: INFO:     127.0.0.1:48436 - "GET /health HTTP/1.1" 404 Not Found
      server: INFO:     127.0.0.1:48448 - "GET /health HTTP/1.1" 404 Not Found
      server: INFO:     127.0.0.1:48450 - "GET /health HTTP/1.1" 404 Not Found
      server: INFO:     127.0.0.1:48462 - "GET /health HTTP/1.1" 404 Not Found
      server: INFO:     127.0.0.1:48474 - "GET /health HTTP/1.1" 404 Not Found
    FxRates: 4 passed, unscored HTTP checks (server did not start)
  stderr:
    --- drydock: values at failure ---
      result = CompletedProcess(args=['sh', 'sources/run.sh'], returncode=1, stdout='FAIL A1: fxrates init\n  exit: expected 0, got 2\n  stderr: usage: fxrates [-h] {serve} ...\n  stderr: fxrates: error: argument command: invalid choice: \'init\' (choose from serve)\nFAIL A2: fxrates load /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261024.051856/build/FxRates/sources/eurofxref-hist_2025-01.csv\n  exit… (+3381 chars)
    --- drydock: end values ---
    Traceback (most recent call last):
      File "terminal-grader.py", line 10, in <module>
        assert result.returncode == 0
               ^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: pytest-launcher (VERIFICATION.md)
  intent: The project's POSIX test launcher runs the complete pytest suite successfully.
  return code: 1
  stdout:
    sh: 0: cannot open bin/test.sh: No such file
  stderr:
    --- drydock: values at failure ---
      result = CompletedProcess(args=['sh', 'bin/test.sh'], returncode=2, stdout='', stderr='sh: 0: cannot open bin/test.sh: No such file\n')
    --- drydock: end values ---
    Traceback (most recent call last):
      File "pytest-launcher.py", line 10, in <module>
        assert result.returncode == 0
               ^^^^^^^^^^^^^^^^^^^^^^
    AssertionError

## Post-build programmatic acceptance
- PASS: init-exit (FEATURE-Initialize-Store.md)
  intent: Initializing the store succeeds.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: init-repeat (FEATURE-Initialize-Store.md)
  intent: Store initialization can be repeated successfully.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: load-valid-file (FEATURE-Load-History.md)
  intent: A valid staged history file loads successfully.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: load-preserves-rate-text (FEATURE-Load-History.md)
  intent: Loaded rates are readable through the generated repository with their published text preserved.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: load-skips-na (FEATURE-Load-History.md)
  intent: Currency cells marked N/A do not create stored rate rows.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: load-replaces-existing (FEATURE-Load-History.md)
  intent: Loading a publication row stores or replaces its matching rate.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: reject-invalid-file (FEATURE-Reject-History.md)
  intent: The staged malformed history file is rejected with the specified exit status.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: reject-preserves-existing-rate (FEATURE-Reject-History.md)
  intent: Rejecting a file with a valid row before its invalid row leaves an existing rate unchanged.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: fetch-loads-stubbed-archive (FEATURE-Fetch-History.md)
  intent: Fetch loads an ECB-format CSV from a locally supplied archive without opening a network connection.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: fetch-download-failure (FEATURE-Fetch-History.md)
  intent: A failed archive download returns the conventional operational failure exit code.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: currencies-route (FEATURE-Currencies.md)
  intent: The currencies route is reachable and identifies EUR as the base.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
  stderr:
    /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
- PASS: currencies-include-stored (FEATURE-Currencies.md)
  intent: A currency with a stored rate appears in the returned currency list.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
  stderr:
    /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
- PASS: health-route (FEATURE-Health-Stats.md)
  intent: The health route is reachable and returns a successful response.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
  stderr:
    /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
- PASS: stats-route (FEATURE-Health-Stats.md)
  intent: The statistics route is reachable and returns the declared response fields.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
  stderr:
    /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
- PASS: stats-reflects-stored-rates (FEATURE-Health-Stats.md)
  intent: Statistics reflect a rate inserted before the request.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
  stderr:
    /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
- DISPUTED: history-route-returns-bounded-summary (FEATURE-History.md)
  intent: The history route returns the supplied points and summary derived from their rates.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 1
  stderr:
    /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
    --- drydock: values at failure ---
      response = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "history-route-returns-bounded-summary.py", line 15, in <module>
        assert response.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- FAIL: history-route-empty-range (FEATURE-History.md)
  intent: A currency with stored history returns the declared empty summary for a range with no points.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 1
  stderr:
    /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
    --- drydock: values at failure ---
      response = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "history-route-empty-range.py", line 11, in <module>
        assert response.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- FAIL: date-resolves-to-effective-publication (FEATURE-Rates.md)
  intent: The requested-date route returns the effective stored publication and preserves the requested date.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 1
  stderr:
    /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
    --- drydock: values at failure ---
      date = '2098-01-02'
      body = {'date': '2025-01-31', 'requested': '2098-01-03', 'base': 'EUR', 'rates': {'USD': '1.0393', 'JPY': '160.99', 'GBP': '0.83608', 'CHF': '0.9449', 'SEK': '11.474', 'CAD': '1.5035', 'AUD': '1.6702', 'CNY': '7.5363'}}
    --- drydock: end values ---
    Traceback (most recent call last):
      File "date-resolves-to-effective-publication.py", line 15, in <module>
        assert body["date"] == date
               ^^^^^^^^^^^^^^^^^^^^
    AssertionError
- FAIL: latest-rates-route-works (FEATURE-Rates.md)
  intent: The latest route returns a successful response and the latest stored publication.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 1
  stderr:
    /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
    --- drydock: values at failure ---
      date = '2098-02-04'
      body = {'date': '2025-01-31', 'requested': 'latest', 'base': 'EUR', 'rates': {'USD': '1.0393', 'JPY': '160.99', 'GBP': '0.83608', 'CHF': '0.9449', 'SEK': '11.474', 'CAD': '1.5035', 'AUD': '1.6702', 'CNY': '7.5363'}}
    --- drydock: end values ---
    Traceback (most recent call last):
      File "latest-rates-route-works.py", line 14, in <module>
        assert body["date"] == date
               ^^^^^^^^^^^^^^^^^^^^
    AssertionError
- PASS: no-publication-before-date-is-not-found (FEATURE-Rates.md)
  intent: A date with no earlier stored publication returns 404.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
  stderr:
    /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
- DISPUTED: convert-route-returns-computed-values (FEATURE-Convert.md)
  intent: The conversion route returns the echoed inputs and values derived from the supplied rates.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 1
  stderr:
    /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
    --- drydock: values at failure ---
      response = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "convert-route-returns-computed-values.py", line 20, in <module>
        assert response.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- FAIL: euro-conversion-uses-implicit-unit-rate (FEATURE-Convert.md)
  intent: EUR conversions use the implicit unit rate without requiring an EUR row.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 1
  stderr:
    /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
    --- drydock: values at failure ---
      response = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "euro-conversion-uses-implicit-unit-rate.py", line 14, in <module>
        assert response.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- PASS: serve-command-entry (FEATURE-Serve.md)
  intent: The CLI exposes the serve command.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: serve-app-factory (FEATURE-Serve.md)
  intent: The server command's application factory is available.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: usage-unknown-command (FEATURE-CLI-Usage.md)
  intent: An unknown command returns the usage exit status.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: usage-wrong-arguments (FEATURE-CLI-Usage.md)
  intent: A command missing its required argument returns the usage exit status.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: usage-invalid-port (FEATURE-CLI-Usage.md)
  intent: A non-integer port returns the usage exit status.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: malformed-date-is-unprocessable (FEATURE-API-Validation.md)
  intent: A malformed requested rate date returns 422.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
  stderr:
    /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
- PASS: missing-conversion-amount-is-unprocessable (FEATURE-API-Validation.md)
  intent: A conversion missing its required amount returns 422.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
  stderr:
    /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
- PASS: malformed-amount-is-unprocessable (FEATURE-API-Validation.md)
  intent: A malformed conversion amount returns 422.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
  stderr:
    /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
- PASS: unknown-currency-is-not-found (FEATURE-API-Validation.md)
  intent: A conversion naming an unknown currency returns 404.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
  stderr:
    /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
      from starlette.testclient import TestClient as TestClient  # noqa
- PASS: terminal-grader (VERIFICATION.md)
  intent: The supplied end-to-end grader passes against the completed application.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
  stdout:
    PASS A1: fxrates init
    PASS A2: fxrates load /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261024.051856/build/FxRates/sources/eurofxref-hist_2025-01.csv
    PASS A3: fxrates load /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261024.051856/build/FxRates/sources/eurofxref-hist_2025-01.csv
    PASS A4: fxrates load /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261024.051856/build/FxRates/sources/eurofxref-hist_bad.csv
    PASS A5: fxrates load /tmp/tmp.Re0cJqkYhn/no-such-file.csv
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
    PASS L1: fxrates load /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261024.051856/build/FxRates/sources/eurofxref-hist_2025-02-03_04.csv
    PASS L2: GET /stats
    PASS L3: GET /rates/latest
    PASS L4: GET /rates/2025-02-01
    PASS L5: GET /history/AUD?start=2025-01-30
    FxRates: 35 passed, 0 failed (of 35)
- PASS: pytest-launcher (VERIFICATION.md)
  intent: The project's POSIX test launcher runs the complete pytest suite successfully.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not required
  return code: 0
  stdout:
    ..................                                                       [100%]
    =============================== warnings summary ===============================
    ../../../../../../.venv/lib/python3.12/site-packages/fastapi/testclient.py:1
      /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
        from starlette.testclient import TestClient as TestClient  # noqa
    
    -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
    18 passed, 1 warning in 3.44s

## Repair attempts
- attempt 0 (initial build): failed; 27/33 checks; 35/35 cases model=gpt-6-luna; execution 20261024.053324.021Z-3d282252; reason: programmatic acceptance failed: history-route-empty-range, date-resolves-to-effective-publication, latest-rates-route-works, euro-conversion-uses-implicit-unit…
- attempt 1 (repair 1): failed; 27/33 checks; 35/35 cases model=gpt-6-luna; execution 20261024.053608.354Z-27e31631; reason: programmatic acceptance failed: history-route-empty-range, date-resolves-to-effective-publication, latest-rates-route-works, euro-conversion-uses-implicit-unit…
- attempt 2 (repair 2): failed; 27/33 checks; 35/35 cases model=gpt-6-luna; execution 20261024.054026.852Z-038863a6; stopped: deterministic acceptance score did not improve on 2 consecutive calls; reason: programmatic acceptance failed: history-route-empty-range, date-resolves-to-effective-publication, latest-rates-route-works, euro-conversion-uses-implicit-unit…

## Agent self-report (advisory)
The build agent declared a failure. This is advisory only; the programmatic acceptance above is the authority for this block's outcome.
- summary: Four HTTP acceptance criteria query rows their setup rolled back.
- detail:
    The declared `db_session()` rolls back on exit, and each failing criterion exits it before calling `web_client()`. Those rows cannot be returned through the persistence contract. Update the criteria to use committed setup and cleanup, or make the request within the rollback session, then rerun. No project files were changed.

## Failure
- summary: programmatic acceptance failed: history-route-empty-range, date-resolves-to-effective-publication, latest-rates-route-works, euro-conversion-uses-implicit-unit-rate
- detail:
    Block "Block 3 · Service" [block-3] failed its acceptance criteria.
      Story "Return bounded currency history and summary statistics." [api_005] does not meet its own acceptance criteria:
        - AC history-route-empty-range — A currency with stored history returns the declared empty summary for a range with no points.
            assertion: assert response.status_code == 200 → AssertionError
            raised at: history-route-empty-range.py:11
            process exit code: 1
            values at failure:
              response = <Response [404 Not Found]>
            check stderr:
              /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
                from starlette.testclient import TestClient as TestClient  # noqa
              Traceback (most recent call last):
                File "history-route-empty-range.py", line 11, in <module>
                  assert response.status_code == 200
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^
              AssertionError
      Story "Resolve rates for requested and latest dates." [api_003] does not meet its own acceptance criteria:
        - AC date-resolves-to-effective-publication — The requested-date route returns the effective stored publication and preserves the requested date.
            assertion: assert body["date"] == date → AssertionError
            raised at: date-resolves-to-effective-publication.py:15
            process exit code: 1
            values at failure:
              date = '2098-01-02'
              body = {'date': '2025-01-31', 'requested': '2098-01-03', 'base': 'EUR', 'rates': {'USD': '1.0393', 'JPY': '160.99', 'GBP': '0.83608', 'CHF': '0.9449', 'SEK': '11.474', 'CAD': '1.5035', 'AUD': '1.6702', 'CNY': '7.5363'}}
            check stderr:
              /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
                from starlette.testclient import TestClient as TestClient  # noqa
              Traceback (most recent call last):
                File "date-resolves-to-effective-publication.py", line 15, in <module>
                  assert body["date"] == date
                         ^^^^^^^^^^^^^^^^^^^^
              AssertionError
        - AC latest-rates-route-works — The latest route returns a successful response and the latest stored publication.
            assertion: assert body["date"] == date → AssertionError
            raised at: latest-rates-route-works.py:14
            process exit code: 1
            values at failure:
              date = '2098-02-04'
              body = {'date': '2025-01-31', 'requested': 'latest', 'base': 'EUR', 'rates': {'USD': '1.0393', 'JPY': '160.99', 'GBP': '0.83608', 'CHF': '0.9449', 'SEK': '11.474', 'CAD': '1.5035', 'AUD': '1.6702', 'CNY': '7.5363'}}
            check stderr:
              /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
                from starlette.testclient import TestClient as TestClient  # noqa
              Traceback (most recent call last):
                File "latest-rates-route-works.py", line 14, in <module>
                  assert body["date"] == date
                         ^^^^^^^^^^^^^^^^^^^^
              AssertionError
      Story "Convert amounts between currencies." [api_004] does not meet its own acceptance criteria:
        - AC euro-conversion-uses-implicit-unit-rate — EUR conversions use the implicit unit rate without requiring an EUR row.
            assertion: assert response.status_code == 200 → AssertionError
            raised at: euro-conversion-uses-implicit-unit-rate.py:14
            process exit code: 1
            values at failure:
              response = <Response [404 Not Found]>
            check stderr:
              /mnt/c/Users/barlo/projects/drydock/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
                from starlette.testclient import TestClient as TestClient  # noqa
              Traceback (most recent call last):
                File "euro-conversion-uses-implicit-unit-rate.py", line 14, in <module>
                  assert response.status_code == 200
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^
              AssertionError

## Build summary
AC_BROKEN: history-route-empty-range, date-resolves-to-effective-publication, latest-rates-route-works, euro-conversion-uses-implicit-unit-rate

RESULT: FAILED

FILES CHANGED:
- None

SUMMARY:
Reproduced all four failures. Their setup writes are rolled back before the HTTP requests, so those rows are unavailable to the API. The project suite passed (18 tests), and the supplied grader passed (35 checks).

BLOCKERS:
- The four acceptance criteria need committed setup with criterion-owned cleanup, or must keep setup and request within the same rollback session. The current criteria close the session before making the request.

FAILURE_SUMMARY: Four HTTP acceptance criteria query rows their setup rolled back.
FAILURE_DETAIL: The declared `db_session()` rolls back on exit, and each failing criterion exits it before calling `web_client()`. Those rows cannot be returned through the persistence contract. Update the criteria to use committed setup and cleanup, or make the request within the rollback session, then rerun. No project files were changed.
