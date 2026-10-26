"""Runtime configuration boundary for FxRates."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    database_url: str


def get_settings() -> Settings:
    """Resolve the database DSN using the documented precedence."""
    return Settings(
        database_url=(
            os.environ.get("DATABASE_URL")
            or os.environ.get("DATABASE_PATH")
            or "data/app.db"
        )
    )
