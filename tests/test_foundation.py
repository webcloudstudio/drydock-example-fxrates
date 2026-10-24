from app_server.main import create_app
from app_server.testing import web_client
from cli import main
from cli.testing import cli_runner


def test_application_factory_and_cli_are_importable():
    assert create_app() is not None
    assert callable(main)


def test_health_route_returns_ok():
    response = web_client().get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_invalid_cli_invocation_returns_usage_status():
    exit_code, stdout, stderr = cli_runner("unknown-command")
    assert isinstance(exit_code, int)
    assert exit_code == 2
    assert stdout == ""
    assert stderr != ""


def test_database_configuration_precedence():
    from rates.config import database_dsn

    assert database_dsn({}) == "data/app.db"
    assert database_dsn({"DATABASE_PATH": "path.db"}) == "path.db"
    assert database_dsn({"DATABASE_URL": "sqlite:///url.db", "DATABASE_PATH": "path.db"}) == "sqlite:///url.db"

