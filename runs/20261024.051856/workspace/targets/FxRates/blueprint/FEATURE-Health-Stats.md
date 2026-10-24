# FEATURE: Health Stats

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Provide service health and live rates-store statistics. |
| Depends On  | FEATURE-API-Foundation.md, DATABASE.md |
| Provides    | GET /health, GET /stats |
| Consumes    | rates repository operations |

## Purpose

Expose a health response and statistics derived from the rates currently stored. Statistics include the number of distinct publication dates with rates, the total number of stored rates, and the first and last publication dates. Empty stores report null date bounds.

## Routes

- `GET /health` returns HTTP 200 with a JSON object whose `status` is `"ok"`.
- `GET /stats` returns HTTP 200 with `dates`, `rates`, `first`, and `last`, calculated from current stored rows. A load completed while the service runs is visible on the next request.

## Programmatic Acceptance

=== AC health-route ===
Intent: The health route is reachable and returns a successful response.

from app_server.testing import web_client

client = web_client()
response = client.get("/health")
assert response.status_code == 200
assert response.json()["status"] == "ok"
=== END AC health-route ===

=== AC stats-route ===
Intent: The statistics route is reachable and returns the declared response fields.

from app_server.testing import web_client

response = web_client().get("/stats")
assert response.status_code == 200
body = response.json()
assert {"dates", "rates", "first", "last"} <= body.keys()
assert isinstance(body["dates"], int)
assert isinstance(body["rates"], int)
=== END AC stats-route ===

=== AC stats-reflects-stored-rates ===
Intent: Statistics reflect a rate inserted before the request.

from app_server.testing import web_client
from persistence.testing import committed_session

date = "2099-01-08"
currency = "ZZT"
rate = "8.901"

with committed_session() as db:
    db.rates.upsert(date=date, currency=currency, rate=rate)

try:
    response = web_client().get("/stats")
    assert response.status_code == 200
    body = response.json()
    assert body["dates"] >= 1
    assert body["rates"] >= 1
    assert body["first"] is not None
    assert body["last"] is not None
finally:
    with committed_session() as db:
        db.rates.delete(date=date, currency=currency)
=== END AC stats-reflects-stored-rates ===

## User Acceptance

- None.

## Guardrails

- Derive all counts and date bounds from the rates store; do not hardcode them.
- All database access goes through the generated persistence package.
