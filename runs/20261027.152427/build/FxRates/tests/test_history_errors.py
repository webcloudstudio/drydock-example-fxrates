"""GET /history/{code} refusals: no stored rate at all answers 404, a malformed bound answers 422.

Each test shares one acceptance transaction with the web client and rolls back at the end. The
status code is the oracle; no test reads the error body, whose wording is not part of the contract.
"""

from __future__ import annotations

from collections.abc import Iterator

import pytest

from fxrates_app import history as history_service
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


def test_currency_with_no_stored_rate_is_not_found(web_client) -> None:
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date="1902-01-01", currency="ZZA", rate="1.5")

        response = web_client.get("/history/ZZX")

    assert response.status_code == 404


def test_base_currency_is_not_found_even_when_other_rates_are_stored(web_client) -> None:
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date="1902-01-02", currency="ZZA", rate="1.5")

        response = web_client.get("/history/EUR")

    assert response.status_code == 404


def test_currency_with_a_rate_is_found_after_it_is_stored(web_client) -> None:
    with db_session() as db:
        empty_store(db)
        before = web_client.get("/history/ZZB")
        db.rates.replace_rate(date="1902-01-03", currency="ZZB", rate="2")
        after = web_client.get("/history/ZZB")

    assert before.status_code == 404
    assert after.status_code == 200
    assert after.json()["count"] == 1


def test_currency_with_rates_only_outside_the_bounds_is_ok(web_client) -> None:
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date="1902-02-01", currency="ZZH", rate="2")

        response = web_client.get("/history/ZZH", params={"start": "1902-03-01", "end": "1902-03-31"})

    assert response.status_code == 200
    assert response.json()["count"] == 0


@pytest.mark.parametrize("bad", ["2025-01-31-x", "2025-13-01", "2025-02-30", "notadate", "20251031"])
def test_malformed_start_is_unprocessable_for_a_stored_currency(web_client, bad: str) -> None:
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date="1902-04-01", currency="ZZH", rate="5")

        response = web_client.get("/history/ZZH", params={"start": bad})

    assert response.status_code == 422


@pytest.mark.parametrize("bad", ["2025-01-31-x", "2025-13-01", "2025-02-30", "notadate", "20251031"])
def test_malformed_end_is_unprocessable_for_a_stored_currency(web_client, bad: str) -> None:
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date="1902-04-02", currency="ZZH", rate="5")

        response = web_client.get("/history/ZZH", params={"end": bad})

    assert response.status_code == 422


def test_malformed_bound_with_a_valid_other_bound_is_unprocessable(web_client) -> None:
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date="1902-04-03", currency="ZZH", rate="5")

        response = web_client.get("/history/ZZH", params={"start": "1902-04-01", "end": "2025-13-01"})

    assert response.status_code == 422


def test_service_raises_unknown_currency_only_for_an_empty_whole_history() -> None:
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date="1902-05-01", currency="ZZH", rate="5")

        assert history_service.history_points("ZZH", "1903-01-01", None) == []
        with pytest.raises(history_service.UnknownCurrency):
            history_service.history_points("ZZX", None, None)
