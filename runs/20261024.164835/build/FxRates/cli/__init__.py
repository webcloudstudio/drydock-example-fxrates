from __future__ import annotations
import argparse, sys
from cli.parser import build_parser, UsageError
from services.rates import load_file, fetch, RejectedFile, OperationalFailure
from config import database_dsn
from persistence import open_database

def main(argv=None):
    try: args=build_parser().parse_args(argv)
    except UsageError as e:
        print(f'error: {e}', file=sys.stderr)
        return 2
    except SystemExit as e: return int(e.code)
    try:
        if args.command=='init':
            with open_database(database_dsn()) as db:
                db.execute_script('DROP TABLE IF EXISTS "rates"; CREATE TABLE "rates" ("date" TEXT NOT NULL, "currency" TEXT NOT NULL, "rate" TEXT NOT NULL, "id" INTEGER PRIMARY KEY, UNIQUE ("date", "currency")); CREATE INDEX "rates_date_idx" ON "rates" ("date"); CREATE INDEX "rates_currency_date_idx" ON "rates" ("currency", "date");')
            return 0
        if args.command=='load': counts=load_file(args.csv)
        elif args.command=='fetch': counts=fetch()
        elif args.command=='serve':
            import signal
            import uvicorn
            server = uvicorn.Server(uvicorn.Config('app_server.main:app', host='127.0.0.1', port=args.port, log_level='error'))
            previous = signal.getsignal(signal.SIGTERM)
            def stop_server(signum, frame):
                server.should_exit = True
            signal.signal(signal.SIGTERM, stop_server)
            try:
                server.run()
            finally:
                signal.signal(signal.SIGTERM, previous)
            return 0
        print('dates,rates'); print(f'{counts[0]},{counts[1]}'); return 0
    except RejectedFile as e: print(f'error: {e}',file=sys.stderr); return 3
    except (OperationalFailure, OSError, Exception) as e: print(f'error: {e}',file=sys.stderr); return 1
