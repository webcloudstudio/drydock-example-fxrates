<!-- Compacted from ARCHITECTURE.md sha256=6f19609e3501b5c81682988bc8e666bd2505beb5942c619bd31e54613eef90f4 on 2026-10-24 by drydock build agent -->

# FxRates module contract

- `cli` owns command dispatch and the root `./fxrates` entry point; it depends on application services and configuration.
- `app_server` owns the FastAPI factory, routes, and HTTP test client; it depends on application services.
- Application services own CSV validation, ingestion, rate lookup, conversion, and history calculations; they use only public `persistence` operations.
- `persistence` owns the database connection, schema, and generated repository operations.
- Configuration owns database location resolution from environment variables.

Python 3.11+, FastAPI, SQLite through the generated persistence library, pytest, and ECB CSV/ZIP inputs are the specified stack. Preserve published rate text and use `decimal` for calculations. The public packages `cli`, `app_server`, and `persistence` must be importable.
