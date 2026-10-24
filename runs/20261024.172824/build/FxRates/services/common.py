"""Shared settings, CSV validation, and rate lookup helpers."""
import csv
import io
import os
import re
from datetime import date
from decimal import Decimal, ROUND_HALF_EVEN

from persistence import open_database

RATE_RE = re.compile(r"[0-9]+(?:\.[0-9]+)?\Z")
AMOUNT_RE = RATE_RE


def database_dsn() -> str:
    return os.environ.get("DATABASE_URL") or os.environ.get("DATABASE_PATH") or "data/app.db"


def load_csv_text(text: str) -> tuple[int, int]:
    rows = list(csv.reader(io.StringIO(text, newline="")))
    if not rows:
        raise ValueError("empty CSV")
    header = rows[0]
    if not header or header[0] != "Date":
        raise ValueError("invalid header")
    if header[-1] == "":
        header = header[:-1]
    currencies = header[1:]
    if any(not re.fullmatch(r"[A-Z]{3}", code or "") for code in currencies) or len(set(currencies)) != len(currencies):
        raise ValueError("invalid currency header")
    parsed, seen = [], set()
    for row in rows[1:]:
        if row and row[-1] == "":
            row = row[:-1]
        if len(row) != len(currencies) + 1:
            raise ValueError("invalid row width")
        try:
            date.fromisoformat(row[0])
            if date.fromisoformat(row[0]).isoformat() != row[0]:
                raise ValueError("invalid date")
        except ValueError as exc:
            raise ValueError("invalid date") from exc
        if row[0] in seen:
            raise ValueError("duplicate date")
        seen.add(row[0])
        vals = []
        for currency, raw in zip(currencies, row[1:]):
            if raw == "N/A":
                continue
            if not RATE_RE.fullmatch(raw) or Decimal(raw) == 0:
                raise ValueError("invalid rate")
            vals.append((row[0], currency, raw))
        parsed.extend(vals)
    with open_database(database_dsn()) as db:
        for day, currency, rate in parsed:
            db.rates.upsert(date=day, currency=currency, rate=rate)
    return len({item[0] for item in parsed}), len(parsed)


def all_rates():
    with open_database(database_dsn()) as db:
        return db.rates.list()


def effective(requested: str | None):
    rows = all_rates()
    dates = sorted({r.date for r in rows})
    if not dates:
        return None
    if requested is None or requested == "latest":
        chosen = dates[-1]
    else:
        chosen = next((d for d in reversed(dates) if d <= requested), None)
    return (chosen, {r.currency: r.rate for r in rows if r.date == chosen}) if chosen else None


def valid_date(value: str) -> bool:
    try:
        return date.fromisoformat(value).isoformat() == value
    except ValueError:
        return False


def rounded(value: Decimal, places: int) -> str:
    quantum = Decimal(1).scaleb(-places)
    return format(value.quantize(quantum, rounding=ROUND_HALF_EVEN), f".{places}f")
