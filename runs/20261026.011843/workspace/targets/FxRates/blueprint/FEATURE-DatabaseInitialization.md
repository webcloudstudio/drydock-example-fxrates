# FEATURE: Database Initialization

| Field       | Value |
|-------------|-------|
| Version     | 20261026 V1 |
| Description | Initializes the rates table through the `fxrates init` command. |
| Depends On  | ARCHITECTURE.md, DATABASE.md |
| Provides    | `fxrates init` |

## Purpose

Allow operators and the supplied harness to initialize an empty rates table before loading history.

## Trigger and behavior

`fxrates init` drops the existing `rates` table if present and creates it empty. It writes nothing to standard output on success. A later initialization removes previously stored rates.

The command line provides usable help text. Unknown commands, incorrect argument counts, and a non-integer `serve --port` are usage errors with exit code 2.

## Database Interface

- None — persistence is owned by DATABASE.md.

## Programmatic Acceptance

=== AC init-empty ===
Intent: Initialization clears existing rates and leaves the table empty.

from cli.testing import cli_runner
from persistence.testing import db_session

date = "2098-06-01"
currency = "ZZZ"
rate = "1.5"

with db_session() as db:
    db.rates.upsert(date=date, currency=currency, rate=rate)

exit_code, stdout, stderr = cli_runner("init")
assert exit_code == 0
with db_session() as db:
    rows = db.rates.by_date(date=date)
    assert not any(row.currency == currency for row in rows)
=== END AC init-empty ===

=== AC init-usage ===
Intent: Initialization accepts no extra arguments and unknown commands return the declared usage status.

from cli.testing import cli_runner

init_code, _, _ = cli_runner("init", "extra")
unknown_code, _, _ = cli_runner("frobnicate")
assert init_code == 2
assert unknown_code == 2
=== END AC init-usage ===

## User Acceptance

- None.

## Guardrails

- Resolve the configured database as `DATABASE_URL`, then `DATABASE_PATH`, then `data/app.db`.
- Do not assume the database is empty before initialization.
- Do not open a database driver outside the shipped persistence library.
