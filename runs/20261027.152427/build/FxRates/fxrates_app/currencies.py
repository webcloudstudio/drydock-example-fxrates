"""Currency codes the store can quote: every code with at least one stored rate, ascending.

The base currency is not a stored code and is never listed. The list comes from
`db.rates.list_currencies`, which returns one row per stored rate, so duplicates are removed here.
"""

from __future__ import annotations

from fxrates_app.config import open_store
from fxrates_app.rates import BASE


def currencies() -> list[str]:
    """Return the distinct stored currency codes, ascending, without the base currency."""
    db = open_store()
    try:
        rows = db.rates.list_currencies()
    finally:
        db.close()
    return sorted({row.currency for row in rows} - {BASE})
