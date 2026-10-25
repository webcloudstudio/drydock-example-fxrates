# FEATURE: ECB Fetch

| Field       | Value |
|-------------|-------|
| Version     | 20261025 V1 |
| Description | Downloads the ECB history archive and loads its CSV through the existing load workflow. |
| Depends On  | FEATURE-ECB-Loading.md |
| Provides    | fxrates fetch |
| Consumes    | fxrates load |

## Purpose

Fetch the ECB history archive, extract `eurofxref-hist.csv`, and delegate its contents to the established load workflow.

## Trigger and Sequence

`fxrates fetch` downloads `https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip`, extracts `eurofxref-hist.csv`, and loads it using the same validation, replacement, reporting, and exit-code behavior as `fxrates load`.

A download failure is an operational failure: exit `1`, no standard output, and one diagnostic line on standard error. Tests replace the downloader with a stub; they do not use the network.

## Programmatic Acceptance

=== AC fetch-command ===
Intent: The fetch command is available and reports operational failure when the stubbed downloader fails.

from cli.testing import cli_runner
import cli.fetch as fetch_module

def fail_download():
    raise OSError("stubbed download failure")

fetch_module.download_archive = fail_download
code, stdout, stderr = cli_runner("fetch")
assert code == 1
assert stdout == ""
assert stderr.count("\n") == 1
=== END AC fetch-command ===

=== AC fetch-stubbed-archive-load ===
Intent: A stubbed archive is extracted and passed to the load workflow without network access.

from cli.testing import cli_runner
import cli.fetch as fetch_module
import io
import zipfile
from persistence.testing import db_session

csv_data = "Date,USD,\n2099-01-02,1.2300,\n"
archive = io.BytesIO()
with zipfile.ZipFile(archive, "w") as zipped:
    zipped.writestr("eurofxref-hist.csv", csv_data)
archive_bytes = archive.getvalue()
fetch_module.download_archive = lambda: archive_bytes

with db_session() as db:
    before = len(db.rates.list())
code, stdout, stderr = cli_runner("fetch")
assert code == 0
assert stderr == ""
with db_session() as db:
    rows = db.rates.list(currency="USD")
stored = next(row for row in rows if row.date == "2099-01-02")
assert stored.rate == "1.2300"
=== END AC fetch-stubbed-archive-load ===

## User Acceptance

- None.

## Guardrails

- Tests stub the downloader and never open a network connection.
- Use the existing load workflow so validation, atomicity, replacement, and summary behavior remain consistent.
- Do not modify files under `sources/`.
