# Evidence: Block 10 · Service (block-10)

- block type: block
- date: 2026-10-27
- resulting state: closed/verified
- story points (combined assembled cost): 8985
- execution id: 20261027.161413.795Z-d52acad2

## Stories built
- `fxrates serve` listens on 127.0.0.1 and answers /health, /openapi.json, and /docs. (rates-001-serve-health) [story]

## Acceptance tooling authorization
- FEATURE-ServeHealth.md#serve-health-route: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-ServeHealth.md#serve-health-route: python-package=httpx2; scope=test; authorization=existing Target environment
- FEATURE-ServeHealth.md#serve-live-sigterm: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-ServeHealth.md#serve-live-sigterm: python-package=uvicorn; scope=test; authorization=existing Target environment
- FEATURE-ServeHealth.md#serve-port-in-use: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-ServeHealth.md#serve-port-in-use: python-package=uvicorn; scope=test; authorization=existing Target environment

## Stacked context
- stack: python_compact.md (SP 921)
- compass: COMPASS.md (SP 1152)
- implements: FEATURE-ServeHealth.md (SP 1910)
- context: ARCHITECTURE_compact.md (SP 386)
- context: DATABASE_compact.md (SP 707)
- stack: fastapi_compact.md (SP 1122)
- stack: cli.md (SP 2689)

## Build directory changes
- app_server/routes.py
- cli/__init__.py
- cli/serve_command.py
- data/app.db-shm
- data/app.db-wal
- tests/test_health.py
- tests/test_serve.py

## Pre-build acceptance observation
- RED: serve-health-route (FEATURE-ServeHealth.md)
  intent: The application answers GET /health with status 200 and the exact status body, and its OpenAPI description and interactive docs are served with status 200.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      response = <Response [404 Not Found]>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "serve-health-route.py", line 5, in <module>
        assert response.status_code == 200
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError
- RED: serve-live-sigterm (FEATURE-ServeHealth.md)
  intent: The serve command listens on 127.0.0.1 at the requested port, answers /health within a bounded wait, and exits 0 when it receives SIGTERM.
  return code: 1
  stdout:
    error: command not available in this build: serve
  stderr:
    --- drydock: values at failure ---
      proc = <Popen: returncode: 2 args: ['/mnt/c/Users/barlo/projects/drydock/uat/FxRate...>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "serve-live-sigterm.py", line 34, in <module>
        assert proc.poll() is None, "server exited before answering /health"
               ^^^^^^^^^^^^^^^^^^^
    AssertionError: server exited before answering /health
- RED: serve-port-in-use (FEATURE-ServeHealth.md)
  intent: When the requested port is already bound, serve exits 1 with empty stdout and one stderr line instead of serving.
  return code: 1
  stdout:
    error: command not available in this build: serve
  stderr:
    --- drydock: values at failure ---
      proc = <Popen: returncode: 2 args: ['/mnt/c/Users/barlo/projects/drydock/uat/FxRate...>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "serve-port-in-use.py", line 21, in <module>
        assert proc.returncode == 1
               ^^^^^^^^^^^^^^^^^^^^
    AssertionError

## Post-build programmatic acceptance
- PASS: serve-health-route (FEATURE-ServeHealth.md)
  intent: The application answers GET /health with status 200 and the exact status body, and its OpenAPI description and interactive docs are served with status 200.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: serve-live-sigterm (FEATURE-ServeHealth.md)
  intent: The serve command listens on 127.0.0.1 at the requested port, answers /health within a bounded wait, and exits 0 when it receives SIGTERM.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
  stdout:
    INFO:     127.0.0.1:46472 - "GET /health HTTP/1.1" 200 OK
    
    INFO:     Started server process [1589263]
    INFO:     Waiting for application startup.
    INFO:     Application startup complete.
    INFO:     Uvicorn running on http://127.0.0.1:50849 (Press CTRL+C to quit)
    INFO:     Shutting down
    INFO:     Waiting for application shutdown.
    INFO:     Application shutdown complete.
    INFO:     Finished server process [1589263]
- PASS: serve-port-in-use (FEATURE-ServeHealth.md)
  intent: When the requested port is already bound, serve exits 1 with empty stdout and one stderr line instead of serving.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
  stdout:
    error: port 39103 on 127.0.0.1 is already in use

## Build summary
The spec needs a `/health` route and a `serve` command. Uvicorn's default signal capture re-raises SIGTERM after shutdown, which would end the process by signal rather than exit 0, so I'll check that behavior with a real run after writing the command.Now the tests: the route through the in-process client, and the port-in-use path through `cli_runner`.The suite passes (182). Next I'll run the two live acceptance checks from the spec against the real launcher, with the script kept outside the project.Both live checks pass. Checking the changed-file set before reporting.RESULT: SUCCESS

FILES CHANGED:
- app_server/routes.py
- cli/__init__.py
- cli/serve_command.py
- tests/test_health.py
- tests/test_serve.py

SUMMARY:
- `fxrates serve [--port n]` now runs uvicorn on `app_server.main:app`, bound to 127.0.0.1, default port 8000, in the foreground. SIGTERM or SIGINT stops it cleanly with exit 0.
- Uvicorn's default signal capture re-raises SIGTERM after shutdown, which would end the process by signal instead of exit 0. `serve` replaces that capture so the signal only asks the server to stop.
- Before binding, `serve` probes the port. If it is taken, it prints one stderr line and exits 1 with empty stdout.
- `GET /health` returns `{"status": "ok"}` and does not touch the database. `/openapi.json` and `/docs` remain enabled.
- `cli/__init__.py` imports the new module so the `serve` handler registers at import.

Checks run:
- `.venv/bin/pytest -q` in the build directory: 182 passed. This includes the new `tests/test_health.py` and `tests/test_serve.py`.
- Live acceptance `serve-live-sigterm`, run by hand against `./fxrates serve --port <free>`: `/health` answered `{"status": "ok"}`, SIGTERM gave exit 0, and clean shutdown was logged to stderr. PASS.
- Live acceptance `serve-port-in-use`, run by hand with the port held: exit 1, empty stdout, one stderr line. PASS.
- `serve-health-route` is covered by `tests/test_health.py`, which uses the same client calls as the spec.

Choices I made:
- The live SIGTERM path is not in the pytest suite. Starting a server in-process would need the socket connect that the suite blocks, so that check is the spec's acceptance criterion instead.
- The port probe sets SO_REUSEADDR, the same as uvicorn, so a port in TIME_WAIT is not reported as busy. A small race remains between the probe and uvicorn's bind.
- `sh bin/test.sh` was not run. I ran `pytest -q` directly, which is the command it wraps.
