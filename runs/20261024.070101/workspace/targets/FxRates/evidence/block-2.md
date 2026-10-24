# Evidence: Block 2 · Foundational (block-2)

- block type: block
- date: 2026-10-24
- resulting state: closed/failed
- story points (combined assembled cost): 9596
- execution id: -

## Stories built
- Declare the rates schema and repository contract. (database) [story]

## Stacked context
- stack: python_compact.md (SP 601)
- compass: COMPASS.md (SP 752)
- implements: DATABASE.md (SP 1337)
- stack: common_compact.md (SP 1079)
- stack: persistence.md (SP 3845)
- stack: sqlite_compact.md (SP 1943)

## Pre-build acceptance observation
- RED: rates-upsert (DATABASE.md)
  intent: The rates upsert operation stores the supplied published text and replaces the row for the same date and currency.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "rates-upsert.py", line 1, in <module>
        from persistence.testing import db_session
    ModuleNotFoundError: No module named 'persistence.testing'
- RED: rates-list (DATABASE.md)
  intent: The rates list operation returns stored rows and applies its declared date and currency equality filters.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "rates-list.py", line 1, in <module>
        from persistence.testing import db_session
    ModuleNotFoundError: No module named 'persistence.testing'
- RED: rates-delete (DATABASE.md)
  intent: The rates delete operation removes only the row selected by its date and currency key.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "rates-delete.py", line 1, in <module>
        from persistence.testing import db_session
    ModuleNotFoundError: No module named 'persistence.testing'

## Post-build programmatic acceptance
- PASS: rates-upsert (DATABASE.md)
  intent: The rates upsert operation stores the supplied published text and replaces the row for the same date and currency.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not requested
  return code: 0
- PASS: rates-list (DATABASE.md)
  intent: The rates list operation returns stored rows and applies its declared date and currency equality filters.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not requested
  return code: 0
- FAIL: rates-delete (DATABASE.md)
  intent: The rates delete operation removes only the row selected by its date and currency key.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/.venv/bin/python
  provisioning: not requested
  return code: 1
  stderr:
    --- drydock: values at failure ---
      operation = Operation(identifier='FEATURE-RATE-003', table='rates', verb='delete', inputs=('date', 'currency'), row=<class 'persistence.schema.FieldType'>, columns=('date', 'currency'), match=('date', 'currency'), name='delete')
    --- drydock: end values ---
    Traceback (most recent call last):
      File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261024.070101/build/FxRates/persistence/db.py", line 390, in run
        result = self._dispatch(operation, cursor, names, values)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261024.070101/build/FxRates/persistence/db.py", line 474, in _dispatch
        return self._build(operation, names, values) if cursor.rowcount else None
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261024.070101/build/FxRates/persistence/db.py", line 503, in _build
        return operation.row(**{
               ^^^^^^^^^^^^^^^^^
    TypeError: FieldType.__init__() missing 2 required positional arguments: 'id' and 'rate'
    
    The above exception was the direct cause of the following exception:
    
    Traceback (most recent call last):
      File "rates-delete.py", line 8, in <module>
        deleted = db.rates.delete(date=date, currency=currency)
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261024.070101/build/FxRates/persistence/db.py", line 218, in <lambda>
        return lambda **arguments: self._database.run(operation, arguments)
                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261024.070101/build/FxRates/persistence/db.py", line 398, in run
        raise PersistenceError(f"{operation.identifier} failed: {exc}") from exc
    persistence.db.PersistenceError: FEATURE-RATE-003 failed: FieldType.__init__() missing 2 required positional arguments: 'id' and 'rate'

## Failure
- summary: programmatic acceptance failed: rates-delete
- detail:
    Block "Block 2 · Foundational" [block-2] failed its acceptance criteria.
      Story "Declare the rates schema and repository contract." [database] does not meet its own acceptance criteria:
        - AC rates-delete — The rates delete operation removes only the row selected by its date and currency key.
            assertion: persistence.db.PersistenceError: FEATURE-RATE-003 failed: FieldType.__init__() missing 2 required positional arguments: 'id' and 'rate'
            raised at: db.py:398
            process exit code: 1
            error: persistence.db.PersistenceError: FEATURE-RATE-003 failed: FieldType.__init__() missing 2 required positional arguments: 'id' and 'rate'
            values at failure:
              operation = Operation(identifier='FEATURE-RATE-003', table='rates', verb='delete', inputs=('date', 'currency'), row=<class 'persistence.schema.FieldType'>, columns=('date', 'currency'), match=('date', 'currency'), name='delete')
            check stderr:
                  result = self._dispatch(operation, cursor, names, values)
                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261024.070101/build/FxRates/persistence/db.py", line 474, in _dispatch
                  return self._build(operation, names, values) if cursor.rowcount else None
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261024.070101/build/FxRates/persistence/db.py", line 503, in _build
                  return operation.row(**{
                         ^^^^^^^^^^^^^^^^^
              TypeError: FieldType.__init__() missing 2 required positional arguments: 'id' and 'rate'
              The above exception was the direct cause of the following exception:
              Traceback (most recent call last):
                File "rates-delete.py", line 8, in <module>
                  deleted = db.rates.delete(date=date, currency=currency)
                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261024.070101/build/FxRates/persistence/db.py", line 218, in <lambda>
                  return lambda **arguments: self._database.run(operation, arguments)
                                             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                File "/mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261024.070101/build/FxRates/persistence/db.py", line 398, in run
                  raise PersistenceError(f"{operation.identifier} failed: {exc}") from exc
              persistence.db.PersistenceError: FEATURE-RATE-003 failed: FieldType.__init__() missing 2 required positional arguments: 'id' and 'rate'
              … 2 earlier line(s) omitted, --full for all

## Build summary
(no summary returned)
