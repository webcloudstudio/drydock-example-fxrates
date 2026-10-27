"""GET /history/{code} summary fields: count, min, max, and mean over the points the response lists.

Each test shares one acceptance transaction with the web client and rolls back at the end. Expected
values are derived with Decimal from the seeded rate texts; min and max are compared as the stored
text, never re-formatted.
"""

from __future__ import annotations

from collections.abc import Iterator
from decimal import ROUND_HALF_EVEN, Decimal

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


def mean_of(texts: list[str]) -> str:
    """Return the exact mean of `texts`, rounded half to even at six decimals, with six decimals."""
    total = sum(Decimal(text) for text in texts)
    return f"{(total / len(texts)).quantize(Decimal('0.000001'), rounding=ROUND_HALF_EVEN):.6f}"


def test_count_is_the_number_of_points(web_client) -> None:
    code = "ZZH"
    rates = {
        "1900-12-01": "0.9453",
        "1900-12-02": "0.943",
        "1900-12-03": "0.9441",
        "1900-12-04": "10.5",
        "1900-12-05": "9.75",
    }
    with db_session() as db:
        empty_store(db)
        for d, r in rates.items():
            db.rates.replace_rate(date=d, currency=code, rate=r)

        body = web_client.get(f"/history/{code}").json()

    assert body["count"] == len(rates)


def test_min_is_the_smallest_rate_by_decimal_value_as_stored_text(web_client) -> None:
    code = "ZZH"
    rates = {"1900-12-01": "0.9453", "1900-12-02": "0.943", "1900-12-04": "10.5", "1900-12-05": "9.75"}
    with db_session() as db:
        empty_store(db)
        for d, r in rates.items():
            db.rates.replace_rate(date=d, currency=code, rate=r)

        body = web_client.get(f"/history/{code}").json()

    assert body["min"] == "0.943"


def test_max_is_the_largest_rate_by_decimal_value_as_stored_text(web_client) -> None:
    code = "ZZH"
    rates = {"1900-12-01": "0.9453", "1900-12-02": "0.943", "1900-12-04": "10.5", "1900-12-05": "9.75"}
    with db_session() as db:
        empty_store(db)
        for d, r in rates.items():
            db.rates.replace_rate(date=d, currency=code, rate=r)

        body = web_client.get(f"/history/{code}").json()

    assert body["max"] == "10.5"


def test_min_and_max_keep_trailing_zeros_of_the_stored_text(web_client) -> None:
    code = "ZZH"
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date="1900-12-06", currency=code, rate="2.50")
        db.rates.replace_rate(date="1900-12-07", currency=code, rate="3.000")

        body = web_client.get(f"/history/{code}").json()

    assert body["min"] == "2.50"
    assert body["max"] == "3.000"


def test_mean_is_half_even_at_six_decimals_for_the_first_tie(web_client) -> None:
    code = "ZZM"
    rates = {"1901-01-01": "1.000000", "1901-01-02": "1.000001"}
    with db_session() as db:
        empty_store(db)
        for d, r in rates.items():
            db.rates.replace_rate(date=d, currency=code, rate=r)

        body = web_client.get(f"/history/{code}").json()

    assert body["mean"] == mean_of(list(rates.values()))
    assert body["mean"] == "1.000000"


def test_mean_is_half_even_at_six_decimals_for_the_second_tie(web_client) -> None:
    code = "ZZN"
    rates = {"1901-01-01": "1.000001", "1901-01-02": "1.000002"}
    with db_session() as db:
        empty_store(db)
        for d, r in rates.items():
            db.rates.replace_rate(date=d, currency=code, rate=r)

        body = web_client.get(f"/history/{code}").json()

    assert body["mean"] == mean_of(list(rates.values()))
    assert body["mean"] == "1.000002"


def test_mean_is_written_with_exactly_six_decimals(web_client) -> None:
    code = "ZZP"
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date="1901-01-03", currency=code, rate="2")
        db.rates.replace_rate(date="1901-01-04", currency=code, rate="3")

        body = web_client.get(f"/history/{code}").json()

    assert body["mean"] == "2.500000"


def test_statistics_cover_only_the_points_inside_the_bounds(web_client) -> None:
    code = "ZZH"
    rates = {"1901-02-01": "100", "1901-02-02": "1.5", "1901-02-03": "2.25", "1901-02-04": "0.5"}
    start = "1901-02-02"
    end = "1901-02-03"
    inside = [rates[d] for d in sorted(rates) if start <= d <= end]
    with db_session() as db:
        empty_store(db)
        for d, r in rates.items():
            db.rates.replace_rate(date=d, currency=code, rate=r)

        body = web_client.get(f"/history/{code}", params={"start": start, "end": end}).json()

    assert body["count"] == len(inside)
    assert body["min"] == min(inside, key=Decimal)
    assert body["max"] == max(inside, key=Decimal)
    assert body["mean"] == mean_of(inside)


def test_empty_range_reports_count_zero_and_null_statistics(web_client) -> None:
    code = "ZZH"
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date="1901-03-01", currency=code, rate="4")

        response = web_client.get(f"/history/{code}", params={"start": "1901-04-01"})

    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 0
    assert body["min"] is None
    assert body["max"] is None
    assert body["mean"] is None
    assert body["points"] == []


def test_single_point_is_its_own_min_max_and_mean(web_client) -> None:
    code = "ZZH"
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date="1901-05-01", currency=code, rate="0.9430")

        body = web_client.get(f"/history/{code}").json()

    assert body["count"] == 1
    assert body["min"] == "0.9430"
    assert body["max"] == "0.9430"
    assert body["mean"] == "0.943000"


def test_summary_fields_are_present_alongside_the_existing_fields(web_client) -> None:
    code = "ZZH"
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date="1901-05-02", currency=code, rate="1")

        body = web_client.get(f"/history/{code}").json()

    assert set(body) == {"currency", "base", "count", "min", "max", "mean", "points"}


def test_summary_helper_on_no_points_returns_null_statistics() -> None:
    assert history_service.history_summary([]) == {"count": 0, "min": None, "max": None, "mean": None}


def test_summary_helper_matches_the_route(web_client) -> None:
    code = "ZZH"
    with db_session() as db:
        empty_store(db)
        db.rates.replace_rate(date="1901-06-01", currency=code, rate="5")
        db.rates.replace_rate(date="1901-06-02", currency=code, rate="6")

        body = web_client.get(f"/history/{code}").json()
        direct = history_service.history_summary(history_service.history_points(code))

    assert {key: body[key] for key in direct} == direct
