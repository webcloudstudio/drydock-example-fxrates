"""FxRates command line interface."""
from __future__ import annotations
import argparse, sys
from datetime import date
from config import get_settings
from persistence import open_database

def _parser():
    p=argparse.ArgumentParser(prog='fxrates', description='Load and serve ECB euro reference rates.')
    s=p.add_subparsers(dest='command', required=True)
    s.add_parser('init', help='drop and recreate the rates database')
    x=s.add_parser('load', help='validate and load a CSV history file'); x.add_argument('file')
    s.add_parser('fetch', help='download and load ECB history')
    x=s.add_parser('serve', help='run the HTTP API'); x.add_argument('--host',default='127.0.0.1'); x.add_argument('--port',type=int,default=8000)
    return p

def main(argv: list[str] | None = None) -> int:
    args=_parser().parse_args(argv)
    try:
        if args.command=='init':
            from services.loader import initialize
            initialize(); return 0
        if args.command=='load':
            from services.loader import load_path
            dates,rates=load_path(args.file); print(f'dates,rates\n{dates},{rates}'); return 0
        if args.command=='fetch':
            from services.fetch import fetch
            dates,rates=fetch(); print(f'dates,rates\n{dates},{rates}'); return 0
        if args.command=='serve':
            import uvicorn
            uvicorn.run('app_server.main:app',host=args.host,port=args.port); return 0
    except FileNotFoundError as e:
        print(f'error: {e}',file=sys.stderr); return 1
    except (OSError, ValueError, RuntimeError) as e:
        code=3 if args.command=='load' or args.command=='fetch' else 1
        print(f'error: {e}',file=sys.stderr); return code
    return 1
