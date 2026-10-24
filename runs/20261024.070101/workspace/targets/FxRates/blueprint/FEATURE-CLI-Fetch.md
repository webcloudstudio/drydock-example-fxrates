# FEATURE: CLI Fetch

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Downloads and loads the ECB reference history archive with the same rules as the load command. |
| Depends On  | FEATURE-CLI-Load.md |
| Provides    | fxrates fetch |
| Consumes    | fxrates load |

## Workflow

Fetch downloads `https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip` using Python's standard-library HTTPS support, extracts `eurofxref-hist.csv`, and loads it using the same validation, replacement, and reporting rules as `fxrates load`. Tests stub the download and must not use the network. Download failures return exit code 1.

## Programmatic Acceptance

=== AC fetch-loads-stubbed-archive ===
Intent: Fetch loads the CSV supplied by a stubbed archive download without opening a network connection.

import io
import zipfile
from unittest.mock import patch
from cli.testing import cli_runner
from persistence.testing import db_session

csv_bytes = b"Date,USD,\n2099-01-02,1.2300,\n"
archive = io.BytesIO()
with zipfile.ZipFile(archive, "w") as zipped:
    zipped.writestr("eurofxref-hist.csv", csv_bytes)

with patch("urllib.request.urlopen", return_value=io.BytesIO(archive.getvalue())):
    code, out, err = cli_runner("fetch")
assert code == 0

with db_session() as db:
    rows = db.rates.list(date="2099-01-02", currency="USD")
    assert len(rows) == 1
    assert rows[0].rate == "1.2300"
=== END AC fetch-loads-stubbed-archive ===

=== AC fetch-download-failure ===
Intent: A failed stubbed download returns the operational failure exit status.

from unittest.mock import patch
from cli.testing import cli_runner

with patch("urllib.request.urlopen", side_effect=OSError):
    code, out, err = cli_runner("fetch")
assert code == 1
=== END AC fetch-download-failure ===

## User Acceptance

- None.

## Guardrails

- Tests must stub the archive download and make no network connection.
- Extract the named `eurofxref-hist.csv` member and apply the load command's validation rules.
