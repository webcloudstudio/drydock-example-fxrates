# FEATURE: CLI Initialization

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Initializes the rates store with no stored rates. |
| Depends On  | DATABASE.md, ARCHITECTURE.md |

## Purpose

`fxrates init` initializes the rates store and prints nothing. Per decision Q-001, it drops existing rates and leaves the store empty. Use only the declared persistence operations: list existing rows and delete them by their natural keys.

## Trigger and Workflow

1. The caller runs `./fxrates init`.
2. The command removes every stored rate through the repository interface.
3. The command returns success.

## Reads and Writes

- Reads: `FEATURE-RATE-002` to list rates.
- Writes: `FEATURE-RATE-003` to delete rates by date and currency.

## Programmatic Acceptance

=== AC cli-init-clears-rates ===
Intent: Initialization removes stored rates and the repository readback finds none.

from cli.testing import cli_runner
from persistence.testing import db_session

with db_session() as db:
    date = "2099-01-02"
    currency = "ZZZ"
    db.rates.upsert(date=date, currency=currency, rate="1.23")
    code, _, _ = cli_runner("init")
    assert code == 0
    assert db.rates.list(date=date, currency=currency) == []
=== END AC cli-init-clears-rates ===

=== AC cli-init-empty-store ===
Intent: Initialization succeeds when there are no rates to clear.

from cli.testing import cli_runner
from persistence.testing import db_session

with db_session() as db:
    code, _, _ = cli_runner("init")
    assert code == 0
    assert db.rates.list(date="2099-01-02", currency="ZZZ") == []
=== END AC cli-init-empty-store ===

## User Acceptance

- None.

## Guardrails

- Initialization must use the generated persistence interface; application code does not access the database driver directly.
- After initialization, no rates remain in the configured store.

## Database Interface

- `FEATURE-RATE-003` — write: rates.delete - supplies: `date`, `currency` - returns: `date`, `currency`
