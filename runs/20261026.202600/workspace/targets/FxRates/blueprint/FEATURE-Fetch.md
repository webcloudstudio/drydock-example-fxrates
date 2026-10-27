# FEATURE: ECB History Fetch

| Field       | Value |
|-------------|-------|
| Version     | 20261026 V1 |
| Description | Downloads and extracts the ECB history archive before loading its CSV through the shared loader. |
| Depends On  | FEATURE-Load.md |

## Purpose

`./fxrates fetch` downloads `https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip`, extracts `eurofxref-hist.csv`, and passes that file through the same validation, persistence, and reporting workflow as `./fxrates load`.

A download failure returns status 1, writes no standard output, and emits a diagnostic to standard error. Automated tests replace the download with a stub and do not access the network.

## Programmatic Acceptance

=== AC fetch-stubbed-success ===
Intent: Fetch loads the CSV from a stubbed ECB archive and reports its fixture-derived counts.
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

import csv
import io
import urllib.request
import zipfile
from unittest.mock import patch
from cli.testing import cli_runner
from persistence.testing import db_session

buffer = io.BytesIO()
with zipfile.ZipFile(buffer, "w") as archive:
    archive.writestr("eurofxref-hist.csv", "Date,USD,\n2099-06-01,1.25,\n")
payload = buffer.getvalue()

class Response:
    def read(self):
        return payload
    def __enter__(self):
        return self
    def __exit__(self, *args):
        return None

with patch("urllib.request.urlopen", return_value=Response()):
    code, stdout, stderr = cli_runner("fetch")

rows = list(csv.reader(stdout.splitlines()))
with db_session() as db:
    stored = db.rates.by_date(date="2099-06-01")
assert code == 0
assert rows[0] == ["dates", "rates"]
assert rows[1] == ["1", "1"]
assert len(stored) == 1
assert stored[0].currency == "USD"
assert stored[0].rate == "1.25"
=== END AC fetch-stubbed-success ===

=== AC fetch-stubbed-failure ===
Intent: A failed stubbed download returns the operational failure status without standard output.
from unittest.mock import patch
from cli.testing import cli_runner

with patch("urllib.request.urlopen", side_effect=OSError("offline")):
    code, stdout, stderr = cli_runner("fetch")

assert code == 1
assert stdout == ""
=== END AC fetch-stubbed-failure ===

## User Acceptance

- None.

## Guardrails

- Extract the `eurofxref-hist.csv` member and use the shared loader's validation and reporting behavior.
- Never make network requests in automated tests; replace the download operation with a stub.
- On download failure, return status 1 and write no standard output.
