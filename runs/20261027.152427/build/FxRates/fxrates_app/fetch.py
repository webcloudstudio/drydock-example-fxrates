"""ECB history archive download: the single function in the application that opens a network connection.

`download_archive` returns the bytes of the ECB history zip. The fetch command calls it through this
module attribute, so a test replaces this one seam and never reaches the network.
"""

from __future__ import annotations

import urllib.request

ECB_ARCHIVE_URL = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip"
TIMEOUT_SECONDS = 30.0


def download_archive(url: str) -> bytes:
    """Return the bytes served at `url`. A transport failure or timeout raises OSError."""
    with urllib.request.urlopen(url, timeout=TIMEOUT_SECONDS) as response:
        return response.read()
