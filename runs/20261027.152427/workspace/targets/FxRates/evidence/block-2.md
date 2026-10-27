# Evidence: Block 2 · Foundational (block-2)

- block type: block
- date: 2026-10-27
- resulting state: closed/verified
- story points (combined assembled cost): 18693
- execution id: -

## Stories built
- Declare the rates table and every repository operation the stories need; Drydock generates the persistence package. (database) [story]

## Acceptance tooling authorization
- DATABASE.md#rates-replace-rate: executable=python3; scope=test; authorization=existing Target environment
- DATABASE.md#rates-list-for-date: executable=python3; scope=test; authorization=existing Target environment
- DATABASE.md#rates-list-on-or-before: executable=python3; scope=test; authorization=existing Target environment
- DATABASE.md#rates-list-all-keys: executable=python3; scope=test; authorization=existing Target environment
- DATABASE.md#rates-list-currencies: executable=python3; scope=test; authorization=existing Target environment
- DATABASE.md#rates-list-currency-history: executable=python3; scope=test; authorization=existing Target environment
- DATABASE.md#rates-delete-from-date: executable=python3; scope=test; authorization=existing Target environment

## Stacked context
- stack: python_compact.md (SP 921)
- compass: COMPASS.md (SP 1152)
- implements: DATABASE.md (SP 4877)
- stack: common_compact.md (SP 1653)
- stack: persistence.md (SP 6507)
- stack: sqlite.md (SP 3364)

## Pre-build acceptance observation
- RED: rates-replace-rate (DATABASE.md)
  intent: Storing a rate for an existing (date, currency) replaces its text rather than adding a row, and the read-back returns the second text exactly.
  error: foundation not built: `persistence` is the package the database foundation (postgres.md, sqlite.md) builds, and the build directory has no `persistence/`. The criterion exercises the built application, so it was not run.
- RED: rates-list-for-date (DATABASE.md)
  intent: Listing one date returns only that date's rates, ordered by currency ascending.
  error: foundation not built: `persistence` is the package the database foundation (postgres.md, sqlite.md) builds, and the build directory has no `persistence/`. The criterion exercises the built application, so it was not run.
- RED: rates-list-on-or-before (DATABASE.md)
  intent: Dates come back latest first and bounded by as_of inclusive, so the first row is the effective date for a request between two publications.
  error: foundation not built: `persistence` is the package the database foundation (postgres.md, sqlite.md) builds, and the build directory has no `persistence/`. The criterion exercises the built application, so it was not run.
- RED: rates-list-all-keys (DATABASE.md)
  intent: Every stored key at or after the lower bound is listed in ascending date order, and a bound after a row excludes it.
  error: foundation not built: `persistence` is the package the database foundation (postgres.md, sqlite.md) builds, and the build directory has no `persistence/`. The criterion exercises the built application, so it was not run.
- RED: rates-list-currencies (DATABASE.md)
  intent: Currency codes are listed in ascending order for rows at or after the lower bound.
  error: foundation not built: `persistence` is the package the database foundation (postgres.md, sqlite.md) builds, and the build directory has no `persistence/`. The criterion exercises the built application, so it was not run.
- RED: rates-list-currency-history (DATABASE.md)
  intent: A currency's history is filtered by inclusive optional bounds and sorted by date ascending; an inverted range is empty.
  error: foundation not built: `persistence` is the package the database foundation (postgres.md, sqlite.md) builds, and the build directory has no `persistence/`. The criterion exercises the built application, so it was not run.
- RED: rates-delete-from-date (DATABASE.md)
  intent: Deleting from a date removes rates on or after it and leaves earlier ones, and reports how many rows went.
  error: foundation not built: `persistence` is the package the database foundation (postgres.md, sqlite.md) builds, and the build directory has no `persistence/`. The criterion exercises the built application, so it was not run.

## Post-build programmatic acceptance
- PASS: rates-replace-rate (DATABASE.md)
  intent: Storing a rate for an existing (date, currency) replaces its text rather than adding a row, and the read-back returns the second text exactly.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not requested
  return code: 0
- PASS: rates-list-for-date (DATABASE.md)
  intent: Listing one date returns only that date's rates, ordered by currency ascending.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not requested
  return code: 0
- PASS: rates-list-on-or-before (DATABASE.md)
  intent: Dates come back latest first and bounded by as_of inclusive, so the first row is the effective date for a request between two publications.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not requested
  return code: 0
- PASS: rates-list-all-keys (DATABASE.md)
  intent: Every stored key at or after the lower bound is listed in ascending date order, and a bound after a row excludes it.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not requested
  return code: 0
- PASS: rates-list-currencies (DATABASE.md)
  intent: Currency codes are listed in ascending order for rows at or after the lower bound.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not requested
  return code: 0
- PASS: rates-list-currency-history (DATABASE.md)
  intent: A currency's history is filtered by inclusive optional bounds and sorted by date ascending; an inverted range is empty.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not requested
  return code: 0
- PASS: rates-delete-from-date (DATABASE.md)
  intent: Deleting from a date removes rates on or after it and leaves earlier ones, and reports how many rows went.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not requested
  return code: 0

## Build summary
(no summary returned)
