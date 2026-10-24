# FEATURE: ECB Store Initialization

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Defines the command that drops and recreates the empty rates table. |
| Depends On  | DATABASE.md, FEATURE-CLI-Foundation.md |
| Provides    | fxrates init |
| Consumes    | rates repository operations |

## Purpose

`fxrates init` resets the configured store's rates table by dropping and recreating it empty. It prints nothing on success.

## Workflow

1. Invoke `fxrates init`.
2. Drop the existing `rates` table if present and recreate the table using the configured database.
3. Return success with empty standard output.

The command uses the persistence boundary and the database configuration contract. It does not initialize or alter unrelated application data.

## Programmatic Acceptance

=== AC init-clears-rates ===
Intent: Initialization removes previously stored rates and returns success.

from cli.testing import cli_runner
from persistence.testing import db_session

date = "2099-01-02"
currency = "ZZZ"
rate = "1.25"
with db_session() as db:
    db.rates.replace_rate(date=date, currency=currency, rate=rate)

code, stdout, stderr = cli_runner("init")
assert code == 0
with db_session() as db:
    assert db.rates.latest() == []
=== END AC init-clears-rates ===

=== AC init-repeat ===
Intent: Initialization can be run again against an already initialized store.

from cli.testing import cli_runner
from persistence.testing import db_session

first = cli_runner("init")
second = cli_runner("init")
assert first[0] == 0
assert second[0] == 0
with db_session() as db:
    assert db.rates.latest() == []
=== END AC init-repeat ===

## User Acceptance

- None.

## Guardrails

- Use the configured store and the shipped persistence boundary.
- Initialization drops and recreates the `rates` table empty.
- Successful initialization writes nothing to standard output.
