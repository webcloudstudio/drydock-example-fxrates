# FEATURE: Fetch ECB History

| Field | Value |
|-------|-------|
| Version | 20261025 V1 |
| Description | Fetch and load the ECB reference-rate history archive. |
| Depends On | FEATURE-CliFoundation.md, FEATURE-LoadHistory.md |
| Provides | `fxrates fetch` |
| Consumes | `fxrates load` |

## Purpose

`fxrates fetch` downloads the ECB history ZIP, extracts `eurofxref-hist.csv`, and loads it using the same validation, replacement, reporting, and exit-code behavior as `fxrates load`.

## Workflow

Use Python standard-library download and ZIP facilities. Keep the download replaceable so automated tests can provide archive bytes without network access. Pass the extracted CSV through the shared loader; do not implement a separate parser or persistence path.

A failed download returns exit code `1`, writes no standard output, and emits one diagnostic line to standard error. A successfully fetched file follows the loader’s behavior.

## Programmatic Acceptance

=== AC fetch_entry_point ===
Intent: The fetch command is callable and reports an operational failure when its download fails.

import io
import zipfile
from cli.testing import cli_runner

code, stdout, stderr = cli_runner("fetch")
assert code in (0, 1)
=== END AC fetch_entry_point ===

=== AC fetch_loads_stubbed_archive ===
Intent: Fetch loads a valid ECB archive supplied by a stub without opening a network connection.

import io
import zipfile
from unittest.mock import patch
from cli.testing import cli_runner

csv_data = (
    "Date,ZZZ,\n"
    "2099-01-02,1.2300,\n"
).encode("ascii")
archive = io.BytesIO()
with zipfile.ZipFile(archive, "w") as bundle:
    bundle.writestr("eurofxref-hist.csv", csv_data)
payload = archive.getvalue()

with patch("urllib.request.urlopen") as download:
    download.return_value.__enter__.return_value.read.return_value = payload
    code, stdout, stderr = cli_runner("fetch")

assert code == 0
=== END AC fetch_loads_stubbed_archive ===

## User Acceptance

- None.

## Guardrails

- Use the ECB history ZIP URL and extract `eurofxref-hist.csv`.
- Reuse the shared loader and its validation and reporting behavior.
- Automated tests replace the download with a stub and never use the network.
- Do not read or modify supplied files under `sources/`.
