# FEATURE: ECB Loading

| Field       | Value |
|-------------|-------|
| Version     | 20261025 V1 |
| Description | Validates and atomically loads ECB history CSV files into the rates store. |
| Depends On  | DATABASE.md, FEATURE-CLI-Foundation.md, FEATURE-Store-Initialization.md |
| Provides    | fxrates load |
| Consumes    | rates repository operations |

## Purpose

`fxrates load <csv>` reads an ECB history CSV, validates the complete file before writing, then stores each non-`N/A` published rate as text. A rate for an existing `(date, currency)` replaces the stored rate. Loading the same file again leaves the stored rates unchanged.

The header begins with `Date`, followed by three-letter uppercase currency codes. ECB files may have a trailing empty field on each line; ignore that field. Each data row has a real `YYYY-MM-DD` date, unique within the file, and one value per currency. Values are `N/A` or nonzero numbers matching `[0-9]+(\.[0-9]+)?`.

On success, stdout contains CSV with a `dates,rates` header and counts for dates with at least one stored rate and rates stored from the file. A rejected file returns 3 and changes nothing. A file read failure returns 1. Failed commands write no stdout and emit one diagnostic line to stderr.

## Programmatic Acceptance

=== AC load-published-text ===
Intent: Loading the staged January history stores every non-N/A rate with its published text and reports counts derived from that fixture.

import csv
import io
from cli.testing import cli_runner
from persistence.testing import db_session

fixture = "sources/eurofxref-hist_2025-01.csv"
expected = []
with open(fixture, newline="") as source_file:
    reader = csv.reader(source_file)
    header = next(reader)
    currencies = [value for value in header[1:] if value]
    for row in reader:
        fields = row[:-1] if row and row[-1] == "" else row
        day = fields[0]
        for currency, published_rate in zip(currencies, fields[1:]):
            if published_rate != "N/A":
                expected.append((day, currency, published_rate))

code, stdout, stderr = cli_runner("load", fixture)
assert code == 0
output_rows = list(csv.reader(io.StringIO(stdout)))
assert output_rows[0] == ["dates", "rates"]
assert output_rows[1] == [str(len({row[0] for row in expected})), str(len(expected))]

with db_session() as db:
    actual_rows = db.rates.list()
actual = [(row.date, row.currency, row.rate) for row in actual_rows]
assert actual == sorted(expected)

=== END AC load-published-text ===

=== AC load-rejects-atomically ===
Intent: A rejected file preserves existing rows and does not partially store its valid first row.

from cli.testing import cli_runner
from persistence.testing import db_session

sentinel = "7.6500"
first_date = "2025-02-04"
second_date = "2025-02-03"

with db_session() as db:
    db.rates.upsert(date=first_date, currency="USD", rate=sentinel)
    before_second = db.rates.get(date=second_date, currency="USD")

code, stdout, stderr = cli_runner("load", "sources/eurofxref-hist_bad.csv")
assert code == 3

with db_session() as db:
    first_after = db.rates.get(date=first_date, currency="USD")
    second_after = db.rates.get(date=second_date, currency="USD")

assert first_after is not None
assert first_after.rate == sentinel
assert second_after == before_second
=== END AC load-rejects-atomically ===

=== AC load-replacement-is-idempotent ===
Intent: Loading the same valid fixture twice replaces matching rates without changing the stored values.

import csv
from cli.testing import cli_runner
from persistence.testing import db_session

fixture = "sources/eurofxref-hist_2025-02-03_04.csv"
expected = []
with open(fixture, newline="") as source_file:
    reader = csv.reader(source_file)
    header = next(reader)
    currencies = [value for value in header[1:] if value]
    for row in reader:
        fields = row[:-1] if row and row[-1] == "" else row
        for currency, published_rate in zip(currencies, fields[1:]):
            if published_rate != "N/A":
                expected.append((fields[0], currency, published_rate))

first_code, _, _ = cli_runner("load", fixture)
with db_session() as db:
    after_first = db.rates.list()
second_code, _, _ = cli_runner("load", fixture)
with db_session() as db:
    after_second = db.rates.list()

assert first_code == 0
assert second_code == 0
first_values = [(row.date, row.currency, row.rate) for row in after_first if row.date in {item[0] for item in expected}]
second_values = [(row.date, row.currency, row.rate) for row in after_second if row.date in {item[0] for item in expected}]
assert first_values == sorted(expected)
assert second_values == first_values
=== END AC load-replacement-is-idempotent ===

## User Acceptance

- None.

## Guardrails

- Validate the entire file before the first database write.
- Store every non-`N/A` rate exactly as published text; never convert it to floating point.
- Replace an existing rate for the same date and currency.
- Do not modify any file under `sources/`.
- Keep database access inside the generated persistence package.
