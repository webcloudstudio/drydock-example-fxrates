"""Behavior tests for app_server.deps.get_db: per-request store access over a test-owned store."""

from pathlib import Path

import pytest

from app_server.deps import get_db
from config import DATABASE_PATH_ENV, DATABASE_URL_ENV
from persistence import initialize_database


@pytest.fixture
def request_store(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    """Provision a store owned by this test and point the configuration at it."""
    path = tmp_path / "request.db"
    monkeypatch.delenv(DATABASE_URL_ENV, raising=False)
    monkeypatch.setenv(DATABASE_PATH_ENV, str(path))
    initialize_database(str(path)).close()
    return path


def test_get_db_yields_a_database_exposing_the_rates_operations(request_store: Path) -> None:
    gen = get_db()
    db = next(gen)

    assert hasattr(db, "rates")
    gen.close()


def test_get_db_finishes_after_one_yield(request_store: Path) -> None:
    gen = get_db()
    next(gen)

    with pytest.raises(StopIteration):
        next(gen)


def test_get_db_sees_a_rate_written_before_the_request(request_store: Path) -> None:
    writer = initialize_database(str(request_store))
    writer.rates.replace_rate(date="2025-01-02", currency="USD", rate="1.0345")
    writer.close()

    gen = get_db()
    db = next(gen)
    rows = db.rates.list_all()
    gen.close()

    assert [(row.date, row.currency, row.rate) for row in rows] == [("2025-01-02", "USD", "1.0345")]


def test_get_db_opens_the_store_at_the_configured_location(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    other = tmp_path / "elsewhere.db"
    monkeypatch.delenv(DATABASE_URL_ENV, raising=False)
    monkeypatch.setenv(DATABASE_PATH_ENV, str(other))
    writer = initialize_database(str(other))
    writer.rates.replace_rate(date="2025-01-03", currency="GBP", rate="0.8512")
    writer.close()

    gen = get_db()
    rows = next(gen).rates.list_all()
    gen.close()

    assert [(row.currency, row.rate) for row in rows] == [("GBP", "0.8512")]
