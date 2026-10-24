"""Argument parser construction, kept separate from command behavior."""

from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="fxrates")
    subcommands = parser.add_subparsers(dest="command", required=True)
    subcommands.add_parser("init", help="Initialize the rates database")
    load = subcommands.add_parser("load", help="Load rates from a CSV file")
    load.add_argument("path")
    fetch = subcommands.add_parser("fetch", help="Fetch and load ECB rates")
    fetch.add_argument("--url")
    serve = subcommands.add_parser("serve", help="Run the HTTP service")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8000)
    return parser

