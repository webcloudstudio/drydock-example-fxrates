"""Deterministic checks for the database and application foundation contracts."""

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app_server.main import app, create_app
from app_server.testing import web_client
from cli import main
from cli.testing import cli_runner


def test_app_factory_and_test_client_contract() -> None:
    created = create_app()
    client = web_client()
    assert isinstance(created, FastAPI)
    assert isinstance(app, FastAPI)
    assert isinstance(client, TestClient)
    assert isinstance(client.app, FastAPI)
    assert client.get("/openapi.json").status_code == 200
    client.close()


def test_cli_interfaces_and_no_command_usage_error() -> None:
    assert callable(main)
    result = cli_runner()
    assert isinstance(result, tuple) and len(result) == 3
    assert result[0] == 2
    assert result[1] == ""
    assert result[2]


def test_cli_missing_load_path_is_usage_error() -> None:
    code, out, err = cli_runner("load")
    assert code == 2
    assert out == ""
    assert err
