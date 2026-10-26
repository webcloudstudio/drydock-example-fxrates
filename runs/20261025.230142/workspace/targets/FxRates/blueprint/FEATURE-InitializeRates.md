# FEATURE: Initialize Rates

| Field       | Value |
|-------------|-------|
| Version     | 20261025 V1 |
| Description | Initializes the rates store from the command line. |
| Depends On  | FEATURE-CliFoundation.md, DATABASE.md |
| Provides    | `fxrates init` |
| Consumes    | `rates.delete` |

## Trigger and Behavior

`fxrates init` removes existing rate records and leaves the rates store empty. It succeeds with exit code `0` and no standard output. The command uses the declared `rates.delete` repository operation and does not open the database driver directly.

## Programmatic Acceptance

=== AC init_clears_rates ===
Intent: Initialization removes existing rates from the configured repository.

from cli.testing import cli_runner
from persistence.testing import db_session

date = "2099-01-02"
currency = "ZZZ"
rate = "1.2300"

with db_session() as db:
    db.rates.upsert(date=date, currency=currency, rate=rate)
    assert db.rates.get(date=date, currency=currency) is not None

code, stdout, stderr = cli_runner("init")
assert code == 0

with db_session() as db:
    assert db.rates.get(date=date, currency=currency) is None
=== END AC init_clears_rates ===

=== AC init_usage_errors ===
Intent: Initialization command dispatch does not treat an unknown command as successful.

from cli.testing import cli_runner

code, stdout, stderr = cli_runner("unknown-command")
assert code == 2
=== END AC init_usage_errors ===

## User Acceptance

- None.

## Guardrails

- Initialization drops and recreates the rates table empty, as specified.
- The command accesses persistence only through the generated repository package.
- A failing command writes no standard output and emits a diagnostic to standard error.

## Database Interface

- `FEATURE-RATE-004` — write: rates.delete - supplies: `date`, `currency` - returns: `date`, `currency`
