"""GET /rates/latest and fxrates_app.rates.latest_rates.

Each test shares one acceptance transaction with the web client and rolls back at the end. Tests
start from an emptied store inside that transaction so the latest publication is the one they seed.
"""

from __future__ import annotations

from collections.abc import Iterator

import pytest

from fxrates_app.rates import latest_rates
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


def test_latest_returns_the_latest_publication_with_requested_latest(web_client) -> None:
    older = "1900-10-01"
    newest = "1900-10-05"
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date=older, currency="ZZA", rate="9.9")
        db.rates.replace_rate(date=newest, currency="ZZA", rate="1.2500")
        db.rates.replace_rate(date=newest, currency="ZZB", rate="0.943")

        response = web_client.get("/rates/latest")

    assert response.status_code == 200
    assert response.json() == {
        "date": newest,
        "requested": "latest",
        "base": "EUR",
        "rates": {"ZZA": "1.2500", "ZZB": "0.943"},
    }


def test_latest_is_the_greatest_date_regardless_of_insertion_order(web_client) -> None:
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date="1900-10-05", currency="ZZA", rate="2")
        db.rates.replace_rate(date="1900-10-02", currency="ZZA", rate="1")
        db.rates.replace_rate(date="1900-10-09", currency="ZZA", rate="3")
        db.rates.replace_rate(date="1900-10-07", currency="ZZA", rate="4")

        body = web_client.get("/rates/latest").json()

    assert body["date"] == "1900-10-09"
    assert body["rates"] == {"ZZA": "3"}


def test_latest_matches_the_dated_route_for_the_same_publication(web_client) -> None:
    d = "1900-10-03"
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date=d, currency="ZZA", rate="4.5")
        db.rates.replace_rate(date=d, currency="ZZB", rate="5.25")

        latest = web_client.get("/rates/latest").json()
        dated = web_client.get(f"/rates/{d}").json()

    assert latest["date"] == dated["date"]
    assert latest["rates"] == dated["rates"]
    assert latest["requested"] == "latest"
    assert dated["requested"] == d


def test_latest_never_lists_the_base_currency(web_client) -> None:
    d = "1900-10-04"
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date=d, currency="EUR", rate="1")
        db.rates.replace_rate(date=d, currency="ZZA", rate="2")

        body = web_client.get("/rates/latest").json()

    assert "EUR" not in body["rates"]
    assert body["rates"] == {"ZZA": "2"}


def test_latest_on_an_empty_store_is_not_found(web_client) -> None:
    with db_session() as db:
        empty_store(db)

        response = web_client.get("/rates/latest")

    assert response.status_code == 404


def test_latest_is_not_parsed_as_a_date(web_client) -> None:
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date="1900-10-06", currency="ZZA", rate="3")

        latest = web_client.get("/rates/latest")
        malformed = web_client.get("/rates/not-a-date")

    assert latest.status_code == 200
    assert malformed.status_code == 422


def test_latest_rates_function_returns_none_on_an_empty_store() -> None:
    with db_session() as db:
        empty_store(db)

        assert latest_rates() is None


def test_latest_rates_function_returns_the_latest_date_and_its_rates() -> None:
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date="1900-10-01", currency="ZZA", rate="1")
        db.rates.replace_rate(date="1900-10-08", currency="ZZA", rate="8")
        db.rates.replace_rate(date="1900-10-08", currency="ZZB", rate="9")

        assert latest_rates() == ("1900-10-08", {"ZZA": "8", "ZZB": "9"})
