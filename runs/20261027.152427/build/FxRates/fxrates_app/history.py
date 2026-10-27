"""A currency's stored rates over a period, ascending by date, returned as the stored text.

Points come from `db.rates.list_currency_history` in one call per request, so a load completed
before the request is visible to it. Both bounds are optional and inclusive; a start later than the
end matches nothing. Rates are never converted to a float: the statistics compare and average them
as `Decimal`, and min and max return the stored text unchanged.
"""

from __future__ import annotations

from decimal import ROUND_HALF_EVEN, Decimal

from fxrates_app.config import open_store

MEAN_QUANTUM = Decimal("0.000001")


class UnknownCurrency(LookupError):
    """A currency has no stored rate anywhere in its history, so the bounds cannot make it known."""


def history_points(code: str, start: str | None = None, end: str | None = None) -> list[dict[str, str]]:
    """Return {"date", "rate"} points for `code` from `start` through `end`, ascending by date.

    Raises UnknownCurrency when the whole stored history of `code` is empty; a currency with stored
    rates but none inside the bounds returns an empty list.
    """
    arguments: dict[str, str] = {"currency": code}
    if start is not None:
        arguments["start_date"] = start
    if end is not None:
        arguments["end_date"] = end
    db = open_store()
    try:
        rows = db.rates.list_currency_history(**arguments)
        if not rows and not db.rates.list_currency_history(currency=code):
            raise UnknownCurrency(code)
    finally:
        db.close()
    return [{"date": row.date, "rate": row.rate} for row in rows]


def history_summary(points: list[dict[str, str]]) -> dict[str, int | str | None]:
    """Return count, min, max, and mean over `points`; min and max are stored text, mean has six decimals.

    With no points, count is 0 and min, max, and mean are None.
    """
    if not points:
        return {"count": 0, "min": None, "max": None, "mean": None}
    total = sum((Decimal(point["rate"]) for point in points), Decimal(0))
    mean = (total / len(points)).quantize(MEAN_QUANTUM, rounding=ROUND_HALF_EVEN)
    return {
        "count": len(points),
        "min": min(points, key=lambda point: Decimal(point["rate"]))["rate"],
        "max": max(points, key=lambda point: Decimal(point["rate"]))["rate"],
        "mean": f"{mean:.6f}",
    }
