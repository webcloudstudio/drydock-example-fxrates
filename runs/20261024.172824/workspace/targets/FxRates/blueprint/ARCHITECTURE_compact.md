<!-- Compacted from ARCHITECTURE.md sha256=2117d9b60b76e3cb1122735faf06c04b4a2eec03c7650e4549abb34fc11a5baf on 2026-10-24 by drydock build agent -->

# FxRates Architecture Contract

- Python 3.11+, FastAPI, SQLite through the generated persistence package, CLI executable `./fxrates`, and pytest.
- Boundaries: `app_server` registers routes and calls services; `services` owns rate behavior and calls declared persistence operations; `cli` parses and dispatches to services or the server runner; `persistence` owns database access; `bin` provides the POSIX test launcher.
- Interfaces: `app_server.main:create_app() -> FastAPI`, module-level `app`; `cli.main(argv: list[str] | None = None) -> int`; `persistence.open_database(dsn)` and `db.rates`; `app_server.testing.web_client()`; `cli.testing.cli_runner(*args) -> (exit_code, stdout, stderr)`.
- Database location precedence: `DATABASE_URL`, then `DATABASE_PATH`, then `data/app.db`. Store published rates as text and use `decimal` for arithmetic.
- CLI commands: `init`, `load`, `fetch`, `serve`. The root executable is `fxrates`.
- Acceptance contract `architecture-imports`: the app factory, app, web client, CLI entry point, and CLI runner must be importable and callable as applicable.
- Do not access SQLite directly from the CLI or API, and do not read grader scripts or supplied data from application code.
