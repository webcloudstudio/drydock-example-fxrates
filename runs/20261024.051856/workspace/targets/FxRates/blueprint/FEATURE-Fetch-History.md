# FEATURE: Fetch History

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Fetch the ECB history archive and load its CSV through the shared history loader. |
| Depends On  | FEATURE-Load-History.md, DATABASE.md |
| Provides    | fxrates fetch |
| Consumes    | fxrates load, rates repository operations |

## Purpose

`fxrates fetch` retrieves the ECB history ZIP archive, extracts `eurofxref-hist.csv`, and loads it using the same validation, replacement, storage, and reporting behavior as `fxrates load`.

## Workflow

The download boundary is a callable `download_archive(destination)` in `cli.fetch`. It writes the downloaded archive to the supplied destination. Keep this boundary replaceable so automated tests can provide a local ZIP archive without network access.

The command extracts the named CSV to a temporary location and passes that file to the shared loader. A download failure returns exit code `1`; invalid extracted history follows the loader's rejection behavior.

## Programmatic Acceptance

=== AC fetch-loads-stubbed-archive ===
Intent: Fetch loads an ECB-format CSV from a locally supplied archive without opening a network connection.

import tempfile
import zipfile
from unittest.mock import patch

from cli.testing import cli_runner
from persistence.testing import committed_session

date = "2099-01-07"
currency = "ZZU"
rate = "7.890"

with tempfile.TemporaryDirectory() as directory:
    archive = f"{directory}/history.zip"
    with zipfile.ZipFile(archive, "w") as output:
        output.writestr(
            "eurofxref-hist.csv",
            f"Date,{currency},\n{date},{rate},\n",
        )

    def stub_download(destination):
        with open(archive, "rb") as source, open(destination, "wb") as target:
            target.write(source.read())

    try:
        with patch("cli.fetch.download_archive", side_effect=stub_download):
            code, stdout, stderr = cli_runner("fetch")
        assert code == 0
        with committed_session() as db:
            row = db.rates.get(date=date, currency=currency)
            assert row is not None
            assert row.rate == rate
    finally:
        with committed_session() as db:
            db.rates.delete(date=date, currency=currency)
=== END AC fetch-loads-stubbed-archive ===

=== AC fetch-download-failure ===
Intent: A failed archive download returns the conventional operational failure exit code.

from unittest.mock import patch

from cli.testing import cli_runner

with patch("cli.fetch.download_archive", side_effect=OSError):
    code, stdout, stderr = cli_runner("fetch")
assert code == 1
=== END AC fetch-download-failure ===

## User Acceptance

- None.

## Guardrails

- Automated tests stub the download and never use the network.
- Extract and load the archive's `eurofxref-hist.csv` through the shared history loader.
- Do not access SQLite outside the generated persistence package.
