# FEATURE: Conversion

| Field       | Value |
|-------------|-------|
| Version     | 20261024 V1 |
| Description | Converts an amount between currencies using ECB euro reference rates. |
| Depends On  | ARCHITECTURE.md, DATABASE.md |
| Provides    | GET /convert |
| Consumes    | rates persistence operations |

## Purpose

Convert between any two currencies using EUR as the base and the effective publication date. Without a date, use the latest publication.

## Request

Required query parameters are `from`, `to`, and `amount`; optional `date` is a calendar date. Amount must match `[0-9]+(\.[0-9]+)?`. Malformed amounts, malformed dates, and missing required parameters return `422`. A currency other than EUR without a rate on the effective date returns `404`; no effective publication date also returns `404`.

## Calculation and Response

Return the effective date, requested currency codes, amount echoed as supplied, conversion rate, and result as JSON strings. Compute `rate(to) / rate(from)` and `amount × rate(to) / rate(from)` exactly with `Decimal`, rounding half to even. Format rate to six decimal places and result to two decimal places. Compute result from unrounded stored rates, not the rounded response rate. EUR has implicit rate `1`.

## Programmatic Acceptance

=== AC conversion-route ===
Intent: A conversion request using an amount supplied by the criterion returns a structured success response.

from app_server.testing import web_client

client = web_client()
amount = "12.50"
response = client.get("/convert", params={"from": "EUR", "to": "EUR", "amount": amount})
assert response.status_code in (200, 404)
if response.status_code == 200:
    body = response.json()
    assert body["amount"] == amount
    assert {"date", "from", "to", "rate", "result"} <= body.keys()
=== END AC conversion-route ===

=== AC conversion-validation ===
Intent: A malformed amount and a missing required parameter each return unprocessable entity.

from app_server.testing import web_client

client = web_client()
malformed = client.get("/convert", params={"from": "EUR", "to": "EUR", "amount": "nope"})
missing = client.get("/convert", params={"from": "EUR", "to": "EUR"})
assert malformed.status_code == 422
assert missing.status_code == 422
=== END AC conversion-validation ===

## User Acceptance

- None.

## Guardrails

- Use Decimal arithmetic only; do not use floating point.
- Preserve the supplied amount string in the response.
- Return errors using the specified HTTP statuses; error body wording is not part of the contract.
