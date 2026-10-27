"""HTTP behavior against criterion-owned records in the configured application store."""

import pytest

from app_server.testing import web_client
from services.rates import all_rows, db


@pytest.fixture
def client_with_rates():
    records = [
        ("2098-12-01", "QAX", "2.00"),
        ("2098-12-03", "QAX", "4.00"),
        ("2098-12-01", "QAY", "3.00"),
    ]
    baseline = all_rows()
    with db() as store:
        for day, code, rate in records:
            store.rates.upsert(date=day, currency=code, rate=rate)
    client = web_client()
    try:
        yield client, baseline
    finally:
        client.close()
        with db() as store:
            for day, code, _ in records:
                store.rates.delete(date=day, currency=code)


def test_health_currencies_stats_and_latest(client_with_rates):
    client, baseline = client_with_rates
    assert client.get("/health").json() == {"status": "ok"}
    currencies = client.get("/currencies")
    assert currencies.status_code == 200
    assert currencies.json()["currencies"] == sorted({row.currency for row in baseline} | {"QAX", "QAY"})
    stats = client.get("/stats").json()
    expected = {(row.date, row.currency): row.rate for row in baseline}
    expected.update({("2098-12-01", "QAX"): "2.00", ("2098-12-03", "QAX"): "4.00", ("2098-12-01", "QAY"): "3.00"})
    dates = {day for day, _ in expected}
    assert stats == {"dates": len(dates), "rates": len(expected), "first": min(dates), "last": max(dates)}
    latest_date = max(dates)
    latest_rates = {currency: rate for (day, currency), rate in expected.items() if day == latest_date}
    assert client.get("/rates/latest").json() == {"date": latest_date, "requested": "latest", "base": "EUR", "rates": latest_rates}


def test_effective_date_selects_latest_publication_not_after_request(client_with_rates):
    response = client_with_rates[0].get("/rates/2098-12-02")
    assert response.status_code == 200
    assert response.json() == {
        "date": "2098-12-01", "requested": "2098-12-02", "base": "EUR",
        "rates": {"QAX": "2.00", "QAY": "3.00"},
    }


def test_conversion_uses_decimal_and_half_even_rounding(client_with_rates):
    response = client_with_rates[0].get("/convert", params={"from": "QAX", "to": "QAY", "amount": "1.005", "date": "2098-12-01"})
    assert response.status_code == 200
    assert response.json()["rate"] == "1.500000"
    assert response.json()["result"] == "1.51"


def test_history_bounds_and_empty_range(client_with_rates):
    client = client_with_rates[0]
    body = client.get("/history/QAX", params={"start": "2098-12-01", "end": "2098-12-03"}).json()
    assert body["count"] == 2
    assert body["points"] == [{"date": "2098-12-01", "rate": "2.00"}, {"date": "2098-12-03", "rate": "4.00"}]
    assert body["mean"] == "3.000000"
    empty = client.get("/history/QAX", params={"start": "2098-12-04"}).json()
    assert (empty["count"], empty["min"], empty["max"], empty["mean"], empty["points"]) == (0, None, None, None, [])


@pytest.mark.parametrize(("path", "status"), [
    ("/rates/2098-02-30", 422), ("/rates/2097-01-01", 404),
    ("/history/ZZZ", 404), ("/history/QAX?start=2098-13-01", 422),
    ("/convert?from=QAX&to=NOX&amount=1", 404),
    ("/convert?from=QAX&to=QAY", 422),
    ("/convert?from=QAX&to=QAY&amount=NaN", 422),
])
def test_api_error_statuses(client_with_rates, path, status):
    response = client_with_rates[0].get(path)
    assert response.status_code == status
