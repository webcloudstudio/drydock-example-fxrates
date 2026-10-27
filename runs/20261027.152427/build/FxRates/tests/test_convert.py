"""GET /convert and fxrates_app.convert: exact decimal conversion rounded half to even.

Each test shares one acceptance transaction with the web client and rolls back at the end. Tests
that depend on which publications exist start from an emptied store inside that transaction, and
expected values are derived with Decimal from the seeded rates.
"""

from __future__ import annotations

from collections.abc import Iterator
from decimal import ROUND_HALF_EVEN, Decimal

import pytest

from fxrates_app import convert as convert_service
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


def test_two_currencies_convert_with_six_and_two_decimals(web_client) -> None:
    d = "2999-01-01"
    rate_from = "1.0298"
    rate_to = "0.84453"
    amount = "100"
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date=d, currency="ZZA", rate=rate_from)
        db.rates.replace_rate(date=d, currency="ZZB", rate=rate_to)

        response = web_client.get("/convert", params={"from": "ZZA", "to": "ZZB", "amount": amount, "date": d})

    assert response.status_code == 200
    expected_rate = (Decimal(rate_to) / Decimal(rate_from)).quantize(Decimal("0.000001"), rounding=ROUND_HALF_EVEN)
    expected_result = (Decimal(amount) * Decimal(rate_to) / Decimal(rate_from)).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_EVEN
    )
    assert response.json() == {
        "date": d,
        "from": "ZZA",
        "to": "ZZB",
        "amount": amount,
        "rate": f"{expected_rate:.6f}",
        "result": f"{expected_result:.2f}",
    }


def test_amount_is_echoed_as_given(web_client) -> None:
    d = "2999-01-02"
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date=d, currency="ZZA", rate="2")

        body = web_client.get("/convert", params={"from": "EUR", "to": "ZZA", "amount": "007.50", "date": d}).json()

    assert body["amount"] == "007.50"
    assert body["result"] == "15.00"


def test_eur_to_stored_currency_uses_rate_one_for_eur(web_client) -> None:
    published = "2999-02-01"
    requested = "2999-02-03"
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date=published, currency="ZZA", rate="161.77")

        body = web_client.get(
            "/convert", params={"from": "EUR", "to": "ZZA", "amount": "250.25", "date": requested}
        ).json()

    assert body["date"] == published
    assert body["rate"] == "161.770000"
    assert body["result"] == "40482.94"


def test_stored_currency_to_eur_divides_by_the_stored_rate(web_client) -> None:
    published = "2999-02-01"
    requested = "2999-02-03"
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date=published, currency="ZZA", rate="161.77")

        body = web_client.get(
            "/convert", params={"from": "ZZA", "to": "EUR", "amount": "1000", "date": requested}
        ).json()

    expected_rate = (Decimal(1) / Decimal("161.77")).quantize(Decimal("0.000001"), rounding=ROUND_HALF_EVEN)
    expected_result = (Decimal("1000") / Decimal("161.77")).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
    assert body["date"] == published
    assert body["rate"] == f"{expected_rate:.6f}"
    assert body["result"] == f"{expected_result:.2f}"


def test_without_date_the_latest_publication_is_used(web_client) -> None:
    older = "2999-03-01"
    newest = "2999-03-09"
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date=older, currency="ZZA", rate="2")
        db.rates.replace_rate(date=older, currency="ZZB", rate="3")
        db.rates.replace_rate(date=newest, currency="ZZA", rate="2")
        db.rates.replace_rate(date=newest, currency="ZZB", rate="5")

        body = web_client.get("/convert", params={"from": "ZZA", "to": "ZZB", "amount": "2.00"}).json()

    assert body["date"] == newest
    assert body["rate"] == "2.500000"
    assert body["result"] == "5.00"


def test_date_between_publications_resolves_to_the_earlier_one(web_client) -> None:
    early = "2999-04-01"
    late = "2999-04-05"
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date=early, currency="ZZA", rate="4")
        db.rates.replace_rate(date=late, currency="ZZA", rate="8")

        body = web_client.get("/convert", params={"from": "EUR", "to": "ZZA", "amount": "1", "date": "2999-04-03"}).json()

    assert body["date"] == early
    assert body["result"] == "4.00"


def test_same_currency_gives_rate_one_and_rounds_the_amount(web_client) -> None:
    d = "2999-05-01"
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date=d, currency="ZZA", rate="1.5")

        body = web_client.get("/convert", params={"from": "ZZA", "to": "ZZA", "amount": "0.125", "date": d}).json()

    assert body["rate"] == "1.000000"
    assert body["result"] == "0.12"


def test_same_eur_gives_rate_one(web_client) -> None:
    d = "2999-05-02"
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date=d, currency="ZZA", rate="1.5")

        body = web_client.get("/convert", params={"from": "EUR", "to": "EUR", "amount": "2", "date": d}).json()

    assert body["rate"] == "1.000000"
    assert body["result"] == "2.00"


def test_zero_amount_gives_zero_with_two_decimals(web_client) -> None:
    d = "2999-06-01"
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date=d, currency="ZZA", rate="1.5")

        body = web_client.get("/convert", params={"from": "ZZA", "to": "EUR", "amount": "0", "date": d}).json()

    assert body["result"] == "0.00"


@pytest.mark.parametrize(("amount", "expected"), [("0.125", "0.12"), ("0.135", "0.14"), ("0.145", "0.14")])
def test_result_rounds_half_to_even(web_client, amount: str, expected: str) -> None:
    d = "2999-07-01"
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date=d, currency="ZZA", rate="1")

        body = web_client.get("/convert", params={"from": "ZZA", "to": "EUR", "amount": amount, "date": d}).json()

    assert body["result"] == expected


@pytest.mark.parametrize(("target_rate", "expected"), [("0.0000025", "0.000002"), ("0.0000035", "0.000004")])
def test_pair_rate_rounds_half_to_even_at_six_decimals(web_client, target_rate: str, expected: str) -> None:
    d = "2999-07-02"
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date=d, currency="ZZB", rate=target_rate)

        body = web_client.get("/convert", params={"from": "EUR", "to": "ZZB", "amount": "1", "date": d}).json()

    assert body["rate"] == expected


@pytest.mark.parametrize("amount", ["-1", "1e3", "abc", ".5", "1,5", "", "1."])
def test_malformed_amount_is_unprocessable(web_client, amount: str) -> None:
    d = "2999-08-01"
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date=d, currency="ZZA", rate="1")

        response = web_client.get("/convert", params={"from": "EUR", "to": "ZZA", "amount": amount, "date": d})

    assert response.status_code == 422


@pytest.mark.parametrize("date", ["2999-02-30", "2999-13-01", "not-a-date", "20990101"])
def test_malformed_or_impossible_date_is_unprocessable(web_client, date: str) -> None:
    response = web_client.get("/convert", params={"from": "EUR", "to": "ZZA", "amount": "1", "date": date})

    assert response.status_code == 422


@pytest.mark.parametrize(
    "params",
    [
        {"to": "ZZA", "amount": "1"},
        {"from": "EUR", "amount": "1"},
        {"from": "EUR", "to": "ZZA"},
    ],
)
def test_missing_parameter_is_unprocessable(web_client, params: dict[str, str]) -> None:
    response = web_client.get("/convert", params=params)

    assert response.status_code == 422


def test_unknown_currency_is_not_found(web_client) -> None:
    d = "2999-08-02"
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date=d, currency="ZZA", rate="1")

        response = web_client.get("/convert", params={"from": "ZZA", "to": "ZZQ", "amount": "1", "date": d})

    assert response.status_code == 404


def test_no_publication_on_or_before_the_date_is_not_found(web_client) -> None:
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date="2999-09-05", currency="ZZA", rate="1")

        response = web_client.get("/convert", params={"from": "EUR", "to": "ZZA", "amount": "1", "date": "2999-09-01"})

    assert response.status_code == 404


def test_empty_store_without_date_is_not_found(web_client) -> None:
    with db_session() as db:
        empty_store(db)

        response = web_client.get("/convert", params={"from": "EUR", "to": "ZZA", "amount": "1"})

    assert response.status_code == 404


def test_zero_stored_rate_is_unprocessable(web_client) -> None:
    d = "2999-09-10"
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date=d, currency="ZZA", rate="0")

        response = web_client.get("/convert", params={"from": "EUR", "to": "ZZA", "amount": "1", "date": d})

    assert response.status_code == 422


def test_service_matches_the_route(web_client) -> None:
    d = "2999-10-01"
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date=d, currency="ZZA", rate="3")

        body = web_client.get("/convert", params={"from": "EUR", "to": "ZZA", "amount": "9", "date": d}).json()
        direct = convert_service.convert("EUR", "ZZA", "9", d)

    assert body == direct
