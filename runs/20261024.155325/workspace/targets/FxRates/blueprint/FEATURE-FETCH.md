# FEATURE: Fetch ECB History

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Downloads, extracts, and loads ECB euro reference rate history. |
| Depends On  | FEATURE-CLI.md, FEATURE-LOAD.md |
| Provides    | fxrates fetch |
| Consumes    | fxrates load |

## Purpose

`fxrates fetch` downloads the ECB history ZIP, extracts `eurofxref-hist.csv`, and loads it using the same validation, storage, reporting, and exit-code behavior as `fxrates load`.

## Workflow

The command retrieves `https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip`, extracts the named CSV, and passes its contents through the load workflow. Tests stub the download and make no network connection.

A download failure is an operational failure: exit status `1`, no standard output, and one diagnostic line on standard error.

## Programmatic Acceptance

=== AC fetch-download-failure ===
Intent: A failed ECB download returns the operational failure signal with empty standard output and one diagnostic line on standard error.

import io
import urllib.request
from unittest.mock import patch
from cli.testing import cli_runner

with patch.object(urllib.request, "urlopen", side_effect=OSError()):
    code, stdout, stderr = cli_runner("fetch")
assert code == 1
assert stdout == ""
assert len(stderr.splitlines()) == 1
=== END AC fetch-download-failure ===

=== AC fetch-reuses-loader ===
Intent: Fetch accepts an ECB archive supplied by a stub and stores the extracted published rate text.

import csv
import io
import tempfile
import urllib.request
import zipfile
from unittest.mock import patch
from cli.testing import cli_runner
from persistence.testing import db_session

date = "2099-02-01"
currency = "TST"
rate = "1.2300"
csv_text = f"Date,{currency},\n{date},{rate},\n"
archive = io.BytesIO()
with zipfile.ZipFile(archive, "w") as zipped:
    zipped.writestr("eurofxref-hist.csv", csv_text)
response = io.BytesIO(archive.getvalue())
response.status = 200
response.getcode = lambda: 200
with patch.object(urllib.request, "urlopen", return_value=response):
    code, stdout, stderr = cli_runner("fetch")
assert code == 0
with db_session() as db:
    stored = db.rates.get(date=date, currency=currency)
    assert stored is not None
    assert stored.rate == rate
=== END AC fetch-reuses-loader ===

## User Acceptance

- None.

## Guardrails

- Fetch tests stub the download and never use the network.
- Extract only the archive member named `eurofxref-hist.csv`; validate and load it through the same behavior as `fxrates load`.
