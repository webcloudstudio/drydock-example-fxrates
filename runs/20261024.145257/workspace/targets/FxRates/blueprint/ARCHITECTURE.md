# ARCHITECTURE: FxRates

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Defines the application modules and their ownership boundaries. |

## System Structure

The application is a Python 3.11+ command-line program and JSON HTTP API. The root `fxrates` executable delegates to `cli.main`. The API is created by `app_server.main.create_app()` and served by uvicorn. Features call the generated `persistence` package for all database access.

## Module Ownership

| Boundary | Owner | Allowed access |
|----------|-------|----------------|
| Configuration | `config` | Reads `DATABASE_URL`, then `DATABASE_PATH`, then the `data/app.db` default. |
| Persistence | generated `persistence` package | Opens the configured database and performs declared repository operations. |
| CLI | `cli` | Parses commands and arguments, invokes feature services, and writes command output and diagnostics. |
| API | `app_server` | Defines FastAPI routes and delegates data operations to feature services. |
| ECB fetch integration | CLI fetch service | Downloads and extracts the ECB archive; passes its CSV to the shared loading behavior. |

No application module may open a database driver or issue SQL directly. Persisted rates use their published ECB text; arithmetic uses `decimal.Decimal`.

## Technology Stack

| Technology | Use |
|------------|-----|
| Python | Application language and project test suite. |
| FastAPI | JSON HTTP API. |
| SQLite | Local relational store, accessed only through the generated persistence package. |
| CLI | Root `fxrates` executable with `init`, `load`, `fetch`, and `serve` commands. |
| ECB reference rates | ECB history CSV obtained from the published ZIP archive. |
| Shell | POSIX-compatible command and test runners. |
| pytest | Automated project test suite. |
| uvicorn | Runs the FastAPI application on localhost. |

## Programmatic Acceptance

=== AC architecture-imports ===
Intent: The application entry points import successfully.

import cli
import app_server.main

assert callable(cli.main)
assert callable(app_server.main.create_app)
=== END AC architecture-imports ===

## User Acceptance

- None.

## Guardrails

- Keep database access behind the shipped persistence package.
- Do not read the supplied grader or data files from application code.
- Do not embed exchange rates, dates, counts, or computed answers.
