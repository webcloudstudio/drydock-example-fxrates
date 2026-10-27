<!-- Compacted from DATABASE.md sha256=54097832936d2ba5b7c2f8d44ed278d915a1ad842f4bab76d284889f3ecf4a66 on 2026-10-26 by drydock build agent -->

Rates are stored in `rates(id, date, currency, rate)`, with text values and a unique `(date, currency)` key. The generated repository currently exposes `upsert`, `by_date`, `publications_through`, `history`, and `list`; history bounds are inclusive and results use their declared ordering. Application code must use the generated persistence package and resolve the store from `DATABASE_URL`, then `DATABASE_PATH`, then `data/app.db`.
