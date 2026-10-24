<!-- Compacted from ARCHITECTURE.md sha256=56a190fe12e4c91ef834fd0f9f064a75b62ed94ade400a1205ce945f80b666a9 on 2026-10-24 by drydock build agent -->

- `config.database_dsn()` resolves `DATABASE_URL`, then `DATABASE_PATH`, then `data/app.db`; runtime settings belong at the configuration boundary.
- `cli` owns command parsing and dispatch; `app_server` owns the FastAPI and HTTP boundary; `services` owns application behavior; `persistence` owns database access through the shipped persistence library.
- Application modules must not import database drivers or issue SQL. Store ECB rates as published text and use `decimal.Decimal` for arithmetic.
- Stack: Python 3.11+, FastAPI, uvicorn, SQLite, pytest, and POSIX sh.
