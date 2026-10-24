"""CLI command behavior."""

import csv
import io
from pathlib import Path
import re
import signal
import sys
import tempfile
import urllib.request
import zipfile
from datetime import date

from persistence import PersistenceError, open_database
from services.common import database_dsn, load_csv_text


def dispatch(args: object) -> int:
    """Dispatch parsed arguments to their command implementation."""
    try:
        if args.command == "init":
            with open_database(database_dsn()) as db:
                # A fresh configured store has not received the build's default-store DDL.
                # Provision the generated schema only in that case; ordinary initialization
                # clears rows using the declared repository operation.
                try:
                    rows = db.rates.list()
                except PersistenceError as exc:
                    if "no such table" not in str(exc).lower():
                        raise
                    db.execute_script((Path(__file__).resolve().parent.parent / "schema.sql").read_text(encoding="utf-8"))
                    rows = db.rates.list()
                for row in rows:
                    db.rates.delete(date=row.date, currency=row.currency)
            return 0
        if args.command == "load":
            try:
                text = open(args.csv, encoding="utf-8", newline="").read()
            except OSError as exc:
                print(f"error: {exc}", file=sys.stderr)
                return 1
            try:
                dates, rates = load_csv_text(text)
            except ValueError as exc:
                print(f"error: {exc}", file=sys.stderr)
                return 3
            print("dates,rates")
            print(f"{dates},{rates}")
            return 0
        if args.command == "fetch":
            try:
                with urllib.request.urlopen("https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip") as response:
                    payload = response.read()
                with zipfile.ZipFile(io.BytesIO(payload)) as archive:
                    text = archive.read("eurofxref-hist.csv").decode("utf-8")
                dates, rates = load_csv_text(text)
            except (OSError, KeyError, zipfile.BadZipFile, UnicodeError) as exc:
                print(f"error: {exc}", file=sys.stderr)
                return 1 if not isinstance(exc, ValueError) else 3
            except ValueError as exc:
                print(f"error: {exc}", file=sys.stderr)
                return 3
            print("dates,rates")
            print(f"{dates},{rates}")
            return 0
        if args.command == "serve":
            import uvicorn
            server = uvicorn.Server(
                uvicorn.Config("app_server.main:app", host="127.0.0.1", port=args.port)
            )
            previous = signal.getsignal(signal.SIGTERM)
            signal.signal(signal.SIGTERM, lambda signum, frame: setattr(server, "should_exit", True))
            try:
                server.run()
            finally:
                signal.signal(signal.SIGTERM, previous)
            return 0
        return 2
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
