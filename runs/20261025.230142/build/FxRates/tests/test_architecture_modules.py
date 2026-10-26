"""Import contract for the application module boundaries."""

import importlib


def test_architecture_modules_import() -> None:
    cli = importlib.import_module("cli")
    app_server = importlib.import_module("app_server.main")
    persistence = importlib.import_module("persistence")

    assert callable(cli.main)
    assert callable(app_server.create_app)
    assert app_server.app is not None
    assert callable(persistence.open_database)


def test_database_setting_precedence(monkeypatch) -> None:
    from config import get_settings

    monkeypatch.setenv("DATABASE_URL", "sqlite:///primary.db")
    monkeypatch.setenv("DATABASE_PATH", "fallback.db")
    assert get_settings().database_url == "sqlite:///primary.db"

    monkeypatch.delenv("DATABASE_URL")
    assert get_settings().database_url == "fallback.db"


def test_default_database_setting(monkeypatch) -> None:
    from config import get_settings

    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("DATABASE_PATH", raising=False)
    assert get_settings().database_url == "data/app.db"
