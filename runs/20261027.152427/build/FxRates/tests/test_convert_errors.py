"""GET /convert refusals: unknown currencies answer 404, bad or missing inputs answer 422.

Each test shares one acceptance transaction with the web client and rolls back at the end. The
status code is the oracle; no test reads the error body, whose wording is not part of the contract.
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


def test_unknown_source_currency_is_not_found(web_client) -> None:
    d = "2999-05-01"
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date=d, currency="ZZA", rate="1.5")

        response = web_client.get("/convert", params={"from": "ZZX", "to": "ZZA", "amount": "1", "date": d})

    assert response.status_code == 404


def test_unknown_target_currency_is_not_found(web_client) -> None:
    d = "2999-05-01"
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date=d, currency="ZZA", rate="1.5")

        response = web_client.get("/convert", params={"from": "ZZA", "to": "ZZX", "amount": "1", "date": d})

    assert response.status_code == 404


def test_date_earlier_than_every_publication_is_not_found_for_a_stored_currency(web_client) -> None:
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date="2999-06-01", currency="ZZA", rate="1.5")

        response = web_client.get("/convert", params={"from": "ZZA", "to": "EUR", "amount": "10", "date": "0001-01-01"})

    assert response.status_code == 404


def test_store_with_no_publication_is_not_found_without_a_date(web_client) -> None:
    with db_session() as db:
        empty_store(db)

        response = web_client.get("/convert", params={"from": "EUR", "to": "EUR", "amount": "1"})

    assert response.status_code == 404


@pytest.mark.parametrize(
    "params",
    [
        {"to": "USD", "amount": "1"},
        {"from": "USD", "amount": "1"},
        {"from": "USD", "to": "GBP"},
    ],
)
def test_each_missing_required_parameter_is_unprocessable(web_client, params: dict[str, str]) -> None:
    response = web_client.get("/convert", params=params)

    assert response.status_code == 422


@pytest.mark.parametrize("amount", ["abc", "-1", "1.", ".5", "1e3"])
def test_malformed_amount_is_unprocessable_for_the_declared_pattern(web_client, amount: str) -> None:
    response = web_client.get("/convert", params={"from": "USD", "to": "GBP", "amount": amount})

    assert response.status_code == 422


@pytest.mark.parametrize("date", ["2025-13-01", "2025-01-31-x", "yesterday"])
def test_malformed_or_impossible_date_is_unprocessable_for_the_declared_inputs(web_client, date: str) -> None:
    response = web_client.get("/convert", params={"from": "USD", "to": "GBP", "amount": "1", "date": date})

    assert response.status_code == 422
