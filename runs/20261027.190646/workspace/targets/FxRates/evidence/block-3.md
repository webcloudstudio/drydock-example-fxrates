# Evidence: Block 3 · Foundational (block-3)

- block type: block
- date: 2026-10-27
- resulting state: closed/verified
- story points (combined assembled cost): 14825
- execution id: 20261027.192738.675Z-f1ac60b0

## Stories built
- Provide the cli package, dispatcher, exit-code mapping and the fxrates executable. (foundation-cli) [story]
- Provide the app_server package with create_app and the web_client fixture. (foundation-web) [story]

## Acceptance tooling authorization
- FEATURE-CliFoundation.md#cli-runner-interface: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-CliFoundation.md#dispatch-exit-codes: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-CliFoundation.md#fxrates-executable: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-WebFoundation.md#app-factory: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-WebFoundation.md#app-factory: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-WebFoundation.md#app-factory: python-package=httpx2; scope=test; authorization=existing Target environment
- FEATURE-WebFoundation.md#unknown-path-404: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-WebFoundation.md#unknown-path-404: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-WebFoundation.md#unknown-path-404: python-package=httpx2; scope=test; authorization=existing Target environment
- FEATURE-WebFoundation.md#request-scoped-db: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-WebFoundation.md#request-scoped-db: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-WebFoundation.md#startup-does-not-initialize: executable=python3; scope=test; authorization=existing Target environment
- FEATURE-WebFoundation.md#startup-does-not-initialize: python-package=fastapi; scope=test; authorization=existing Target environment
- FEATURE-WebFoundation.md#startup-does-not-initialize: python-package=httpx2; scope=test; authorization=existing Target environment

## Reusable compacts
- DATABASE_compact.md

## Stacked context
- stack: python_compact.md (SP 1002)
- compass: COMPASS.md (SP 1152)
- implements: FEATURE-CliFoundation.md (SP 1499)
- context: ARCHITECTURE_compact.md (SP 361)
- context: DATABASE.md (SP 3607)
- stack: common_compact.md (SP 1653)
- stack: cli.md (SP 2689)
- implements: FEATURE-WebFoundation.md (SP 1481)
- stack: fastapi.md (SP 1022)

## Build directory changes
- app_server/__init__.py
- app_server/deps.py
- app_server/main.py
- app_server/routers/__init__.py
- app_server/testing.py
- cli/__init__.py
- cli/__main__.py
- cli/commands/__init__.py
- cli/dispatch.py
- cli/errors.py
- cli/testing.py
- conftest.py
- data/app.db-shm
- data/app.db-wal
- fxrates
- tests/test_app_deps.py
- tests/test_app_server.py
- tests/test_cli_dispatch.py
- tests/test_cli_main.py
- tests/test_fxrates_launcher.py

## Pre-build acceptance observation
- RED: cli-runner-interface (FEATURE-CliFoundation.md)
  intent: cli_runner returns an (int, str, str) tuple without spawning a process, and a failing command writes nothing to standard output.
  error: foundation not built: `cli` is the package the cli foundation (cli.md) builds, and the build directory has no `cli/`. The criterion exercises the built application, so it was not run.
- RED: dispatch-exit-codes (FEATURE-CliFoundation.md)
  intent: execute maps a clean handler to its result and each error class to exit codes 1, 2 and 3, with empty stdout and a single stderr line.
  error: foundation not built: `cli` is the package the cli foundation (cli.md) builds, and the build directory has no `cli/`. The criterion exercises the built application, so it was not run.
- RED: fxrates-executable (FEATURE-CliFoundation.md)
  intent: The fxrates file exists at the application root, is executable and begins with an interpreter line.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      path = PosixPath('fxrates')
    --- drydock: end values ---
    Traceback (most recent call last):
      File "fxrates-executable.py", line 5, in <module>
        assert path.is_file()
               ^^^^^^^^^^^^^^
    AssertionError
- RED: app-factory (FEATURE-WebFoundation.md)
  intent: create_app returns a FastAPI application, a module-level app exists, and web_client returns a working test client.
  error: foundation not built: `app_server` is the package the web-server foundation (django.md, fastapi.md, flask.md) builds, and the build directory has no `app_server/`. The criterion exercises the built application, so it was not run.
- RED: unknown-path-404 (FEATURE-WebFoundation.md)
  intent: A path no router owns answers 404, showing the application serves requests.
  error: foundation not built: `app_server` is the package the web-server foundation (django.md, fastapi.md, flask.md) builds, and the build directory has no `app_server/`. The criterion exercises the built application, so it was not run.
- RED: request-scoped-db (FEATURE-WebFoundation.md)
  intent: get_db yields an opened database exposing the rates table operations and closes cleanly when the request ends.
  error: foundation not built: `app_server` is the package the web-server foundation (django.md, fastapi.md, flask.md) builds, and the build directory has no `app_server/`. The criterion exercises the built application, so it was not run.
- RED: startup-does-not-initialize (FEATURE-WebFoundation.md)
  intent: Starting the application opens no store: with no database configured, startup leaves data/app.db uncreated.
  error: foundation not built: `app_server` is the package the web-server foundation (django.md, fastapi.md, flask.md) builds, and the build directory has no `app_server/`. The criterion exercises the built application, so it was not run.

## Post-build programmatic acceptance
- PASS: cli-runner-interface (FEATURE-CliFoundation.md)
  intent: cli_runner returns an (int, str, str) tuple without spawning a process, and a failing command writes nothing to standard output.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.190646/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
  stderr:
    error: unknown command 'zzprobe-unknown-command'
- PASS: dispatch-exit-codes (FEATURE-CliFoundation.md)
  intent: execute maps a clean handler to its result and each error class to exit codes 1, 2 and 3, with empty stdout and a single stderr line.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.190646/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: fxrates-executable (FEATURE-CliFoundation.md)
  intent: The fxrates file exists at the application root, is executable and begins with an interpreter line.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.190646/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: app-factory (FEATURE-WebFoundation.md)
  intent: create_app returns a FastAPI application, a module-level app exists, and web_client returns a working test client.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.190646/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: unknown-path-404 (FEATURE-WebFoundation.md)
  intent: A path no router owns answers 404, showing the application serves requests.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.190646/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: request-scoped-db (FEATURE-WebFoundation.md)
  intent: get_db yields an opened database exposing the rates table operations and closes cleanly when the request ends.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.190646/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: startup-does-not-initialize (FEATURE-WebFoundation.md)
  intent: Starting the application opens no store: with no database configured, startup leaves data/app.db uncreated.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.190646/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0

## Build summary
I'll start by checking the build directory's current state and the existing files.The persistence layer and config are in place, and `cli/` and `app_server/` don't exist yet. Next I'll check the persistence API, the acceptance helper module the criteria import, and the current test baseline.Baseline is 17 passing tests. The `request-scoped-db` and `startup-does-not-initialize` criteria import `drydock_acceptance`, which isn't importable here. I'll check whether the staged test-store plugin provides it before deciding how to handle that.The `drydock_acceptance` module is a Drydock harness import that isn't in the build directory, and the staged test plugin doesn't provide it. I won't create a substitute for it. I'll cover the same behavior with my own tests. Before writing code, I'll check how `Database.close` and the SQLite driver open the store, and whether `fastapi.testclient` works with the installed `httpx2`.The store opens lazily and the test client works with deprecations treated as errors, so the design is settled. I'll write the CLI package first.Next, the `fxrates` launcher, the `app_server` package, and the root `conftest.py` that provides the two pytest fixtures.Now the tests. Per the spec, each behavior gets its own test and the oracles are return values, stored rows, and HTTP status codes. Command modules are faked through `sys.modules` so no command files are needed in the project.I wrote two tests carelessly and will fix them before running anything. One assertion in `test_app_server.py` is tautological, and `test_app_deps.py` initializes the store twice. I'll also remove a trivial test and move an inline import to the top of its file.Next I'll make the launcher executable, run the full suite, and then run the declared acceptance criteria that don't depend on `drydock_acceptance`. I'll keep those check scripts outside the project directory.All 72 tests pass: the 17 existing ones plus 55 new. Now the declared acceptance criteria, run from outside the project tree.All five criteria that can run here pass, and the launcher behaves as specified. I'll clean up the probe directory and confirm which files changed.Both foundations are built and the project suite passes. Two declared criteria could not run here because they import a module that is not in the build directory.

Build block 3 (foundation-cli and foundation-web) is in place. The project suite passes with 72 tests: the 17 existing ones and 55 new ones. Five declared criteria that don't need the missing harness module also pass when run directly.

**What was built**
- `cli/`: `main(argv) -> int` and `dispatch.py` (imports `cli.commands.<name>` and calls its `run(args)`). Also `errors.py` (exit codes 1/2/3), `testing.py` (`cli_runner`), `__main__.py`, and an empty `commands/` package.
- `fxrates` (root, executable): activates `.venv` if present, then runs `python -m cli "$@"` and exits with its result.
- `app_server/`: `main.py` (`create_app()` and module-level `app`, which includes every `router` found in `routers/`), `deps.py` (`get_db`, which opens `persistence.open_database` per request and closes it after), `testing.py` (`web_client()`).
- `conftest.py`: `cli_runner` and `web_client` pytest fixtures.
- Tests: `test_cli_dispatch.py`, `test_cli_main.py`, `test_fxrates_launcher.py`, `test_app_server.py`, `test_app_deps.py`.

**Verified by running**
- `sh bin/test.sh`: 72 passed, exit 0.
- Declared criteria `cli-runner-interface`, `dispatch-exit-codes`, `fxrates-executable`, `app-factory`, `unknown-path-404`: all pass. I ran them from scripts outside the project tree.
- `./fxrates zzprobe-unknown-command` exits 2 with empty stdout. `./fxrates` with no arguments exits 2.

**Not verified**
- `request-scoped-db` and `startup-does-not-initialize` import `drydock_acceptance`, which is not in the build directory. I did not create a substitute. Their behavior is covered by `test_app_deps.py` and `test_app_server.py`, but the declared criteria themselves did not run.

**Choices I made**
- The launcher keeps the caller's working directory, so the relative `data/app.db` resolves where the user runs it. It sets `PYTHONPATH` to the project root.
- Command names must match `[a-z][a-z0-9_]*`. Anything else is a usage error.
- A command module that exists but fails to import internally propagates its error. Only a missing command module is reported as an unknown command.
- I did not add `bin/run.sh`, `bin/run.ps1`, or a `[project.scripts]` entry. The spec names only the root `fxrates` executable.
- I did not run `git add` or `git commit`, per the build instructions.

<reusable-compact filename="DATABASE.md">
FxRates persistence surface (DATABASE.md, build order 1)
- Open: persistence.open_database(dsn) -> Database; persistence.initialize_database(dsn) -> Database (applies schema.sql, preserves data; close the result). Engine chosen from DSN: plain path or sqlite:// -> SQLite; postgres(ql):// -> PostgreSQL.
- Table rates(id INTEGER PK, date TEXT NOT NULL 'YYYY-MM-DD', currency TEXT NOT NULL, rate TEXT NOT NULL), UNIQUE(date, currency). Rates are stored as published text; never float.
- db.rates.replace_rate(date, currency, rate) -> (date, currency, rate): upsert on (date, currency).
- db.rates.list_through(through_date=None) -> rows (date, currency, rate): date <= through_date when given; order date desc, currency asc.
- db.rates.list_all() -> rows (date, currency, rate): order date asc, currency asc.
- db.rates.history(currency, start_date=None, end_date=None) -> rows (date, rate): inclusive bounds; order date asc.
- Rows are frozen dataclasses with attribute access. Application code never authors SQL or opens a driver.
- Startup never initializes; only explicit init uses initialize_database.
</reusable-compact>

<blueprint-decisions>
[{"spec":"FEATURE-CliFoundation.md","severity":"Low","subject":"fxrates launcher working directory","decision":"The launcher runs python -m cli in the caller's working directory instead of changing to the application root, so the relative data/app.db default resolves where the user runs it. It only adds the root to PYTHONPATH. Is that acceptable, or should it cd to the root?"}]
</blueprint-decisions>

RESULT: SUCCESS

FILES CHANGED:
- cli/__init__.py
- cli/__main__.py
- cli/dispatch.py
- cli/errors.py
- cli/testing.py
- cli/commands/__init__.py
- fxrates
- app_server/__init__.py
- app_server/main.py
- app_server/deps.py
- app_server/testing.py
- app_server/routers/__init__.py
- conftest.py
- tests/test_cli_dispatch.py
- tests/test_cli_main.py
- tests/test_fxrates_launcher.py
- tests/test_app_server.py
- tests/test_app_deps.py

SUMMARY:
Built the cli package (main, dispatcher, exit-code mapping, cli_runner) and the fxrates root launcher; built the app_server package (create_app, module-level app, get_db per-request dependency, web_client) and the pytest fixtures in conftest.py. `sh bin/test.sh`: 72 passed (17 existing + 55 new), exit 0. Declared criteria cli-runner-interface, dispatch-exit-codes, fxrates-executable, app-factory and unknown-path-404 pass when run directly.

BLOCKERS:
- Not blocking the build, but unverified: the declared criteria request-scoped-db and startup-does-not-initialize import `drydock_acceptance`, which is not present in the build directory. I did not create it. The same behaviors are covered by tests/test_app_deps.py and tests/test_app_server.py, but the declared criteria themselves were not executed here.
