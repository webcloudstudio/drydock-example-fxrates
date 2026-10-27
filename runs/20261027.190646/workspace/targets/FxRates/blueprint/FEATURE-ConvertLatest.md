# FEATURE: Convert Latest

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | Make the date parameter of GET /convert optional, defaulting to the latest publication. |
| Depends On | FEATURE-Convert.md, FEATURE-EffectiveDate.md |
| Provides | GET /convert latest default |
| Consumes | GET /convert, rates.effective_publication |

## Purpose

A caller who omits `date` gets a conversion at the most recent published rates.

## Routes

| Route | Behavior |
|-------|----------|
| `GET /convert?from=<code>&to=<code>&amount=<amount>` | As `GET /convert`, using the latest publication date; the response `date` is that publication date. |

## Behavior

- In `app_server/routers/convert.py`, `date` becomes optional. When absent, call
  `services.effective_date.effective_publication(db, None)`; when present, behave exactly as before.
- Rate, result, rounding and echo rules are unchanged from FEATURE-Convert.md.

## Database Interface

- None — persistence is reached through `rates.effective_publication` in FEATURE-EffectiveDate.md.

## Programmatic Acceptance

=== AC convert-latest-default-date ===
Intent: Omitting date converts at the latest publication and reports that date; a far-future seeded date is always the latest, and the values derive from its stored rates with half-even rounding.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from decimal import Decimal, ROUND_HALF_EVEN
from persistence.testing import db_session
from app_server.testing import web_client

latest = "9999-12-31"
earlier = "9999-12-30"
from_cur, to_cur = "ZZA", "ZZB"
from_rate, to_rate = "0.83608", "160.99"
amount = "1000"

with db_session() as db:
    db.rates.replace_rate(date=latest, currency=from_cur, rate=from_rate)
    db.rates.replace_rate(date=latest, currency=to_cur, rate=to_rate)
    db.rates.replace_rate(date=earlier, currency=from_cur, rate="1")
    db.rates.replace_rate(date=earlier, currency=to_cur, rate="1")
    client = web_client()
    response = client.get(
        "/convert",
        params={"from": from_cur, "to": to_cur, "amount": amount},
    )
    assert response.status_code == 200
    body = response.json()

    rf, rt, amt = Decimal(from_rate), Decimal(to_rate), Decimal(amount)
    rate = (rt / rf).quantize(Decimal("0.000001"), rounding=ROUND_HALF_EVEN)
    result = (amt * rt / rf).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
    assert body["date"] == latest
    assert body["amount"] == amount
    assert body["rate"] == f"{rate:.6f}"
    assert body["result"] == f"{result:.2f}"
=== END AC convert-latest-default-date ===

=== AC convert-latest-explicit-date-still-honoured ===
Intent: Supplying date still selects that date's effective publication even when a later publication exists.
Requires: executable=python3; scope=test
Requires: python-package=fastapi; scope=test
Requires: python-package=httpx2; scope=test

from decimal import Decimal, ROUND_HALF_EVEN
from persistence.testing import db_session
from app_server.testing import web_client

old_day = "1800-08-01"
latest = "9999-12-31"
from_cur, to_cur = "ZZA", "ZZB"
old_from, old_to = "2", "5"
amount = "2.00"

with db_session() as db:
    db.rates.replace_rate(date=old_day, currency=from_cur, rate=old_from)
    db.rates.replace_rate(date=old_day, currency=to_cur, rate=old_to)
    db.rates.replace_rate(date=latest, currency=from_cur, rate="1")
    db.rates.replace_rate(date=latest, currency=to_cur, rate="1")
    client = web_client()
    response = client.get(
        "/convert",
        params={"from": from_cur, "to": to_cur, "amount": amount, "date": old_day},
    )
    assert response.status_code == 200
    body = response.json()
    expected = (Decimal(amount) * Decimal(old_to) / Decimal(old_from)).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_EVEN
    )
    assert body["date"] == old_day
    assert body["result"] == f"{expected:.2f}"
=== END AC convert-latest-explicit-date-still-honoured ===

## User Acceptance

- None.

## Guardrails

- Omitting `date` never changes the rounding, echo or string-typing rules of `GET /convert`.
- The latest date is read from the store on each request, never cached.
