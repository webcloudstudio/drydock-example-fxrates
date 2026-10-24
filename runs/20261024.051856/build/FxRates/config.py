"""Typed runtime configuration for the application."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    database_url: str

    @classmethod
    def load(cls) -> "Config":
        return cls(
            database_url=(
                os.environ.get("DATABASE_URL")
                or os.environ.get("DATABASE_PATH")
                or "data/app.db"
            )
        )
