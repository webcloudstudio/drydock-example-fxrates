# FEATURE: CLI Load

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Loads ECB history CSV files after validating each complete file. |
| Depends On  | DATABASE.md, ARCHITECTURE.md, FEATURE-CLI-Init.md |
| Provides    | fxrates load |
| Consumes    | rates repository operations |

## Purpose

`fxrates load <csv>` validates the whole ECB history file before writing, stores each non-`N/A` published rate as text, replaces matching date and currency rows, and reports the dates and rates stored from the file.

## Workflow

The CSV header starts with `Date`, followed by three-letter uppercase currency codes; a final empty field from the ECB trailing comma is ignored. Each row has a valid, unique calendar date and one value per currency. `N/A` is skipped; other values must match `[0-9]+(\.[0-9]+)?` and be nonzero. Wrong field counts, malformed or repeated dates, and invalid values reject the entire file without writes. An unreadable path is an operational failure.

Success writes:

- `dates,rates`
- The number of dates containing at least one stored rate and the number of rates stored from the input file.

Exit status is 0 on success, 1 when the file cannot be read, and 3 for a rejected file. Failure writes no standard output.

## Database Interface


- None — persistence is owned by DATABASE.md.

## Programmatic Acceptance

=== AC cli-load-valid ===
Intent: A valid ECB file loads successfully and stores the supplied published rate text.

from cli.testing import cli_runner
from persistence.testing import db_session

date = "2099-01-02"
currency = "ZZZ"
published = "0.943"
csv_text = f"Date,{currency},\n{date},{published},\n"
code, out, _ = cli_runner("load", "/tmp/fxrates-valid.csv")
assert code == 0
with db_session() as db:
    rows = db.rates.list_date(date=date)
    assert any(row.currency == currency and row.rate == published for row in rows)
=== END AC cli-load-valid ===

=== AC cli-load-rejects-without-write ===
Intent: A rejected file returns the rejection status and stores none of its valid-prefix rows.

from cli.testing import cli_runner
from persistence.testing import db_session

date = "2099-01-03"
currency = "ZZZ"
csv_text = f"Date,{currency},\n{date},1.2,\n{date},invalid,\n"
code, _, _ = cli_runner("load", "/tmp/fxrates-invalid.csv")
assert code == 3
with db_session() as db:
    assert not any(row.date == date and row.currency == currency for row in db.rates.list_all())
=== END AC cli-load-rejects-without-write ===

=== AC cli-load-replaces-existing ===
Intent: Loading a matching date and currency replaces its previously stored text.

from cli.testing import cli_runner
from persistence.testing import db_session

date = "2099-01-04"
currency = "ZZZ"
published = "1.2"
replacement = "1.3"
with db_session() as db:
    db.rates.upsert(date=date, currency=currency, rate=published)
code, _, _ = cli_runner("load", "/tmp/fxrates-replacement.csv")
assert code == 0
with db_session() as db:
    rows = db.rates.list_date(date=date)
    assert any(row.currency == currency and row.rate == replacement for row in rows)
=== END AC cli-load-replaces-existing ===

=== AC cli-load-unreadable ===
Intent: An unreadable CSV path returns operational failure and no output.

from cli.testing import cli_runner

code, out, _ = cli_runner("load", "/tmp/fxrates-no-such-file.csv")
assert code == 1
assert out == ""
=== END AC cli-load-unreadable ===

## User Acceptance

- None.

## Guardrails

- Validate the complete file before its first write.
- Preserve rates as published text and never store `N/A`.
- Use the persistence library for every database operation.
- Do not read `sources/run.sh` or embed expected answers.
