"""Behavior tests for ratestore.store_rates, run inside the rollback fixture so nothing persists."""

from persistence.testing import db_session
from ratestore import store_rates

D1 = "1800-05-01"
D2 = "1800-05-02"


def test_store_rates_round_trips_exact_text_through_history() -> None:
    records = [(D1, "ZZA", "1.2300"), (D1, "ZZB", "10"), (D2, "ZZA", "1.5")]

    with db_session() as db:
        store_rates(db, records)

        zza = db.rates.history(currency="ZZA", start_date=D1, end_date=D2)
        zzb = db.rates.history(currency="ZZB", start_date=D1, end_date=D2)

        assert [(r.date, r.rate) for r in zza] == [(D1, "1.2300"), (D2, "1.5")]
        assert [(r.date, r.rate) for r in zzb] == [(D1, "10")]


def test_store_rates_returns_distinct_dates_and_records_written() -> None:
    records = [(D1, "ZZA", "1.1"), (D1, "ZZB", "2.2"), (D2, "ZZA", "3.3")]

    with db_session() as db:
        counts = store_rates(db, records)

    assert tuple(counts) == (2, 3)


def test_store_rates_with_empty_input_writes_nothing_and_reports_zero() -> None:
    with db_session() as db:
        before = db.rates.list_all()

        counts = store_rates(db, [])

        assert tuple(counts) == (0, 0)
        assert db.rates.list_all() == before


def test_store_rates_replaces_a_stored_rate_for_the_same_date_and_currency() -> None:
    with db_session() as db:
        store_rates(db, [(D1, "ZZA", "1.1")])

        store_rates(db, [(D1, "ZZA", "9.90")])

        rows = db.rates.history(currency="ZZA", start_date=D1, end_date=D1)
        assert [(r.date, r.rate) for r in rows] == [(D1, "9.90")]


def test_store_rates_replacement_leaves_other_currencies_unchanged() -> None:
    with db_session() as db:
        store_rates(db, [(D1, "ZZA", "1.1"), (D1, "ZZB", "2.2")])

        store_rates(db, [(D1, "ZZA", "9.90")])

        other = db.rates.history(currency="ZZB", start_date=D1, end_date=D1)
        assert [(r.date, r.rate) for r in other] == [(D1, "2.2")]


def test_store_rates_applied_twice_leaves_one_row_per_date_and_currency() -> None:
    records = [(D1, "ZZA", "1.1"), (D1, "ZZB", "2.2")]

    with db_session() as db:
        first = store_rates(db, records)
        before = db.rates.history(currency="ZZA", start_date=D1, end_date=D1)

        second = store_rates(db, records)
        after = db.rates.history(currency="ZZA", start_date=D1, end_date=D1)

        assert tuple(first) == tuple(second) == (1, 2)
        assert [(r.date, r.rate) for r in after] == [(r.date, r.rate) for r in before] == [(D1, "1.1")]


def test_store_rates_keeps_rate_text_exactly_as_given() -> None:
    with db_session() as db:
        store_rates(db, [(D1, "ZZA", "0.00100")])

        rows = db.rates.history(currency="ZZA", start_date=D1, end_date=D1)
        assert [r.rate for r in rows] == ["0.00100"]
