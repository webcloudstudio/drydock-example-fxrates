"""Store parsed rate records through the persistence library, replacing any rate already stored."""

from __future__ import annotations

from collections.abc import Iterable, Sequence

from persistence import Database


def store_rates(db: Database, records: Iterable[Sequence[str]]) -> tuple[int, int]:
    """Write each (date, currency, rate) record and return (distinct dates, rates written).

    Each record goes through the declared upsert, so a (date, currency) already stored takes the new
    text and storing the same records again leaves the rows unchanged. The database is neither
    opened nor closed here.
    """
    dates: set[str] = set()
    written = 0
    for date, currency, rate in records:
        db.rates.replace_rate(date=date, currency=currency, rate=rate)
        dates.add(date)
        written += 1
    return len(dates), written
