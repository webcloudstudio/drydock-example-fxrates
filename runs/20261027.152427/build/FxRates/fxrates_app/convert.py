"""Conversion between two currencies on a calendar day, in exact decimal arithmetic.

The base currency EUR has the implicit rate 1; any other rate is the stored ECB text read as a
Decimal. The pair rate is rate(to) / rate(from), rounded half to even to six decimals. The result is
amount * rate(to) / rate(from), computed exactly from the stored rates and then rounded half to even
to two decimals, so it never depends on the rounded pair rate. No floating point is used.
"""

from __future__ import annotations

from decimal import ROUND_HALF_EVEN, Decimal

from fxrates_app import rates as rate_service

RATE_QUANTUM = Decimal("0.000001")
RESULT_QUANTUM = Decimal("0.01")


class UnknownCurrency(LookupError):
    """A currency other than the base has no stored rate on the effective publication."""


class UnusableRate(ValueError):
    """A stored rate is zero, so it cannot be used as a divisor."""


def _rate_of(code: str, rates: dict[str, str]) -> Decimal:
    """Return the Decimal rate of `code` against the base; the base itself is 1."""
    if code == rate_service.BASE:
        return Decimal(1)
    if code not in rates:
        raise UnknownCurrency(code)
    value = Decimal(rates[code])
    if value == 0:
        raise UnusableRate(code)
    return value


def convert(source: str, target: str, amount: str, requested: str | None = None) -> dict[str, str] | None:
    """Convert `amount` of `source` into `target` using the effective publication.

    `requested` is a calendar date; None selects the latest publication. Returns None when no
    publication exists on or before the requested date.
    """
    found = rate_service.latest_rates() if requested is None else rate_service.rates_on(requested)
    if found is None:
        return None
    effective, rates = found
    rate_from = _rate_of(source, rates)
    rate_to = _rate_of(target, rates)
    rate = (rate_to / rate_from).quantize(RATE_QUANTUM, rounding=ROUND_HALF_EVEN)
    result = (Decimal(amount) * rate_to / rate_from).quantize(RESULT_QUANTUM, rounding=ROUND_HALF_EVEN)
    return {
        "date": effective,
        "from": source,
        "to": target,
        "amount": amount,
        "rate": f"{rate:.6f}",
        "result": f"{result:.2f}",
    }
