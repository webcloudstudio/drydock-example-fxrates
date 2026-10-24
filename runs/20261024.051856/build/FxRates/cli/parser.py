"""Argument parser construction, without command behavior."""

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="fxrates")
    subcommands = parser.add_subparsers(dest="command", required=True)
    subcommands.add_parser("init", help="Clear the rates store")
    load = subcommands.add_parser("load", help="Load an ECB history CSV")
    load.add_argument("csv")
    subcommands.add_parser("fetch", help="Fetch and load ECB history")
    serve = subcommands.add_parser("serve", help="Run the HTTP API")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8000)
    return parser
