<!-- Compacted from ARCHITECTURE.md sha256=c0c8a5e7a3d5142d1daf0fd898de36ed4f766fb554c0250f80d781debf599a34 on 2026-10-26 by drydock build agent -->

Python 3.11+, FastAPI, uvicorn, and SQLite. `cli` owns the root executable and dispatch, `app_server` owns the application factory and routes, `services` owns shared behavior, `persistence` owns generated storage access, and `config` owns database location resolution. HTTP handlers and CLI commands call services; only persistence accesses the database. Preserve ECB rates as text and use `Decimal` for arithmetic.
