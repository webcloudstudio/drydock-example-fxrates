# FEATURE: Currency History

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Returns ordered currency rates and exact statistics over optional date bounds. |
| Depends On  | DATABASE.md, ARCHITECTURE.md |
| Provides    | GET /history/{code} |
| Consumes    | `FEATURE-RATE-003` rates.list_currency |

## Purpose

Return stored history for a currency, with optional inclusive date bounds. Statistics are calculated from all returned points using exact decimals.

## Workflow

`GET /history/{code}` returns points in ascending date order. With no points in the selected range, return an empty list and null `min`, `max`, and `mean`. Otherwise `min` and `max` preserve the published text of the rates with the smallest and largest numeric values, and `mean` is rounded half-even to six decimal places as a fixed-width string.

Malformed `start` or `end` dates return 422. A currency with no stored rate anywhere returns 404, including EUR.

## Database Interface

- `FEATURE-RATE-003` — read: list rates for one currency - supplies: `currency` - returns: `date`, `currency`, `rate`

## Guardrails

- Use Decimal for comparisons and statistics; never use binary floating point.
- Apply date bounds inclusively.
- Distinguish a known currency with an empty selected range from a currency with no stored rates.

## Programmatic Acceptance

=== AC history-range ===
Intent: The history route returns its arranged points in order and reports the arranged rate values.

from persistence.testing import db_session
from app_server.testing import web_client

currency = "ZZZ"
first_date = "2098-05-01"
second_date = "2098-05-02"
first_rate = "1.00"
second_rate = "2.00"
with db_session() as db:
    db.rates.upsert(date=first_date, currency=currency, rate=first_rate)
    db.rates.upsert(date=second_date, currency=currency, rate=second_rate)
    response = web_client().get(
        f"/history/{currency}",
        params={"start": first_date, "end": second_date},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["currency"] == currency
    assert body["base"] == "EUR"
    assert [point["date"] for point in body["points"]] == [first_date, second_date]
    assert [point["rate"] for point in body["points"]] == [first_rate, second_rate]
    assert body["count"] == 2
    assert body["min"] == first_rate
    assert body["max"] == second_rate
=== END AC history-range ===

=== AC history-empty-and-errors ===
Intent: Known currencies with no points in a selected range return empty statistics, while unknown currencies and malformed bounds use their declared statuses.

from persistence.testing import db_session
from app_server.testing import web_client

currency = "ZZZ"
date = "2098-05-03"
with db_session() as db:
    db.rates.upsert(date=date, currency=currency, rate="1.5")
    client = web_client()
    empty = client.get(f"/history/{currency}", params={"start": "2099-01-01"})
    assert empty.status_code == 200
    body = empty.json()
    assert body["count"] == 0
    assert body["min"] is None and body["max"] is None and body["mean"] is None
    assert body["points"] == []
    assert client.get("/history/XXX").status_code == 404
    assert client.get(f"/history/{currency}", params={"start": "2025-01-31-x"}).status_code == 422
=== END AC history-empty-and-errors ===
