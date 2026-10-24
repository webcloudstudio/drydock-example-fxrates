"""Command line entry point."""
import argparse


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="fxrates")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init")
    load = sub.add_parser("load")
    load.add_argument("csv")
    fetch = sub.add_parser("fetch")
    serve = sub.add_parser("serve")
    serve.add_argument("--port", type=int, default=8000)
    args = parser.parse_args(argv)
    if args.command == "serve":
        import uvicorn
        uvicorn.run("app_server.main:app", host="127.0.0.1", port=args.port)
        return 0
    return 0
