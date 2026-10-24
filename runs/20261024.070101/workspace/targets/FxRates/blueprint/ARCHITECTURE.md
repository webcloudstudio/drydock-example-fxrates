# ARCHITECTURE: FxRates

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Defines FxRates application modules and ownership boundaries. |
| Depends On  | — |
| Provides    | application module boundaries |

## Module Boundaries

| Module | Responsibility | May access |
|--------|----------------|------------|
| `cli` | Implements `fxrates` commands and their exit codes. | Application services and configuration. |
| `app_server` | Creates the FastAPI application and serves JSON routes. | Application services and configuration. |
| Application services | Parse and validate ECB input, perform rate queries and exact decimal calculations. | `persistence` repository operations. |
| `persistence` | Owns connections and database operations through the shipped persistence library. | SQLite driver and declared schema. |
| Configuration | Resolves the database location from `DATABASE_URL`, then `DATABASE_PATH`, then `data/app.db`. | Environment variables. |

The CLI and API may share application services. Neither opens a database driver or issues SQL. All stored rates remain their published text; rate arithmetic uses `decimal`.

## Technology Stack

| Technology | Application |
|------------|-------------|
| Python | CLI, services, configuration, and API. |
| FastAPI | JSON API application. |
| SQLite | Rates store, accessed through the shipped persistence library. |
| CLI | Executable named `fxrates` at the application root. |

## Programmatic Acceptance

=== AC architecture-imports ===
Intent: The application, CLI, and persistence entry points are importable.

import importlib

for module_name in ("app_server.main", "cli", "persistence"):
    module = importlib.import_module(module_name)
    assert module is not None
=== END AC architecture-imports ===

=== AC architecture-application-entry ===
Intent: The application exposes its factory and the CLI exposes its callable entry point.

from app_server.main import create_app
from cli import main

assert callable(create_app)
assert callable(main)
=== END AC architecture-application-entry ===

## User Acceptance

- None.

## Guardrails

- Only the shipped persistence library accesses the database driver.
- CLI and API behavior must use the shared application configuration and service boundaries.
- Rates are stored as text and calculations use `decimal`.
