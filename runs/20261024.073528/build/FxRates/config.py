"""Runtime configuration for FxRates."""
from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    database_dsn: str


def get_settings() -> Settings:
    return Settings(os.environ.get("DATABASE_URL") or os.environ.get("DATABASE_PATH") or "data/app.db")
