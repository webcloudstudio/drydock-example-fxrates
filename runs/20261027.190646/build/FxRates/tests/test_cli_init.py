"""Behavior tests for the init command, run against a store owned by each test."""

from pathlib import Path

import pytest

import cli.commands.init as init_command
from persistence import open_database


@pytest.fixture
def store_url(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Point DATABASE_URL at a store file that does not exist yet; no test touches the shared store."""
    store = tmp_path / "init.db"
    monkeypatch.setenv("DATABASE_URL", str(store))
    monkeypatch.delenv("DATABASE_PATH", raising=False)
    return store


def _read_history(store: Path, currency: str) -> list[tuple[str, str]]:
    db = open_database(str(store))
    try:
        return [(row.date, row.rate) for row in db.rates.history(currency=currency)]
    finally:
        db.close()


def _write_rates(store: Path, points: list[tuple[str, str]], currency: str) -> None:
    db = open_database(str(store))
    try:
        for date, rate in points:
            db.rates.replace_rate(date=date, currency=currency, rate=rate)
    finally:
        db.close()


def test_init_on_a_fresh_store_exits_zero_with_empty_stdout(cli_runner, store_url: Path) -> None:
    code, out, _ = cli_runner("init")

    assert code == 0
    assert out == ""


def test_init_on_a_fresh_store_creates_a_store_whose_rates_operations_work(cli_runner, store_url: Path) -> None:
    cli_runner("init")

    db = open_database(str(store_url))
    try:
        stored = db.rates.replace_rate(date="1800-05-01", currency="ZZA", rate="1.2300")
        assert stored.rate == "1.2300"
        rows = db.rates.history(currency="ZZA")
        assert [(r.date, r.rate) for r in rows] == [("1800-05-01", "1.2300")]
    finally:
        db.close()


def test_init_on_a_fresh_store_leaves_it_empty(cli_runner, store_url: Path) -> None:
    cli_runner("init")

    db = open_database(str(store_url))
    try:
        assert db.rates.list_all() == []
    finally:
        db.close()


def test_init_run_returns_zero(store_url: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert init_command.run([]) == 0
    assert capsys.readouterr().out == ""


def test_init_repeated_keeps_every_stored_rate(cli_runner, store_url: Path) -> None:
    points = [("1800-06-01", "3.10"), ("1800-06-02", "4.5")]
    assert cli_runner("init")[0] == 0
    _write_rates(store_url, points, currency="ZZB")

    code, out, _ = cli_runner("init")

    assert code == 0
    assert out == ""
    assert _read_history(store_url, "ZZB") == sorted(points)


def test_init_applied_twice_leaves_the_store_usable(cli_runner, store_url: Path) -> None:
    assert cli_runner("init")[0] == 0
    assert cli_runner("init")[0] == 0

    _write_rates(store_url, [("1800-07-01", "2.00")], currency="ZZC")

    assert _read_history(store_url, "ZZC") == [("1800-07-01", "2.00")]


def test_init_uses_database_path_when_database_url_is_unset(
    cli_runner, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    store = tmp_path / "fallback.db"
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setenv("DATABASE_PATH", str(store))

    code, out, _ = cli_runner("init")

    assert code == 0
    assert out == ""
    assert store.is_file()
    assert _read_history(store, "USD") == []


def test_init_creates_the_parent_directory_of_a_new_store(
    cli_runner, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    store = tmp_path / "nested" / "data" / "app.db"
    monkeypatch.setenv("DATABASE_URL", str(store))
    monkeypatch.delenv("DATABASE_PATH", raising=False)

    assert cli_runner("init")[0] == 0
    assert store.is_file()


def test_init_writes_no_rows_to_a_store_that_has_none(cli_runner, store_url: Path) -> None:
    cli_runner("init")
    cli_runner("init")

    db = open_database(str(store_url))
    try:
        assert db.rates.list_all() == []
    finally:
        db.close()
