# ARCHITECTURE: FxRates Application

| Field       | Value |
|-------------|-------|
| Version     | 20261025 V1 |
| Description | Defines the modules and ownership boundaries for the local currency rates service. |
| Depends On  |  |
| Provides    | application module boundaries |
| Consumes    |  |

## Technology Stack

- Python 3.11 or newer provides the application language and runtime.
- FastAPI defines the JSON API; uvicorn serves it on localhost.
- SQLite stores rates through the generated persistence package.
- The `fxrates` CLI provides initialization, loading, fetching, and serving commands.
- pytest runs the project test suite; FastAPI TestClient exercises the API in-process.
- POSIX sh runs the project test launcher and supplied grader.

## Modules and Ownership

| Module | Owns | May access |
|--------|------|------------|
| `config` | Database location and runtime configuration | Environment variables |
| `cli` | Command parsing and command dispatch | CLI feature services and `app_server` entry point |
| `app_server` | FastAPI application factory and HTTP routes | API services |
| `services` | Loading, rate lookup, conversion, and history behavior | `persistence` package and standard-library helpers |
| `persistence` | Database connections and generated repository operations | SQLite driver through the shipped persistence library |

Application features call declared repository operations through `persistence`; they do not open a database driver or issue SQL directly. Routes delegate behavior to services. The CLI dispatches commands to their feature implementations, and `serve` runs the application exposed by `app_server`.

## Programmatic Acceptance

=== AC architecture_modules_import ===
Intent: The application module boundaries are importable and expose the declared API and CLI entry points.

import importlib

cli = importlib.import_module("cli")
app_server = importlib.import_module("app_server.main")
persistence = importlib.import_module("persistence")

assert callable(cli.main)
assert callable(app_server.create_app)
assert app_server.app is not None
assert callable(persistence.open_database)
=== END AC architecture_modules_import ===

## User Acceptance

- None.

## Guardrails

- Application code accesses SQLite only through the generated persistence package.
- Store rates as ECB-published text and use Decimal for rate arithmetic.
- Resolve database configuration from `DATABASE_URL`, then `DATABASE_PATH`, then `data/app.db`.
- Do not read or modify `sources/run.sh` or supplied data files from application code.
