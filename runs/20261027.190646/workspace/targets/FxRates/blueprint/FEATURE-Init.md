# FEATURE: Init Command

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | The fxrates init command creates missing tables and indexes and preserves stored rates. |
| Depends On | FEATURE-CliFoundation.md, DATABASE.md |
| Provides | fxrates init |
| Consumes | cli.main, config.database_path |

## Purpose

Initialize the rates store explicitly; it is the only place the schema is created.

## Behavior

`cli/commands/init.py` exposes `run(args) -> int`. It calls `persistence.initialize_database(dsn)` with the location from `config.database_path()`, closes the returned database, writes nothing to standard output and returns 0. Repeating init succeeds and preserves every stored rate. It never drops a table, deletes a row or migrates an existing table, and application code contains no DDL.

## Database Interface

- None — persistence is owned by DATABASE.md.

## Programmatic Acceptance

=== AC init-fresh-store ===
Intent: init on a fresh store exits 0 with empty stdout and leaves a store whose rates operations work.
Requires: executable=python3; scope=test

from cli.testing import cli_runner
from drydock_acceptance import database_environment
from persistence import open_database

date, currency, rate = "1800-05-01", "ZZA", "1.2300"

with database_environment(url="init.db") as root:
    code, out, err = cli_runner("init")
    assert code == 0
    assert out == ""
    db = open_database(str(root / "init.db"))
    try:
        stored = db.rates.replace_rate(date=date, currency=currency, rate=rate)
        assert stored.rate == rate
        rows = db.rates.history(currency=currency)
        assert [(r.date, r.rate) for r in rows] == [(date, rate)]
    finally:
        db.close()
=== END AC init-fresh-store ===

=== AC init-repeat-preserves ===
Intent: Running init again succeeds and leaves previously stored rates unchanged.
Requires: executable=python3; scope=test

from cli.testing import cli_runner
from drydock_acceptance import database_environment
from persistence import open_database

currency = "ZZB"
points = [("1800-06-01", "3.10"), ("1800-06-02", "4.5")]

with database_environment(url="repeat.db") as root:
    code, out, err = cli_runner("init")
    assert code == 0
    db = open_database(str(root / "repeat.db"))
    try:
        for date, rate in points:
            db.rates.replace_rate(date=date, currency=currency, rate=rate)
    finally:
        db.close()

    code, out, err = cli_runner("init")
    assert code == 0
    assert out == ""

    db = open_database(str(root / "repeat.db"))
    try:
        rows = db.rates.history(currency=currency)
        assert [(r.date, r.rate) for r in rows] == sorted(points)
    finally:
        db.close()
=== END AC init-repeat-preserves ===

=== AC init-uses-database-path ===
Intent: With DATABASE_URL unset, init creates the store named by DATABASE_PATH.
Requires: executable=python3; scope=test

from cli.testing import cli_runner
from drydock_acceptance import database_environment
from persistence import open_database

with database_environment(path="fallback.db") as root:
    code, out, err = cli_runner("init")
    assert code == 0
    assert out == ""
    assert (root / "fallback.db").is_file()
    db = open_database(str(root / "fallback.db"))
    try:
        assert db.rates.list_all() == []
    finally:
        db.close()
=== END AC init-uses-database-path ===

## User Acceptance

- None.

## Guardrails

- Init never drops tables, deletes records or migrates existing table definitions.
- No DDL is authored in application code; the schema comes from the generated persistence package.
- Init writes nothing to standard output.
