# ARCHITECTURE: FxRates

| Field       | Value |
|-------------|-------|
| Version     | 20261026 V1 |
| Description | Defines the application modules and boundaries for the FxRates CLI and API. |
| Provides    | application module boundaries |

## Purpose

The application loads ECB euro reference rates into SQLite through the CLI and exposes them through a local JSON API. The `fxrates` executable is the application entry point; `fxrates serve` runs the API in the foreground.

## Modules and interfaces

| Module | Responsibility | Interface |
|--------|----------------|-----------|
| `config` | Resolve the database location. | `DATABASE_URL`, then `DATABASE_PATH`, then `data/app.db`. |
| `persistence` | Own database connections, schema access, and declared repository operations. | Generated package; callers use `open_database(dsn)` and `db.rates.<operation>(...)`. |
| `cli` | Parse commands and arguments, perform initialization and loading, and start the server. | `main(argv: list[str] | None = None) -> int`; root executable `fxrates`. |
| `services` | Coordinate rate loading and read queries through `persistence`. | Internal application services. |
| `app_server` | Build the FastAPI application and expose JSON endpoints. | `create_app() -> FastAPI`; `app_server.main:app`. |

## Ownership and boundaries

| Boundary | Owner | Allowed access |
|----------|-------|----------------|
| Configuration | `config` | Read the database environment variables and provide the resolved location. |
| Persistence | `persistence` | The only module that opens database connections or accesses the database driver. |
| File loading | `services` | Read the requested CSV or fetched archive and call declared repository operations. |
| External download | `services` | Download the ECB archive only for `fxrates fetch`; tests replace the download with a stub. |
| CLI | `cli` | Parse user commands, invoke services, and write specified output and diagnostics. |
| HTTP API | `app_server` | Validate requests, call services, and return JSON status and bodies. |

Application code must not open SQLite drivers directly. Persist rates as the ECB publishes them, using text values and decimal arithmetic for calculations. Resolve the database location from `DATABASE_URL`, then `DATABASE_PATH`, then `data/app.db`.

## Runtime and failure boundaries

The API uses FastAPI with uvicorn and listens on `127.0.0.1`; it remains in the foreground until stopped and handles SIGTERM cleanly. The CLI returns the specified exit status for success, usage errors, rejected files, and operational failures. Diagnostics go to standard error. The health route responds independently of stored rates.

## Technology Stack

| Technology | Use |
|------------|-----|
| Python | Application modules and executable implementation, Python 3.11 or newer. |
| FastAPI | JSON API request handling. |
| SQLite | Persistent rate storage through the generated persistence package. |
| CLI | `fxrates` commands: `init`, `load`, `fetch`, and `serve`. |
| pytest | Automated project tests; fetch tests use a stub and no network. |
| ECB reference rates | Published history CSV inside the downloaded ECB ZIP archive. |
| Shell | POSIX `bin/test.sh` and supplied grader invocation. |

## Programmatic Acceptance

=== AC architecture-imports ===
Intent: The application factory and CLI entry point are importable.

from app_server.main import create_app
from cli import main

assert callable(create_app)
assert callable(main)
=== END AC architecture-imports ===

## User Acceptance

- None.

## Guardrails

- Database access goes only through the shipped persistence library.
- Do not read `sources/run.sh` or supplied data files from application code.
- Do not hardcode rates, dates, counts, or computed values in application code.
- Store published rates as text and use `decimal` for arithmetic.
- The `fxrates` executable is located at the application root and serves on `127.0.0.1`.
