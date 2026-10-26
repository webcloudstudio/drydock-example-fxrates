# Evidence: Block 2 · Foundational (block-2)

- block type: block
- date: 2026-10-25
- resulting state: closed/verified
- story points (combined assembled cost): 9632
- execution id: -

## Stories built
- Declare the rates persistence contract. (database) [story]

## Stacked context
- stack: python_compact.md (SP 601)
- compass: COMPASS.md (SP 752)
- implements: DATABASE.md (SP 2032)
- stack: persistence.md (SP 4001)
- stack: sqlite.md (SP 2195)

## Pre-build acceptance observation
- RED: rates-upsert (DATABASE.md)
  intent: The rates upsert operation replaces an existing date and currency rate and returns the stored row.
  error: foundation not built: `persistence` is the package the database foundation (postgres.md, sqlite.md) builds, and the build directory has no `persistence/`. The criterion exercises the built application, so it was not run.
- RED: rates-effective-rates (DATABASE.md)
  intent: Effective-date lookup returns stored rows on or before its bound in descending date order.
  error: foundation not built: `persistence` is the package the database foundation (postgres.md, sqlite.md) builds, and the build directory has no `persistence/`. The criterion exercises the built application, so it was not run.
- RED: rates-by-date (DATABASE.md)
  intent: Date lookup returns the stored rows for the requested date.
  error: foundation not built: `persistence` is the package the database foundation (postgres.md, sqlite.md) builds, and the build directory has no `persistence/`. The criterion exercises the built application, so it was not run.
- RED: rates-history (DATABASE.md)
  intent: Currency history returns matching rows in ascending date order within its inclusive bounds.
  error: foundation not built: `persistence` is the package the database foundation (postgres.md, sqlite.md) builds, and the build directory has no `persistence/`. The criterion exercises the built application, so it was not run.
- RED: rates-list (DATABASE.md)
  intent: The rates list operation reads back all rows created by the criterion in declared date and currency order.
  error: foundation not built: `persistence` is the package the database foundation (postgres.md, sqlite.md) builds, and the build directory has no `persistence/`. The criterion exercises the built application, so it was not run.

## Post-build programmatic acceptance
- PASS: rates-upsert (DATABASE.md)
  intent: The rates upsert operation replaces an existing date and currency rate and returns the stored row.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261026.011843/build/FxRates/.venv/bin/python
  provisioning: not requested
  return code: 0
- PASS: rates-effective-rates (DATABASE.md)
  intent: Effective-date lookup returns stored rows on or before its bound in descending date order.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261026.011843/build/FxRates/.venv/bin/python
  provisioning: not requested
  return code: 0
- PASS: rates-by-date (DATABASE.md)
  intent: Date lookup returns the stored rows for the requested date.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261026.011843/build/FxRates/.venv/bin/python
  provisioning: not requested
  return code: 0
- PASS: rates-history (DATABASE.md)
  intent: Currency history returns matching rows in ascending date order within its inclusive bounds.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261026.011843/build/FxRates/.venv/bin/python
  provisioning: not requested
  return code: 0
- PASS: rates-list (DATABASE.md)
  intent: The rates list operation reads back all rows created by the criterion in declared date and currency order.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261026.011843/build/FxRates/.venv/bin/python
  provisioning: not requested
  return code: 0

## Build summary
(no summary returned)
