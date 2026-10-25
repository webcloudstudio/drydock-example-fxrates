"""Argument parsing for the ``fxrates`` command line."""

from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="fxrates")
    subcommands = parser.add_subparsers(dest="command", required=True)
    subcommands.add_parser("init", help="Initialize the rates store")
    load = subcommands.add_parser("load", help="Load ECB history from a CSV file")
    load.add_argument("file")
    fetch = subcommands.add_parser("fetch", help="Fetch ECB history")
    fetch.add_argument("--url")
    subcommands.add_parser("serve", help="Run the local HTTP service")
    serve = subcommands.choices["serve"]
    serve.add_argument("--port", type=int, default=8000)
    return parser
