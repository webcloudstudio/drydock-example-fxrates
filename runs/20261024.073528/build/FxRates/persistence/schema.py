from dataclasses import dataclass
from .db import Database, Operation, Schema, Table


@dataclass(frozen=True)
class Rate:
    date: str
    currency: str
    rate: str


SCHEMA = Schema(
    tables=(Table("rates", ("date", "currency", "rate")),),
    operations=(
        Operation("rates.list", "rates", "list", ("date", "currency"), Rate, ("date", "currency", "rate"), name="list"),
        Operation("rates.upsert", "rates", "upsert", ("date", "currency", "rate"), Rate, ("date", "currency", "rate"), ("date", "currency"), name="upsert"),
        Operation("rates.delete", "rates", "delete", ("date", "currency"), None, match=("date", "currency"), name="delete"),
    ),
)


def open_database(dsn: str) -> Database:
    return Database(dsn, SCHEMA)
