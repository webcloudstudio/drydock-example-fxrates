# ARCHITECTURE: FxRates

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Defines the application modules and boundaries for the FxRates service. |
| Provides    | app_server.main:create_app, cli.main, persistence.open_database |

## Purpose

FxRates is a Python application with a CLI for initializing and loading ECB reference rates and a FastAPI service for querying them. The CLI and API share services and the generated persistence package.

## Technology Stack

| Technology | Use |
|------------|-----|
| Python | Application and tests, Python 3.11 or newer. |
| FastAPI | JSON API application and test client. |
| SQLite | Local rates database, accessed only through the generated persistence package. |
| CLI | Root `fxrates` executable with `init`, `load`, `fetch`, and `serve` commands. |
| pytest | Project test suite, invoked by `bin/test.sh`. |
| ECB reference rates | `eurofxref-hist.csv` history downloaded from the ECB archive. |
| Shell | POSIX shell launchers and supplied grader. |

## Module Boundaries

| Module | Owns | Allowed access |
|--------|------|----------------|
| `app_server` | FastAPI app factory and route registration | Calls application services. |
| `services` | Rate loading, validation, date resolution, conversion, and history calculations | Calls `persistence` operations. |
| `cli` | Command parsing and command dispatch | Calls services and the server runner. |
| `persistence` | Generated SQLite access layer and schema contract | Uses the shipped persistence library and selected database driver internally. |
| `bin` | POSIX test launcher | Runs pytest from the application root. |

The CLI and API do not open database connections or issue SQL directly. Route handlers call services; services call only declared `db.rates` operations. Configuration resolves `DATABASE_URL`, then `DATABASE_PATH`, then `data/app.db`.

## Interfaces

- `app_server.main:create_app()` returns the FastAPI application; `app_server.main:app` is the uvicorn entry point.
- `cli.main(argv: list[str] | None = None) -> int` is the command dispatcher.
- `persistence.open_database(dsn)` and `db.rates` expose the generated persistence interface.
- `app_server.testing.web_client()` returns a FastAPI `TestClient` for acceptance criteria and project tests.
- `cli.testing.cli_runner(*args)` returns `(exit_code, stdout, stderr)` for in-process command checks.

## Programmatic Acceptance

=== AC architecture-imports ===
Intent: The declared application entry points and test clients are importable.

from app_server.main import create_app, app
from app_server.testing import web_client
from cli import main
from cli.testing import cli_runner

assert callable(create_app)
assert app is not None
assert callable(web_client)
assert callable(main)
assert callable(cli_runner)
=== END AC architecture-imports ===

## User Acceptance

- None.

## Guardrails

- Store rates exactly as published text and use `decimal` for arithmetic.
- Keep application database access behind the generated persistence library.
- Resolve the database location from `DATABASE_URL`, then `DATABASE_PATH`, then `data/app.db`.
- Do not read grader scripts or supplied data directly from application code.
