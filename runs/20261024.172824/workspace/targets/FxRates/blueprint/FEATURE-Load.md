# FEATURE: Load ECB History

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Validates and loads ECB euro reference rate history CSV files atomically. |
| Depends On  | ARCHITECTURE.md, DATABASE.md |
| Provides    | fxrates load |
| Consumes    | rates.upsert |

## Purpose

Load a local ECB history CSV into the configured rates store. Validate the entire file before the first write. A rejected file must leave the store unchanged.

## Trigger

`./fxrates load <csv>`

## Workflow

1. Read the specified file. A file that cannot be read is an operational failure.
2. Parse the CSV. The first header field must be `Date`; every other nonempty header field must be a three-letter uppercase currency code. Ignore the trailing empty field produced by the ECB's trailing comma.
3. For every row, require a real `YYYY-MM-DD` calendar date unique within the file and exactly one value for every currency column, excluding the ignored trailing empty field.
4. Accept `N/A` as a missing rate and do not store it. Every other rate must match `[0-9]+(\.[0-9]+)?` and be nonzero.
5. Validate all rows before writing any rate. If a row is invalid, reject the file without changing the database.
6. Upsert each non-`N/A` rate using its original text, replacing any existing value for the same date and currency.
7. Report the number of dates with at least one stored rate and the number of rates stored from this file.

## Output and failures

On success, stdout is CSV with header `dates,rates` and one data row containing the two counts. On a rejected file, return exit code `3`, write no stdout, and emit one diagnostic line to stderr. An unreadable file returns exit code `1` with the same failure-output convention.

## Programmatic Acceptance

=== AC load-stores-published-text ===
Intent: Loading a valid staged ECB file stores each non-N/A rate as published text and reports its date and rate counts.

import csv
import io
from pathlib import Path

from cli.testing import cli_runner
from persistence.testing import db_session

fixture = Path("sources/eurofxref-hist_2025-01.csv")
with fixture.open(newline="") as stream:
    rows = list(csv.reader(stream))
header = [value for value in rows[0] if value]
rates_by_date = {}
expected_rates = 0
for row in rows[1:]:
    row = [value for value in row if value]
    day, *values = row
    stored = {currency: rate for currency, rate in zip(header[1:], values) if rate != "N/A"}
    if stored:
        rates_by_date[day] = stored
        expected_rates += len(stored)

code, stdout, stderr = cli_runner("load", str(fixture))
assert code == 0
report = list(csv.reader(io.StringIO(stdout)))
assert report[0] == ["dates", "rates"]
assert report[1] == [str(len(rates_by_date)), str(expected_rates)]
with db_session() as db:
    for day, stored in rates_by_date.items():
        for currency, rate in stored.items():
            observed = db.rates.get(date=day, currency=currency)
            assert observed is not None
            assert observed.rate == rate
=== END AC load-stores-published-text ===

=== AC load-replaces-matching-rate ===
Intent: Loading a file replaces a stored rate for the same date and currency with its published text.

from cli.testing import cli_runner
from persistence.testing import db_session

date = "2025-01-31"
currency = "USD"
with db_session() as db:
    db.rates.upsert(date=date, currency=currency, rate="9.9")

fixture = "sources/eurofxref-hist_2025-01.csv"
code, stdout, stderr = cli_runner("load", fixture)
assert code == 0
with db_session() as db:
    observed = db.rates.get(date=date, currency=currency)
    assert observed is not None
    assert observed.rate == "1.0393"
=== END AC load-replaces-matching-rate ===

=== AC load-rejects-invalid-file-atomically ===
Intent: An invalid staged file is rejected without changing existing rates.

from cli.testing import cli_runner
from persistence.testing import db_session

date = "2001-01-02"
currency = "USD"
existing = "1.25"
with db_session() as db:
    db.rates.upsert(date=date, currency=currency, rate=existing)

code, stdout, stderr = cli_runner("load", "sources/eurofxref-hist_bad.csv")
assert code == 3
with db_session() as db:
    observed = db.rates.get(date=date, currency=currency)
    assert observed is not None
    assert observed.rate == existing
    assert db.rates.get(date="2025-02-04", currency="USD") is None
=== END AC load-rejects-invalid-file-atomically ===

## User Acceptance

- None.

## Guardrails

- Preserve each published rate as text; do not normalize its decimal spelling.
- Do not store `N/A` values.
- Validate the complete file before the first database write.
- Use only the declared persistence operations for database access.
- Loading must not remove or overwrite rates for dates or currencies absent from the input.
- A failed load writes nothing to stdout and emits one diagnostic line to stderr.
- The automated suite stubs fetch downloads and does not use the network.
