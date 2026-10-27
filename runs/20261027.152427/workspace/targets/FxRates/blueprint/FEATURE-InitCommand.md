# FEATURE: Init Command

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | `fxrates init` empties the rates table, prints nothing, and exits 0. |
| Depends On | FEATURE-CliUsageErrors.md, FEATURE-DatabaseSelection.md, DATABASE.md |
| Provides | fxrates init |
| Consumes | cli.main, fxrates_app.config.database_path, rates.delete_from_date |

## Purpose

`fxrates init` resets the rates store to empty. The schema is provisioned by the DATABASE step and
application code never runs DDL or opens a driver, so init removes every stored rate through the
declared `rates.delete_from_date` operation, passing a `from_date` earlier than any publication
(`0000-01-01`). Afterward the table exists and holds no rows.

## Behavior

- Registers the `init` handler with the dispatcher in `cli`.
- Opens the store through `persistence.open_database` using the configured database location.
- Removes every row, prints nothing to standard output, and exits `0`.
- Init takes no arguments; a wrong argument count is a usage error owned by FEATURE-CliUsageErrors.md.
- Running init on an already empty store succeeds and changes nothing.

## Database Interface

- `FEATURE-RATE-007` — write: remove every stored rate - supplies: `from_date` - returns: —

## Programmatic Acceptance

=== AC init-empties-store ===
Intent: After init, rates seeded through the repository are gone, and init prints nothing and exits 0.
Requires: executable=python3; scope=test

from persistence.testing import db_session
from cli.testing import cli_runner

c = "ZZA"
d = "1900-09-01"

with db_session() as db:
    db.rates.replace_rate(date=d, currency=c, rate="1.25")
    assert [r.date for r in db.rates.list_currency_history(currency=c)] == [d]
    code, out, err = cli_runner("init")
    assert code == 0
    assert out == ""
    assert db.rates.list_currency_history(currency=c) == []
    assert db.rates.list_all_keys() == []
=== END AC init-empties-store ===

=== AC init-idempotent ===
Intent: Running init twice in a row exits 0 both times, prints nothing, and leaves the store empty.
Requires: executable=python3; scope=test

from persistence.testing import db_session
from cli.testing import cli_runner

with db_session() as db:
    db.rates.replace_rate(date="1900-09-02", currency="ZZB", rate="2")
    for _ in range(2):
        code, out, err = cli_runner("init")
        assert code == 0
        assert out == ""
    assert db.rates.list_all_keys() == []
=== END AC init-idempotent ===

=== AC init-rejects-extra-argument ===
Intent: Init with an extra argument is a usage error that exits 2 and leaves stored rates untouched.
Requires: executable=python3; scope=test

from persistence.testing import db_session
from cli.testing import cli_runner

c = "ZZC"
d = "1900-09-03"

with db_session() as db:
    db.rates.replace_rate(date=d, currency=c, rate="3")
    code, out, err = cli_runner("init", "extra")
    assert code == 2
    assert out == ""
    assert [r.date for r in db.rates.list_currency_history(currency=c)] == [d]
=== END AC init-rejects-extra-argument ===

## User Acceptance

- None.

## Guardrails

- Application code never runs DDL or imports a database driver; init uses the declared repository operation.
- Standard output stays empty; diagnostics go to standard error.
