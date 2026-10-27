"""ECB archive fetch behavior, with the network fully stubbed."""

import io
import zipfile
from unittest.mock import patch

from cli.testing import cli_runner
from persistence.testing import db_session


def _archive(csv_text: str) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("eurofxref-hist.csv", csv_text)
    return buffer.getvalue()


class _Response:
    def __init__(self, payload: bytes):
        self.payload = payload

    def read(self) -> bytes:
        return self.payload

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return None


def test_fetch_loads_archive_csv_and_reports_counts() -> None:
    payload = _archive("Date,USD,\n2099-06-01,1.25,\n")
    with patch("urllib.request.urlopen", return_value=_Response(payload)):
        code, stdout, _ = cli_runner("fetch")
    with db_session() as db:
        stored = db.rates.by_date(date="2099-06-01")
    assert code == 0
    assert [line.split(",") for line in stdout.splitlines()] == [["dates", "rates"], ["1", "1"]]
    assert [(row.currency, row.rate) for row in stored] == [("USD", "1.25")]


def test_fetch_download_failure_has_no_stdout_and_fails() -> None:
    with patch("urllib.request.urlopen", side_effect=OSError("offline")):
        code, stdout, stderr = cli_runner("fetch")
    assert code == 1
    assert stdout == ""
    assert stderr
