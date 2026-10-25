# FxRates application boundaries

FxRates is a Python 3.11+ command-line and HTTP service. The root `fxrates`
executable delegates command handling to `cli`; the `app_server` package owns
the FastAPI application and uvicorn entry point.

## Module ownership

- **Configuration:** one application configuration module resolves
  `DATABASE_URL`, then `DATABASE_PATH`, then `data/app.db`.
- **Persistence:** the generated `persistence` package is the only code allowed
  to open a database driver. It provides the rates repository operations.
- **CLI:** `cli` parses commands and arguments, returns exit codes, and writes
  command output. The root `fxrates` file is only the executable launcher.
- **HTTP service:** `app_server` creates the FastAPI application and exposes
  JSON routes through uvicorn.
- **ECB integration:** the CLI fetch workflow downloads and extracts the ECB
  archive. Tests can replace its downloader with a stub.

CLI workflows and HTTP routes call application behavior and its declared
repository operations; neither accesses database connections directly.
