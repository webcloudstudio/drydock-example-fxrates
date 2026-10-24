# FEATURE: Load History

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Validates and loads ECB history CSV files through the CLI. |
| Depends On  | FEATURE-Initialize-Store.md, DATABASE.md |
| Provides    | `fxrates load` |
| Consumes    | rates repository operations |

## Purpose

`fxrates load <csv>` validates the complete CSV before writing. The header begins with `Date`; currency fields are three-letter uppercase codes, with a trailing empty field ignored. Each date is a unique real calendar date in `YYYY-MM-DD` form. `N/A` values are skipped; other values must match `[0-9]+(\.[0-9]+)?` and be nonzero. Valid rates are stored exactly as published, replacing any stored value for the same date and currency.

On success, standard output is two lines: `dates,rates`, followed by the counts of dates with at least one stored rate and rates stored from the input.

## Programmatic Acceptance

=== AC load-valid-file ===
Intent: A valid staged history file loads successfully.
Suite: scoped

from cli.testing import cli_runner

result = cli_runner("load", "sources/eurofxref-hist_2025-01.csv")
assert result[0] == 0
=== END AC load-valid-file ===

=== AC load-preserves-rate-text ===
Intent: Loaded rates are readable through the generated repository with their published text preserved.

from cli.testing import cli_runner
from persistence.testing import committed_session

result = cli_runner("load", "sources/eurofxref-hist_2025-01.csv")
assert result[0] == 0
with committed_session() as db:
    rows = db.rates.list(date="2025-01-29", currency="CHF")
    assert len(rows) == 1
    assert rows[0].rate == "0.943"
=== END AC load-preserves-rate-text ===

=== AC load-skips-na ===
Intent: Currency cells marked N/A do not create stored rate rows.

from cli.testing import cli_runner
from persistence.testing import committed_session

result = cli_runner("load", "sources/eurofxref-hist_2025-01.csv")
assert result[0] == 0
with committed_session() as db:
    rows = db.rates.list(currency="HRK")
    assert rows == []
=== END AC load-skips-na ===

=== AC load-replaces-existing ===
Intent: Loading a publication row stores or replaces its matching rate.
Suite: scoped

from cli.testing import cli_runner
from persistence.testing import committed_session

with committed_session() as db:
    db.rates.upsert(date="2025-01-29", currency="CHF", rate="9.876")
result = cli_runner("load", "sources/eurofxref-hist_2025-01.csv")
assert result[0] == 0
with committed_session() as db:
    rows = db.rates.list(date="2025-01-29", currency="CHF")
    assert len(rows) == 1
    assert rows[0].rate == "0.943"
=== END AC load-replaces-existing ===

## User Acceptance

- None.

## Guardrails

- Validate the whole file before its first write.
- Preserve each ECB rate as published text; do not store rates as floating-point values.
- Use the generated `persistence` package for all database access.

## Database Interface

- `FEATURE-RATE-003` — write: rates.upsert - supplies: `date`, `currency`, `rate` - returns: `id`, `date`, `currency`, `rate`
