# ARCHITECTURE: FxRates

| Field | Value |
|-------|-------|
| Version | 20261024 V1 |
| Description | Defines the application modules and boundaries for the FxRates service. |
| Provides | application module boundaries |

## Technology Stack

- Python 3.11 or newer provides the application language and runtime.
- FastAPI provides the JSON API, served by uvicorn.
- SQLite stores rates through the generated persistence package.
- The root `fxrates` executable exposes the command line.
- pytest and FastAPI TestClient support automated tests.

## Modules

| Module | Responsibility |
|--------|----------------|
| `cli` | Dispatches `init`, `load`, `fetch`, and `serve` commands. |
| `app_server` | Creates the FastAPI application and serves API routes. |
| `persistence` | Provides generated database operations from `DATABASE.md`. |
| `services` | Implements loading, rate lookup, conversion, and history behavior using `persistence`. |

## Module Ownership

| Boundary | Owner | Allowed access |
|----------|-------|----------------|
| Configuration | `config` | Reads `DATABASE_URL`, then `DATABASE_PATH`, then `data/app.db`. |
| Persistence | `persistence` | Only this generated package accesses the database driver and store. |
| File input | `services` | Reads a caller-supplied CSV or the extracted fetch file; does not read grader assets by application-specific paths. |
| External service | `services.fetch` | Downloads the ECB archive; tests replace the download with a stub. |
| HTTP | `app_server` | Calls service functions and returns JSON/status responses. |
| CLI | `cli` | Calls service functions and maps outcomes to stdout, stderr, and exit codes. |

Application modules must not import or open a database driver directly. Rates remain published text; arithmetic uses `decimal.Decimal`.

## Programmatic Acceptance

=== AC architecture-imports ===
Intent: The shared application packages import successfully.

import app_server.main
import cli

assert callable(app_server.main.create_app)
assert callable(cli.main)
=== END AC architecture-imports ===

## User Acceptance

- None.

## Guardrails

- Database access goes only through the generated persistence package.
- Do not hardcode rates, dates, counts, or computed answers.
- Application code never reads `sources/run.sh` or supplied data files by grader-specific paths.
