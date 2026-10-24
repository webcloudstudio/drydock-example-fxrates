# Evidence: Block 2 · Foundational (block-2)

- block type: block
- date: 2026-10-24
- resulting state: closed/verified
- story points (combined assembled cost): 8859
- execution id: -

## Stories built
- Declare the rates schema and repository operations. (database) [story]

## Stacked context
- stack: python_compact.md (SP 601)
- compass: COMPASS.md (SP 752)
- implements: DATABASE.md (SP 1523)
- stack: sqlite_compact.md (SP 1943)
- stack: persistence.md (SP 4001)

## Pre-build acceptance observation
- RED: rates-get-round-trip (DATABASE.md)
  intent: A rate can be retrieved by its date and currency key.
  error: foundation not built: `persistence` is the package the database foundation (postgres.md, sqlite.md) builds, and the build directory has no `persistence/`. The criterion exercises the built application, so it was not run.
- RED: rates-list-date (DATABASE.md)
  intent: Listing rates filters by publication date and returns currency order.
  error: foundation not built: `persistence` is the package the database foundation (postgres.md, sqlite.md) builds, and the build directory has no `persistence/`. The criterion exercises the built application, so it was not run.
- RED: rates-upsert-replaces (DATABASE.md)
  intent: Upserting the same date and currency replaces its stored text.
  error: foundation not built: `persistence` is the package the database foundation (postgres.md, sqlite.md) builds, and the build directory has no `persistence/`. The criterion exercises the built application, so it was not run.
- RED: rates-delete-round-trip (DATABASE.md)
  intent: Deleting a rate by date and currency removes that stored row.
  error: foundation not built: `persistence` is the package the database foundation (postgres.md, sqlite.md) builds, and the build directory has no `persistence/`. The criterion exercises the built application, so it was not run.

## Post-build programmatic acceptance
- PASS: rates-get-round-trip (DATABASE.md)
  intent: A rate can be retrieved by its date and currency key.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not requested
  return code: 0
- PASS: rates-list-date (DATABASE.md)
  intent: Listing rates filters by publication date and returns currency order.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not requested
  return code: 0
- PASS: rates-upsert-replaces (DATABASE.md)
  intent: Upserting the same date and currency replaces its stored text.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not requested
  return code: 0
- PASS: rates-delete-round-trip (DATABASE.md)
  intent: Deleting a rate by date and currency removes that stored row.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not requested
  return code: 0

## Build summary
(no summary returned)
