"""Deterministic tests for the declared CLI and HTTP foundation contracts."""

from fastapi import FastAPI
from fastapi.testclient import TestClient


def test_application_factory_and_module_app() -> None:
    from app_server.main import app, create_app

    assert isinstance(create_app(), FastAPI)
    assert isinstance(app, FastAPI)


def test_web_client_uses_application_factory() -> None:
    from app_server.testing import web_client

    client = web_client()
    assert isinstance(client, TestClient)
    assert client.get("/health").status_code in (200, 404)


def test_cli_unknown_command_returns_usage_error() -> None:
    from cli import main

    assert callable(main)
    assert main(["frobnicate"]) == 2


def test_cli_runner_returns_error_code_and_streams() -> None:
    from cli.testing import cli_runner

    result = cli_runner("load")
    assert isinstance(result, tuple)
    assert len(result) == 3
    assert result[0] == 2


def test_declared_commands_parse_and_reach_dispatch(monkeypatch) -> None:
    from cli.testing import cli_runner
    import cli.fetch

    monkeypatch.setattr(cli.fetch, "download_archive", lambda: (_ for _ in ()).throw(OSError("stub")))
    assert cli_runner("init")[0] == 0
    assert cli_runner("fetch")[0] == 1
    assert cli_runner("load", "rates.csv")[0] == 1


def test_root_executable_exists() -> None:
    from pathlib import Path

    assert Path("fxrates").is_file()
