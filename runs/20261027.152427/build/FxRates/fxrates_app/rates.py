"""Rates on a calendar day: the effective publication date and the rates published on it.

The ECB publishes on working days only, so a request for any date resolves to the latest
publication on or before it. Rates are returned as the stored text, never converted to a float.
Reads go through `db.rates` only.
"""

from __future__ import annotations

from persistence import Database

from fxrates_app.config import open_store

BASE = "EUR"


def _effective(db: Database, day: str) -> str | None:
    """Return the latest stored publication date on or before `day`, or None when none exists."""
    rows = db.rates.list_on_or_before(as_of=day)
    return rows[0].date if rows else None


def effective_date(d: str) -> str | None:
    """Return the latest publication date on or before `d`, or None when no such date exists."""
    db = open_store()
    try:
        return _effective(db, d)
    finally:
        db.close()


def _rates_of(db: Database, effective: str) -> dict[str, str]:
    """Return {currency: stored rate text} for the publication on `effective`, base excluded."""
    rows = db.rates.list_for_date(date=effective)
    return {row.currency: row.rate for row in rows if row.currency != BASE}


def rates_on(requested: str) -> tuple[str, dict[str, str]] | None:
    """Return (effective date, {currency: stored rate text}) for `requested`, or None.

    None means no publication exists on or before `requested`. The base currency never appears in
    the mapping.
    """
    db = open_store()
    try:
        effective = _effective(db, requested)
        if effective is None:
            return None
        rates = _rates_of(db, effective)
    finally:
        db.close()
    return effective, rates


def latest_rates() -> tuple[str, dict[str, str]] | None:
    """Return (latest publication date, {currency: stored rate text}), or None when nothing is stored.

    The latest date is the first row of `list_on_or_before` called without a bound.
    """
    db = open_store()
    try:
        rows = db.rates.list_on_or_before()
        if not rows:
            return None
        effective = rows[0].date
        rates = _rates_of(db, effective)
    finally:
        db.close()
    return effective, rates
