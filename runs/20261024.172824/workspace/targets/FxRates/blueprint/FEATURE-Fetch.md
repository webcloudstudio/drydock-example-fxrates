# FEATURE: Fetch ECB History

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Downloads the ECB history archive and loads its CSV through the validated load workflow. |
| Depends On  | ARCHITECTURE.md, DATABASE.md, FEATURE-Load.md |
| Provides    | fxrates fetch |
| Consumes    | fxrates load, rates.upsert |

## Purpose

Fetch the ECB history archive, extract `eurofxref-hist.csv`, and load its data under the same validation, atomicity, storage, and counting rules as `fxrates load`.

## Trigger and workflow

`./fxrates fetch` downloads `https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip`, extracts the member named `eurofxref-hist.csv`, and processes it using the load workflow. Do not depend on the process working directory for extraction paths. A download failure is an operational failure with exit code `1`, no stdout, and one diagnostic line on stderr. A downloaded but invalid CSV follows the rejected-file behavior and returns exit code `3`.

## Programmatic Acceptance

=== AC fetch-download-is-stubbed ===
Intent: The fetch command loads a valid archive member using a stubbed download without opening a network connection.

from pathlib import Path
from unittest.mock import patch
from zipfile import ZipFile
import io

from cli.testing import cli_runner
from persistence.testing import db_session

source = Path("sources/eurofxref-hist_2025-02-03_04.csv").read_bytes()
archive_buffer = io.BytesIO()
with ZipFile(archive_buffer, "w") as archive:
    archive.writestr("eurofxref-hist.csv", source)
archive_bytes = archive_buffer.getvalue()

with patch("urllib.request.urlopen") as download:
    download.return_value.__enter__.return_value.read.return_value = archive_bytes
    code, stdout, stderr = cli_runner("fetch")
assert code == 0
with db_session() as db:
    first = db.rates.get(date="2025-02-03", currency="USD")
    second = db.rates.get(date="2025-02-04", currency="USD")
    assert first is not None and second is not None
    assert first.rate == "1.0274"
    assert second.rate == "1.0335"
=== END AC fetch-download-is-stubbed ===

=== AC fetch-rejects-download-error ===
Intent: A failed download returns the operational failure exit status.

from unittest.mock import patch

from cli.testing import cli_runner

with patch("urllib.request.urlopen", side_effect=OSError("offline")):
    code, stdout, stderr = cli_runner("fetch")
assert code == 1
=== END AC fetch-rejects-download-error ===

## User Acceptance

- None.

## Guardrails

- Download only the specified ECB archive URL.
- Automated tests replace the download with a stub and never use the network.
- Extract and process only the archive member `eurofxref-hist.csv`.
- Reuse the validated load behavior; do not create a separate parsing or persistence path.
- Keep rates in their published text form.
