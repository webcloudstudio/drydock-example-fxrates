# ARCHITECTURE: FxRates

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Defines the application modules and boundaries for the FxRates command line and JSON API. |
| Depends On  | DATABASE.md |
| Provides    | app_server.create_app, cli.main, persistence.open_database |
| Consumes    | rates.list, rates.upsert, rates.delete |

## System Overview

The application is a Python 3.11+ service with a root `fxrates` executable. The CLI initializes and loads ECB rates, fetches the ECB history archive, and starts a FastAPI application served by uvicorn. The API reads the same SQLite database used by the CLI. Rates remain ECB-published text in storage; calculations use `decimal.Decimal`.

## Module Ownership

| Boundary | Owner | Allowed access |
|----------|-------|----------------|
| Persistence | Generated `persistence/` package | Owns SQLite connections and schema operations; application modules call `open_database` and declared `db.rates` operations. No application module opens a database driver. |
| Configuration | `config.py` | Resolves `DATABASE_URL`, then `DATABASE_PATH`, then `data/app.db`. |
| File loading | `rate_loader.py` | Reads, parses, validates, and loads CSV files through the persistence interface. |
| ECB download | `rate_fetch.py` | Downloads and extracts the ECB archive; delegates rate validation and persistence to the loader. |
| CLI | `cli/` | Parses commands and arguments, delegates to loader, fetcher, and server startup. |
| API | `app_server/` | Creates FastAPI routes and obtains data through declared persistence operations. |

## Request and Command Boundaries

`fxrates init` uses the declared persistence boundary to drop and recreate the `rates` table. `fxrates load <csv>` validates the entire file before writing. `fxrates fetch` downloads the ECB ZIP archive and sends its CSV through the same loader. `fxrates serve [--port <n>]` runs the API on `127.0.0.1`, defaulting to port 8000.

The API provides health, database summary, sorted currencies, effective-date rates, conversions, and currency history. A load completed while the server is running is visible to the next request. API details and response contracts are specified in the feature Blueprints.

## Technology Stack

| Technology | Application |
|------------|-------------|
| Python | Application modules and CLI implementation, Python 3.11 or newer. |
| FastAPI | JSON API application and request validation. |
| SQLite | Persistent rates database, accessed only through the generated persistence package. |
| CLI | Root `fxrates` executable and its `init`, `load`, `fetch`, and `serve` commands. |
| pytest | Project test suite, run by `bin/test.sh`, with FastAPI `TestClient`. |
| ECB reference rates | CSV input from the history archive; published rate text is preserved. |
| Shell | POSIX shell launchers and supplied grader invocation. |

## Programmatic Acceptance

=== AC app-factory ===
Intent: The application factory creates a FastAPI app that answers the public health route.
Requires: python-package=httpx; scope=test

from app_server.main import create_app
from fastapi.testclient import TestClient

client = TestClient(create_app())
response = client.get("/health")
assert response.status_code == 200
=== END AC app-factory ===

=== AC architecture-boundary ===
Intent: The generated persistence interface opens the configured database and exposes the declared rates operations.

from persistence import open_database

db = open_database("")
assert hasattr(db, "rates")
assert callable(db.rates.list)
assert callable(db.rates.upsert)
assert callable(db.rates.delete)
=== END AC architecture-boundary ===

## User Acceptance

- None.

## Guardrails

- Application code must not import or call a database driver directly.
- Resolve the database location from `DATABASE_URL`, then `DATABASE_PATH`, then `data/app.db`.
- Preserve published rates as text and use Decimal for arithmetic.
- Do not read the grader or supplied CSV fixtures from application code.
