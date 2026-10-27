"""The init command: create the declared rates schema in the configured store, keeping stored rows."""

from __future__ import annotations

import config
from cli.errors import OperationalError
from persistence import PersistenceError, initialize_database


def run(args: list[str]) -> int:
    """Apply the generated schema to the configured store and return 0; writes nothing to stdout."""
    dsn = str(config.database_path())
    try:
        database = initialize_database(dsn)
    except PersistenceError as exc:
        raise OperationalError(f"init could not initialize the store: {exc}") from exc
    database.close()
    return 0
