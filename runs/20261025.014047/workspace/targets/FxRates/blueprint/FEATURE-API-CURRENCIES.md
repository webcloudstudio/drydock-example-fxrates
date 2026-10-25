# FEATURE: API Currencies

| Field       | Value |
|-------------|-------|
| Version     | 20261025 V1 |
| Description | Lists currencies with stored rates. |
| Depends On  | DATABASE.md, ARCHITECTURE.md |
| Provides    | GET /currencies |
| Consumes    | rates.list |

## Purpose

List EUR as the base currency and every currency with at least one stored rate, in ascending code order.

## Route

`GET /currencies` returns JSON containing `base` and `currencies`.

## Programmatic Acceptance

=== AC currencies-route-responds ===
Intent: The currency catalog endpoint responds successfully with its declared fields.
Suite: scoped

from app_server.testing import web_client

response = web_client().get("/currencies")
assert response.status_code == 200
body = response.json()
assert body["base"] == "EUR"
assert isinstance(body["currencies"], list)
assert body["currencies"] == sorted(body["currencies"])
=== END AC currencies-route-responds ===

## User Acceptance

- None.

## Guardrails

- Include only currencies with at least one stored rate.
- Return currencies in ascending order and EUR as the base.
- Access persistent data only through the shipped persistence library.
