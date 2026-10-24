"""Typed application configuration boundary."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Settings:
    """Runtime settings resolved from the process environment."""

    database_dsn: str


def settings() -> Settings:
    """Resolve runtime settings, honoring the documented database precedence."""
    return Settings(
        database_dsn=(
            os.environ.get("DATABASE_URL")
            or os.environ.get("DATABASE_PATH")
            or "data/app.db"
        )
    )


def database_dsn() -> str:
    """Return the configured database location."""
    return settings().database_dsn
