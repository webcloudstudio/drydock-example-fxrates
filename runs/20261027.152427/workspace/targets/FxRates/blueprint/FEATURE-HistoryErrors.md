# FEATURE: History Errors

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | GET /history/{code} answers 404 for a currency with no stored rate and 422 for a malformed start or end. |
| Depends On | FEATURE-HistoryStats.md, DATABASE.md |
| Provides | history error contract |
| Consumes | GET /history/{code} |

## Purpose

Define the failure statuses of `GET /history/{code}`.

## Behavior

- A currency with no stored rate at all answers `404`. This includes `EUR`, which is the base and
  is never stored as a rate.
- A currency that has stored rates but none inside the requested bounds is not an error: it answers
  `200` with `count` 0.
- A malformed `start` or `end` (not a real calendar date `YYYY-MM-DD`, for example `2025-01-31-x`
  or `2025-13-01`) answers `422`. The status is produced by FastAPI request validation of date
  query parameters.
- Existence of a currency is judged on the whole stored history, not on the requested bounds.

## Database Interface

- `FEATURE-RATE-006` — read: list a currency's rates over a period - supplies: `currency` - returns: `date`

## Programmatic Acceptance

=== AC history-errors-unknown-currency ===
Intent: A currency with no stored rate answers 404, including EUR; neither code is seeded by this criterion.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

unknown = "ZZX"
base = "EUR"

with db_session() as db:
    assert db.rates.list_currency_history(currency=unknown) == []
    assert db.rates.list_currency_history(currency=base) == []
    client = web_client()
    assert client.get(f"/history/{unknown}").status_code == 404
    assert client.get(f"/history/{base}").status_code == 404
=== END AC history-errors-unknown-currency ===

=== AC history-errors-empty-range-is-not-404 ===
Intent: A known currency whose bounds exclude every point answers 200, so 404 is reserved for a currency with no stored rate at all.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

code = "ZZH"
stored = "1901-05-01"
after = "1901-06-01"

with db_session() as db:
    db.rates.replace_rate(date=stored, currency=code, rate="2")
    client = web_client()
    resp = client.get(f"/history/{code}", params={"start": after})
    assert resp.status_code == 200
    assert resp.json()["count"] == 0
=== END AC history-errors-empty-range-is-not-404 ===

=== AC history-errors-malformed-bounds ===
Intent: A malformed start or end is refused with 422 for a stored currency, whether the text is a bad shape or an impossible calendar date.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

code = "ZZH"
good = "1901-07-01"
bad_values = ["2025-01-31-x", "2025-13-01", "notadate"]

with db_session() as db:
    db.rates.replace_rate(date=good, currency=code, rate="5")
    client = web_client()
    for bad in bad_values:
        assert client.get(f"/history/{code}", params={"start": bad}).status_code == 422
        assert client.get(f"/history/{code}", params={"end": bad}).status_code == 422
        assert client.get(
            f"/history/{code}", params={"start": good, "end": bad}
        ).status_code == 422
=== END AC history-errors-malformed-bounds ===

## User Acceptance

- None.

## Guardrails

- A response body is never compared for error statuses; only the status code is the contract.
- Validation of dates is delegated to FastAPI request validation, not hand-rolled in the handler.
