"""GET /history/{code} and fxrates_app.history: a currency's stored points between optional bounds.

Each test shares one acceptance transaction with the web client and rolls back at the end. Rates
are compared as the stored text; no test converts them to a number.
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


def test_points_between_inclusive_bounds_are_ascending(web_client) -> None:
    code = "ZZH"
    rates = {"1900-08-03": "1.50", "1900-08-01": "1.0316", "1900-08-02": "2", "1900-08-04": "0.943"}
    with db_session() as db:
        empty_store(db)
        for d, r in rates.items():
            db.rates.replace_rate(date=d, currency=code, rate=r)

        body = web_client.get(f"/history/{code}", params={"start": "1900-08-02", "end": "1900-08-03"}).json()

    assert body["points"] == [{"date": "1900-08-02", "rate": "2"}, {"date": "1900-08-03", "rate": "1.50"}]
    assert body["count"] == 2


def test_response_names_the_currency_and_base(web_client) -> None:
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date="1900-08-05", currency="ZZH", rate="1")

        response = web_client.get("/history/ZZH")

    assert response.status_code == 200
    body = response.json()
    assert body["currency"] == "ZZH"
    assert body["base"] == "EUR"


def test_each_bound_is_optional_on_its_own(web_client) -> None:
    code = "ZZH"
    rates = {"1900-09-04": "0.943", "1900-09-02": "1.50", "1900-09-03": "1.0316", "1900-09-01": "7"}
    cut = "1900-09-03"
    with db_session() as db:
        empty_store(db)
        for d, r in rates.items():
            db.rates.replace_rate(date=d, currency=code, rate=r)

        everything = web_client.get(f"/history/{code}").json()
        from_cut = web_client.get(f"/history/{code}", params={"start": cut}).json()
        to_cut = web_client.get(f"/history/{code}", params={"end": cut}).json()

    assert everything["points"] == [{"date": d, "rate": rates[d]} for d in sorted(rates)]
    assert from_cut["points"] == [{"date": d, "rate": rates[d]} for d in sorted(rates) if d >= cut]
    assert to_cut["points"] == [{"date": d, "rate": rates[d]} for d in sorted(rates) if d <= cut]


def test_stored_rate_text_is_returned_exactly(web_client) -> None:
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date="1900-09-10", currency="ZZH", rate="0.943")

        points = web_client.get("/history/ZZH").json()["points"]

    assert points == [{"date": "1900-09-10", "rate": "0.943"}]


def test_start_after_end_is_ok_with_no_points(web_client) -> None:
    code = "ZZH"
    with db_session() as db:
        empty_store(db)
        for d in ["1900-10-01", "1900-10-02", "1900-10-03"]:
            db.rates.replace_rate(date=d, currency=code, rate="3")

        response = web_client.get(f"/history/{code}", params={"start": "1900-10-03", "end": "1900-10-01"})

    assert response.status_code == 200
    body = response.json()
    assert body["points"] == []
    assert body["count"] == 0


def test_replaced_rate_is_what_the_next_request_returns(web_client) -> None:
    code = "ZZH"
    d = "1900-11-01"
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date=d, currency=code, rate="1.25")
        assert web_client.get(f"/history/{code}").json()["points"] == [{"date": d, "rate": "1.25"}]

        db.rates.replace_rate(date=d, currency=code, rate="1.75")
        body = web_client.get(f"/history/{code}").json()

    assert body["points"] == [{"date": d, "rate": "1.75"}]
    assert body["count"] == 1


def test_points_are_only_those_of_the_requested_currency(web_client) -> None:
    d = "1900-11-02"
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date=d, currency="ZZH", rate="1")
        db.rates.replace_rate(date=d, currency="ZZJ", rate="2")

        body = web_client.get("/history/ZZH").json()

    assert body["points"] == [{"date": d, "rate": "1"}]


def test_unknown_currency_is_not_found(web_client) -> None:
    with db_session() as db:
        empty_store(db)

        response = web_client.get("/history/ZZNONE")

    assert response.status_code == 404


def test_bounds_equal_to_a_publication_date_include_it(web_client) -> None:
    d = "1900-11-03"
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date=d, currency="ZZH", rate="4")

        body = web_client.get("/history/ZZH", params={"start": d, "end": d}).json()

    assert body["points"] == [{"date": d, "rate": "4"}]


@pytest.mark.parametrize(
    "params",
    [
        {"start": "2025-02-30"},
        {"end": "2025-13-01"},
        {"start": "not-a-date"},
        {"end": "20251031"},
    ],
)
def test_malformed_or_impossible_bound_is_unprocessable(web_client, params: dict[str, str]) -> None:
    response = web_client.get("/history/ZZH", params=params)

    assert response.status_code == 422


def test_service_matches_the_route(web_client) -> None:
    code = "ZZH"
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date="1900-12-01", currency=code, rate="5")
        db.rates.replace_rate(date="1900-12-02", currency=code, rate="6")

        body = web_client.get(f"/history/{code}", params={"start": "1900-12-02"}).json()
        direct = history_service.history_points(code, "1900-12-02", None)

    assert body["points"] == direct
