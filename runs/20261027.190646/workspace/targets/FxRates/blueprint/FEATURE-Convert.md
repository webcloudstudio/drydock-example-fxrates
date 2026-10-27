# FEATURE: Convert

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | Serve GET /convert for an explicit date, converting an amount between two currencies with exact decimal arithmetic. |
| Depends On | FEATURE-WebFoundation.md, FEATURE-EffectiveDate.md |
| Provides | GET /convert |
| Consumes | rates.effective_publication |

## Purpose

Convert an amount from one currency to another using the euro reference rates on the effective date.

## Routes

| Route | Behavior |
|-------|----------|
| `GET /convert?from=<code>&to=<code>&amount=<amount>&date=<date>` | 200 with `{"date": <effective date>, "from": <code>, "to": <code>, "amount": <amount>, "rate": <rate>, "result": <result>}`; every value is a JSON string. |

## Behavior

- The router lives in `app_server/routers/convert.py`, included by `create_app()`. Parameters are
  `from` (Python name via alias), `to`, `amount` and `date`.
- The effective date and rates come from `services.effective_date.effective_publication`.
- EUR has the implicit rate `1`; any other currency takes its stored rate on the effective date.
- All arithmetic uses `decimal.Decimal` from the stored text. Never use floats.
- `rate` = `rate(to) / rate(from)`, rounded half to even to six decimals, written with exactly six decimals.
- `result` = `amount * rate(to) / rate(from)`, computed from the stored rates and never from the rounded
  `rate`, rounded half to even to two decimals, written with exactly two decimals.
- `amount` is echoed exactly as given, as a string, and must match `[0-9]+(\.[0-9]+)?`.
- Handling of missing publications, unknown currencies and invalid parameters is specified by
  FEATURE-ConvertErrors.md; this story implements the successful conversion.

## Database Interface

- None — persistence is reached through `rates.effective_publication` in FEATURE-EffectiveDate.md.

## Programmatic Acceptance

=== AC convert-cross-currency-fallback-date ===
Intent: A cross conversion on a non-publication date uses the earlier effective date and returns rate and result derived from the stored rates with half-even rounding.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from decimal import Decimal, ROUND_HALF_EVEN
from persistence.testing import db_session
from app_server.testing import web_client

published = "1800-07-01"
requested = "1800-07-05"
from_cur, to_cur = "ZZA", "ZZB"
from_rate, to_rate = "1.0298", "0.84453"
amount = "100"

with db_session() as db:
    db.rates.replace_rate(date=published, currency=from_cur, rate=from_rate)
    db.rates.replace_rate(date=published, currency=to_cur, rate=to_rate)
    client = web_client()
    response = client.get(
        "/convert",
        params={"from": from_cur, "to": to_cur, "amount": amount, "date": requested},
    )
    assert response.status_code == 200
    body = response.json()

    rf, rt, amt = Decimal(from_rate), Decimal(to_rate), Decimal(amount)
    rate = (rt / rf).quantize(Decimal("0.000001"), rounding=ROUND_HALF_EVEN)
    result = (amt * rt / rf).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
    assert body["date"] == published
    assert body["from"] == from_cur
    assert body["to"] == to_cur
    assert body["amount"] == amount
    assert body["rate"] == f"{rate:.6f}"
    assert body["result"] == f"{result:.2f}"
=== END AC convert-cross-currency-fallback-date ===

=== AC convert-eur-legs ===
Intent: EUR carries the implicit rate 1 as source and as target, and the amount is echoed exactly as given including its decimals.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from decimal import Decimal, ROUND_HALF_EVEN
from persistence.testing import db_session
from app_server.testing import web_client

day = "1800-07-10"
cur = "ZZA"
cur_rate = "161.77"
amount = "250.25"

with db_session() as db:
    db.rates.replace_rate(date=day, currency=cur, rate=cur_rate)
    client = web_client()

    out = client.get("/convert", params={"from": "EUR", "to": cur, "amount": amount, "date": day})
    assert out.status_code == 200
    body = out.json()
    rate = (Decimal(cur_rate) / Decimal(1)).quantize(Decimal("0.000001"), rounding=ROUND_HALF_EVEN)
    result = (Decimal(amount) * Decimal(cur_rate) / Decimal(1)).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_EVEN
    )
    assert body["amount"] == amount
    assert body["rate"] == f"{rate:.6f}"
    assert body["result"] == f"{result:.2f}"

    back = client.get("/convert", params={"from": cur, "to": "EUR", "amount": amount, "date": day})
    assert back.status_code == 200
    body = back.json()
    rate = (Decimal(1) / Decimal(cur_rate)).quantize(Decimal("0.000001"), rounding=ROUND_HALF_EVEN)
    result = (Decimal(amount) * Decimal(1) / Decimal(cur_rate)).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_EVEN
    )
    assert body["rate"] == f"{rate:.6f}"
    assert body["result"] == f"{result:.2f}"
=== END AC convert-eur-legs ===

=== AC convert-result-from-unrounded-rate ===
Intent: The result is computed from the stored rates, not from the six-decimal rounded rate: with a from rate 3 and a to rate 1 the exact result differs from amount times the rounded rate.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from decimal import Decimal, ROUND_HALF_EVEN
from persistence.testing import db_session
from app_server.testing import web_client

day = "1800-07-15"
from_cur, to_cur = "ZZA", "ZZB"
from_rate, to_rate = "3", "1"
amount = "3000000"

with db_session() as db:
    db.rates.replace_rate(date=day, currency=from_cur, rate=from_rate)
    db.rates.replace_rate(date=day, currency=to_cur, rate=to_rate)
    client = web_client()
    response = client.get(
        "/convert",
        params={"from": from_cur, "to": to_cur, "amount": amount, "date": day},
    )
    assert response.status_code == 200
    body = response.json()

    rf, rt, amt = Decimal(from_rate), Decimal(to_rate), Decimal(amount)
    rounded_rate = (rt / rf).quantize(Decimal("0.000001"), rounding=ROUND_HALF_EVEN)
    exact = (amt * rt / rf).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
    from_rounded = (amt * rounded_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
    assert exact != from_rounded
    assert body["rate"] == f"{rounded_rate:.6f}"
    assert body["result"] == f"{exact:.2f}"
=== END AC convert-result-from-unrounded-rate ===

=== AC convert-half-even-tie ===
Intent: A result exactly halfway between two cents rounds half to even, so 0.125 at equal rates becomes the even neighbour rather than rounding up.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from decimal import Decimal, ROUND_HALF_EVEN, ROUND_HALF_UP
from persistence.testing import db_session
from app_server.testing import web_client

day = "1800-07-20"
from_cur, to_cur = "ZZA", "ZZB"
same_rate = "2"
amount = "0.125"

with db_session() as db:
    db.rates.replace_rate(date=day, currency=from_cur, rate=same_rate)
    db.rates.replace_rate(date=day, currency=to_cur, rate=same_rate)
    client = web_client()
    response = client.get(
        "/convert",
        params={"from": from_cur, "to": to_cur, "amount": amount, "date": day},
    )
    assert response.status_code == 200
    body = response.json()

    exact = Decimal(amount) * Decimal(same_rate) / Decimal(same_rate)
    even = exact.quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
    up = exact.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    assert even != up
    assert body["result"] == f"{even:.2f}"
=== END AC convert-half-even-tie ===

## User Acceptance

- None.

## Guardrails

- Never use floating point for rates, amounts or results; use `decimal` on the stored text.
- `result` is never derived from the rounded `rate`.
- `amount` is echoed exactly as received, not normalized.
- The route does not query the database directly; it calls the effective-date service.
