"""Database selection: DATABASE_URL, then DATABASE_PATH, then data/app.db.

Each test sets its own environment with monkeypatch, so no test depends on the caller's variables.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from fxrates_app import config
from fxrates_app.config import database_path, open_store
from persistence import Database


@pytest.fixture(autouse=True)
def clean_database_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("DATABASE_PATH", raising=False)


def test_database_url_wins_over_database_path(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "sqlite://primary.db")
    monkeypatch.setenv("DATABASE_PATH", "fallback.db")

    assert database_path() == "primary.db"


def test_database_url_without_prefix_is_used_as_is(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "plain.db")
    monkeypatch.setenv("DATABASE_PATH", "fallback.db")

    assert database_path() == "plain.db"


def test_sqlite_prefix_keeps_an_absolute_path(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    target = tmp_path / "absolute.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite://{target}")

    assert database_path() == str(target)


def test_database_path_is_used_when_url_is_unset(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_PATH", "fallback.db")

    assert database_path() == "fallback.db"


def test_database_path_is_used_when_url_is_empty(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "")
    monkeypatch.setenv("DATABASE_PATH", "fallback.db")

    assert database_path() == "fallback.db"


def test_default_path_applies_when_both_unset() -> None:
    assert database_path() == "data/app.db"


def test_default_path_applies_when_both_empty(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "")
    monkeypatch.setenv("DATABASE_PATH", "")

    assert database_path() == "data/app.db"


def test_environment_is_read_at_call_time(monkeypatch: pytest.MonkeyPatch) -> None:
    assert database_path() == "data/app.db"

    monkeypatch.setenv("DATABASE_PATH", "later.db")

    assert database_path() == "later.db"


def test_default_constant_names_the_documented_path() -> None:
    assert config.DEFAULT_DATABASE_PATH == "data/app.db"


def test_open_store_opens_the_selected_file_through_persistence(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    target = tmp_path / "opened.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite://{target}")

    db = open_store()

    assert isinstance(db, Database)
    db.close()
