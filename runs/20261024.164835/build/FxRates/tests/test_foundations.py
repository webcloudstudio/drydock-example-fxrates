from pathlib import Path
import os

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app_server.main import app, create_app
from app_server.testing import web_client
from cli import main
from cli.testing import cli_runner


def test_api_factory_and_module_app_are_fastapi_instances():
    assert isinstance(create_app(), FastAPI)
    assert isinstance(app, FastAPI)


def test_web_client_can_call_health_endpoint():
    client = web_client()
    assert isinstance(client, TestClient)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_cli_entry_points_return_a_result_without_spawning():
    assert callable(main)
    assert callable(cli_runner)
    result = cli_runner()
    assert isinstance(result, tuple)
    assert len(result) == 3
    assert result[0] == 2


def test_fxrates_is_executable():
    executable = Path("fxrates")
    assert executable.is_file()
    assert os.access(executable, os.X_OK)
