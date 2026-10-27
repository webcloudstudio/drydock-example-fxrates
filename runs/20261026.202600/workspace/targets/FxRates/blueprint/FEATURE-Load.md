# FEATURE: ECB CSV Loading

| Field       | Value |
|-------------|-------|
| Version     | 20261026 V1 |
| Description | Validates and loads ECB history CSV files atomically while preserving published rate text. |
| Depends On  | FEATURE-CLI.md, DATABASE.md |

## Purpose

`./fxrates load <csv>` reads an ECB history file, validates the entire file before its first database write, then stores every rate other than `N/A`. A valid rate replaces the stored value for the same publication date and currency. On success, print CSV output with header `dates,rates` and one data row containing the number of dates with at least one rate and the number of rates stored from this file.

## CSV Rules

- The first header field is `Date`; subsequent fields are three-letter uppercase currency codes. Ignore the final empty field produced by the ECB trailing comma.
- Each row has a real, non-repeated `YYYY-MM-DD` date and exactly one value per currency, excluding the ignored trailing field.
- `N/A` denotes no rate and creates no stored row. Other values match `[0-9]+(\.[0-9]+)?` and are nonzero.
- A malformed header or row, wrong field count, invalid or repeated date, or invalid rate rejects the file. Reject it before writing any row.
- A file read failure is an operational failure. A rejected file and an operational failure produce no standard output; diagnostics go to standard error.

## Database Interface

- `FEATURE-RATE-001` — write: store or replace a published rate - supplies: `date`, `currency`, `rate` - returns: `date`, `currency`, `rate`

## Programmatic Acceptance

=== AC load-valid-file ===
Intent: Loading the supplied January history succeeds and reports the fixture-derived date and rate counts.
import csv
from cli.testing import cli_runner

path = "sources/eurofxref-hist_2025-01.csv"
code, stdout, stderr = cli_runner("load", path)
rows = list(csv.reader(stdout.splitlines()))
assert code == 0
assert rows[0] == ["dates", "rates"]
assert rows[1] == [str(22), str(22 * 8)]
=== END AC load-valid-file ===

=== AC load-rejects-atomically ===
Intent: A rejected CSV file leaves the rates it would otherwise have changed untouched.
from cli.testing import cli_runner
from persistence.testing import db_session

date = "2025-02-04"
currency = "USD"
rate = "9.876"

with db_session() as db:
    seeded = db.rates.upsert(date=date, currency=currency, rate=rate)
    assert seeded.rate == rate
    code, stdout, stderr = cli_runner("load", "sources/eurofxref-hist_bad.csv")
    stored = db.rates.by_date(date=date)
    assert code == 3
    assert stdout == ""
    assert any(row.currency == currency and row.rate == rate for row in stored)
=== END AC load-rejects-atomically ===

=== AC load-replaces-published-text ===
Intent: Loading a valid file stores its rate text exactly and replaces a matching stored rate.
from cli.testing import cli_runner
from persistence.testing import db_session

date = "2025-01-31"
currency = "USD"
published = "1.0393"
prior = "9.876"

with db_session() as db:
    seeded = db.rates.upsert(date=date, currency=currency, rate=prior)
    assert seeded.rate == prior
    code, stdout, stderr = cli_runner("load", "sources/eurofxref-hist_2025-01.csv")
    stored = db.rates.by_date(date=date)
    found = next(row for row in stored if row.currency == currency)
    assert code == 0
    assert found.rate == published
=== END AC load-replaces-published-text ===

## User Acceptance

- None.

## Guardrails

- Check the entire file before its first write; a rejected file changes nothing.
- Store published rate strings unchanged, omit `N/A`, and replace matching `(date, currency)` rows.
- Access persistence only through the shipped library and generated relational layer.
