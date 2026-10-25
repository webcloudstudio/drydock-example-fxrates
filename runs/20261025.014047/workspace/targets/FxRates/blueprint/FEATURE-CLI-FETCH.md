# FEATURE: CLI Fetch

| Field       | Value |
|-------------|-------|
| Version     | 20261025 V1 |
| Description | Downloads and loads the ECB euro reference history archive. |
| Depends On  | FEATURE-CLI-LOAD.md, ARCHITECTURE.md |
| Provides    | `fxrates fetch` |
| Consumes    | `fxrates load` |

## Purpose

Download the ECB history ZIP archive, extract `eurofxref-hist.csv`, and load it using the same validation, storage, and summary behavior as `fxrates load`.

## Workflow

1. Download `https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip`.
2. Extract the `eurofxref-hist.csv` member.
3. Pass the extracted CSV through the shared loader.
4. Return exit status `0` on success or `1` if the download fails. A rejected extracted CSV follows the loader's rejected-file behavior.

Automated tests replace the download with a stub and must not open a network connection.

## Programmatic Acceptance

=== AC fetch-loads-stubbed-archive ===
Intent: The fetch command loads the CSV supplied by a stubbed download.
Suite: scoped

from io import BytesIO
from zipfile import ZipFile
from unittest.mock import patch
from cli.testing import cli_runner
from persistence.testing import db_session

date = "2099-12-30"
currency = "ZZZ"
rate = "1.234"
archive_buffer = BytesIO()
with ZipFile(archive_buffer, "w") as archive:
    archive.writestr("eurofxref-hist.csv", f"Date,{currency},\n{date},{rate},\n")
archive_bytes = archive_buffer.getvalue()

with patch("cli.fetch.urlopen") as urlopen:
    urlopen.return_value.__enter__.return_value.read.return_value = archive_bytes
    code, stdout, stderr = cli_runner("fetch")
    assert code == 0

with db_session() as db:
    row = db.rates.get(date=date, currency=currency)
    assert row is not None
    assert row.rate == rate
=== END AC fetch-loads-stubbed-archive ===

=== AC fetch-download-failure ===
Intent: A failed download returns the operational failure status.
Suite: scoped

from unittest.mock import patch
from cli.testing import cli_runner

with patch("cli.fetch.urlopen", side_effect=OSError):
    code, stdout, stderr = cli_runner("fetch")
assert code == 1
=== END AC fetch-download-failure ===

## User Acceptance

- None.

## Guardrails

- Route archive contents through the same complete-file validation and load path as `fxrates load`.
- Fetch tests must stub the download and must not open a network connection.
