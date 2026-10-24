# ARCHITECTURE: FxRates

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Defines the application modules, configuration boundary, and ownership rules for FxRates. |
| Provides    | application modules, configuration boundary |

## Purpose

FxRates is a local command-line application and JSON HTTP service. It loads ECB reference-rate history into SQLite, then serves queries against the stored rates. The CLI, API, and service logic use the generated `persistence` package for all database access.

## Module Boundaries

| Module | Owns | May call |
|--------|------|----------|
| `config.py` | Resolve the database DSN | Python standard library |
| `cli` | Command parsing and dispatch | Application services, `app_server.main`, configuration |
| `app_server` | FastAPI application factory and HTTP request/response boundary | Application services |
| `services` | ECB loading, effective-date queries, conversion, history, and statistics | `persistence` operations |
| `persistence` | Database connections, generated schema, and declared repository operations | Shipped persistence library and SQLite engine |

The application may use `config.database_dsn()` to resolve the configured DSN: `DATABASE_URL` takes precedence over `DATABASE_PATH`, which takes precedence over `data/app.db`. Application modules do not import a database driver or issue SQL. The generated persistence package is the only application boundary that reaches the database.

Rates remain ECB-published text in storage. Any arithmetic uses `decimal.Decimal`; application behavior does not use binary floating-point arithmetic for rates or conversion results.

## Technology Stack

| Technology | Application |
|------------|-------------|
| Python 3.11 or newer | CLI, services, configuration, and API |
| FastAPI and uvicorn | JSON API and local server |
| SQLite | Persistent rate store, accessed through the shipped persistence library |
| pytest and FastAPI TestClient | Automated tests and in-process API checks |
| POSIX sh | Test runner and supplied grader |

## Programmatic Acceptance

=== AC architecture-imports ===
Intent: The application configuration and service boundary modules import successfully.

import importlib

for module_name in ("config", "services"):
    module = importlib.import_module(module_name)
    assert module is not None
=== END AC architecture-imports ===

=== AC database-dsn-precedence ===
Intent: Database configuration resolves DATABASE_URL before DATABASE_PATH and the default path.

import config

url = "sqlite:///first.db"
path = "second.db"
original_url = __import__("os").environ.get("DATABASE_URL")
original_path = __import__("os").environ.get("DATABASE_PATH")
try:
    __import__("os").environ["DATABASE_URL"] = url
    __import__("os").environ["DATABASE_PATH"] = path
    assert config.database_dsn() == url
    __import__("os").environ.pop("DATABASE_URL")
    assert config.database_dsn() == path
    __import__("os").environ.pop("DATABASE_PATH")
    assert config.database_dsn()
finally:
    if original_url is None:
        __import__("os").environ.pop("DATABASE_URL", None)
    else:
        __import__("os").environ["DATABASE_URL"] = original_url
    if original_path is None:
        __import__("os").environ.pop("DATABASE_PATH", None)
    else:
        __import__("os").environ["DATABASE_PATH"] = original_path
=== END AC database-dsn-precedence ===

## User Acceptance

- None.

## Guardrails

- Application database access goes through the shipped persistence library.
- Resolve the database location from `DATABASE_URL`, then `DATABASE_PATH`, then `data/app.db`.
- Store rates as ECB-published text and use decimal arithmetic for calculations.
- Do not read `sources/run.sh` or supplied data files from application code.
