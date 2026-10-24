"""Behavior tests for the configuration boundary."""

import config


def test_database_url_takes_precedence_over_database_path(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///first.db")
    monkeypatch.setenv("DATABASE_PATH", "second.db")

    assert config.database_dsn() == "sqlite:///first.db"


def test_database_path_is_used_without_database_url(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setenv("DATABASE_PATH", "second.db")

    assert config.database_dsn() == "second.db"


def test_default_database_path_is_used_when_environment_is_unset(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("DATABASE_PATH", raising=False)

    assert config.database_dsn() == "data/app.db"


def test_settings_are_an_immutable_typed_snapshot(monkeypatch):
    monkeypatch.setenv("DATABASE_PATH", "snapshot.db")
    resolved = config.settings()
    monkeypatch.setenv("DATABASE_PATH", "later.db")

    assert resolved.database_dsn == "snapshot.db"
