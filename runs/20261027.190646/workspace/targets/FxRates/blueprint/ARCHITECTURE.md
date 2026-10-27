# ARCHITECTURE: FxRates

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | Modules, boundaries, configuration resolution and test runner for the FxRates currency rates service. |
| Depends On | DATABASE.md |
| Provides | config.database_path, bin/test.sh |

## Purpose

FxRates keeps the ECB euro reference rate history in SQLite. A command line (`fxrates init`, `load`, `fetch`, `serve`) fills and runs it, and a FastAPI JSON API serves rates on a date, conversions and currency history. The product is an executable named `fxrates` at the application root.

## Technology Stack

Derived from `TECHNOLOGY_STACK.md`; that file is the decision of record.

| Technology | Where it applies |
|------------|------------------|
| Python 3.11+ | All application code. |
| FastAPI served by uvicorn | The `app_server` package, bound to 127.0.0.1. |
| SQLite | The one store, reached only through the shipped `persistence` package. |
| CLI | The `cli` package and the `fxrates` executable. |
| pytest | The test suite behind `bin/test.sh`; FastAPI `TestClient` for the API. |
| ECB reference rates | Input format: `eurofxref-hist.csv`, downloaded as `eurofxref-hist.zip`. |
| POSIX sh | `bin/test.sh` and the launchers in `bin/`. |

## Project Root

| Item | Rule |
|------|------|
| `pyproject.toml` | Python 3.11 or newer; dependencies fastapi, uvicorn, pytest, httpx2. |
| `uv.lock` | Committed. |
| `.venv` | Created by `uv venv`; activated by the launchers in `bin/`. |
| `bin/test.sh` | POSIX sh. Runs `pytest -q` from the application root and exits nonzero when any test fails. |
| `fxrates` | Executable at the application root; owned by the CLI foundation. |
| `sources/` | Read-only scoring assets; never modified and never read by application code. |

## Modules and Ownership

| Boundary | Owning module | Allowed low-level access |
|----------|---------------|--------------------------|
| Configuration | `config.py` (`database_path()`) | Environment variables `DATABASE_URL`, `DATABASE_PATH`. |
| Persistence | `persistence/` (shipped and generated) | The only code that imports a database driver. |
| Command line | `cli/` | Calls `persistence` and services; never a driver. |
| HTTP API | `app_server/` | Opens the store per request through `persistence.open_database`. |
| ECB parsing and download | `ecb` module (later stories) | Network access only in `ecb.download_history`. |
| File store | none | The loader reads one CSV path given on the command line. |
| External services | `ecb.download_history` | One GET of the ECB zip; stubbed in every test. |

## Configuration

`config.database_path()` resolves the database location in this order: `DATABASE_URL` (a file path, optionally prefixed `sqlite://`), then `DATABASE_PATH`, then `data/app.db`. An unset or empty variable is skipped. The function reads the environment on every call.

## Technical Decisions

- Rates are stored as the ECB's published text and all arithmetic uses `decimal`; floating point is never used for a rate.
- Only `fxrates init` creates the schema, through `persistence.initialize_database(dsn)`. Ordinary opens never initialize.
- Diagnostics go to standard error and are never compared. A failing command writes nothing to standard output.
- Exit codes: 0 success, 1 operational failure, 2 usage error, 3 rejected file.
- Tests stub the ECB download and never open a network connection.

## Programmatic Acceptance

=== AC config-precedence ===
Intent: database_path prefers DATABASE_URL (with or without the sqlite:// prefix), then DATABASE_PATH, then data/app.db, with names derived from the scratch root the fixture yields.
Requires: executable=python3; scope=test

from config import database_path
from drydock_acceptance import database_environment

with database_environment(url="sqlite://primary.db", path="fallback.db") as root:
    assert str(database_path()) == str(root / "primary.db")

with database_environment(url="plain.db", path="fallback.db") as root:
    assert str(database_path()) == str(root / "plain.db")

with database_environment(path="fallback.db") as root:
    assert str(database_path()) == str(root / "fallback.db")

with database_environment(url="", path="fallback.db") as root:
    assert str(database_path()) == str(root / "fallback.db")

with database_environment() as root:
    assert str(database_path()) == "data/app.db"
=== END AC config-precedence ===

=== AC project-toolchain ===
Intent: The project root carries a committed lock file, a manifest declaring Python 3.11+ with the web dependencies, and a bin/test.sh that runs pytest.
Requires: executable=python3; scope=test

import sys
import tomllib
from pathlib import Path

assert sys.version_info >= (3, 11)
assert Path("uv.lock").is_file()
assert Path("bin/test.sh").is_file()

data = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
deps = " ".join(data["project"]["dependencies"]).lower()
for name in ("fastapi", "uvicorn"):
    assert name in deps, name

script = Path("bin/test.sh").read_text(encoding="utf-8")
assert "pytest" in script
=== END AC project-toolchain ===

=== AC no-driver-imports ===
Intent: No application module outside the persistence package imports a database driver directly.
Requires: executable=python3; scope=test

from pathlib import Path

targets = [Path("config.py")]
for package in ("cli", "app_server"):
    root = Path(package)
    if root.is_dir():
        targets.extend(root.rglob("*.py"))

checked = 0
for path in targets:
    if not path.is_file():
        continue
    checked += 1
    text = path.read_text(encoding="utf-8")
    for driver in ("sqlite3", "psycopg"):
        assert f"import {driver}" not in text, (str(path), driver)
        assert f"from {driver}" not in text, (str(path), driver)
print(f"checked {checked} files")
assert checked >= 1
=== END AC no-driver-imports ===

## User Acceptance

- None.

## Guardrails

- Do not modify, rewrite or substitute any file under `sources/`, and never read `sources/run.sh` or a supplied data file from application code.
- Do not hardcode a rate, a date, a count or a computed value; every value comes from a query.
- Do not open a database driver outside the shipped persistence library.
- Do not initialize the schema from application startup.
- Do not use floating point for a rate.
