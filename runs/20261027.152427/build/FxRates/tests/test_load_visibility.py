"""Load visibility: a completed load is seen by the next API request; a rejected load changes nothing.

The command and the web client share one acceptance transaction, so a rate the command writes is
read back by the next request through the same store. Each test empties the store first and rolls
back at the end.
"""

from __future__ import annotations

import csv
import io
from collections.abc import Iterator
from pathlib import Path

import pytest

from cli.testing import cli_runner
from persistence import db as persistence_db
from persistence.testing import db_session


@pytest.fixture(autouse=True)
def rolled_back_transaction() -> Iterator[None]:
    """Share one connection between the command, the route and the test, then roll everything back."""
    persistence_db.begin_acceptance_transaction()
    try:
        yield
    finally:
        persistence_db.end_acceptance_transaction()


def write_history(path: Path, header: list[str], rows: list[list[str]]) -> Path:
    """Write a file the way the ECB does: every line ends with a trailing comma."""
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(header + [""])
    for row in rows:
        writer.writerow(row + [""])
    path.write_text(buf.getvalue(), encoding="utf-8")
    return path


def empty_store(db) -> None:
    """Remove every stored rate inside the acceptance transaction."""
    db.rates.delete_from_date(from_date="0000-01-01")


def test_completed_load_is_visible_to_the_next_stats_request(web_client, tmp_path: Path) -> None:
    d = "1900-12-30"
    path = write_history(tmp_path / "load.csv", ["Date", "ZZA", "ZZB"], [[d, "1.5", "2.25"]])
    with db_session() as db:
        empty_store(db)
        before = web_client.get("/stats").json()

        code, out, err = cli_runner("load", str(path))
        after = web_client.get("/stats").json()

    assert code == 0
    assert after == {"dates": 1, "rates": 2, "first": d, "last": d}
    assert after["dates"] == before["dates"] + 1
    assert after["rates"] == before["rates"] + 2
    assert after["last"] == d


def test_completed_load_is_visible_to_the_next_latest_request(web_client, tmp_path: Path) -> None:
    d = "1900-12-31"
    path = write_history(tmp_path / "latest.csv", ["Date", "ZZA"], [[d, "3.5"]])
    with db_session() as db:
        empty_store(db)

        code, _, _ = cli_runner("load", str(path))
        response = web_client.get("/rates/latest")

    assert code == 0
    assert response.status_code == 200
    assert response.json()["date"] == d
    assert response.json()["rates"] == {"ZZA": "3.5"}


def test_rejected_load_leaves_stats_unchanged(web_client, tmp_path: Path) -> None:
    good = "1900-11-01"
    bad = "1900-11-02"
    path = write_history(
        tmp_path / "bad.csv",
        ["Date", "ZZA"],
        [[bad, "1.5"], [good, "1.5x"]],
    )
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date="1900-10-30", currency="ZZA", rate="1")
        before = web_client.get("/stats").json()

        code, out, err = cli_runner("load", str(path))
        after = web_client.get("/stats").json()
        written = db.rates.list_for_date(date=bad)

    assert code == 3
    assert out == ""
    assert after == before
    assert written == []


def test_loading_the_same_file_twice_leaves_stats_unchanged(web_client, tmp_path: Path) -> None:
    path = write_history(tmp_path / "again.csv", ["Date", "ZZA"], [["1900-10-07", "7.5"]])
    with db_session() as db:
        empty_store(db)

        assert cli_runner("load", str(path))[0] == 0
        first = web_client.get("/stats").json()
        assert cli_runner("load", str(path))[0] == 0
        second = web_client.get("/stats").json()

    assert second == first
