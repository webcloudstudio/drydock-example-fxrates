"""The `fetch` command: downloads the ECB archive, extracts its CSV, and loads it as `load` does.

Every test replaces `fxrates_app.fetch.download_archive`, the single network seam, so no test opens a
connection. Each test runs the command in-process through `cli_runner` and reads the stored state back
through `db.rates`, inside one acceptance transaction that rolls back at the end.
"""

from __future__ import annotations

import csv
import http.client
import io
import zipfile
from collections.abc import Iterator
from unittest import mock

import pytest

from fxrates_app import fetch
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


def csv_text(header: list[str], rows: list[list[str]]) -> str:
    """Write CSV the way the ECB does: every line ends with a trailing comma."""
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(header + [""])
    for row in rows:
        writer.writerow(row + [""])
    return buf.getvalue()


def zip_with(member: str, text: str) -> bytes:
    bio = io.BytesIO()
    with zipfile.ZipFile(bio, "w") as z:
        z.writestr(member, text)
    return bio.getvalue()


def stored(db, currency: str) -> list[tuple[str, str]]:
    return [(r.date, r.rate) for r in db.rates.list_currency_history(currency=currency)]


def test_fetch_loads_archive(cli_runner) -> None:
    d = "1900-08-01"
    ra = "1.50"
    rb = "2.250"
    data = zip_with("eurofxref-hist.csv", csv_text(["Date", "ZZA", "ZZB"], [[d, ra, rb]]))

    with db_session() as db:
        with mock.patch("fxrates_app.fetch.download_archive", return_value=data):
            code, out, err = cli_runner("fetch")
        assert code == 0
        lines = out.splitlines()
        assert lines[0] == "dates,rates"
        assert lines[1].split(",") == [str(1), str(2)]
        rows = {r.currency: r.rate for r in db.rates.list_for_date(date=d)}
        assert rows["ZZA"] == ra
        assert rows["ZZB"] == rb


def test_fetch_download_failure(cli_runner) -> None:
    d = "1900-08-02"

    with db_session() as db:
        before = db.rates.list_all_keys()
        with mock.patch("fxrates_app.fetch.download_archive", side_effect=OSError("network down")):
            code, out, err = cli_runner("fetch")
        assert code == 1
        assert out == ""
        assert len(err.strip().splitlines()) == 1
        assert db.rates.list_for_date(date=d) == []
        assert len(db.rates.list_all_keys()) == len(before)


def test_fetch_bad_archive(cli_runner) -> None:
    d = "1900-08-03"
    wrong_member = zip_with("other.csv", csv_text(["Date", "ZZA"], [[d, "1.5"]]))
    not_a_zip = bytes(range(32))

    with db_session() as db:
        before = len(db.rates.list_all_keys())
        for payload in (not_a_zip, wrong_member):
            with mock.patch("fxrates_app.fetch.download_archive", return_value=payload):
                code, out, err = cli_runner("fetch")
            assert code == 1
            assert out == ""
            assert len(err.strip().splitlines()) == 1
            assert db.rates.list_for_date(date=d) == []
        assert len(db.rates.list_all_keys()) == before


def test_fetch_rejected_member(cli_runner) -> None:
    good = "1900-08-05"
    bad = "1900-08-04"
    data = zip_with(
        "eurofxref-hist.csv",
        csv_text(["Date", "ZZA"], [[good, "1.5"], [bad, "0"]]),
    )

    with db_session() as db:
        with mock.patch("fxrates_app.fetch.download_archive", return_value=data):
            code, out, err = cli_runner("fetch")
        assert code == 3
        assert out == ""
        assert len(err.strip().splitlines()) == 1
        assert db.rates.list_for_date(date=good) == []
        assert db.rates.list_for_date(date=bad) == []


def test_fetch_downloads_the_ecb_archive_url_once(cli_runner) -> None:
    data = zip_with("eurofxref-hist.csv", csv_text(["Date", "ZZA"], [["1900-09-01", "1.5"]]))

    with mock.patch("fxrates_app.fetch.download_archive", return_value=data) as download:
        code, _, _ = cli_runner("fetch")

    assert code == 0
    download.assert_called_once_with(
        "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip"
    )


def test_fetch_timeout_exits_one_and_stores_nothing(cli_runner) -> None:
    with db_session() as db:
        before = db.rates.list_all_keys()
        with mock.patch("fxrates_app.fetch.download_archive", side_effect=TimeoutError("timed out")):
            code, out, err = cli_runner("fetch")
        assert code == 1
        assert out == ""
        assert len(err.strip().splitlines()) == 1
        assert db.rates.list_all_keys() == before


def test_fetch_protocol_error_exits_one(cli_runner) -> None:
    with mock.patch(
        "fxrates_app.fetch.download_archive",
        side_effect=http.client.RemoteDisconnected("closed"),
    ):
        code, out, err = cli_runner("fetch")

    assert code == 1
    assert out == ""
    assert len(err.strip().splitlines()) == 1


def test_fetch_member_that_is_not_utf8_exits_one_and_stores_nothing(cli_runner) -> None:
    bio = io.BytesIO()
    with zipfile.ZipFile(bio, "w") as z:
        z.writestr("eurofxref-hist.csv", b"Date,ZZA,\n\xff\xfe,1.5,\n")

    with db_session() as db:
        before = db.rates.list_all_keys()
        with mock.patch("fxrates_app.fetch.download_archive", return_value=bio.getvalue()):
            code, out, err = cli_runner("fetch")
        assert code == 1
        assert out == ""
        assert len(err.strip().splitlines()) == 1
        assert db.rates.list_all_keys() == before


def test_fetch_twice_reports_the_same_counts_and_leaves_rates_unchanged(cli_runner) -> None:
    data = zip_with(
        "eurofxref-hist.csv",
        csv_text(["Date", "ZZA", "ZZB"], [["1900-09-03", "1.5", "2.5"], ["1900-09-02", "1.25", "N/A"]]),
    )

    with db_session() as db:
        with mock.patch("fxrates_app.fetch.download_archive", return_value=data):
            first = cli_runner("fetch")
            once = db.rates.list_all_keys()
            second = cli_runner("fetch")

        assert first[0] == second[0] == 0
        assert first[1] == second[1]
        assert db.rates.list_all_keys() == once
        assert stored(db, "ZZA") == [("1900-09-02", "1.25"), ("1900-09-03", "1.5")]
        assert stored(db, "ZZB") == [("1900-09-03", "2.5")]


def test_fetch_stores_rates_as_published_text(cli_runner) -> None:
    data = zip_with("eurofxref-hist.csv", csv_text(["Date", "ZZA"], [["1900-09-04", "160.0"]]))

    with db_session() as db:
        with mock.patch("fxrates_app.fetch.download_archive", return_value=data):
            code, _, _ = cli_runner("fetch")

        assert code == 0
        assert stored(db, "ZZA") == [("1900-09-04", "160.0")]


def test_fetch_help_exits_zero_without_downloading(cli_runner) -> None:
    with mock.patch("fxrates_app.fetch.download_archive") as download:
        code, out, err = cli_runner("fetch", "--help")

    assert code == 0
    assert out.splitlines()[0] == "usage: fxrates fetch"
    download.assert_not_called()


def test_fetch_with_an_argument_is_a_usage_error(cli_runner) -> None:
    with mock.patch("fxrates_app.fetch.download_archive") as download:
        code, out, err = cli_runner("fetch", "extra.csv")

    assert code == 2
    assert out == ""
    download.assert_not_called()


def test_archive_download_is_the_module_attribute_seam() -> None:
    assert callable(fetch.download_archive)
    assert fetch.ECB_ARCHIVE_URL.startswith("https://www.ecb.europa.eu/")
