<!-- Compacted from DATABASE.md sha256=0a49cb53f2c442a164ebfe3827cd07d7ad2d554f02ac23f0e1eaa9d3ffbe5100 on 2026-10-24 by drydock build agent -->

# FxRates persistence contract

The generated `persistence` package is the only database access boundary. It exposes `open_database(dsn)`, `SCHEMA`, and `db.rates` operations. Rates retain ECB text exactly; arithmetic belongs in application services and uses `decimal`.

The `rates` table has `id INTEGER PRIMARY KEY`, `date TEXT NOT NULL`, `currency TEXT NOT NULL`, and `rate TEXT NOT NULL`, with a unique `(date, currency)` key.

- `rates.get(date: str, currency: str)` returns a rate row or `None`.
- `rates.list(date?: str, currency?: str)` returns rows filtered by supplied equality fields.
- `rates.upsert(date: str, currency: str, rate: str)` inserts or replaces a rate and returns its row.
- `rates.delete(date: str, currency: str)` deletes the matching row and returns its date and currency or `None`.

Resolve the database location from `DATABASE_URL`, then `DATABASE_PATH`, then `data/app.db`. `fxrates init` resets the rates store through the persistence boundary. Do not access the database driver outside `persistence/` or create schema at application startup.

Database criteria use `persistence.testing.db_session()` and its configured, provisioned store. Pass its yielded database through the operation and read back state in the same rollback transaction. Do not replace the configured store or delete unrelated records.
