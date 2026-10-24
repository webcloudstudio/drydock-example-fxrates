"""Command behavior and dispatch."""

from __future__ import annotations

import sys


def serve(*, host: str, port: int) -> int:
    import uvicorn

    uvicorn.run("app_server.main:app", host=host, port=port)
    return 0


def dispatch(args: object) -> int:
    from services import InvalidHistory, database, load_history
    command = getattr(args, "command", None)
    if command == "init":
        with database() as db:
            db.execute_script('DROP TABLE IF EXISTS "rates"; CREATE TABLE "rates" ("id" INTEGER PRIMARY KEY, "date" TEXT NOT NULL, "currency" TEXT NOT NULL, "rate" TEXT NOT NULL, UNIQUE ("date", "currency"));')
        return 0
    if command == "load":
        try:
            dates, rates = load_history(args.csv)
        except InvalidHistory as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 3
        except OSError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        print("dates,rates")
        print(f"{dates},{rates}")
        return 0
    if command == "fetch":
        from .fetch import fetch
        return fetch(load_history)
    if command == "serve":
        return serve(host=args.host, port=args.port)
    print("error: a command is required", file=sys.stderr)
    return 2
