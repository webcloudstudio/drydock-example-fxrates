# FEATURE: Effective Date Rates

| Field | Value |
|-------|-------|
| Version | 20261025 V1 |
| Description | Retrieve rates for effective and latest publication dates. |
| Depends On | FEATURE-ApiFoundation.md, DATABASE.md |
| Provides | GET /rates/{date}, GET /rates/latest |
| Consumes | rates repository operations |

## Purpose

Resolve a requested date to the latest publication on or before it. Return all rates stored for that effective date. The latest route uses the latest publication date and reports `"latest"` as its requested value. Return 404 when no publication is available on or before a requested date or when the store has no rates.

## Database Interface


- None — persistence is owned by FEATURE-InitializeRates.md, FEATURE-LoadHistory.md.

## Programmatic Acceptance

=== AC effective_date_routes ===
Intent: Both rate routes return the stored publication selected by the effective-date rule.
Requires: python-package=httpx; scope=test

from persistence.testing import db_session
from app_server.testing import web_client

date = "2099-01-02"
currency = "ZZZ"
rate = "1.2300"
with db_session() as db:
    db.rates.upsert(date=date, currency=currency, rate=rate)

client = web_client()
response = client.get(f"/rates/{date}")
latest = client.get("/rates/latest")
assert response.status_code == 200
assert latest.status_code == 200
assert response.json()["date"] == date
assert response.json()["requested"] == date
assert response.json()["rates"][currency] == rate
assert latest.json()["date"] == date
assert latest.json()["requested"] == "latest"
assert latest.json()["rates"][currency] == rate
=== END AC effective_date_routes ===

=== AC no_prior_publication ===
Intent: A request before every stored publication returns 404.
Requires: python-package=httpx; scope=test

from persistence.testing import db_session
from app_server.testing import web_client

date = "2099-01-02"
currency = "ZZZ"
rate = "1.2300"
earlier = "2099-01-01"
with db_session() as db:
    db.rates.upsert(date=date, currency=currency, rate=rate)

response = web_client().get(f"/rates/{earlier}")
assert response.status_code == 404
=== END AC no_prior_publication ===

## User Acceptance

- None.

## Guardrails

- Preserve stored rate text in JSON strings.
- Date resolution is inclusive and uses the latest publication on or before the requested date.
- Do not embed dates, counts, or rates as application answers.
