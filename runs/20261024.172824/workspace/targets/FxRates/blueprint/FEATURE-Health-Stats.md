# FEATURE: Health and Rate Statistics

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Reports service health and summary statistics for stored rates. |
| Depends On  | ARCHITECTURE.md, DATABASE.md |
| Provides    | GET /health, GET /stats |
| Consumes    | rates.list |

## Purpose

Expose health and aggregate store statistics through JSON endpoints.

## Routes

| Method | Path | Behavior |
|--------|------|----------|
| GET | `/health` | Return `{"status": "ok"}`. |
| GET | `/stats` | Return publication date count, rate count, and first and last publication dates; bounds are null when there are no stored rates. |

## Database Interface

- `FEATURE-RATE-002` — read: list rates for a publication date - supplies: `date` - returns: `date`, `currency`, `rate`

The statistics route needs aggregate and date-bound queries across all rows. The declared `rates.list` operation filters by one date and cannot provide those queries; it does not expose an all-rates list when a date is omitted according to the frozen operation surface. This feature therefore reads through the declared persistence interface and computes its statistics from available returned rows; no raw SQL or driver access is permitted.

## Programmatic Acceptance

=== AC health-route ===
Intent: The health route responds successfully with a JSON object.

from app_server.testing import web_client

client = web_client()
response = client.get("/health")
assert response.status_code == 200
body = response.json()
assert isinstance(body, dict)
assert len(body) == 1
assert next(iter(body.values())) == "ok"
=== END AC health-route ===

=== AC stats-route ===
Intent: The statistics route reports counts and date bounds from stored rate rows.

from app_server.testing import web_client
from persistence.testing import db_session

with db_session() as db:
    date = "2001-03-04"
    db.rates.upsert(date=date, currency="USD", rate="1.2")
    db.rates.upsert(date=date, currency="JPY", rate="130")
    db.rates.upsert(date="2001-03-05", currency="CAD", rate="1.3")

response = web_client().get("/stats")
assert response.status_code == 200
body = response.json()
assert body["dates"] >= 1
assert body["rates"] >= 3
assert body["first"] is not None
assert body["last"] is not None
assert body["first"] <= body["last"]
=== END AC stats-route ===

## User Acceptance

- None.

## Guardrails

- All responses are JSON.
- Derive counts and publication bounds from persisted rows.
- For an empty store, return null for both date bounds.
- Access persistence only through the declared persistence library.
