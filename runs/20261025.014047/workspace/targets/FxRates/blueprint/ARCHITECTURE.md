# ARCHITECTURE: FxRates

| Field       | Value |
|-------------|-------|
| Version     | 20261025 V1 |
| Description | Defines the application modules, runtime wiring, and persistence boundaries. |
| Depends On  | DATABASE.md |
| Provides    | FastAPI application factory, `fxrates` command entry point |
| Consumes    | `persistence.open_database`, `persistence.db_session` |

## Purpose

The application loads ECB euro reference rates into SQLite and serves them through a local JSON API. The `fxrates` executable provides database initialization, CSV loading, archive fetching, and API serving.

## Technology Stack

- Python 3.11 or newer implements the application.
- FastAPI defines the JSON API and uvicorn serves it on `127.0.0.1`.
- SQLite stores rates through the generated persistence library.
- The CLI exposes `init`, `load`, `fetch`, and `serve`.
- pytest runs the automated test suite.

## Modules and Boundaries

| Module | Responsibility |
|--------|----------------|
| `cli` | Parse commands and arguments, return conventional exit codes, and write diagnostics to stderr. |
| `persistence` | Resolve the configured database and expose generated rate operations. It is the only application boundary that accesses the database driver. |
| `app_server` | Build the FastAPI application and implement JSON routes using application services. |
| `services` | Parse and validate complete ECB files, load rates, resolve effective dates, and calculate exact decimal values. |
| `fxrates` | Executable launcher for the CLI entry point. |

## Module Ownership

| Boundary | Owner | Allowed access |
|----------|-------|----------------|
| Persistence | `persistence` | The generated package opens the database and provides declared `db.rates` operations. Application modules call those operations only. |
| Configuration | `config` | Resolves `DATABASE_URL`, then `DATABASE_PATH`, then `data/app.db`. Other modules obtain the configured DSN through this boundary. |
| File store | None | ECB CSV inputs are read by `load` or `fetch`; no persistent file store is used. |
| External service | `services.ecb_fetch` | Downloads the ECB archive for `fetch`; tests replace the download operation with a stub. |

## Runtime Wiring

`fxrates` calls `cli.main(argv)`. The CLI dispatches to the relevant service or starts uvicorn with the FastAPI application. The application factory creates routes that query the generated persistence package. Loads performed while the server is running are visible to later requests through the configured database.

The database path resolves from `DATABASE_URL`, then `DATABASE_PATH`, then `data/app.db`. Rates are stored exactly as published text; calculations use Python `decimal`.

## Interfaces

- Persistence calls use `persistence.open_database(dsn)` and the declared operations `db.rates.get`, `db.rates.list`, `db.rates.upsert`, and `db.rates.delete`.
- The web foundation exposes `app_server.main.create_app() -> FastAPI` and `app_server.main.app`.
- The CLI foundation exposes `cli.main(argv: list[str] | None = None) -> int`.
- `fxrates serve [--port <n>]` binds to `127.0.0.1`, defaults to port `8000`, and exits cleanly on SIGTERM.

## Programmatic Acceptance

=== AC foundation-imports ===
Intent: The published application, CLI, and persistence entry points can be imported and the application factory creates a FastAPI app.

from fastapi import FastAPI
from app_server.main import create_app
from cli import main
from persistence import open_database

assert isinstance(create_app(), FastAPI)
assert callable(main)
assert callable(open_database)
=== END AC foundation-imports ===

=== AC foundation-routes-registered ===
Intent: The application registers the health and statistics routes supplied by its feature.

from app_server.main import create_app

routes = {route.path for route in create_app().routes}
assert "/health" in routes
assert "/stats" in routes
=== END AC foundation-routes-registered ===

## User Acceptance

- None.

## Guardrails

- Application code must access SQLite only through the shipped persistence library.
- Resolve the database location from `DATABASE_URL`, then `DATABASE_PATH`, then `data/app.db`.
- Preserve ECB rate text and use `decimal` for arithmetic.
- Do not read `sources/run.sh` or supplied data files from application code.
- Fetch tests must stub downloads and never open a network connection.
