# FEATURE: Store Initialization

| Field       | Value |
|-------------|-------|
| Version     | 20261025 V1 |
| Description | Defines initialization of an empty rates store through the fxrates command. |
| Depends On  | DATABASE.md, FEATURE-CLI-Foundation.md |
| Provides    | fxrates init |
| Consumes    | rates repository operations |

## Purpose

`fxrates init` drops the `rates` table if present and creates it empty. It uses the configured database location and exits with status 0 on success. The command writes nothing to standard output on success.

## Workflow

1. Resolve the database location from `DATABASE_URL`, then `DATABASE_PATH`, then `data/app.db`.
2. Drop and recreate the rates table.
3. Return success.

## Programmatic Acceptance

=== AC init-clears-rates ===
Intent: Initialization succeeds and a separate repository read finds no rates afterward.

from cli.testing import cli_runner
from persistence.testing import db_session

code, stdout, stderr = cli_runner("init")
assert code == 0

with db_session() as db:
    rows = db.rates.list()
assert rows == []
=== END AC init-clears-rates ===

=== AC init-repeat ===
Intent: Repeating initialization succeeds and leaves the rates repository empty.

from cli.testing import cli_runner
from persistence.testing import db_session

first = cli_runner("init")
second = cli_runner("init")
assert first[0] == 0
assert second[0] == 0

with db_session() as db:
    rows = db.rates.list()
assert rows == []
=== END AC init-repeat ===

## User Acceptance

- None.

## Guardrails

- Initialization drops and recreates the rates table.
- Use the configured database location.
- Route database access through the generated persistence package.
