# ARCHITECTURE: FxRates Application

| Field       | Value |
|-------------|-------|
| Version     | 20261026 V1 |
| Description | Defines the application modules and ownership boundaries for the FxRates command line and API. |

## Module Boundaries

| Module | Owns | Allowed dependencies |
|--------|------|---------------------|
| `cli` | The `fxrates` executable, argument handling, command dispatch, and diagnostics. | Feature services, configuration |
| `app_server` | The FastAPI application factory and HTTP route registration. | Feature services, configuration |
| `services` | ECB CSV validation and loading, fetching, store initialization, rate queries, and exact decimal calculations. | `persistence`, configuration, standard library |
| `persistence` | The generated relational layer and shipped database library. | Database engine and schema |
| `config` | Resolving the database location from `DATABASE_URL`, then `DATABASE_PATH`, then `data/app.db`. | Standard library |

HTTP handlers call services. CLI commands call services. Services call the generated persistence operations through the shipped persistence library. Only the persistence boundary reaches the database. No application module opens a database driver directly.

The load workflow validates the complete input file before its first write. The fetch workflow extracts the archive's CSV and passes it through the same validation and loading behavior. Rate calculations use `decimal.Decimal`; published values remain text in storage and API responses.

## Technology Stack

| Technology | Use |
|------------|-----|
| Python 3.11 or newer | Application, CLI, services, and tests |
| FastAPI | JSON HTTP API |
| uvicorn | Serving the API on `127.0.0.1` |
| SQLite | Local rates store, accessed through the shipped persistence library |
| pytest | Offline automated tests |
| FastAPI `TestClient` | In-process API checks |

## Programmatic Acceptance

=== AC architecture-service-boundary ===
Intent: The application provides an importable services boundary for shared CLI and API behavior.

import importlib.util

services_spec = importlib.util.find_spec("services")
assert services_spec is not None
=== END AC architecture-service-boundary ===

## User Acceptance

- None.

## Guardrails

- Application code reaches SQLite only through the shipped persistence library and generated relational layer.
- Preserve rates as ECB-published text; use `decimal.Decimal` for arithmetic and never floating point.
- Keep file validation ahead of the first database write.
- Resolve database configuration in this order: `DATABASE_URL`, `DATABASE_PATH`, then `data/app.db`.
