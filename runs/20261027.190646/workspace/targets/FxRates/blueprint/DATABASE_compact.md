<!-- Compacted from DATABASE.md sha256=67b7e9b8bdd2c825a3fedda981b4063c04c50608d7bcf8a3f3a11f5477dd137c on 2026-10-27 by drydock build agent -->

FxRates persistence surface (DATABASE.md, build order 1)
- Open: persistence.open_database(dsn) -> Database; persistence.initialize_database(dsn) -> Database (applies schema.sql, preserves data; close the result). Engine chosen from DSN: plain path or sqlite:// -> SQLite; postgres(ql):// -> PostgreSQL.
- Table rates(id INTEGER PK, date TEXT NOT NULL 'YYYY-MM-DD', currency TEXT NOT NULL, rate TEXT NOT NULL), UNIQUE(date, currency). Rates are stored as published text; never float.
- db.rates.replace_rate(date, currency, rate) -> (date, currency, rate): upsert on (date, currency).
- db.rates.list_through(through_date=None) -> rows (date, currency, rate): date <= through_date when given; order date desc, currency asc.
- db.rates.list_all() -> rows (date, currency, rate): order date asc, currency asc.
- db.rates.history(currency, start_date=None, end_date=None) -> rows (date, rate): inclusive bounds; order date asc.
- Rows are frozen dataclasses with attribute access. Application code never authors SQL or opens a driver.
- Startup never initializes; only explicit init uses initialize_database.
