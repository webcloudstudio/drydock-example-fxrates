# FEATURE: ECB History Loading

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Defines complete validation and atomic loading of ECB history CSV files. |
| Depends On  | DATABASE.md, FEATURE-CLI-Foundation.md |
| Provides    | fxrates load |
| Consumes    | rates repository operations |

## Purpose

`fxrates load <csv>` validates a complete ECB history CSV before making any database writes, then stores each non-`N/A` rate using the published text. A stored `(date, currency)` rate is replaced when the input contains that key again.

## File Rules

- The header begins with `Date`, followed by three-letter uppercase currency codes; a trailing empty field is ignored.
- Each row contains a real `YYYY-MM-DD` date, unique within the file, and one value per currency.
- `N/A` values are omitted. Every other value matches `[0-9]+(\.[0-9]+)?` and is nonzero.
- A malformed file changes no database state and exits with code `3`. An unreadable file exits with code `1`.
- Success reports `dates,rates`, followed by counts of dates with at least one stored rate and rates stored from the input.

## Workflow

1. Read and validate the entire file, including its header, row shapes, dates, duplicate dates, and values.
2. If validation fails, return the specified failure without writing any rates.
3. Otherwise, upsert each non-`N/A` value as published text through the declared repository operation.
4. Report the counts derived from the file's stored rates.

## Programmatic Acceptance

=== AC load-published-text-and-counts ===
Intent: Loading the staged January file reports counts derived from its rows and persists published rate text.

import csv
from pathlib import Path
from cli.testing import cli_runner
from persistence.testing import db_session

source = Path("sources/eurofxref-hist_2025-01.csv")
with source.open(newline="") as file:
    rows = list(csv.reader(file))
currency_count = len([field for field in rows[0][1:] if field])
date_count = sum(1 for row in rows[1:] if row and row[0])
rate_count = sum(1 for row in rows[1:] for value in row[1:] if value and value != "N/A")
code, stdout, stderr = cli_runner("load", str(source))
assert code == 0
reported = list(csv.reader(stdout.splitlines()))
assert reported == [["dates", "rates"], [str(date_count), str(rate_count)]]
sample_date = rows[1][0]
sample_currency = rows[0][1]
sample_rate = rows[1][1]
with db_session() as db:
    stored = db.rates.for_date(date=sample_date)
    row = next(item for item in stored if item.currency == sample_currency)
    assert row.rate == sample_rate
=== END AC load-published-text-and-counts ===

=== AC load-rejection-is-atomic ===
Intent: A rejected staged file leaves the existing rates unchanged.

from pathlib import Path
from cli.testing import cli_runner
from persistence.testing import db_session

date = "2099-01-02"
currency = "ZZZ"
rate = "1.25"
with db_session() as db:
    db.rates.replace_rate(date=date, currency=currency, rate=rate)
    before = [(row.date, row.currency, row.rate) for row in db.rates.all()]
code, stdout, stderr = cli_runner("load", "sources/eurofxref-hist_bad.csv")
assert code == 3
with db_session() as db:
    after = [(row.date, row.currency, row.rate) for row in db.rates.all()]
assert after == before
=== END AC load-rejection-is-atomic ===

=== AC load-replaces-existing-key ===
Intent: Loading a file replaces a previously stored value for the same date and currency.

import csv
from pathlib import Path
from cli.testing import cli_runner
from persistence.testing import db_session

source = Path("sources/eurofxref-hist_2025-01.csv")
with source.open(newline="") as file:
    rows = list(csv.reader(file))
date = rows[1][0]
currency = rows[0][1]
published_rate = rows[1][1]
replacement = "9.876"
with db_session() as db:
    db.rates.replace_rate(date=date, currency=currency, rate=replacement)
code, stdout, stderr = cli_runner("load", str(source))
assert code == 0
with db_session() as db:
    stored = db.rates.for_date(date=date)
    row = next(item for item in stored if item.currency == currency)
    assert row.rate == published_rate
=== END AC load-replaces-existing-key ===

## User Acceptance

- None.

## Guardrails

- Validate the whole file before the first write.
- Preserve published rate text; omit `N/A`; do not store a numeric conversion of a rate.
- A rejected file changes nothing.
- Do not hardcode fixture answers, dates, counts, or rates in application code.
- All persistence uses the generated repository operations declared by `DATABASE.md`.

## Database Interface

- `FEATURE-ECB-001` — write: rates.replace_rate - supplies: `date`, `currency`, `rate` - returns: `date`, `currency`, `rate`
