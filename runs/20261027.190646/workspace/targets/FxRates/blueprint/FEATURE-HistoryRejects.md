# FEATURE: History Rejects

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | GET /history/{code} answers 404 for a currency with no stored rate at all and 422 for a malformed start or end date. |
| Depends On | FEATURE-HistoryEmpty.md |
| Provides | GET /history/{code} rejects |
| Consumes | GET /history/{code} empty |

## Purpose

Distinguish a currency the store has never held, or EUR, which is never stored, from a known currency with an empty range, and refuse malformed dates.

## Routes

| Route | Condition | Status |
|-------|-----------|--------|
| `GET /history/{code}` | The currency has no stored rate at all, including `EUR`, regardless of range | 404 |
| `GET /history/{code}` | `start` or `end` is not a real `YYYY-MM-DD` date | 422 |

## Behavior

- The 404 test considers all stored dates, not the requested range; a known currency with an empty range is 200 (FEATURE-HistoryEmpty.md).
- Date validation is FastAPI request validation.
- Error response bodies are not part of the contract.

## Database Interface

- None — persistence is owned by DATABASE.md.

## Programmatic Acceptance

=== AC history-unknown-currency ===
Intent: A currency with no stored rate returns 404 with or without a range, and EUR returns 404 even while other currencies are stored.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

route = "/history/{code}"
unknown = "ZZQ"
with db_session() as db:
    db.rates.replace_rate(date="1800-01-10", currency="ZZA", rate="1.5")
    client = web_client()
    for code in [unknown, "EUR"]:
        resp = client.get(route.format(code=code))
        assert resp.status_code == 404, code
        resp = client.get(
            route.format(code=code), params={"start": "1800-01-01", "end": "1800-12-31"}
        )
        assert resp.status_code == 404, code
=== END AC history-unknown-currency ===

=== AC history-known-currency-out-of-range ===
Intent: A currency with stored rates is not a 404 when the range is empty, so the 404 depends on the whole store and not the range.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

code = "ZZK"
route = "/history/{code}"
with db_session() as db:
    db.rates.replace_rate(date="1800-02-10", currency=code, rate="1.5")
    client = web_client()
    resp = client.get(route.format(code=code), params={"start": "1801-01-01"})
    assert resp.status_code == 200
    assert resp.json()["count"] == 0
=== END AC history-known-currency-out-of-range ===

=== AC history-malformed-dates ===
Intent: Malformed or impossible start and end dates on a stored currency are rejected with 422.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

code = "ZZD"
route = "/history/{code}"
bad_values = ["2025-01-31-x", "2025-13-01", "2025-02-30", "20250131", "today"]
with db_session() as db:
    db.rates.replace_rate(date="1800-03-10", currency=code, rate="1.5")
    client = web_client()
    for bad in bad_values:
        resp = client.get(route.format(code=code), params={"start": bad})
        assert resp.status_code == 422, ("start", bad, resp.status_code)
        resp = client.get(route.format(code=code), params={"end": bad})
        assert resp.status_code == 422, ("end", bad, resp.status_code)
        resp = client.get(route.format(code=code), params={"start": "1800-01-01", "end": bad})
        assert resp.status_code == 422, ("both", bad, resp.status_code)
=== END AC history-malformed-dates ===

## User Acceptance

- None.

## Guardrails

- A currency's absence is judged over all stored dates, never over the requested range.
- Do not hand-parse dates; rely on FastAPI request validation for 422.
