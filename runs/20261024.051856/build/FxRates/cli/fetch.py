"""ECB archive download boundary and command workflow."""
from __future__ import annotations

import tempfile
import urllib.request
import zipfile
from pathlib import Path

ARCHIVE_URL = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip"


def download_archive(destination: str) -> None:
    urllib.request.urlretrieve(ARCHIVE_URL, destination)


def fetch(loader) -> int:
    try:
        with tempfile.TemporaryDirectory() as directory:
            archive = str(Path(directory) / "history.zip")
            download_archive(archive)
            with zipfile.ZipFile(archive) as zipped:
                member = next(name for name in zipped.namelist() if name.rsplit("/", 1)[-1] == "eurofxref-hist.csv")
                csv_path = str(Path(directory) / "history.csv")
                with zipped.open(member) as src, open(csv_path, "wb") as dst:
                    dst.write(src.read())
            dates, rates = loader(csv_path)
        print("dates,rates")
        print(f"{dates},{rates}")
        return 0
    except Exception as exc:
        from services import InvalidHistory
        print(f"error: {exc}", file=__import__("sys").stderr)
        return 3 if isinstance(exc, InvalidHistory) else 1
