"""The `init` command: empties the rates store, prints nothing, exits 0.

Seeds and reads back through the persistence library, and runs the command in-process through
`cli_runner`. Stored state is read back through `db.rates` rather than inferred from output.

`init` removes every row, so each test runs inside one acceptance transaction: the command and the
read-back share one connection, and the transaction rolls back at the end. The configured store is
never left changed.
"""

from __future__ import annotations

from collections.abc import Iterator

import pytest

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


def test_init_removes_seeded_rates_for_a_currency(cli_runner) -> None:
    currency = "ZZI"
    date = "1900-10-01"
    with db_session() as db:
        db.rates.replace_rate(date=date, currency=currency, rate="1.10")
        assert [r.date for r in db.rates.list_currency_history(currency=currency)] == [date]

        code, _, _ = cli_runner("init")

        assert code == 0
        assert db.rates.list_currency_history(currency=currency) == []


def test_init_removes_rates_across_many_dates(cli_runner) -> None:
    seeded = [("1900-10-02", "ZZJ", "1.1"), ("2025-01-02", "ZZK", "2.2"), ("9999-12-31", "ZZL", "3.3")]
    with db_session() as db:
        for date, currency, rate in seeded:
            db.rates.replace_rate(date=date, currency=currency, rate=rate)

        code, _, _ = cli_runner("init")

        assert code == 0
        assert db.rates.list_all_keys() == []


def test_init_prints_nothing_to_stdout_or_stderr(cli_runner) -> None:
    with db_session() as db:
        db.rates.replace_rate(date="1900-10-03", currency="ZZM", rate="4")

        code, out, err = cli_runner("init")

        assert code == 0
        assert out == ""
        assert err == ""


def test_init_on_an_empty_store_succeeds_and_leaves_it_empty(cli_runner) -> None:
    with db_session() as db:
        assert db.rates.list_all_keys() == []

        code, out, _ = cli_runner("init")

        assert code == 0
        assert out == ""
        assert db.rates.list_all_keys() == []


def test_init_applied_twice_exits_zero_both_times_and_stays_empty(cli_runner) -> None:
    with db_session() as db:
        db.rates.replace_rate(date="1900-10-04", currency="ZZN", rate="5")

        first = cli_runner("init")
        second = cli_runner("init")

        assert first[0] == 0
        assert second[0] == 0
        assert first[1] == second[1] == ""
        assert db.rates.list_all_keys() == []
