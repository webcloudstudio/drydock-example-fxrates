"""Command dispatch for FxRates."""

from __future__ import annotations

import sys
import os
import csv
import re
from datetime import date
from persistence import open_database, PersistenceError

def _dsn() -> str:
    return os.environ.get("DATABASE_URL") or os.environ.get("DATABASE_PATH") or "data/app.db"

def _load_file(path: str) -> tuple[int, int]:
    try:
        with open(path, newline="", encoding="utf-8") as stream:
            rows = list(csv.reader(stream))
    except OSError as exc:
        raise FileNotFoundError(str(exc)) from exc
    try:
        if not rows or len(rows[0]) < 2:
            raise ValueError("invalid header")
        header = rows[0]
        if header[-1] == "": header = header[:-1]
        codes = header[1:]
        if header[0] != "Date" or any(not re.fullmatch(r"[A-Z]{3}", x) for x in codes) or len(set(codes)) != len(codes):
            raise ValueError("invalid header")
        parsed=[]; days=set()
        for raw in rows[1:]:
            fields = raw[:-1] if raw and raw[-1] == "" else raw
            if len(fields) != len(codes)+1: raise ValueError("invalid row")
            day=fields[0]
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", day): raise ValueError("invalid date")
            date.fromisoformat(day)
            if day in days: raise ValueError("duplicate date")
            days.add(day)
            for code, value in zip(codes, fields[1:]):
                if value == "N/A": continue
                if not re.fullmatch(r"[0-9]+(?:\.[0-9]+)?", value) or not any(c != "0" for c in value if c.isdigit()): raise ValueError("invalid rate")
                parsed.append((day,code,value))
    except (ValueError, IndexError) as exc:
        raise InvalidCSV(str(exc)) from exc
    with open_database(_dsn()) as db:
        for day, code, value in parsed:
            db.rates.upsert(date=day, currency=code, rate=value)
    return len(days), len(parsed)

class InvalidCSV(Exception): pass


def dispatch(args: object) -> int:
    command = getattr(args, "command", None)
    if command == "serve":
        import uvicorn

        uvicorn.run("app_server.main:app", host="127.0.0.1", port=args.port)
        return 0

    if command == "init":
        with open_database(_dsn()) as db:
            try:
                db.reset_rates()
            except PersistenceError:
                # Acceptance and project rollback sessions own a transaction that cannot
                # be replaced with DDL. Clear the declared repository rows in that session.
                for row in db.rates.list():
                    db.rates.delete(date=row.date, currency=row.currency)
        return 0
    if command == "load":
        try: dates, rates = _load_file(args.file)
        except FileNotFoundError as exc:
            print(f"error: {exc}", file=sys.stderr); return 1
        except InvalidCSV as exc:
            print(f"error: {exc}", file=sys.stderr); return 3
        print("dates,rates")
        print(f"{dates},{rates}")
        return 0
    if command == "fetch":
        from . import fetch
        try: archive = fetch.download_archive()
        except Exception as exc:
            print(f"error: {exc}", file=sys.stderr); return 1
        import io, zipfile, tempfile
        try:
            with zipfile.ZipFile(io.BytesIO(archive)) as zipped: payload=zipped.read("eurofxref-hist.csv")
            with tempfile.NamedTemporaryFile() as tmp:
                tmp.write(payload); tmp.flush()
                dates, rates = _load_file(tmp.name)
        except Exception as exc:
            print(f"error: {exc}", file=sys.stderr); return 3
        print("dates,rates"); print(f"{dates},{rates}"); return 0

    print("error: unknown command", file=sys.stderr)
    return 2
