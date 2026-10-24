"""Application configuration boundary."""

from dataclasses import dataclass
import os
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Settings:
    """Runtime settings shared by the application."""

    database_url: str


def get_settings() -> Settings:
    """Read the configured SQLite location using the project's precedence."""
    location = os.environ.get("DATABASE_URL") or os.environ.get("DATABASE_PATH")
    if not location:
        location = str(Path("data") / "app.db")
    return Settings(database_url=location)
