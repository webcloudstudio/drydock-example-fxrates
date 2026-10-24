# COMPASS: FxRates

## Compass

Build a currency rates service, an executable named `fxrates` at the application root, as
described in `sources/INSTRUCTIONS.md`. A command line loads the ECB euro reference rate history
into SQLite, and a FastAPI JSON API serves the rates on a date, conversions between any two
currencies, and a currency's history with minimum, maximum, and mean.

Correctness is measured by `sources/run.sh`: it loads the supplied ECB files, starts the server on
a free local port, and makes 35 checks of command output and HTTP status and JSON body. The goal is
every check passing.

## Constraints

- Implement in Python 3.11 or newer with FastAPI and uvicorn over SQLite.
- Provide an executable named `fxrates` at the application root, invoked as `./fxrates <command>`.
  `fxrates serve` runs the server in the foreground and stops cleanly on SIGTERM.
- Read the database location from `DATABASE_URL`, then `DATABASE_PATH`, then `data/app.db`.
- Store rates as the ECB's published text; compute with `decimal`, never with floating point.
- Check a file in full before its first write.
- Tests stub the ECB download; no test opens a network connection.
- Diagnostics go to standard error and are never compared.

## Guardrails

- Do not modify, rewrite, regenerate, or substitute any file under `sources/`.
- Do not read `sources/run.sh` or any supplied data file from application code. Data reaches the
  database only through `fxrates load` or `fxrates fetch`.
- Do not hardcode a rate, a date, a count, or a computed value. Every value comes from a query.
- Do not open a database driver outside the shipped persistence library.

## Verification Protocol

| Story kind | Command | Asserts |
|---|---|---|
| Every behavioral story | `sh bin/test.sh` | exit `0` |
| Terminal story (once, last) | `sh sources/run.sh` | exit `0` |

<!-- drydock:build-write-guardrail:start -->
## Build Write Guardrail

- Authorized build directory: `/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261024.070101/build/FxRates`
- Authorized Target directory: `/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261024.070101/workspace/targets/FxRates`
- Build agents have permission to create, modify, and remove files required by the active build block inside these authorized directories.
- No path outside these authorized directories may be modified.
- Protected Drydock artifacts:
  - `/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261024.070101/workspace/targets/FxRates/blueprint/`
  - `/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261024.070101/workspace/targets/FxRates/MANIFEST.md`
  - `/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261024.070101/workspace/targets/FxRates/COMPASS.md`
  - `/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261024.070101/workspace/targets/FxRates/QuarterDeck/`
  - `/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261024.070101/workspace/targets/FxRates/evidence/`
<!-- drydock:build-write-guardrail:end -->
