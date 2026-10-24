# FEATURE: Rate Fetch

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Downloads and loads the ECB history archive through the shared CSV loader. |
| Depends On  | FEATURE-Rate-Loading.md, ARCHITECTURE.md |
| Provides    | fxrates fetch |
| Consumes    | fxrates.load |

## Purpose

Fetch the ECB history ZIP archive and load its `eurofxref-hist.csv` file using the same validation, atomicity, persistence, and reporting behavior as `fxrates load`.

## Trigger and Workflow

`fxrates fetch` downloads `https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip`, extracts the archive member named `eurofxref-hist.csv`, and passes that CSV to the shared loader. A download or unusable archive is an operational failure with exit code 1. Invalid CSV follows the loader's rejected-file behavior and exit code 3. The downloader is replaceable in tests; automated tests use a stub and make no network connection.

## Database Interface

- None — persistence is owned by FEATURE-Rate-Loading.md.

## Programmatic Acceptance

=== AC fetch-stubbed ===
Intent: Fetch loads the CSV returned by the replaceable downloader without opening a network connection.

from io import BytesIO
from unittest.mock import patch
from cli.testing import cli_runner
from persistence.testing import db_session

csv_bytes = b"Date,USD,\n2099-01-05,1.234,\n"
with patch("rate_fetch.download_archive", return_value=csv_bytes):
    code, _, _ = cli_runner("fetch")
assert code == 0

with db_session() as db:
    rows = db.rates.list(date="2099-01-05", currency="USD")
    assert len(rows) == 1
    assert rows[0].rate == "1.234"
=== END AC fetch-stubbed ===

=== AC fetch-invalid-payload ===
Intent: Fetch sends downloaded content through the shared validator and reports a rejected CSV by exit status.
Requires: python-package=httpx; scope=test

from unittest.mock import patch
from cli.testing import cli_runner

bad_csv = b"Date,USD,\n2099-01-05,0,\n"
with patch("rate_fetch.download_archive", return_value=bad_csv):
    code, _, _ = cli_runner("fetch")
assert code == 3
=== END AC fetch-invalid-payload ===

## User Acceptance

- None.

## Guardrails

- Automated tests must not open a network connection.
- Extract only the expected CSV archive member and delegate validation and persistence to the shared loader.
