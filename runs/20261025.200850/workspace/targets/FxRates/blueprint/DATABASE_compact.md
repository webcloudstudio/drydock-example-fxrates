<!-- Compacted from DATABASE.md sha256=24a0053d7865e21871afcd03af9f4bf6f463aecd1ba0442128113a363ddbe2ed on 2026-10-25 by drydock build agent -->

# FxRates Persistence Contract

- Use the generated `persistence` package as the only database access boundary. Resolve the store from `DATABASE_URL`, then `DATABASE_PATH`, then `data/app.db`.
- `rates` stores `date`, `currency`, and published `rate` as text, with a surrogate integer `id` and a unique `(date, currency)` key.
- Repository operations: `rates.upsert(date, currency, rate)`, `rates.get(date, currency)`, `rates.list(currency?, start_date?, end_date?)` ordered by date then currency ascending, and `rates.delete(date, currency)`.
- Preserve rate text exactly. Do not access the database driver outside `persistence/` or create schema at application startup.
