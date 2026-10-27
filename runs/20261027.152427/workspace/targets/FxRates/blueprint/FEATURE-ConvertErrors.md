# FEATURE: Convert Errors

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | GET /convert refuses unknown currencies and missing publications with 404 and bad or missing inputs with 422. |
| Depends On | FEATURE-Convert.md |
| Provides | convert error contract |
| Consumes | GET /convert |

## Purpose

Fix the failure statuses of `/convert`.

## Behavior

- 404: a currency other than EUR with no rate on the effective date; no publication on or before the requested date; no publication stored at all.
- 422 (FastAPI request validation): missing `from`, `to`, or `amount`; `amount` not matching `[0-9]+(\.[0-9]+)?`; a malformed or impossible `date`.
- Error-response bodies are not part of the contract.

## Programmatic Acceptance

=== AC convert-unknown-currency-404 ===
Intent: A currency with no stored rate on the effective date answers 404, whichever side it is on.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from persistence.testing import db_session
from app_server.testing import web_client

d = "2999-05-01"

with db_session() as db:
    db.rates.replace_rate(date=d, currency="ZZA", rate="1.5")
    client = web_client()
    to_unknown = client.get("/convert", params={"from": "ZZA", "to": "ZZX", "amount": "1", "date": d})
    assert to_unknown.status_code == 404
    from_unknown = client.get("/convert", params={"from": "ZZX", "to": "ZZA", "amount": "1", "date": d})
    assert from_unknown.status_code == 404
=== END AC convert-unknown-currency-404 ===

=== AC convert-no-publication-404 ===
Intent: A date earlier than every publication answers 404 even for stored currencies.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from persistence.testing import db_session
from app_server.testing import web_client

with db_session() as db:
    db.rates.replace_rate(date="2999-06-01", currency="ZZA", rate="1.5")
    client = web_client()
    response = client.get("/convert", params={"from": "ZZA", "to": "EUR", "amount": "10", "date": "0001-01-01"})
    assert response.status_code == 404
=== END AC convert-no-publication-404 ===

=== AC convert-validation-422 ===
Intent: Missing parameters, a malformed amount, and malformed or impossible dates are all refused with 422.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from app_server.testing import web_client

client = web_client()
base = {"from": "USD", "to": "GBP", "amount": "1"}

for missing in ["from", "to", "amount"]:
    params = {k: v for k, v in base.items() if k != missing}
    assert client.get("/convert", params=params).status_code == 422, missing

for bad_amount in ["abc", "-1", "1.", ".5", "1e3"]:
    params = dict(base, amount=bad_amount)
    assert client.get("/convert", params=params).status_code == 422, bad_amount

for bad_date in ["2025-13-01", "2025-01-31-x", "yesterday"]:
    params = dict(base, date=bad_date)
    assert client.get("/convert", params=params).status_code == 422, bad_date
=== END AC convert-validation-422 ===

## User Acceptance

- None.

## Guardrails

- Validation statuses come from FastAPI request validation, not hand-built responses.
- Error-response bodies and wording are never part of the contract.
