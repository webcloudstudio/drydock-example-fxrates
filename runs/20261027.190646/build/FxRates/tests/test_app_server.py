"""Behavior tests for the app_server factory, module-level app, test client and startup behavior."""

from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app_server.main import app, create_app
from app_server.testing import web_client
from config import DATABASE_PATH_ENV, DATABASE_URL_ENV


@pytest.fixture
def unconfigured_database(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    """Run in an empty directory with no database variables, so the default location is what would be used."""
    monkeypatch.delenv(DATABASE_URL_ENV, raising=False)
    monkeypatch.delenv(DATABASE_PATH_ENV, raising=False)
    monkeypatch.chdir(tmp_path)
    return tmp_path


def test_create_app_returns_a_fastapi_application() -> None:
    assert isinstance(create_app(), FastAPI)


def test_create_app_returns_a_new_application_each_call() -> None:
    assert create_app() is not create_app()


def test_module_level_app_is_a_fastapi_application() -> None:
    assert isinstance(app, FastAPI)


def test_web_client_returns_a_test_client_over_a_fastapi_application() -> None:
    client = web_client()

    assert isinstance(client, TestClient)
    assert isinstance(client.app, FastAPI)


def test_unknown_path_answers_not_found() -> None:
    response = web_client().get("/zz-no-such-route-probe")

    assert response.status_code == 404


def test_pytest_web_client_fixture_serves_requests(web_client) -> None:
    assert web_client.get("/zz-no-such-route-probe").status_code == 404


def test_starting_the_application_does_not_create_the_default_store(unconfigured_database: Path) -> None:
    with TestClient(create_app()) as client:
        assert client.get("/zz-no-such-route-probe").status_code == 404

    assert not (unconfigured_database / "data" / "app.db").exists()


def test_building_the_application_does_not_create_the_default_store(unconfigured_database: Path) -> None:
    create_app()

    assert not (unconfigured_database / "data" / "app.db").exists()
