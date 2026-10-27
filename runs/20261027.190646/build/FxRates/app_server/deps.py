"""Request-scoped dependencies shared by every router."""

from __future__ import annotations

from collections.abc import Iterator

import config
from persistence import Database, open_database


def get_db() -> Iterator[Database]:
    """Open the configured store for one request and close it when the request ends.

    The store is opened per request, so a load completed by another process is visible to the next request.
    """
    db = open_database(str(config.database_path()))
    try:
        yield db
    finally:
        db.close()
