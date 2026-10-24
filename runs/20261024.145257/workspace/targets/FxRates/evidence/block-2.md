# Evidence: Block 2 · Foundational (block-2)

- block type: block
- date: 2026-10-24
- resulting state: closed/failed
- story points (combined assembled cost): 9509
- execution id: -

## Stories built
- Declare the rates schema and persistence operations. (database-contract) [story]

## Stacked context
- stack: python_compact.md (SP 601)
- compass: COMPASS.md (SP 752)
- implements: DATABASE.md (SP 1472)
- context: ARCHITECTURE.md (SP 601)
- stack: persistence.md (SP 3845)
- stack: sqlite.md (SP 2195)

## Pre-build acceptance observation
- RED: rates-upsert (DATABASE.md)
  intent: Upserting a rate stores its published text and replaces the matching date and currency row.
  error: foundation not built: `persistence` is the package the database foundation (postgres.md, sqlite.md) builds, and the build directory has no `persistence/`. The criterion exercises the built application, so it was not run.
- RED: rates-list-date (DATABASE.md)
  intent: Listing rates by date returns the rate rows stored for that date.
  error: foundation not built: `persistence` is the package the database foundation (postgres.md, sqlite.md) builds, and the build directory has no `persistence/`. The criterion exercises the built application, so it was not run.
- RED: rates-list-currency (DATABASE.md)
  intent: Listing rates by currency returns its stored publication rows.
  error: foundation not built: `persistence` is the package the database foundation (postgres.md, sqlite.md) builds, and the build directory has no `persistence/`. The criterion exercises the built application, so it was not run.
- RED: rates-list-all (DATABASE.md)
  intent: Listing all rates includes a rate inserted by this check.
  error: foundation not built: `persistence` is the package the database foundation (postgres.md, sqlite.md) builds, and the build directory has no `persistence/`. The criterion exercises the built application, so it was not run.

## Post-build programmatic acceptance
- FAIL: rates-upsert (DATABASE.md)
  intent: Upserting a rate stores its published text and replaces the matching date and currency row.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not requested
  return code: 1
  stderr:
    --- drydock: values at failure ---
      name = 'get'
      granted = 'list_all, list_currency, list_date, upsert'
      self = <TableAccess rates: list_all, list_currency, list_date, upsert>
    --- drydock: end values ---
    Traceback (most recent call last):
      File "rates-upsert.py", line 9, in <module>
        first = db.rates.get(date=date, currency=currency)
                ^^^^^^^^^^^^
      File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261024.145257/build/FxRates/persistence/db.py", line 214, in __getattr__
        raise UnknownOperation(
    persistence.db.UnknownOperation: rates declares no 'get' operation. Declared: list_all, list_currency, list_date, upsert. Add an access pattern to DATABASE.md rather than reaching around this class.
- PASS: rates-list-date (DATABASE.md)
  intent: Listing rates by date returns the rate rows stored for that date.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not requested
  return code: 0
- PASS: rates-list-currency (DATABASE.md)
  intent: Listing rates by currency returns its stored publication rows.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not requested
  return code: 0
- PASS: rates-list-all (DATABASE.md)
  intent: Listing all rates includes a rate inserted by this check.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not requested
  return code: 0

## Failure
- summary: programmatic acceptance failed: rates-upsert
- detail:
    Block "Block 2 · Foundational" [block-2] failed its acceptance criteria.
      Story "Declare the rates schema and persistence operations." [database-contract] does not meet its own acceptance criteria:
        - AC rates-upsert — Upserting a rate stores its published text and replaces the matching date and currency row.
            assertion: failed with no diagnostic output
            raised at: db.py:214
            process exit code: 1
            values at failure:
              name = 'get'
              granted = 'list_all, list_currency, list_date, upsert'
              self = <TableAccess rates: list_all, list_currency, list_date, upsert>
            check stderr:
              Traceback (most recent call last):
                File "rates-upsert.py", line 9, in <module>
                  first = db.rates.get(date=date, currency=currency)
                          ^^^^^^^^^^^^
                File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261024.145257/build/FxRates/persistence/db.py", line 214, in __getattr__
                  raise UnknownOperation(
              persistence.db.UnknownOperation: rates declares no 'get' operation. Declared: list_all, list_currency, list_date, upsert. Add an access pattern to DATABASE.md rather than reaching around this class.

## Build summary
(no summary returned)
