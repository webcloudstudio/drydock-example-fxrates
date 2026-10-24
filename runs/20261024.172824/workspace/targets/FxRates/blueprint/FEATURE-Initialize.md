# FEATURE: Initialize Rates Store

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Initializes an empty rates store through the command line. |
| Depends On  | ARCHITECTURE.md, DATABASE.md |
| Provides    | fxrates init |
| Consumes    | rates.delete |

## Purpose

`fxrates init` drops and recreates the `rates` table empty, using the configured database location and the generated persistence boundary.

## Trigger and Workflow

1. The user runs `./fxrates init`.
2. The command opens the configured database through `persistence.open_database`.
3. It deletes existing rates through the declared persistence operation and succeeds with no standard output.

Initialization must be safe to run repeatedly. It affects the rates table only.

## Database Interface

- `FEATURE-RATE-004` — write: delete rates by date and currency - supplies: `date`, `currency` - returns: `date`, `currency`

## Programmatic Acceptance

=== AC initialize-clears-rates ===
Intent: Initialization removes existing rates and produces no standard output.

from cli.testing import cli_runner
from persistence.testing import db_session

date = "2001-02-03"
currency = "USD"
rate = "1.25"

with db_session() as db:
    db.rates.upsert(date=date, currency=currency, rate=rate)

code, stdout, stderr = cli_runner("init")
assert code == 0
assert stdout == ""

with db_session() as db:
    assert db.rates.get(date=date, currency=currency) is None
=== END AC initialize-clears-rates ===

=== AC initialize-repeat ===
Intent: Initialization can be run again after the rates table is empty.

from cli.testing import cli_runner
from persistence.testing import db_session

first = cli_runner("init")
second = cli_runner("init")
assert first[0] == 0
assert second[0] == 0
=== END AC initialize-repeat ===

## User Acceptance

- None.

## Guardrails

- Use the configured database location and the generated persistence library.
- Initialization clears only rates data.
