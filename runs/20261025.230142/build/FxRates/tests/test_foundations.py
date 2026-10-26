from dataclasses import FrozenInstanceError

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app_server.main import app, create_app
from app_server.testing import web_client
from cli import main
from cli.testing import cli_runner
from persistence.testing import db_session


def test_api_factory_and_module_app() -> None:
    assert isinstance(create_app(), FastAPI)
    assert isinstance(app, FastAPI)


def test_api_test_client() -> None:
    client = web_client()
    assert isinstance(client, TestClient)
    client.close()


def test_cli_entry_point_returns_integer() -> None:
    assert isinstance(main(["__foundation_probe__"]), int)


def test_cli_runner_captures_unknown_command() -> None:
    code, stdout, stderr = cli_runner("__foundation_probe__")
    assert code == 2
    assert stdout == ""
    assert "unknown command" in stderr


def test_rates_get_and_upsert_round_trip() -> None:
    with db_session() as db:
        db.rates.upsert(date="2099-01-02", currency="ZZZ", rate="1.2300")
        row = db.rates.get(date="2099-01-02", currency="ZZZ")
        assert (row.date, row.currency, row.rate) == ("2099-01-02", "ZZZ", "1.2300")
        with pytest.raises(FrozenInstanceError):
            row.rate = "2"


def test_rates_list_filters_and_orders() -> None:
    with db_session() as db:
        db.rates.upsert(date="2099-02-02", currency="ZZZ", rate="2.00")
        db.rates.upsert(date="2099-02-01", currency="ZZZ", rate="1.00")
        db.rates.upsert(date="2099-02-01", currency="YYY", rate="8.00")
        rows = db.rates.list(currency="ZZZ", start_date="2099-02-01", end_date="2099-02-02")
        assert [(row.date, row.currency, row.rate) for row in rows] == [
            ("2099-02-01", "ZZZ", "1.00"),
            ("2099-02-02", "ZZZ", "2.00"),
        ]


def test_rates_upsert_replaces_published_text() -> None:
    with db_session() as db:
        db.rates.upsert(date="2099-03-01", currency="ZZZ", rate="1.20")
        db.rates.upsert(date="2099-03-01", currency="ZZZ", rate="1.2000")
        row = db.rates.get(date="2099-03-01", currency="ZZZ")
        assert row.rate == "1.2000"


def test_rates_delete_round_trip() -> None:
    with db_session() as db:
        db.rates.upsert(date="2099-04-01", currency="ZZZ", rate="4.50")
        deleted = db.rates.delete(date="2099-04-01", currency="ZZZ")
        assert (deleted.date, deleted.currency) == ("2099-04-01", "ZZZ")
        assert db.rates.get(date="2099-04-01", currency="ZZZ") is None
