from __future__ import annotations
import sys
from cli.parser import ParsedArgs

def dispatch(args: ParsedArgs) -> int:
    from services.rates import load_file, initialize
    if args.command == 'load':
        try: dates, rates = load_file(args.path)
        except OSError as exc:
            print(f'error: {exc}', file=sys.stderr); return 1
        except ValueError as exc:
            print(f'error: {exc}', file=sys.stderr); return 3
        print('dates,rates'); print(f'{dates},{rates}'); return 0
    if args.command == 'fetch':
        from services.rates import fetch_file
        try: dates, rates = fetch_file()
        except Exception as exc:
            print(f'error: {exc}', file=sys.stderr); return 1
        print('dates,rates'); print(f'{dates},{rates}'); return 0
    if args.command == 'init':
        initialize(); return 0
    if args.command == 'serve':
        import uvicorn
        uvicorn.run('app_server.main:app', host='127.0.0.1', port=args.port); return 0
    return 2
