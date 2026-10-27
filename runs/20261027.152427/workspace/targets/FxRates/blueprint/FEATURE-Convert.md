# FEATURE: Convert

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | GET /convert converts an amount between two currencies with exact decimal arithmetic rounded half to even. |
| Depends On | FEATURE-RatesByDate.md, DATABASE.md |
| Provides | GET /convert |
| Consumes | fxrates_app.rates.effective_date, rates repository operations |

## Purpose

Answer "how much of currency B is this amount of currency A" on a date, from stored ECB rates.

## Behavior

- Query parameters: `from`, `to`, `amount` matching `[0-9]+(\.[0-9]+)?`, and optional `date`.
- Effective date: with `date`, `effective_date(date)`; without it, the latest publication date.
- EUR has the implicit rate 1. Any other currency's rate is read from the effective date's rates.
- `rate = rate(to) / rate(from)` computed with `decimal`, rounded half to even to six decimals, returned as a string with exactly six decimals.
- `result = amount * rate(to) / rate(from)` computed exactly from the stored rates, not from the rounded `rate`, rounded half to even to two decimals, returned as a string with exactly two decimals.
- `amount` is echoed as given, as a string. The body is `{date, from, to, amount, rate, result}`.
- Same `from` and `to` gives rate `1.000000` and the amount rounded half to even to two decimals. Amount `0` gives `0.00`.
- No floating point is used anywhere.

## Database Interface

- None — persistence is owned by DATABASE.md.

## Programmatic Acceptance

=== AC convert-two-currencies ===
Intent: Converting ZZA to ZZB on a seeded date returns the effective date, a six-decimal rate and a two-decimal result derived with Decimal from the seeded rates, rounded half to even.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from decimal import Decimal, ROUND_HALF_EVEN
from persistence.testing import db_session
from app_server.testing import web_client

d = "2999-01-01"
rate_from = "1.0298"
rate_to = "0.84453"
amount = "100"

with db_session() as db:
    db.rates.replace_rate(date=d, currency="ZZA", rate=rate_from)
    db.rates.replace_rate(date=d, currency="ZZB", rate=rate_to)
    client = web_client()
    response = client.get("/convert", params={"from": "ZZA", "to": "ZZB", "amount": amount, "date": d})
    assert response.status_code == 200
    body = response.json()
    expected_rate = (Decimal(rate_to) / Decimal(rate_from)).quantize(Decimal("0.000001"), rounding=ROUND_HALF_EVEN)
    expected_result = (Decimal(amount) * Decimal(rate_to) / Decimal(rate_from)).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
    assert body["date"] == d
    assert body["from"] == "ZZA"
    assert body["to"] == "ZZB"
    assert body["amount"] == amount
    assert body["rate"] == f"{expected_rate:.6f}"
    assert body["result"] == f"{expected_result:.2f}"
=== END AC convert-two-currencies ===

=== AC convert-eur-implicit-rate ===
Intent: EUR to a stored currency uses rate 1 for EUR, and a stored currency to EUR divides by the stored rate; the effective date is the latest publication on or before a weekend-style gap date.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from decimal import Decimal, ROUND_HALF_EVEN
from persistence.testing import db_session
from app_server.testing import web_client

published = "2999-02-01"
requested = "2999-02-03"
rate_zza = "161.77"
amount = "250.25"

with db_session() as db:
    db.rates.replace_rate(date=published, currency="ZZA", rate=rate_zza)
    client = web_client()
    out = client.get("/convert", params={"from": "EUR", "to": "ZZA", "amount": amount, "date": requested})
    assert out.status_code == 200
    body = out.json()
    expected_rate = (Decimal(rate_zza) / Decimal(1)).quantize(Decimal("0.000001"), rounding=ROUND_HALF_EVEN)
    expected_result = (Decimal(amount) * Decimal(rate_zza)).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
    assert body["date"] == published
    assert body["rate"] == f"{expected_rate:.6f}"
    assert body["result"] == f"{expected_result:.2f}"
    back = client.get("/convert", params={"from": "ZZA", "to": "EUR", "amount": "1000", "date": requested})
    assert back.status_code == 200
    back_rate = (Decimal(1) / Decimal(rate_zza)).quantize(Decimal("0.000001"), rounding=ROUND_HALF_EVEN)
    back_result = (Decimal("1000") / Decimal(rate_zza)).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
    assert back.json()["rate"] == f"{back_rate:.6f}"
    assert back.json()["result"] == f"{back_result:.2f}"
=== END AC convert-eur-implicit-rate ===

=== AC convert-default-latest ===
Intent: Without date the latest publication date is used: a seeded date later than any real one is the effective date.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from persistence.testing import db_session
from app_server.testing import web_client

older = "2999-03-01"
newest = "2999-03-09"

with db_session() as db:
    db.rates.replace_rate(date=older, currency="ZZA", rate="2")
    db.rates.replace_rate(date=older, currency="ZZB", rate="3")
    db.rates.replace_rate(date=newest, currency="ZZA", rate="2")
    db.rates.replace_rate(date=newest, currency="ZZB", rate="5")
    client = web_client()
    response = client.get("/convert", params={"from": "ZZA", "to": "ZZB", "amount": "2.00"})
    assert response.status_code == 200
    assert response.json()["date"] == newest
=== END AC convert-default-latest ===

=== AC convert-same-currency-and-zero ===
Intent: Same from and to gives rate 1.000000 and the amount rounded half to even (derived with Decimal from a tie amount); amount 0 gives 0.00.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from decimal import Decimal, ROUND_HALF_EVEN
from persistence.testing import db_session
from app_server.testing import web_client

d = "2999-04-01"
tie = "0.125"
zero = "0"

with db_session() as db:
    db.rates.replace_rate(date=d, currency="ZZA", rate="1.5")
    client = web_client()
    same = client.get("/convert", params={"from": "ZZA", "to": "ZZA", "amount": tie, "date": d})
    assert same.status_code == 200
    expected = (Decimal(tie) * Decimal("1.5") / Decimal("1.5")).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
    assert same.json()["rate"] == f"{Decimal(1):.6f}"
    assert same.json()["result"] == f"{expected:.2f}"
    eur = client.get("/convert", params={"from": "EUR", "to": "EUR", "amount": tie, "date": d})
    assert eur.status_code == 200
    assert eur.json()["rate"] == f"{Decimal(1):.6f}"
    assert eur.json()["result"] == f"{expected:.2f}"
    zero_response = client.get("/convert", params={"from": "ZZA", "to": "EUR", "amount": zero, "date": d})
    assert zero_response.status_code == 200
    assert zero_response.json()["result"] == f"{Decimal(0):.2f}"
=== END AC convert-same-currency-and-zero ===

## User Acceptance

- None.

## Guardrails

- All arithmetic uses `decimal`; no floating point.
- `result` is computed from the stored rates, never from the rounded `rate`.
- Rounding is half to even; `rate` has exactly six decimals and `result` exactly two.
- No rate, date, or value is hardcoded in application code.
