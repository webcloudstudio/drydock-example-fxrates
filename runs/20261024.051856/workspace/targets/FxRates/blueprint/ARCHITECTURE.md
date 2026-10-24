# ARCHITECTURE: FxRates

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Defines application modules and their ownership boundaries. |
| Provides    | application module boundaries |

## Module Ownership

| Module | Owns | Permitted dependencies |
|--------|------|-----------------------|
| `cli` | `fxrates` entry point and command dispatch | Application services, configuration |
| `app_server` | FastAPI factory, routes, and HTTP test client | Application services |
| Application services | CSV validation, ingestion, rate lookup, conversion, and history calculations | `persistence` public operations |
| `persistence` | Database connections, schema, and generated repository operations | SQLite engine |
| Configuration | Database location resolution | Environment variables |

Application code accesses persistent data only through the generated `persistence` package. No application module opens a database driver directly.

## Technology Stack

| Technology | Use |
|------------|-----|
| Python 3.11+ | Application and test code |
| FastAPI | JSON HTTP API |
| SQLite | Persistent rates store through the generated persistence library |
| CLI | Root `fxrates` executable |
| pytest | Automated test suite |
| ECB reference rates | CSV history input and ZIP archive for fetch |
| POSIX shell | Test launcher and supplied grader |

## Programmatic Acceptance

=== AC architecture-boundaries ===
Intent: The published application packages can be imported.

import importlib

for name in ("cli", "app_server", "persistence"):
    module = importlib.import_module(name)
    assert module is not None
=== END AC architecture-boundaries ===

## User Acceptance

- None.

## Guardrails

- Only the generated persistence package may access the database driver.
- Preserve ECB rate text in storage and use `decimal` for arithmetic.
- Resolve the database location from `DATABASE_URL`, then `DATABASE_PATH`, then `data/app.db`.
