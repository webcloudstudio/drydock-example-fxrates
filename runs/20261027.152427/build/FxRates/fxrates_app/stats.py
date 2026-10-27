"""Summary of the store: how many dates and rates it holds, and its first and last publication dates.

Every value is derived from `db.rates.list_all_keys`; the service counts and takes the extremes.
"""

from __future__ import annotations

from fxrates_app.config import open_store


def stats() -> dict[str, int | str | None]:
    """Return the dates and rates counts and the first and last dates, None when nothing is stored."""
    db = open_store()
    try:
        keys = db.rates.list_all_keys()
    finally:
        db.close()
    dates = sorted({key.date for key in keys})
    return {
        "dates": len(dates),
        "rates": len(keys),
        "first": dates[0] if dates else None,
        "last": dates[-1] if dates else None,
    }
