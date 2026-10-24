"""Command line argument parsing, kept separate from command behavior."""

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="fxrates")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("init")
    load = commands.add_parser("load")
    load.add_argument("csv")
    commands.add_parser("fetch")
    serve = commands.add_parser("serve")
    serve.add_argument("--port", type=int, default=8000)
    return parser
