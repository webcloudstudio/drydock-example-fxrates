# FEATURE: ECB History Loading

| Field       | Value |
|-------------|-------|
| Version     | 20261026 V1 |
| Description | Validates and atomically loads ECB history CSV files. |
| Depends On  | ARCHITECTURE.md, DATABASE.md |
| Provides    | `fxrates load` |

## Purpose

Load ECB historical rates supplied as a CSV file while preserving their published text.

## Trigger and workflow

`fxrates load <csv>` reads the requested file, validates the entire file before the first database write, and then upserts every valid rate through the declared persistence operations. Loading a row for an existing date and currency replaces its rate. The input may include a trailing empty field, which is ignored. `N/A` values are skipped.

The header begins with `Date`; remaining fields are three-letter uppercase currency codes. Each row has one date and one value per currency. Dates must be real `YYYY-MM-DD` calendar dates and cannot repeat within the file. Rates must match `[0-9]+(\.[0-9]+)?` and must be nonzero. A wrong field count, invalid or repeated date, or invalid value rejects the whole file without storing anything.

On success, standard output is CSV with header `dates,rates`, followed by the count of dates having at least one stored rate and the number of rates stored from the file. A read failure exits 1; a rejected file exits 3; usage errors exit 2. A failing command writes nothing to standard output and one diagnostic line to standard error.

## Database Interface

- `FEATURE-RATE-001` — write: replace a stored rate - supplies: `date`, `currency`, `rate` - returns: `date`, `currency`, `rate`

## Programmatic Acceptance

=== AC load-valid-fixture ===
Intent: Loading the staged January fixture preserves source rate text and stores every non-N/A cell.

from cli.testing import cli_runner
from persistence.testing import db_session

with db_session() as db:
    before = len(db.rates.list())
code, stdout, stderr = cli_runner("load", "sources/eurofxref-hist_2025-01.csv")
assert code == 0
with db_session() as db:
    rows = db.rates.list()
    added = [row for row in rows if row.date.startswith("2025-01-")]
    assert len(added) == 176
    assert any(row.date == "2025-01-29" and row.currency == "CHF" and row.rate == "0.943" for row in added)
=== END AC load-valid-fixture ===

=== AC load-repeat ===
Intent: Loading the same file twice leaves the rates table unchanged.

from cli.testing import cli_runner
from persistence.testing import db_session

first_code, _, _ = cli_runner("load", "sources/eurofxref-hist_2025-01.csv")
assert first_code == 0
with db_session() as db:
    first = sorted((row.date, row.currency, row.rate) for row in db.rates.list() if row.date.startswith("2025-01-"))
second_code, _, _ = cli_runner("load", "sources/eurofxref-hist_2025-01.csv")
assert second_code == 0
with db_session() as db:
    second = sorted((row.date, row.currency, row.rate) for row in db.rates.list() if row.date.startswith("2025-01-"))
assert second == first
=== END AC load-repeat ===

=== AC load-rejection-atomic ===
Intent: An invalid rate rejects the complete file without storing its valid first row.

from cli.testing import cli_runner
from persistence.testing import db_session

with db_session() as db:
    before = len(db.rates.list())
code, _, _ = cli_runner("load", "sources/eurofxref-hist_bad.csv")
assert code == 3
with db_session() as db:
    after = len(db.rates.list())
assert after == before
=== END AC load-rejection-atomic ===

=== AC load-missing-file ===
Intent: A missing input file is an operational failure.

from cli.testing import cli_runner

code, _, _ = cli_runner("load", "sources/no-such-file.csv")
assert code == 1
=== END AC load-missing-file ===

## User Acceptance

- None.

## Guardrails

- Validate the complete input before writing any rate.
- Do not convert published rate strings to floating point or normalize their spelling.
- Use the same database location precedence as the rest of the application.
- Diagnostics are sent to standard error; do not use messages as the acceptance oracle.
