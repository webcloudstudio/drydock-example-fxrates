<!-- Compacted from ARCHITECTURE.md sha256=89e00be8e977894123614efc8507ad660a4675307e5e2e0658a8af65bdfb37dc on 2026-10-27 by drydock build agent -->

Foundation contract (FxRates, block-1)
- Executable `fxrates` at app root is owned by the CLI foundation (not in this block).
- `config.database_path() -> pathlib.Path`: resolves DATABASE_URL (optional `sqlite://` prefix stripped; unset/empty skipped), then DATABASE_PATH (unset/empty skipped), then `data/app.db` (returned as relative `Path("data/app.db")`). Reads env on every call.
- Env vars: DATABASE_URL, DATABASE_PATH (documented in .env.example).
- `bin/test.sh`: POSIX sh; activates `.venv`; `exec pytest -q`; exit status is pytest's; nonzero if `.venv` missing.
- pyproject: requires-python >=3.11; deps fastapi, httpx2, pytest, uvicorn; pytest testpaths=tests, pythonpath=["."].
- Module rule: `config.py` and any `cli/`, `app_server/` modules must not import sqlite3 or psycopg.
