"""ECB archive downloader, replaceable in tests."""
from urllib.request import urlopen

URL = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip"

def download_archive() -> bytes:
    with urlopen(URL, timeout=30) as response:
        return response.read()
