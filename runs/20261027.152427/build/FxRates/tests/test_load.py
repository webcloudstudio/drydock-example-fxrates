"""The `load` command: validates a file, stores its rates as text, reports the dates and rates counts.

Each test runs the command in-process through `cli_runner` and reads the stored state back through
`db.rates`. Every test shares one acceptance transaction with the command, which rolls back at the
end, so the configured store is never left changed. Test currencies use the ZZ prefix so they never
collide with rates already in a store.
"""

from __future__ import annotations

import csv
import io
from collections.abc import Iterator
from pathlib import Path

import pytest

from fxrates_app.ecb import parse_history
from persistence import db as persistence_db
from persistence.testing import db_session


@pytest.fixture(autouse=True)
def rolled_back_transaction() -> Iterator[None]:
    """Share one connection between the command and the test, then roll everything back."""
    persistence_db.begin_acceptance_transaction()
    try:
        yield
    finally:
        persistence_db.end_acceptance_transaction()


def build(header: list[str], rows: list[list[str]]) -> str:
    """Write a file the way the ECB does: every line ends with a trailing comma."""
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(header + [""])
    for row in rows:
        writer.writerow(row + [""])
    return buf.getvalue()


def write(tmp_path: Path, name: str, text: str) -> str:
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return str(path)


def stored(db, currency: str) -> list[tuple[str, str]]:
    return [(r.date, r.rate) for r in db.rates.list_currency_history(currency=currency)]


def test_valid_file_exits_zero_and_reports_dates_and_rates(cli_runner, tmp_path) -> None:
    path = write(tmp_path, "in.csv", build(["Date", "ZZA", "ZZB"], [["1900-08-02", "1.5", "2"], ["1900-08-01", "0.9", "N/A"]]))

    code, out, _ = cli_runner("load", path)

    assert code == 0
    assert out.splitlines() == ["dates,rates", "2,3"]


def test_valid_file_stores_each_rate_as_published_text(cli_runner, tmp_path) -> None:
    path = write(tmp_path, "in.csv", build(["Date", "ZZA", "ZZB"], [["1900-08-02", "0.943", "160.0"]]))

    with db_session() as db:
        code, _, _ = cli_runner("load", path)

        assert code == 0
        assert stored(db, "ZZA") == [("1900-08-02", "0.943")]
        assert stored(db, "ZZB") == [("1900-08-02", "160.0")]


def test_all_na_date_is_not_counted_as_a_date(cli_runner, tmp_path) -> None:
    path = write(
        tmp_path,
        "in.csv",
        build(["Date", "ZZA", "ZZB"], [["1900-08-03", "1.5", "N/A"], ["1900-08-01", "N/A", "N/A"]]),
    )

    code, out, _ = cli_runner("load", path)

    assert code == 0
    assert out.splitlines() == ["dates,rates", "1,1"]


def test_file_of_only_na_reports_zero_and_stores_nothing(cli_runner, tmp_path) -> None:
    path = write(tmp_path, "na.csv", build(["Date", "ZZH", "ZZI"], [["1900-08-05", "N/A", "N/A"]]))

    with db_session() as db:
        before = db.rates.list_all_keys()

        code, out, _ = cli_runner("load", path)

        assert code == 0
        assert out.splitlines() == ["dates,rates", "0,0"]
        assert db.rates.list_for_date(date="1900-08-05") == []
        assert db.rates.list_all_keys() == before


def test_loading_same_file_twice_reports_the_same_counts(cli_runner, tmp_path) -> None:
    path = write(tmp_path, "in.csv", build(["Date", "ZZA", "ZZB"], [["1900-08-12", "1.5", "2.5"], ["1900-08-11", "1.25", "N/A"]]))

    first = cli_runner("load", path)
    second = cli_runner("load", path)

    assert first[0] == second[0] == 0
    assert first[1] == second[1]


def test_loading_same_file_twice_leaves_stored_rates_unchanged(cli_runner, tmp_path) -> None:
    path = write(tmp_path, "in.csv", build(["Date", "ZZA", "ZZB"], [["1900-08-12", "1.5", "2.5"], ["1900-08-11", "1.25", "N/A"]]))

    with db_session() as db:
        cli_runner("load", path)
        once = db.rates.list_all_keys()
        cli_runner("load", path)

        assert db.rates.list_all_keys() == once
        assert stored(db, "ZZA") == [("1900-08-11", "1.25"), ("1900-08-12", "1.5")]
        assert stored(db, "ZZB") == [("1900-08-12", "2.5")]


def test_later_file_replaces_stored_rate_and_keeps_other_dates(cli_runner, tmp_path) -> None:
    first = write(tmp_path, "a.csv", build(["Date", "ZZA"], [["1900-08-21", "3.3"], ["1900-08-22", "1.10"]]))
    second = write(tmp_path, "b.csv", build(["Date", "ZZA"], [["1900-08-22", "9.9"]]))

    with db_session() as db:
        assert cli_runner("load", first)[0] == 0
        assert cli_runner("load", second)[0] == 0

        assert stored(db, "ZZA") == [("1900-08-21", "3.3"), ("1900-08-22", "9.9")]


def test_replacing_a_rate_does_not_add_a_row(cli_runner, tmp_path) -> None:
    first = write(tmp_path, "a.csv", build(["Date", "ZZA"], [["1900-08-22", "1.10"]]))
    second = write(tmp_path, "b.csv", build(["Date", "ZZA"], [["1900-08-22", "9.9"]]))

    with db_session() as db:
        before = len(db.rates.list_all_keys())
        cli_runner("load", first)
        cli_runner("load", second)

        assert len(db.rates.list_all_keys()) == before + 1


def test_rejected_file_exits_three_with_empty_stdout_and_one_stderr_line(cli_runner, tmp_path) -> None:
    path = write(
        tmp_path,
        "bad.csv",
        build(["Date", "ZZB", ""], [["1900-08-31", "1.5", ""], ["1900-08-30", "1.0x", ""]]),
    )

    code, out, err = cli_runner("load", path)

    assert code == 3
    assert out == ""
    assert len(err.splitlines()) == 1


def test_rejected_file_stores_nothing_not_even_its_valid_first_row(cli_runner, tmp_path) -> None:
    path = write(
        tmp_path,
        "bad.csv",
        build(["Date", "ZZB", ""], [["1900-08-31", "1.5", ""], ["1900-08-30", "1.0x", ""]]),
    )

    with db_session() as db:
        before = db.rates.list_all_keys()

        cli_runner("load", path)

        assert stored(db, "ZZB") == []
        assert db.rates.list_all_keys() == before


def test_rejected_file_leaves_previously_stored_rates_alone(cli_runner, tmp_path) -> None:
    good = write(tmp_path, "good.csv", build(["Date", "ZZC"], [["1900-08-10", "2.0"]]))
    bad = write(tmp_path, "bad.csv", build(["Date", "ZZC"], [["1900-08-11", "3.0"], ["1900-08-12", "x"]]))

    with db_session() as db:
        cli_runner("load", good)

        code, _, _ = cli_runner("load", bad)

        assert code == 3
        assert stored(db, "ZZC") == [("1900-08-10", "2.0")]


def test_supplied_bad_file_exits_three_and_adds_no_rows(cli_runner, project_root) -> None:
    path = str(project_root / "sources" / "eurofxref-hist_bad.csv")

    with db_session() as db:
        before = db.rates.list_all_keys()

        code, out, _ = cli_runner("load", path)

        assert code == 3
        assert out == ""
        assert db.rates.list_all_keys() == before


def test_supplied_january_file_reports_counts_derived_from_its_cells(cli_runner, project_root) -> None:
    path = project_root / "sources" / "eurofxref-hist_2025-01.csv"
    table = list(csv.reader(path.read_text(encoding="utf-8").splitlines()))
    codes = [h for h in table[0][1:] if h]
    cells = [
        (row[0], code, value)
        for row in table[1:]
        for code, value in zip(codes, row[1:1 + len(codes)])
        if value != "N/A"
    ]
    expected_dates = len({date for date, _, _ in cells})

    with db_session() as db:
        code, out, _ = cli_runner("load", str(path))

        assert code == 0
        assert out.splitlines() == ["dates,rates", f"{expected_dates},{len(cells)}"]
        usd = {r.date: r.rate for r in db.rates.list_currency_history(currency="USD")}
        assert usd == {date: value for date, currency, value in cells if currency == "USD"}
        assert db.rates.list_currency_history(currency="HRK") == []


def test_supplied_january_file_round_trips_through_parse_history(cli_runner, project_root) -> None:
    path = project_root / "sources" / "eurofxref-hist_2025-01.csv"
    parsed = parse_history(path.read_text(encoding="utf-8"))

    with db_session() as db:
        code, _, _ = cli_runner("load", str(path))

        assert code == 0
        for date, currency, rate in parsed:
            assert (date, rate) in stored(db, currency)


def test_missing_file_exits_one_with_empty_stdout_and_one_stderr_line(cli_runner, tmp_path) -> None:
    path = str(tmp_path / "no-such-file.csv")

    code, out, err = cli_runner("load", path)

    assert code == 1
    assert out == ""
    assert len(err.splitlines()) == 1


def test_missing_file_stores_nothing(cli_runner, tmp_path) -> None:
    path = str(tmp_path / "no-such-file.csv")

    with db_session() as db:
        before = db.rates.list_all_keys()

        cli_runner("load", path)

        assert db.rates.list_all_keys() == before


def test_directory_path_exits_one_with_empty_stdout_and_one_stderr_line(cli_runner, tmp_path) -> None:
    code, out, err = cli_runner("load", str(tmp_path))

    assert code == 1
    assert out == ""
    assert len(err.splitlines()) == 1


def test_undecodable_file_exits_one_with_empty_stdout_and_one_stderr_line(cli_runner, tmp_path) -> None:
    path = tmp_path / "binary.csv"
    path.write_bytes(b"\xff\xfe\xfa\x80\x81\xff")

    code, out, err = cli_runner("load", str(path))

    assert code == 1
    assert out == ""
    assert len(err.splitlines()) == 1


def test_undecodable_file_stores_nothing(cli_runner, tmp_path) -> None:
    path = tmp_path / "binary.csv"
    path.write_bytes(b"\xff\xfe\xfa\x80\x81\xff")

    with db_session() as db:
        before = db.rates.list_all_keys()

        cli_runner("load", str(path))

        assert db.rates.list_all_keys() == before


def test_help_after_load_exits_zero_without_reading_a_file(cli_runner) -> None:
    code, out, err = cli_runner("load", "--help")

    assert code == 0
    assert out.splitlines()[0] == "usage: fxrates load <file>"
