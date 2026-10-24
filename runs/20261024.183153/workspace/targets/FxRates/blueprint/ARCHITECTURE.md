# ARCHITECTURE: FxRates

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Defines the application modules, runtime configuration, and service boundaries for FxRates. |
| Provides    | application module boundaries |

## Purpose

FxRates loads ECB euro reference rates into the configured SQLite store and serves them through a JSON API. The root `fxrates` executable provides `init`, `load`, `fetch`, and `serve`.

## Module Boundaries

| Module | Owns | Allowed low-level access |
|--------|------|-------------------------|
| `cli` | Argument parsing and command dispatch | Calls application services and the ASGI application; does not access a database driver. |
| Rate loading service | CSV validation and atomic load workflow | Calls declared `persistence` operations. |
| Fetch service | ECB archive download and CSV extraction | Passes extracted CSV content to the rate loading service. |
| API application | FastAPI routes and request handling | Calls rate and conversion/history services. |
| Rate services | Effective-date lookup, conversion, and history calculations | Call declared `persistence` operations; use `decimal.Decimal` for arithmetic. |
| `persistence` | Database connections and declared rate operations | Sole owner of database driver access. |

## Runtime Configuration

Resolve the database location in this order: `DATABASE_URL`, `DATABASE_PATH`, then `data/app.db`. Store published rates as text. Do not use floating-point arithmetic for rates.

## Technology Stack

- Python 3.11 or newer implements the CLI, application services, API, and tests.
- FastAPI defines the JSON API; uvicorn serves it on `127.0.0.1`.
- SQLite is accessed through the generated persistence package.
- pytest runs the project test suite, with FastAPI `TestClient` for API tests.
- The `fxrates` CLI is the application entry point, and POSIX shell is used by test and conformance runners.
- Python `decimal` provides exact rate arithmetic.

## Programmatic Acceptance

=== AC architecture-imports ===
Intent: The application boundary module imports successfully.

import importlib.util

assert importlib.util.find_spec("app_server.main") is not None
=== END AC architecture-imports ===

## User Acceptance

- None.

## Guardrails

- All database access goes through the shipped persistence library.
- Resolve database configuration from `DATABASE_URL`, then `DATABASE_PATH`, then `data/app.db`.
- Preserve rate text and use Decimal rather than floating point for arithmetic.
- Application code must not read `sources/run.sh` or supplied data files directly.
