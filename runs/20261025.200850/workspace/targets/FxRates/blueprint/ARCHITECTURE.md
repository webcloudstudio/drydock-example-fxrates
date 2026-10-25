# ARCHITECTURE: FxRates

| Field       | Value |
|-------------|-------|
| Version     | 20261025 V1 |
| Description | Defines the Python application structure and module ownership for FxRates. |

## System Structure

The application is a Python 3.11 or newer command-line and HTTP service. The root `fxrates` executable dispatches commands through the `cli` package. The `app_server` package owns the FastAPI application and uvicorn entry point. Application code uses the generated `persistence` package for all database access.

## Module Ownership

| Boundary | Owner | Responsibility |
|----------|-------|----------------|
| Configuration | Application configuration module | Resolve `DATABASE_URL`, then `DATABASE_PATH`, then `data/app.db`. |
| Persistence | Generated `persistence` package | Open the configured SQLite database and expose declared rates repository operations. |
| CLI | `cli` package and root `fxrates` executable | Parse commands and arguments, return the specified exit codes, and write command output. |
| HTTP service | `app_server` package | Create the FastAPI app and expose JSON API routes through uvicorn. |
| ECB integration | CLI fetch workflow | Download and extract the ECB archive; tests replace the downloader with a stub. |

Only the generated persistence package may access a database driver. CLI workflows and HTTP routes call application behavior that uses its declared repository operations; they do not open database connections directly.

## Technology Stack

| Technology | Application |
|------------|-------------|
| Python 3.11 or newer | Application code and pytest suite. |
| FastAPI | JSON HTTP API and application factory. |
| SQLite | Rates store, accessed through the generated persistence package. |
| CLI | Root `fxrates` executable and its command package. |
| pytest | Automated project test suite. |
| ECB reference rates | Published history CSV contained in the ECB archive. |
| POSIX shell | `bin/test.sh` and the supplied grader. |

## Programmatic Acceptance

=== AC python-structure ===
Intent: The application exposes its CLI and HTTP foundation packages.

import importlib.util

assert importlib.util.find_spec("cli") is not None
assert importlib.util.find_spec("app_server") is not None
=== END AC python-structure ===

=== AC root-entrypoint ===
Intent: The application root contains the declared executable entry point.

from pathlib import Path

entrypoint = Path("fxrates")
assert entrypoint.is_file()
=== END AC root-entrypoint ===

## User Acceptance

- None.

## Guardrails

- Keep database access inside the generated persistence package.
- Resolve the database location from `DATABASE_URL`, then `DATABASE_PATH`, then `data/app.db`.
- Store ECB rates as published text and use decimal arithmetic for calculations.
- Do not read `sources/run.sh` or supplied data files from application code.
- Validate a complete input file before its first write.
