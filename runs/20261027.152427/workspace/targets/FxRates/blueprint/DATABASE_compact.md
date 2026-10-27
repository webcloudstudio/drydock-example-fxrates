<!-- Compacted from DATABASE.md sha256=7a1850b2e94d8b305d500ff56581a92e07daf9a544b96984e9fed361da8f0b74 on 2026-10-27 by drydock build agent -->

Store: SQLite or PostgreSQL via `open_database(dsn)`; only the generated `persistence` package reaches the store. Calls are `db.rates.<op>(...)`; rows expose `.date`, `.currency`, `.rate` (text, never float).

Table `rates`: `id` INTEGER PK; `date` TEXT NOT NULL (YYYY-MM-DD); `currency` TEXT NOT NULL (3-letter uppercase); `rate` TEXT NOT NULL (as published). UNIQUE(date, currency).

Operations:
- `rates.replace_rate(date: str, currency: str, rate: str)` → row(date, currency, rate). Upsert on (date, currency).
- `rates.list_for_date(date: str)` → rows(date, currency, rate), exact date, order currency asc.
- `rates.list_on_or_before(as_of: str | None = None)` → rows(date), date <= as_of inclusive, order date desc. First row is the effective date; no rows means none.
- `rates.list_all_keys(since: str | None = None)` → rows(date, currency), date >= since, order date asc.
- `rates.list_currencies(since: str | None = None)` → rows(currency), date >= since, order currency asc; one row per stored rate, so dedupe in the service.
- `rates.list_currency_history(currency: str | None, start_date: str | None, end_date: str | None)` → rows(date, currency, rate), inclusive bounds, order date asc. Empty with only `currency` means no stored rate.
- `rates.delete_from_date(from_date: str)` → int removed count, date >= from_date. `init` passes `0000-01-01`.

Config: DATABASE_URL (takes precedence, optional sqlite:// prefix), DATABASE_PATH (default data/app.db).
Testing: `persistence.testing.db_session()` yields a rolled-back session over the provisioned store.
Services derive counts, first/last dates, and distinct currencies from list results; no aggregate operations exist.
