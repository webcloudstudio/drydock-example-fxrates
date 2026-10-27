"""Behavior tests for database location resolution in config.database_path()."""

from pathlib import Path

import pytest

from config import DATABASE_PATH_ENV, DATABASE_URL_ENV, database_path


@pytest.fixture(autouse=True)
def clean_database_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """Start every test with both database variables unset."""
    monkeypatch.delenv(DATABASE_URL_ENV, raising=False)
    monkeypatch.delenv(DATABASE_PATH_ENV, raising=False)


def test_default_is_data_app_db_when_nothing_is_set() -> None:
    assert database_path() == Path("data/app.db")


def test_default_is_used_when_both_variables_are_empty(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(DATABASE_URL_ENV, "")
    monkeypatch.setenv(DATABASE_PATH_ENV, "")

    assert database_path() == Path("data/app.db")


def test_database_url_with_sqlite_prefix_is_stripped(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(DATABASE_URL_ENV, "sqlite://primary.db")

    assert database_path() == Path("primary.db")


def test_database_url_without_prefix_is_used_as_is(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(DATABASE_URL_ENV, "plain.db")

    assert database_path() == Path("plain.db")


def test_database_url_takes_precedence_over_database_path(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(DATABASE_URL_ENV, "sqlite://primary.db")
    monkeypatch.setenv(DATABASE_PATH_ENV, "fallback.db")

    assert database_path() == Path("primary.db")


def test_database_path_is_used_when_url_is_unset(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(DATABASE_PATH_ENV, "fallback.db")

    assert database_path() == Path("fallback.db")


def test_database_path_is_used_when_url_is_empty(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(DATABASE_URL_ENV, "")
    monkeypatch.setenv(DATABASE_PATH_ENV, "fallback.db")

    assert database_path() == Path("fallback.db")


def test_database_path_is_used_when_url_is_only_the_prefix(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(DATABASE_URL_ENV, "sqlite://")
    monkeypatch.setenv(DATABASE_PATH_ENV, "fallback.db")

    assert database_path() == Path("fallback.db")


def test_absolute_database_url_keeps_its_absolute_path(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(DATABASE_URL_ENV, "sqlite:///var/lib/fxrates/app.db")

    assert database_path() == Path("/var/lib/fxrates/app.db")


def test_environment_is_read_on_every_call(monkeypatch: pytest.MonkeyPatch) -> None:
    assert database_path() == Path("data/app.db")

    monkeypatch.setenv(DATABASE_PATH_ENV, "changed.db")
    assert database_path() == Path("changed.db")

    monkeypatch.setenv(DATABASE_URL_ENV, "sqlite://now-url.db")
    assert database_path() == Path("now-url.db")
