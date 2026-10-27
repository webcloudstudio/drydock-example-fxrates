"""Runtime configuration resolved from the environment.

This module is the one configuration boundary. It reads environment variables
on every call and never touches the database itself.
"""

from __future__ import annotations

import os
from pathlib import Path

DATABASE_URL_ENV = "DATABASE_URL"
DATABASE_PATH_ENV = "DATABASE_PATH"
DEFAULT_DATABASE_PATH = "data/app.db"
SQLITE_URL_PREFIX = "sqlite://"


def _environment_value(name: str) -> str:
    """Return the variable's value, or an empty string when unset."""
    return os.environ.get(name, "")


def database_path() -> Path:
    """Resolve the SQLite database file location.

    Order: DATABASE_URL (a file path, optionally prefixed with sqlite://),
    then DATABASE_PATH, then data/app.db. An unset or empty variable is skipped.
    """
    url = _environment_value(DATABASE_URL_ENV)
    if url.startswith(SQLITE_URL_PREFIX):
        url = url[len(SQLITE_URL_PREFIX):]
    if url:
        return Path(url)

    path = _environment_value(DATABASE_PATH_ENV)
    if path:
        return Path(path)

    return Path(DEFAULT_DATABASE_PATH)
