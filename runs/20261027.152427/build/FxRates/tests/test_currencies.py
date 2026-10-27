"""GET /currencies: the base currency and every stored currency code, ascending.

Each test shares one acceptance transaction with the web client and rolls back at the end. Exact
expectations start from an emptied store inside that transaction, so only the seeded codes appear.
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


def test_currencies_lists_stored_codes_ascending(web_client) -> None:
    with db_session() as db:
        empty_store(db)
        for code in ["ZZC", "ZZA", "ZZB"]:
            db.rates.replace_rate(date="1900-11-01", currency=code, rate="1")

        response = web_client.get("/currencies")

    assert response.status_code == 200
    assert response.json() == {"base": "EUR", "currencies": ["ZZA", "ZZB", "ZZC"]}


def test_currencies_matches_the_distinct_stored_codes(web_client) -> None:
    with db_session() as db:
        expected = sorted({r.currency for r in db.rates.list_currencies()})

        body = web_client.get("/currencies").json()

    assert body["currencies"] == expected
    assert body["currencies"] == sorted(set(body["currencies"]))


def test_currencies_lists_a_code_once_across_many_dates(web_client) -> None:
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date="1900-11-02", currency="ZZA", rate="1")
        db.rates.replace_rate(date="1900-11-03", currency="ZZA", rate="2")
        db.rates.replace_rate(date="1900-11-03", currency="ZZB", rate="3")

        body = web_client.get("/currencies").json()

    assert body["currencies"] == ["ZZA", "ZZB"]


def test_currencies_never_lists_the_base(web_client) -> None:
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date="1900-11-04", currency="EUR", rate="1")
        db.rates.replace_rate(date="1900-11-04", currency="ZZA", rate="2")

        body = web_client.get("/currencies").json()

    assert body["base"] == "EUR"
    assert body["currencies"] == ["ZZA"]


def test_currencies_on_an_empty_store_is_an_empty_list(web_client) -> None:
    with db_session() as db:
        empty_store(db)

        response = web_client.get("/currencies")

    assert response.status_code == 200
    assert response.json() == {"base": "EUR", "currencies": []}


def test_currencies_body_has_exactly_base_and_currencies(web_client) -> None:
    body = web_client.get("/currencies").json()

    assert set(body) == {"base", "currencies"}
    assert isinstance(body["currencies"], list)


def test_currencies_applied_twice_returns_the_same_body(web_client) -> None:
    first = web_client.get("/currencies").json()
    second = web_client.get("/currencies").json()

    assert first == second
