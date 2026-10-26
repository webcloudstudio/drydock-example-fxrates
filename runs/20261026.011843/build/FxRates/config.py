"""Runtime configuration for FxRates."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Settings:
    database_location: str


def get_settings() -> Settings:
    """Resolve the configured database location in documented precedence order."""
    location = os.environ.get("DATABASE_URL") or os.environ.get("DATABASE_PATH") or "data/app.db"
    return Settings(database_location=location)


def database_path() -> Path:
    """Return the configured location as a path for the SQLite runtime."""
    return Path(get_settings().database_location)
