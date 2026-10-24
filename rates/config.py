"""Runtime configuration for the FxRates application."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    database_dsn: str
    host: str = "127.0.0.1"
    port: int = 8000


def database_dsn(environ: dict[str, str] | None = None) -> str:
    """Resolve the database location according to the public configuration contract."""
    values = os.environ if environ is None else environ
    return values.get("DATABASE_URL") or values.get("DATABASE_PATH") or "data/app.db"


def get_settings(environ: dict[str, str] | None = None) -> Settings:
    return Settings(database_dsn=database_dsn(environ))

