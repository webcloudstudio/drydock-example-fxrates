<!-- Compacted from ARCHITECTURE.md sha256=fca49b5a503196bbe0f78b1c40a6b9bcf976d04dbe9c7cc5555ce3cc19f60c9e on 2026-10-25 by drydock build agent -->

# FxRates Architecture Contract

- Python 3.11+ application with a root `./fxrates` executable, `cli` package, and `app_server` FastAPI package.
- `app_server.main` provides `create_app() -> FastAPI` and module-level `app`; serve locally on `127.0.0.1` with uvicorn and support clean SIGTERM shutdown.
- Application code uses the generated `persistence` boundary and configured database location. Preserve rates as published text and use decimal arithmetic for calculations.
- Do not read `sources/run.sh` or supplied data files from application code. Validate a complete input file before its first write.
