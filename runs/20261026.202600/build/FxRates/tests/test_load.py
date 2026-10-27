"""CSV loading validates the complete input before changing stored rates."""

from pathlib import Path

import pytest

from cli.testing import cli_runner
from persistence.testing import db_session


def test_load_accepts_header_only_and_reports_zero_rows(tmp_path: Path) -> None:
    source = tmp_path / "empty.csv"
    source.write_text("Date,USD,\n", encoding="utf-8")
    code, output, _ = cli_runner("load", str(source))
    assert code == 0
    assert [line.split(",") for line in output.splitlines()] == [["dates", "rates"], ["0", "0"]]


@pytest.mark.parametrize("contents", [
    "Date,usd\\n2099-01-01,1\\n",
    "Date,USD,USD\\n2099-01-01,1,2\\n",
    "Date,USD\\n2099-01-01,0\\n",
    "Date,USD\\n2099-02-30,1\\n",
    "Date,USD\\n2099-01-01,1\\n2099-01-01,2\\n",
])
def test_invalid_csv_does_not_partially_write(contents: str, tmp_path: Path) -> None:
    with db_session() as db:
        db.rates.upsert(date="2099-01-01", currency="QAT", rate="7.00")
    before = [(row.date, row.currency, row.rate) for row in _rates_on("2099-01-01")]
    source = tmp_path / "invalid.csv"
    source.write_text(contents.replace("\\n", "\n"), encoding="utf-8")
    code, _, _ = cli_runner("load", str(source))
    after = [(row.date, row.currency, row.rate) for row in _rates_on("2099-01-01")]
    assert code == 3
    assert after == before


def _rates_on(day: str):
    with db_session() as db:
        return db.rates.by_date(date=day)
