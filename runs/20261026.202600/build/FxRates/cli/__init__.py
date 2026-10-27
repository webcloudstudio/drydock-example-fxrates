from __future__ import annotations
import argparse, sys
from cli.commands import dispatch

def main(argv: list[str] | None = None) -> int:
    parser=argparse.ArgumentParser(prog='fxrates')
    sub=parser.add_subparsers(dest='command', required=True)
    p=sub.add_parser('load'); p.add_argument('path')
    sub.add_parser('fetch')
    sub.add_parser('init')
    p=sub.add_parser('serve'); p.add_argument('--port', type=int, default=8000)
    try:
        args=parser.parse_args(argv)
        return dispatch(args)
    except SystemExit as exc:
        return int(exc.code)
    except Exception as exc:
        print(f'error: {exc}', file=sys.stderr); return 1
