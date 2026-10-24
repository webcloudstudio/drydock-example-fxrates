"""Command behavior for the FxRates CLI."""

from __future__ import annotations

import sys


def init() -> int:
    return 0


def load(path: str) -> int:
    del path
    return 0


def fetch(url: str | None) -> int:
    del url
    return 0


def serve(*, host: str, port: int) -> int:
    import uvicorn

    uvicorn.run("app_server.main:app", host=host, port=port)
    return 0


def dispatch(args: object) -> int:
    command = args.command
    if command == "init":
        return init()
    if command == "load":
        return load(args.path)
    if command == "fetch":
        return fetch(args.url)
    if command == "serve":
        return serve(host=args.host, port=args.port)
    print(f"error: unsupported command {command}", file=sys.stderr)
    return 2

