"""`<command> --help`: usage and a one-line summary on stdout, exit 0, nothing touched.

Each command runs in-process through `cli_runner`. Stored state is read back through `db.rates`.
The seeded test rate is in one acceptance transaction that rolls back at the end.
"""

from __future__ import annotations

from collections.abc import Iterator
from unittest import mock

import pytest

from persistence import db as persistence_db
from persistence.testing import db_session

COMMANDS = ["init", "load", "fetch", "serve"]


@pytest.fixture(autouse=True)
def rolled_back_transaction() -> Iterator[None]:
    """Share one connection between the command and the test, then roll everything back."""
    persistence_db.begin_acceptance_transaction()
    try:
        yield
    finally:
        persistence_db.end_acceptance_transaction()


@pytest.mark.parametrize("command", COMMANDS)
def test_help_exits_zero_with_usage_on_stdout_and_nothing_on_stderr(cli_runner, command: str) -> None:
    code, out, err = cli_runner(command, "--help")

    assert code == 0
    assert out.strip() != ""
    assert err == ""
    assert command in out


@pytest.mark.parametrize("command", COMMANDS)
def test_help_prints_a_usage_line_then_a_one_line_summary(cli_runner, command: str) -> None:
    _, out, _ = cli_runner(command, "--help")

    lines = [line for line in out.splitlines() if line.strip()]
    assert len(lines) == 2
    assert lines[0].startswith(f"usage: fxrates {command}")
    assert lines[1].startswith("summary:")


def test_load_help_needs_no_file_argument(cli_runner) -> None:
    code, out, _ = cli_runner("load", "--help")

    assert code == 0
    assert out.splitlines()[0] == "usage: fxrates load <file>"


def test_init_help_does_not_reset_the_store(cli_runner) -> None:
    currency = "ZZH"
    date = "2999-09-01"
    text = "6.5"
    with db_session() as db:
        db.rates.replace_rate(date=date, currency=currency, rate=text)

        code, _, _ = cli_runner("init", "--help")

        assert code == 0
        rows = db.rates.list_currency_history(currency=currency, start_date=date, end_date=date)
        assert [r.rate for r in rows] == [text]


def test_fetch_help_does_not_download(cli_runner) -> None:
    with mock.patch("fxrates_app.fetch.download_archive") as download:
        code, _, _ = cli_runner("fetch", "--help")

    assert code == 0
    download.assert_not_called()


def test_help_applied_twice_prints_the_same_text(cli_runner) -> None:
    first = cli_runner("serve", "--help")
    second = cli_runner("serve", "--help")

    assert first == second
