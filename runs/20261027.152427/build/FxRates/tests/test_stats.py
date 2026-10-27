"""GET /stats: counts and first and last dates, read back through the persistence library.

Each test shares one acceptance transaction with the web client and rolls back at the end. Where a
test needs exact numbers it first empties the store inside that transaction, so the expected values
are the ones the test seeded.
"""

from __future__ import annotations

from collections.abc import Iterator

import pytest

from persistence import db as persistence_db
from persistence.testing import db_session


@pytest.fixture(autouse=True)
def rolled_back_transaction() -> Iterator[None]:
    """Share one connection between the route and the test, then roll everything back."""
    persistence_db.begin_acceptance_transaction()
    try:
        yield
    finally:
        persistence_db.end_acceptance_transaction()


def empty_store(db) -> None:
    """Remove every stored rate inside the acceptance transaction."""
    db.rates.delete_from_date(from_date="0000-01-01")


def test_stats_reflects_the_stored_keys(web_client) -> None:
    d1 = "1900-09-01"
    d2 = "1900-09-02"
    with db_session() as db:
        db.rates.replace_rate(date=d1, currency="ZZA", rate="1.1")
        db.rates.replace_rate(date=d1, currency="ZZB", rate="2.2")
        db.rates.replace_rate(date=d2, currency="ZZA", rate="1.2")
        keys = db.rates.list_all_keys()
        dates = sorted({k.date for k in keys})

        response = web_client.get("/stats")

        assert response.status_code == 200
        body = response.json()
        assert body["dates"] == len(dates)
        assert body["rates"] == len(keys)
        assert body["first"] == dates[0]
        assert body["last"] == dates[-1]
        assert isinstance(body["dates"], int)
        assert isinstance(body["rates"], int)
        assert body["first"] <= d1
        assert body["last"] >= d2


def test_stats_body_has_exactly_the_four_declared_keys(web_client) -> None:
    body = web_client.get("/stats").json()

    assert set(body) == {"dates", "rates", "first", "last"}


def test_stats_counts_dates_and_rates_on_an_emptied_store(web_client) -> None:
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date="1900-09-01", currency="ZZA", rate="1")
        db.rates.replace_rate(date="1900-09-01", currency="ZZB", rate="2")
        db.rates.replace_rate(date="1900-09-03", currency="ZZA", rate="3")

        body = web_client.get("/stats").json()

    assert body == {"dates": 2, "rates": 3, "first": "1900-09-01", "last": "1900-09-03"}


def test_stats_on_an_empty_store_reports_zero_and_nulls(web_client) -> None:
    with db_session() as db:
        empty_store(db)

        response = web_client.get("/stats")

    assert response.status_code == 200
    assert response.json() == {"dates": 0, "rates": 0, "first": None, "last": None}


def test_stats_with_one_date_reports_it_as_first_and_last(web_client) -> None:
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date="1900-09-07", currency="ZZA", rate="1")

        body = web_client.get("/stats").json()

    assert body == {"dates": 1, "rates": 1, "first": "1900-09-07", "last": "1900-09-07"}


def test_stats_does_not_double_count_a_replaced_rate(web_client) -> None:
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date="1900-09-08", currency="ZZA", rate="1")
        db.rates.replace_rate(date="1900-09-08", currency="ZZA", rate="9.99")

        body = web_client.get("/stats").json()

    assert body["rates"] == 1
    assert body["dates"] == 1


def test_stats_applied_twice_returns_the_same_body(web_client) -> None:
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date="1900-09-09", currency="ZZA", rate="1")

        first = web_client.get("/stats").json()
        second = web_client.get("/stats").json()

    assert first == second
