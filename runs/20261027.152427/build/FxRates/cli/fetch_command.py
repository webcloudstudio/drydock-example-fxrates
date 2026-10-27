"""The `fetch` command: download the ECB history archive, extract its CSV, and load it as `load` does.

The download is `fxrates_app.fetch.download_archive`, the single network call. It is looked up through
its module at call time so tests replace that one seam. A failed download, bytes that are not a zip,
or an archive without `eurofxref-hist.csv` exits 1 before any parsing. The extracted text then goes
through the same `parse_history` validation and `store_and_report` path as `load`, so a rejected
member exits 3 and stores nothing.
"""

from __future__ import annotations

import http.client
import io
import sys
import zipfile
import zlib

from cli.dispatcher import register_command
from cli.help import print_help
from cli.load_command import store_and_report
from fxrates_app import fetch
from fxrates_app.ecb import RejectedFile, parse_history

OPERATIONAL_FAILURE = 1
REJECTED = 3
HELP_FLAG = "--help"
MEMBER_NAME = "eurofxref-hist.csv"


def fetch_history(rest: list[str]) -> int:
    """Download, extract, validate, and store the ECB history; return the exit code."""
    if rest == [HELP_FLAG]:
        return print_help("fetch")
    try:
        archive = fetch.download_archive(fetch.ECB_ARCHIVE_URL)
    except (OSError, http.client.HTTPException) as error:
        print(f"error: cannot download {fetch.ECB_ARCHIVE_URL}: {error}", file=sys.stderr)
        return OPERATIONAL_FAILURE
    try:
        with zipfile.ZipFile(io.BytesIO(archive)) as zipped:
            text = zipped.read(MEMBER_NAME).decode("utf-8")
    except (zipfile.BadZipFile, KeyError, UnicodeDecodeError, zlib.error) as error:
        print(f"error: cannot read {MEMBER_NAME} from the archive: {error}", file=sys.stderr)
        return OPERATIONAL_FAILURE
    try:
        rates = parse_history(text)
    except RejectedFile as error:
        print(f"error: {error}", file=sys.stderr)
        return REJECTED

    return store_and_report(rates)


register_command("fetch", fetch_history)
