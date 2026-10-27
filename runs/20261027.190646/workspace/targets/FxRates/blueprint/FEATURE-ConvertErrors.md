# FEATURE: Convert Errors

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | Error statuses of GET /convert: 404 for a missing publication or rate and 422 for malformed or missing parameters. |
| Depends On | FEATURE-ConvertLatest.md |
| Provides | GET /convert errors |
| Consumes | GET /convert latest default |

## Purpose

`GET /convert` refuses requests it cannot answer with the status the source defines. Decisions recorded: EUR to EUR still needs a publication on or before the effective date (Q-004).

## Routes

| Route | Condition | Status |
|-------|-----------|--------|
| `GET /convert` | No publication on or before the requested date | 404 |
| `GET /convert` | A currency other than EUR has no rate on the effective date | 404 |
| `GET /convert` | `amount` does not match `[0-9]+(\.[0-9]+)?` | 422 |
| `GET /convert` | Malformed `date`, or `from`, `to` or `amount` missing | 422 |

## Behavior

- Validation is FastAPI request validation; the 422 comes from the framework, not hand-built responses.
- EUR has the implicit rate `1` and never needs a stored rate, but the effective date must exist.
- The effective date is resolved first from the requested date, then each non-EUR currency is looked up on it.
- Error response bodies are not part of the contract.

## Database Interface

- None — persistence is owned by DATABASE.md.

## Programmatic Acceptance

=== AC convert-no-publication ===
Intent: A conversion dated before any publication answers 404, including EUR to EUR, because the effective date must exist.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client

client = web_client()
early = "0001-01-01"
for src, dst in [("EUR", "EUR"), ("USD", "GBP"), ("EUR", "JPY")]:
    resp = client.get("/convert", params={"from": src, "to": dst, "amount": "1", "date": early})
    assert resp.status_code == 404, (src, dst, resp.status_code)
=== END AC convert-no-publication ===

=== AC convert-missing-rate ===
Intent: A non-EUR currency with no rate on the effective date answers 404 on either side of the pair, while the seeded pair converts.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

date = "1800-05-01"
have = "ZZA"
missing = "ZZX"
with db_session() as db:
    db.rates.replace_rate(date=date, currency=have, rate="2")
    client = web_client()
    resp = client.get("/convert", params={"from": have, "to": missing, "amount": "1", "date": date})
    assert resp.status_code == 404
    resp = client.get("/convert", params={"from": missing, "to": have, "amount": "1", "date": date})
    assert resp.status_code == 404
    resp = client.get("/convert", params={"from": missing, "to": missing, "amount": "1", "date": date})
    assert resp.status_code == 404
    resp = client.get("/convert", params={"from": "EUR", "to": have, "amount": "1", "date": date})
    assert resp.status_code == 200
=== END AC convert-missing-rate ===

=== AC convert-malformed-amount ===
Intent: Amounts that do not match the digits-with-optional-fraction pattern are rejected with 422 even when the rest of the request is valid.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

date = "1800-05-02"
with db_session() as db:
    db.rates.replace_rate(date=date, currency="ZZA", rate="2")
    db.rates.replace_rate(date=date, currency="ZZB", rate="5")
    client = web_client()
    for bad in ["abc", "1.", ".5", "-1", "1e3", "1,5", ""]:
        resp = client.get(
            "/convert", params={"from": "ZZA", "to": "ZZB", "amount": bad, "date": date}
        )
        assert resp.status_code == 422, (bad, resp.status_code)
=== END AC convert-malformed-amount ===

=== AC convert-missing-parameters ===
Intent: Omitting any one of from, to or amount is a validation error answered 422.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client
from persistence.testing import db_session

date = "1800-05-03"
full = {"from": "ZZA", "to": "ZZB", "amount": "1", "date": date}
with db_session() as db:
    db.rates.replace_rate(date=date, currency="ZZA", rate="2")
    db.rates.replace_rate(date=date, currency="ZZB", rate="5")
    client = web_client()
    for name in ["from", "to", "amount"]:
        params = {k: v for k, v in full.items() if k != name}
        resp = client.get("/convert", params=params)
        assert resp.status_code == 422, (name, resp.status_code)
=== END AC convert-missing-parameters ===

=== AC convert-malformed-date ===
Intent: A malformed or impossible calendar date in the query is rejected with 422.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client

client = web_client()
for bad in ["2025-13-01", "2025-02-30", "20250101", "2025-01-31-x", "yesterday"]:
    resp = client.get(
        "/convert", params={"from": "USD", "to": "GBP", "amount": "1", "date": bad}
    )
    assert resp.status_code == 422, (bad, resp.status_code)
=== END AC convert-malformed-date ===

## User Acceptance

- None.

## Guardrails

- Error statuses come from FastAPI request validation or explicit 404 handling, never from catching and masking arithmetic errors.
- Error-response bodies are never compared by consumers; do not rely on message wording.
- No floating point in any validation or conversion path.
