# Evidence: Block 2 · Foundational (block-2)

- block type: block
- date: 2026-10-27
- resulting state: closed/verified
- story points (combined assembled cost): 18040
- execution id: -

## Stories built
- Declare the rates store and its repository operations; Drydock generates the persistence package. (database) [story]

## Acceptance tooling authorization
- DATABASE.md#rates-replace-rate: executable=python3; scope=test; authorization=existing Target environment
- DATABASE.md#rates-list-through: executable=python3; scope=test; authorization=existing Target environment
- DATABASE.md#rates-list-all: executable=python3; scope=test; authorization=existing Target environment
- DATABASE.md#rates-history: executable=python3; scope=test; authorization=existing Target environment

## Stacked context
- stack: python_compact.md (SP 1002)
- compass: COMPASS.md (SP 1152)
- implements: DATABASE.md (SP 3607)
- stack: common_compact.md (SP 1653)
- stack: persistence.md (SP 6912)
- stack: sqlite.md (SP 3500)

## Pre-build acceptance observation
- RED: rates-replace-rate (DATABASE.md)
  intent: Upserting the same date and currency twice leaves one row holding the second published text, and the first call returns the row it stored.
  error: foundation not built: `persistence` is the package the database foundation (postgres.md, sqlite.md) builds, and the build directory has no `persistence/`. The criterion exercises the built application, so it was not run.
- RED: rates-list-through (DATABASE.md)
  intent: list_through returns only rates on or before the bound, ordered by date descending then currency ascending, and with no bound it also includes later dates.
  error: foundation not built: `persistence` is the package the database foundation (postgres.md, sqlite.md) builds, and the build directory has no `persistence/`. The criterion exercises the built application, so it was not run.
- RED: rates-list-all (DATABASE.md)
  intent: list_all returns every stored rate ordered by date ascending then currency ascending, so a YYY code precedes ZZZ on one date.
  error: foundation not built: `persistence` is the package the database foundation (postgres.md, sqlite.md) builds, and the build directory has no `persistence/`. The criterion exercises the built application, so it was not run.
- RED: rates-history (DATABASE.md)
  intent: history returns one currency's points ascending by date, honouring optional inclusive start and end bounds and excluding other currencies.
  error: foundation not built: `persistence` is the package the database foundation (postgres.md, sqlite.md) builds, and the build directory has no `persistence/`. The criterion exercises the built application, so it was not run.

## Post-build programmatic acceptance
- PASS: rates-replace-rate (DATABASE.md)
  intent: Upserting the same date and currency twice leaves one row holding the second published text, and the first call returns the row it stored.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.190646/build/FxRates/.venv/bin/python
  provisioning: not requested
  return code: 0
- PASS: rates-list-through (DATABASE.md)
  intent: list_through returns only rates on or before the bound, ordered by date descending then currency ascending, and with no bound it also includes later dates.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.190646/build/FxRates/.venv/bin/python
  provisioning: not requested
  return code: 0
- PASS: rates-list-all (DATABASE.md)
  intent: list_all returns every stored rate ordered by date ascending then currency ascending, so a YYY code precedes ZZZ on one date.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.190646/build/FxRates/.venv/bin/python
  provisioning: not requested
  return code: 0
- PASS: rates-history (DATABASE.md)
  intent: history returns one currency's points ascending by date, honouring optional inclusive start and end bounds and excluding other currencies.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.190646/build/FxRates/.venv/bin/python
  provisioning: not requested
  return code: 0

## Build summary
(no summary returned)
