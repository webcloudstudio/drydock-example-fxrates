"""GET /rates/{date} and fxrates_app.rates.effective_date.

Each test shares one acceptance transaction with the web client and rolls back at the end. Tests
that depend on which publications exist start from an emptied store inside that transaction.
"""

from __future__ import annotations

from collections.abc import Iterator

import pytest

from fxrates_app.rates import effective_date
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


def test_exact_publication_date_returns_its_rates_as_stored_text(web_client) -> None:
    d = "1900-10-01"
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date=d, currency="ZZA", rate="1.50")
        db.rates.replace_rate(date=d, currency="ZZB", rate="2.250")

        response = web_client.get(f"/rates/{d}")

        assert response.status_code == 200
        body = response.json()
        assert body == {
            "date": d,
            "requested": d,
            "base": "EUR",
            "rates": {"ZZA": "1.50", "ZZB": "2.250"},
        }
        stored = {r.currency: r.rate for r in db.rates.list_for_date(date=d)}
        assert body["rates"] == stored


def test_date_between_publications_resolves_to_the_earlier_one(web_client) -> None:
    early = "1900-10-01"
    late = "1900-10-05"
    between = "1900-10-03"
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date=early, currency="ZZA", rate="1.50")
        db.rates.replace_rate(date=late, currency="ZZA", rate="1.6")

        body = web_client.get(f"/rates/{between}").json()

    assert body["date"] == early
    assert body["requested"] == between
    assert body["rates"] == {"ZZA": "1.50"}


def test_date_after_a_later_publication_resolves_to_it(web_client) -> None:
    early = "1900-10-01"
    late = "1900-10-05"
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date=early, currency="ZZA", rate="1")
        db.rates.replace_rate(date=late, currency="ZZA", rate="2")

        body = web_client.get("/rates/1900-10-09").json()

    assert body["date"] == late
    assert body["requested"] == "1900-10-09"
    assert body["rates"] == {"ZZA": "2"}


def test_base_currency_never_appears_in_the_rates(web_client) -> None:
    d = "1900-10-06"
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date=d, currency="EUR", rate="1")
        db.rates.replace_rate(date=d, currency="ZZA", rate="2")

        body = web_client.get(f"/rates/{d}").json()

    assert "EUR" not in body["rates"]
    assert body["rates"] == {"ZZA": "2"}


def test_date_before_every_publication_is_not_found(web_client) -> None:
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date="1900-10-05", currency="ZZA", rate="1")

        response = web_client.get("/rates/1900-10-01")

    assert response.status_code == 404


def test_date_on_an_empty_store_is_not_found(web_client) -> None:
    with db_session() as db:
        empty_store(db)

        response = web_client.get("/rates/1900-10-01")

    assert response.status_code == 404


@pytest.mark.parametrize(
    "path",
    [
        "/rates/2025-13-01",
        "/rates/2025-02-30",
        "/rates/2025-02-29",
        "/rates/not-a-date",
        "/rates/2025-01-31-x",
        "/rates/2025-1-1",
        "/rates/20251031",
        "/rates/2025-01-31T00:00:00",
    ],
)
def test_malformed_or_impossible_date_is_unprocessable(web_client, path: str) -> None:
    response = web_client.get(path)

    assert response.status_code == 422


def test_leap_day_is_accepted_when_it_is_a_real_date(web_client) -> None:
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date="2024-02-29", currency="ZZA", rate="1")

        response = web_client.get("/rates/2024-02-29")

    assert response.status_code == 200
    assert response.json()["date"] == "2024-02-29"


def test_effective_date_is_the_latest_publication_on_or_before(web_client) -> None:
    early = "1900-10-01"
    late = "1900-10-05"
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date=early, currency="ZZA", rate="1")
        db.rates.replace_rate(date=late, currency="ZZA", rate="2")

        assert effective_date("1900-10-03") == early
        assert effective_date(late) == late
        assert effective_date("1899-12-31") is None


def test_effective_date_is_none_on_an_empty_store() -> None:
    with db_session() as db:
        empty_store(db)

        assert effective_date("2030-01-01") is None


def test_rates_route_matches_effective_date_function(web_client) -> None:
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date="1900-10-02", currency="ZZA", rate="7")

        body = web_client.get("/rates/1900-10-04").json()

        assert body["date"] == effective_date("1900-10-04") == "1900-10-02"
