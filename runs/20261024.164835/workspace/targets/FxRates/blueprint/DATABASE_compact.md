<!-- Compacted from DATABASE.md sha256=eb20e468d257f245e115cdae4c69932723bd538b6c0ec34c7f9ecb2288e9870c on 2026-10-24 by drydock build agent -->

# DATABASE: FxRates — consumer contract

Store ECB rates in `rates(date, currency, rate, id)`, with unique `(date, currency)`. Keep rate values as published text. Resolve storage from `DATABASE_URL`, then `DATABASE_PATH`, then `data/app.db`. Only the generated `persistence/` package accesses the database.

Available operations:

- `rates.replace_rate(date, currency, rate)`: upsert by `(date, currency)`.
- `rates.for_date(date)`: list matching rates, ordered by currency ascending.
- `rates.latest_on_or_before(requested_date)`: list rates at the latest publication date on or before the requested date, ordered by date descending.
- `rates.latest()`: list rates at the latest publication date, ordered by date descending.
- `rates.history(currency, start_date, end_date)`: list rates in the inclusive date range, ordered by date ascending.
- `rates.all()`: list all rates, ordered by date ascending.

Each operation returns `StoredRate(date: str, currency: str, rate: str)` rows; list operations return lists. Use the generated persistence package and its configured-store rollback fixture for database access.
