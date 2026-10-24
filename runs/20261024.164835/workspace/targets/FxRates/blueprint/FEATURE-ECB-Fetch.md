# FEATURE: ECB Fetch

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Downloads the ECB history ZIP and loads its CSV using the standard loader rules. |
| Depends On  | FEATURE-ECB-Load.md |
| Provides    | fxrates fetch |
| Consumes    | fxrates load |

## Purpose

Fetch provides the ECB history ZIP as a command-line workflow. It extracts `eurofxref-hist.csv` and loads it through the same validation, storage, and reporting behavior as `fxrates load`.

## Workflow

1. Download `https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip`.
2. Extract `eurofxref-hist.csv`.
3. Pass the extracted CSV through the loader.
4. Report the loader’s result. Return exit code `1` with a diagnostic on download failure.

Use Python’s standard-library `urllib` for the download. Tests stub the download and make no network connection.

## Programmatic Acceptance

=== AC fetch-loads-stubbed-archive ===
Intent: The fetch command loads the CSV from a stubbed ECB archive and returns success.

import io
import zipfile
from unittest.mock import patch

from cli.testing import cli_runner

csv_data = "Date,ZZZ,\n2099-01-02,0.943,\n"
archive = io.BytesIO()
with zipfile.ZipFile(archive, "w") as bundle:
    bundle.writestr("eurofxref-hist.csv", csv_data)
archive_bytes = archive.getvalue()

class StubResponse:
    def read(self):
        return archive_bytes

with patch("urllib.request.urlopen", return_value=StubResponse()):
    code, stdout, stderr = cli_runner("fetch")
assert code == 0
=== END AC fetch-loads-stubbed-archive ===

=== AC fetch-download-failure ===
Intent: A failed download returns the operational-failure exit code.

from unittest.mock import patch

from cli.testing import cli_runner

with patch("urllib.request.urlopen", side_effect=OSError):
    code, stdout, stderr = cli_runner("fetch")
assert code == 1
=== END AC fetch-download-failure ===

## User Acceptance

- None.

## Guardrails

- Tests replace the download with a stub; tests never use the network.
- Extract and load the archive’s `eurofxref-hist.csv` using the same rules as the file loader.
- Use the standard-library `urllib` download implementation.
