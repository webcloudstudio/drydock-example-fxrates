# FEATURE: Database Selection

| Field | Value |
|-------|-------|
| Version | 20261027 V1 |
| Description | Resolve the database location from DATABASE_URL, then DATABASE_PATH, then data/app.db, and open it through the persistence library. |
| Depends On | ARCHITECTURE.md, DATABASE.md |
| Provides | fxrates_app.config.database_path |
| Consumes | persistence.open_database |

## Purpose

Give every command and route one place that decides which SQLite file to use.

## Interface

```python
# fxrates_app/config.py
def database_path() -> str: ...
def open_store() -> Database: ...   # persistence.open_database(database_path())
```

Resolution order:

1. `DATABASE_URL`, when set and nonempty; an optional `sqlite://` prefix is removed.
2. `DATABASE_PATH`, when set and nonempty.
3. `data/app.db`.

An empty value counts as unset. The function reads the environment at call time. Application code
opens the store only through `persistence.open_database` and never imports a driver.

## Database Interface

- None — persistence is owned by DATABASE.md.

## Programmatic Acceptance

=== AC dbsel-url-wins-with-prefix ===
Intent: DATABASE_URL takes precedence over DATABASE_PATH and its sqlite:// prefix is removed.
Requires: executable=python3; scope=test

from drydock_acceptance import database_environment
from fxrates_app.config import database_path

with database_environment(url="sqlite://primary.db", path="fallback.db") as root:
    assert str(database_path()) == str(root / "primary.db")
=== END AC dbsel-url-wins-with-prefix ===

=== AC dbsel-url-without-prefix ===
Intent: A DATABASE_URL without the prefix is used as the file name.
Requires: executable=python3; scope=test

from drydock_acceptance import database_environment
from fxrates_app.config import database_path

with database_environment(url="plain.db", path="fallback.db") as root:
    assert str(database_path()) == str(root / "plain.db")
=== END AC dbsel-url-without-prefix ===

=== AC dbsel-path-fallback ===
Intent: With DATABASE_URL unset or empty, DATABASE_PATH is used.
Requires: executable=python3; scope=test

from drydock_acceptance import database_environment
from fxrates_app.config import database_path

with database_environment(path="fallback.db") as root:
    assert str(database_path()) == str(root / "fallback.db")
with database_environment(url="", path="fallback.db") as root:
    assert str(database_path()) == str(root / "fallback.db")
=== END AC dbsel-path-fallback ===

=== AC dbsel-default-path ===
Intent: With both variables unset, or both empty, the default data/app.db applies.
Requires: executable=python3; scope=test

from drydock_acceptance import database_environment
from fxrates_app.config import database_path

with database_environment():
    assert str(database_path()) == "data/app.db"
with database_environment(url="", path=""):
    assert str(database_path()) == "data/app.db"
=== END AC dbsel-default-path ===

=== AC dbsel-open-store ===
Intent: open_store opens the selected file through the persistence library without error.
Requires: executable=python3; scope=test

from drydock_acceptance import database_environment
from fxrates_app.config import open_store

with database_environment(url="sqlite://opened.db") as root:
    db = open_store()
    assert db is not None
=== END AC dbsel-open-store ===

## User Acceptance

- None.

## Guardrails

- Application code never imports a database driver; the store is reached only through `persistence.open_database`.
- The resolution order is fixed: `DATABASE_URL`, then `DATABASE_PATH`, then `data/app.db`.
