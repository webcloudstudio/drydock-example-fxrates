from __future__ import annotations
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile
from services.loader import load_text
URL='https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip'
def download_archive() -> bytes:
    with urlopen(URL,timeout=30) as response: return response.read()
def fetch():
    archive=ZipFile(BytesIO(download_archive()))
    return load_text(archive.read('eurofxref-hist.csv').decode('utf-8'))
