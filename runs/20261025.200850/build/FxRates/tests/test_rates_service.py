import csv, os
from fastapi.testclient import TestClient
from app_server.main import create_app
from cli.testing import cli_runner

def client_for(tmp_path, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", str(tmp_path / "rates.db"))
    code, _, _ = cli_runner("init")
    assert code == 0
    return TestClient(create_app())

def test_load_and_api_roundtrip(tmp_path, monkeypatch):
    client=client_for(tmp_path,monkeypatch)
    path=tmp_path/"history.csv"
    path.write_text("Date,USD,GBP,\n2025-01-02,2,1,\n2025-01-03,4,3,\n")
    assert cli_runner("load",str(path))[0] == 0
    assert client.get("/stats").json() == {"dates":2,"rates":4,"first":"2025-01-02","last":"2025-01-03"}
    assert client.get("/rates/2025-01-04").json()["date"] == "2025-01-03"
    assert client.get("/convert",params={"from":"USD","to":"GBP","amount":"2","date":"2025-01-02"}).json()["result"] == "1.00"

def test_invalid_load_is_atomic(tmp_path, monkeypatch):
    client=client_for(tmp_path,monkeypatch)
    path=tmp_path/"bad.csv"
    path.write_text("Date,USD,\n2025-01-02,2,\n2025-01-03,1x,\n")
    assert cli_runner("load",str(path))[0] == 3
    assert client.get("/stats").json()["rates"] == 0

def test_history_and_validation(tmp_path, monkeypatch):
    client=client_for(tmp_path,monkeypatch)
    path=tmp_path/"one.csv"; path.write_text("Date,USD,\n2025-01-02,1.0,\n")
    assert cli_runner("load",str(path))[0] == 0
    body=client.get("/history/USD").json()
    assert body["mean"] == "1.000000" and body["points"] == [{"date":"2025-01-02","rate":"1.0"}]
    assert client.get("/rates/2025-13-01").status_code == 422
    assert client.get("/history/XXX").status_code == 404
