<!-- Compacted from ARCHITECTURE.md sha256=3c1ba416c40fca4ccb89d71893212a371cc5e15e1734eecb354bc3418c93aabd on 2026-10-25 by drydock build agent -->

- Python 3.11+; FastAPI and uvicorn; SQLite through the `persistence` package; pytest.
- Module ownership: `config` resolves runtime settings from environment variables; `cli` parses and dispatches commands; `app_server` owns the FastAPI factory and routes; `services` owns feature behavior; `persistence` owns database connections and repository operations.
- Routes delegate to services. Features call declared persistence operations and do not open a database driver or issue SQL directly.
- Export `cli.main`, `app_server.main.create_app`, `app_server.main.app`, and `persistence.open_database`.
- Database location precedence: `DATABASE_URL`, then `DATABASE_PATH`, then `data/app.db`.
- Store ECB rates as published text and use `Decimal` for arithmetic.
- Acceptance import check: the four declared entry points must import and be callable or non-null as specified.
