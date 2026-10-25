# FEATURE: CLI Load

| Field       | Value |
|-------------|-------|
| Version     | 20261025 V1 |
| Description | Loads validated ECB history files into the rates store. |
| Depends On  | DATABASE.md, ARCHITECTURE.md |
| Provides    | `fxrates load` |
| Consumes    | `rates.upsert`, `rates.list` |

## Purpose

Load an ECB history CSV, validating the entire file before writing. A successful load stores non-`N/A` rates as their original text, replaces existing date and currency pairs, and reports the number of dates with stored rates and the number of rates stored.

## Workflow

1. Read and parse the specified CSV, ignoring the trailing empty field produced by the ECB's final comma.
2. Validate the header, currency codes, row field counts, real calendar dates, unique dates, and every rate value.
3. Reject the file without writes if any row is invalid.
4. Upsert all non-`N/A` rates through the generated persistence package.
5. Print the load summary on success. On failure, print no standard output and write one diagnostic line to standard error.

Exit status is `0` on success, `1` when the file cannot be read, `2` for usage errors, and `3` for rejected file content.

## Programmatic Acceptance

=== AC load-stores-published-text ===
Intent: Loading a valid CSV stores each non-N/A rate as the exact input text and reports success.
Suite: scoped

from pathlib import Path
from cli.testing import cli_runner
from persistence.testing import db_session

csv_path = Path("load-valid.csv")
date = "2099-12-30"
currency = "ZZZ"
rate = "1.2300"
csv_path.write_text(f"Date,{currency},\n{date},{rate},\n", encoding="utf-8")

try:
    code, stdout, stderr = cli_runner("load", str(csv_path))
    assert code == 0
    with db_session() as db:
        row = db.rates.get(date=date, currency=currency)
        assert row is not None
        assert row.rate == rate
finally:
    csv_path.unlink(missing_ok=True)
=== END AC load-stores-published-text ===

=== AC load-rejects-invalid-file-without-writing ===
Intent: A rejected CSV leaves its candidate rate absent.
Suite: scoped

from pathlib import Path
from cli.testing import cli_runner
from persistence.testing import db_session

csv_path = Path("load-invalid.csv")
date = "2099-12-31"
currency = "ZZZ"
invalid_rate = "1x"
csv_path.write_text(f"Date,{currency},\n{date},{invalid_rate},\n", encoding="utf-8")

try:
    code, stdout, stderr = cli_runner("load", str(csv_path))
    assert code == 3
    with db_session() as db:
        assert db.rates.get(date=date, currency=currency) is None
finally:
    csv_path.unlink(missing_ok=True)
=== END AC load-rejects-invalid-file-without-writing ===

=== AC load-is-idempotent ===
Intent: Loading the same valid date and currency pair again preserves its latest stored text.
Suite: scoped

from pathlib import Path
from cli.testing import cli_runner
from persistence.testing import db_session

csv_path = Path("load-repeat.csv")
date = "2099-12-30"
currency = "ZZZ"
rate = "1.234"
csv_path.write_text(f"Date,{currency},\n{date},{rate},\n", encoding="utf-8")

try:
    assert cli_runner("load", str(csv_path))[0] == 0
    assert cli_runner("load", str(csv_path))[0] == 0
    with db_session() as db:
        row = db.rates.get(date=date, currency=currency)
        assert row is not None
        assert row.rate == rate
finally:
    csv_path.unlink(missing_ok=True)
=== END AC load-is-idempotent ===

## User Acceptance

- None.

## Guardrails

- Validate the entire file before its first write; rejected files must leave the store unchanged.
- Preserve rate text exactly and omit `N/A` values.
- Replace already stored `(date, currency)` rates with upserts.
- Access the database only through the generated persistence package.
- Do not read `sources/run.sh` or supplied data files from application code.
