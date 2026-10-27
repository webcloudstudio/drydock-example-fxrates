"""Command-line package: `main(argv) -> int` dispatches to handlers registered by command stories."""

from cli.dispatcher import main, register_command
from cli import init_command  # noqa: F401  registers the `init` handler at import
from cli import load_command  # noqa: F401  registers the `load` handler at import
from cli import fetch_command  # noqa: F401  registers the `fetch` handler at import
from cli import serve_command  # noqa: F401  registers the `serve` handler at import

__all__ = ["main", "register_command"]
