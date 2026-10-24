"""Behavior checks for the CLI and HTTP features."""
import csv
import tempfile
import zipfile
from pathlib import Path
from unittest.mock import patch

from app_server.testing import web_client
from cli.testing import cli_runner
from persistence.testing import committed_session, db_session


def test_init_clears_rates():
    with db_session() as db:
        db.rates.upsert(date="2099-01-01", currency="TST", rate="1.0")
    assert cli_runner("init")[0] == 0
    with db_session() as db:
        assert db.rates.get(date="2099-01-01", currency="TST") is None


def test_load_validates_before_write_and_preserves_text():
    with tempfile.TemporaryDirectory() as folder:
        file = Path(folder) / "rates.csv"
        file.write_text("Date,AAA,\n2099-02-01,1.2300,\n", encoding="utf-8")
        assert cli_runner("load", str(file))[0] == 0
        with db_session() as db:
            assert db.rates.get(date="2099-02-01", currency="AAA").rate == "1.2300"
        file.write_text("Date,AAA,\n2099-02-02,2,\n2099-02-03,0,\n", encoding="utf-8")
        assert cli_runner("load", str(file))[0] == 3
        with db_session() as db:
            assert db.rates.get(date="2099-02-02", currency="AAA") is None


def test_fetch_uses_stubbed_archive():
    with tempfile.TemporaryDirectory() as folder:
        archive = Path(folder) / "input.zip"
        with zipfile.ZipFile(archive, "w") as output:
            output.writestr("eurofxref-hist.csv", "Date,BBB,\n2099-03-01,2.5,\n")
        def stub(destination):
            Path(destination).write_bytes(archive.read_bytes())
        with patch("cli.fetch.download_archive", side_effect=stub):
            assert cli_runner("fetch")[0] == 0
        with db_session() as db:
            assert db.rates.get(date="2099-03-01", currency="BBB").rate == "2.5"


def test_api_stats_currencies_rates_and_conversion():
    with committed_session() as db:
        db.rates.upsert(date="2099-04-01", currency="CCC", rate="2.5")
    client = web_client()
    assert client.get("/health").json() == {"status": "ok"}
    assert "CCC" in client.get("/currencies").json()["currencies"]
    assert client.get("/stats").json()["rates"] >= 1
    assert client.get("/rates/latest").json()["rates"]["CCC"] == "2.5"
    assert client.get("/convert", params={"from": "EUR", "to": "CCC", "amount": "2", "date": "2099-04-01"}).json()["result"] == "5.00"
    client.close()
    with committed_session() as db:
        db.rates.delete(date="2099-04-01", currency="CCC")


def test_api_history_and_validation():
    with committed_session() as db:
        db.rates.upsert(date="2099-05-01", currency="DDD", rate="1")
    client = web_client()
    assert client.get("/history/DDD").json()["count"] >= 1
    assert client.get("/rates/2099-13-01").status_code == 422
    assert client.get("/convert", params={"from": "EUR", "to": "DDD", "amount": "x"}).status_code == 422
    assert client.get("/history/EEE").status_code == 404
    client.close()
    with committed_session() as db:
        db.rates.delete(date="2099-05-01", currency="DDD")
