"""Deterministic checks for the database and application foundation contracts."""

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app_server.main import app, create_app
from app_server.testing import web_client
from cli import main
from cli.testing import cli_runner
from config import Config
from persistence import SCHEMA, UnknownOperation
from persistence.testing import db_session


def test_rates_schema_declares_all_operations() -> None:
    assert [operation.name for operation in SCHEMA.operations] == [
        "get", "list", "upsert", "delete"
    ]
    assert SCHEMA.tables[0].name == "rates"


def test_rate_upsert_reads_back_exact_text_and_is_idempotent() -> None:
    with db_session() as db:
        first = db.rates.upsert(date="2099-04-01", currency="TST", rate="1.2300")
        second = db.rates.upsert(date="2099-04-01", currency="TST", rate="1.2300")
        assert first is not None and second is not None
        assert second.rate == "1.2300"
        assert db.rates.get(date=second.date, currency=second.currency) == second


def test_rate_list_accepts_absent_and_present_optional_filters() -> None:
    with db_session() as db:
        row = db.rates.upsert(date="2099-04-02", currency="TSU", rate="2.5")
        assert row is not None
        assert row in db.rates.list(date=row.date)
        assert row in db.rates.list(currency=row.currency)
        assert row in db.rates.list()


def test_rate_get_and_list_cover_empty_and_many_results() -> None:
    with db_session() as db:
        assert db.rates.get(date="2099-04-10", currency="TSA") is None
        assert db.rates.list(date="2099-04-10") == []
        one = db.rates.upsert(date="2099-04-10", currency="TSA", rate="1")
        two = db.rates.upsert(date="2099-04-10", currency="TSB", rate="2")
        assert one is not None and two is not None
        assert len(db.rates.list(date="2099-04-10")) == 2


def test_undeclared_rate_operation_is_rejected() -> None:
    with db_session() as db:
        try:
            db.rates.reprice(rate="1")
        except UnknownOperation:
            pass
        else:
            raise AssertionError("undeclared operation was allowed")


def test_rate_delete_returns_key_and_removes_only_match() -> None:
    with db_session() as db:
        row = db.rates.upsert(date="2099-04-03", currency="TSV", rate="3.5")
        assert row is not None
        deleted = db.rates.delete(date=row.date, currency=row.currency)
        assert deleted is not None
        assert (deleted.date, deleted.currency) == (row.date, row.currency)
        assert db.rates.get(date=row.date, currency=row.currency) is None


def test_app_factory_and_module_instance_are_fastapi() -> None:
    assert isinstance(create_app(), FastAPI)
    assert isinstance(app, FastAPI)


def test_web_client_uses_application_factory() -> None:
    client = web_client()
    assert isinstance(client, TestClient)
    assert client.get("/health").status_code in (200, 404)
    client.close()


def test_cli_entry_and_runner_return_codes_and_streams() -> None:
    assert isinstance(main([]), int)
    code, stdout, stderr = cli_runner()
    assert code == 2
    assert stdout == ""
    assert stderr


def test_cli_help_is_a_usage_path() -> None:
    code, stdout, _ = cli_runner("--help")
    assert code == 0
    assert "serve" in stdout


def test_database_configuration_precedence(monkeypatch) -> None:
    monkeypatch.setenv("DATABASE_PATH", "fallback.db")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///preferred.db")
    assert Config.load().database_url == "sqlite:///preferred.db"
    monkeypatch.delenv("DATABASE_URL")
    assert Config.load().database_url == "fallback.db"


def test_database_configuration_default(monkeypatch) -> None:
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("DATABASE_PATH", raising=False)
    assert Config.load().database_url == "data/app.db"
