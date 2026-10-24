# FEATURE: CLI Fetch

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Downloads and loads the ECB reference history archive. |
| Depends On  | DATABASE.md, ARCHITECTURE.md, FEATURE-CLI-Load.md |
| Provides    | fxrates fetch |
| Consumes    | fxrates load |

## Purpose

`fxrates fetch` downloads the ECB history ZIP, extracts `eurofxref-hist.csv`, and processes it using the same complete-file validation and atomic loading behavior as `fxrates load`.

## Workflow

Download from the ECB history archive URL, extract the named CSV, and pass the extracted content through the shared loader. Successful output follows the load command contract. Download or extraction failures return operational status 1 and produce no standard output.

Tests replace the download operation with a stub; the test suite does not open a network connection.

## Programmatic Acceptance

=== AC fetch-success-stubbed ===
Intent: Fetch loads CSV content provided by a stubbed downloader without network access.

from cli import fetcher
from cli.testing import cli_runner
from persistence.testing import db_session

date = "2099-01-05"
currency = "ZZZ"
published = "1.7"
csv_text = f"Date,{currency},\n{date},{published},\n"
fetcher.download = lambda url: csv_text
code, _, _ = cli_runner("fetch")
assert code == 0
with db_session() as db:
    rows = db.rates.list_date(date=date)
    assert any(row.currency == currency and row.rate == published for row in rows)
=== END AC fetch-success-stubbed ===

=== AC fetch-failure ===
Intent: A download failure returns operational failure and no standard output.

from cli import fetcher
from cli.testing import cli_runner

def fail_download(url):
    raise OSError("offline")

fetcher.download = fail_download
code, out, _ = cli_runner("fetch")
assert code == 1
assert out == ""
=== END AC fetch-failure ===

## User Acceptance

- None.

## Guardrails

- Keep tests network-free by stubbing the downloader.
- Reuse the loader's validation and persistence behavior.
- Do not alter the ECB URL or read supplied grader assets.
