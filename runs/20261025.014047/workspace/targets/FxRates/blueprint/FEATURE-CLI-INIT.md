# FEATURE: CLI Init

| Field       | Value |
|-------------|-------|
| Version     | 20261025 V1 |
| Description | Defines initialization behavior for the rates database. |
| Depends On  | DATABASE.md, ARCHITECTURE.md |
| Provides    | `fxrates init` |
| Consumes    | `persistence.open_database`, `db.rates.delete` |

## Purpose

`fxrates init` drops the existing rates table contents and leaves the rates store empty. It succeeds with exit code `0` and writes nothing to standard output.

## Trigger and Sequence

1. The user invokes `./fxrates init`.
2. The command opens the configured database through the persistence library.
3. It deletes all stored rate rows through the declared repository operation.
4. It returns success without standard output.

Initialization does not issue schema DDL; the generated database foundation provisions the table.

## Programmatic Acceptance

=== AC cli-init-empty ===
Intent: The init command succeeds and emits no standard output.

from cli.testing import cli_runner

code, stdout, stderr = cli_runner("init")
assert code == 0
assert stdout == ""
=== END AC cli-init-empty ===

=== AC cli-init-clears-rates ===
Intent: The init command removes stored rates from the configured store.

from persistence.testing import db_session
from cli.testing import cli_runner

date = "2099-12-30"
currency = "ZZZ"
rate = "1.234"

with db_session() as db:
    db.rates.upsert(date=date, currency=currency, rate=rate)

code, stdout, stderr = cli_runner("init")
assert code == 0

with db_session() as db:
    assert db.rates.get(date=date, currency=currency) is None
=== END AC cli-init-clears-rates ===

## User Acceptance

- None.

## Guardrails

- All database access goes through the shipped persistence library.
- Initialization leaves the rates table empty and prints nothing on success.
