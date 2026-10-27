"""Database location: one place decides which store the application opens.

Resolution order: DATABASE_URL, then DATABASE_PATH, then data/app.db. The environment is read at
call time. Application code opens the store only through `persistence.open_database`.
"""

from __future__ import annotations

import os

from persistence import Database, open_database

DEFAULT_DATABASE_PATH = "data/app.db"
SQLITE_PREFIX = "sqlite://"


def database_path() -> str:
    """Return the database location from the environment, falling back to data/app.db."""
    url = os.environ.get("DATABASE_URL", "")
    if url.startswith(SQLITE_PREFIX):
        url = url[len(SQLITE_PREFIX):]
    if url:
        return url
    path = os.environ.get("DATABASE_PATH", "")
    if path:
        return path
    return DEFAULT_DATABASE_PATH


def open_store() -> Database:
    """Open the store named by `database_path()` through the persistence library."""
    return open_database(database_path())
