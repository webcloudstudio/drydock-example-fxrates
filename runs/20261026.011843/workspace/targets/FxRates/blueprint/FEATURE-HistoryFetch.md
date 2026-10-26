# FEATURE: ECB History Fetch

| Field       | Value |
|-------------|-------|
| Version     | 20261026 V1 |
| Description | Downloads the ECB history archive and loads its CSV through the shared loader. |
| Depends On  | ARCHITECTURE.md, FEATURE-HistoryLoading.md |
| Provides    | `fxrates fetch` |
| Consumes    | `fxrates load` |

## Purpose

Provide an operator command that downloads and loads the ECB euro reference-rate history archive.

## Trigger and workflow

`fxrates fetch` downloads `https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip`, extracts `eurofxref-hist.csv`, and applies the same validation, persistence, and reporting behavior as `fxrates load`. Download failure is operational failure with exit code 1.

Tests must replace the download operation with a stub and must never use a network connection.

## Database Interface

- None — persistence is owned by DATABASE.md.

## Programmatic Acceptance

=== AC fetch-stubbed ===
Intent: The fetch command loads a ZIP archive supplied by a stub without accessing the network.

from cli.testing import cli_runner
from unittest.mock import patch
from io import BytesIO
from zipfile import ZipFile
from persistence.testing import db_session

csv_data = b"Date,ZZZ,\n2097-01-02,1.25,\n"
archive = BytesIO()
with ZipFile(archive, "w") as bundle:
    bundle.writestr("eurofxref-hist.csv", csv_data)

with patch("services.fetch.download_archive", return_value=archive.getvalue()):
    code, stdout, stderr = cli_runner("fetch")
assert code == 0
with db_session() as db:
    rows = db.rates.by_date(date="2097-01-02")
    assert any(row.currency == "ZZZ" and row.rate == "1.25" for row in rows)
=== END AC fetch-stubbed ===

=== AC fetch-operational-error ===
Intent: A failed archive download returns the operational failure exit code.

from cli.testing import cli_runner
from unittest.mock import patch

with patch("services.fetch.download_archive", side_effect=OSError()):
    code, _, _ = cli_runner("fetch")
assert code == 1
=== END AC fetch-operational-error ===

## User Acceptance

- None.

## Guardrails

- Never connect to the network in automated tests; replace the download with a stub.
- Feed the extracted CSV through the shared history loader so validation and reporting remain consistent.
- Do not open SQLite directly; use the declared persistence library through application services.
