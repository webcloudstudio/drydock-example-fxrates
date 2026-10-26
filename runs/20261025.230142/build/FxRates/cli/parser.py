"""Argument parser construction for the FxRates command line."""

from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="fxrates")
    parser.add_argument("command", help="command to run")
    return parser
