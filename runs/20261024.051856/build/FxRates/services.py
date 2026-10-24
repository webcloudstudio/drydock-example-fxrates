"""Rate ingestion and query services."""
from __future__ import annotations

import csv
import re
from collections import defaultdict
from datetime import date as calendar_date
from decimal import Decimal, ROUND_HALF_EVEN

from config import Config
from persistence import open_database

RATE_RE = re.compile(r"[0-9]+(?:\.[0-9]+)?\Z")
CURRENCY_RE = re.compile(r"[A-Z]{3}\Z")
SIX = Decimal("0.000001")
TWO = Decimal("0.01")


class InvalidHistory(ValueError):
    pass


def database():
    return open_database(Config.load().database_url)


def load_history(path: str) -> tuple[int, int]:
    staged: list[tuple[str, str, str]] = []
    dates: set[str] = set()
    try:
        with open(path, newline="", encoding="utf-8-sig") as source:
            rows = csv.reader(source)
            header = next(rows)
            if len(header) > 1 and header[-1] == "":
                header = header[:-1]
            if len(header) < 2 or header[0] != "Date" or any(not CURRENCY_RE.fullmatch(c) for c in header[1:]) or len(set(header[1:])) != len(header[1:]):
                raise InvalidHistory("invalid CSV header")
            for row in rows:
                if len(row) == len(header) + 1 and row[-1] == "":
                    row = row[:-1]
                if len(row) != len(header):
                    raise InvalidHistory("invalid CSV row width")
                date_text = row[0]
                try:
                    parsed = calendar_date.fromisoformat(date_text)
                    if parsed.isoformat() != date_text:
                        raise ValueError
                except ValueError as exc:
                    raise InvalidHistory("invalid date") from exc
                if date_text in dates:
                    raise InvalidHistory("repeated date")
                dates.add(date_text)
                for currency, value in zip(header[1:], row[1:]):
                    if value == "N/A":
                        continue
                    if not RATE_RE.fullmatch(value) or Decimal(value) == 0:
                        raise InvalidHistory("invalid rate")
                    staged.append((date_text, currency, value))
    except OSError:
        raise
    except (UnicodeError, csv.Error, StopIteration) as exc:
        raise InvalidHistory(str(exc) or "invalid CSV") from exc
    with database() as db:
        for date_text, currency, value in staged:
            db.rates.upsert(date=date_text, currency=currency, rate=value)
    return len({date for date, _, _ in staged}), len(staged)


def all_rates():
    with database() as db:
        return db.rates.list()


def effective(requested: str | None):
    rows = all_rates()
    if not rows:
        return None
    dates = [r.date for r in rows]
    target = max(dates) if requested is None else max((d for d in dates if d <= requested), default=None)
    if target is None:
        return None
    return target, {r.currency: r.rate for r in rows if r.date == target}


def history(currency: str, start: str | None, end: str | None):
    rows = sorted((r for r in all_rates() if r.currency == currency), key=lambda r: r.date)
    if not rows:
        return None
    points = [r for r in rows if (start is None or r.date >= start) and (end is None or r.date <= end)]
    if not points:
        return {"currency": currency, "base": "EUR", "count": 0, "min": None, "max": None, "mean": None, "points": []}
    values = [Decimal(r.rate) for r in points]
    mean = (sum(values, Decimal(0)) / len(values)).quantize(SIX, rounding=ROUND_HALF_EVEN)
    return {"currency": currency, "base": "EUR", "count": len(points), "min": min(points, key=lambda r: Decimal(r.rate)).rate, "max": max(points, key=lambda r: Decimal(r.rate)).rate, "mean": f"{mean:.6f}", "points": [{"date": r.date, "rate": r.rate} for r in points]}


def convert(source: str, target: str, amount: str, requested: str | None):
    resolved = effective(requested)
    if resolved is None:
        return None
    date_text, rates = resolved
    if source != "EUR" and source not in rates or target != "EUR" and target not in rates:
        return None
    source_rate = Decimal(rates[source]) if source != "EUR" else Decimal(1)
    target_rate = Decimal(rates[target]) if target != "EUR" else Decimal(1)
    ratio = target_rate / source_rate
    result = Decimal(amount) * target_rate / source_rate
    return {"date": date_text, "from": source, "to": target, "amount": amount,
            "rate": f"{ratio.quantize(SIX, rounding=ROUND_HALF_EVEN):.6f}",
            "result": f"{result.quantize(TWO, rounding=ROUND_HALF_EVEN):.2f}"}
