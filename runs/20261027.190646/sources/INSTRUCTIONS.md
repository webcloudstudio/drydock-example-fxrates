# Build Instructions: A Currency Rates Service

## Objective

Build a small web service that keeps the European Central Bank (ECB) euro reference exchange
rates and answers questions about them: the rates on a date, a currency conversion, and a
currency's history over a period. A command-line tool loads the ECB's published history file into
a local database. A JSON HTTP API serves the answers.

## Stack

Implement in Python 3.11 or newer with FastAPI, served by uvicorn, over SQLite. Tests run under
pytest, using FastAPI's `TestClient` for the API. The product is an executable named `fxrates` at
the application root.

## Run Harness

`sources/run.sh` is the scoring entry point. It is supplied, not authored, and is staged verbatim
into the application root with the data files. `drydock uat` runs `sh sources/run.sh` from the
completed application root and takes its exit code and output as the score.

The harness selects a fresh temporary SQLite database through `DATABASE_URL` and runs
`./fxrates init` before any load or server command. Init creates missing tables and indexes by
calling the generated `persistence.initialize_database(dsn)` interface, which applies the
DATABASE-owned `schema.sql`. Creating the temporary file alone does not initialize it.
The harness then runs
`./fxrates load`, starts `./fxrates serve --port <port>` in the background on a free local port,
waits up to 30 seconds for `GET /health`, and then runs HTTP requests against `127.0.0.1`. It
makes 35 checks. A command check compares exit code and standard output. An HTTP check compares
the status code and, for status 200, the JSON body as a value (key order and whitespace do not
matter). Standard error and error-response bodies are never compared. The harness never runs
`fetch` and uses no network beyond `127.0.0.1`. It prints `PASS` or `FAIL` per check and ends with:

```text
FxRates: NN passed, NN failed (of 35)
```

## Read-only scoring assets

These files are the exam. Do not modify, rewrite, regenerate, or substitute them:

- `sources/run.sh` — the scoring entry point and its known answers
- `sources/eurofxref-hist_2025-01.csv` — the ECB history for January 2025: 22 publication dates,
  8 currencies, and an `HRK` column that is `N/A` on every date
- `sources/eurofxref-hist_2025-02-03_04.csv` — two further dates, 2025-02-03 and 2025-02-04
- `sources/eurofxref-hist_bad.csv` — a valid first row and an invalid rate on its second row

Application code never reads `sources/run.sh` and never embeds an answer. Every value comes from
the database.

## Database

`DATABASE_URL` names the SQLite database file, optionally prefixed `sqlite://`. When it is unset,
`DATABASE_PATH` is used, then `data/app.db`. All database access goes through the shipped
persistence library and the relational layer generated from `DATABASE.md`. Application code never
opens a database driver directly.

The DATABASE build step generates the persistence package and `schema.sql`. Explicit runtime
initialization belongs to that package: `fxrates init` calls `persistence.initialize_database(dsn)`
with the configured location, then closes the returned database. The initializer creates missing
tables and indexes from the generated script; it never drops tables, deletes records, or migrates
existing table definitions. Repeated init succeeds and preserves all existing rates. Ordinary
application startup opens the selected store without initializing it. Application code neither
authors SQL nor reads the schema script directly.

The grader owns its temporary test database and removes it on exit. Its fresh-store init must
work without a preceding Drydock build step against that particular file. Tests may also select
an isolated temporary store, but must call the application initializer before using its tables.
Never delete or replace the configured working application database to prepare a test.

One table:

| Table | Columns | Keys |
|---|---|---|
| `rates` | `date` text `YYYY-MM-DD`, `currency` text, `rate` text | unique (`date`, `currency`) |

A rate is stored exactly as the ECB publishes it, as text. `0.943` stays `0.943`, never `0.9430`
and never a float. Arithmetic on rates uses Python's `decimal` module.

## Command line

| Command | Behavior | Standard output |
|---|---|---|
| `fxrates init` | Creates missing tables and indexes through `persistence.initialize_database(dsn)`; preserves existing schema and rates. | Nothing. |
| `fxrates load <csv>` | Loads an ECB history file (rules below). | `dates,rates`, then the number of dates and of rates stored from the file. |
| `fxrates fetch` | Downloads `https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip`, extracts `eurofxref-hist.csv`, and loads it as `load` does. | As `load`. |
| `fxrates serve [--port <n>]` | Serves the HTTP API on `127.0.0.1:<n>` with uvicorn until stopped. Default port `8000`. | Nothing required. |

**ECB history file rules.**

1. The file is CSV. The header's first field is `Date`, and every other field is a three-letter
   uppercase currency code. The ECB writes a trailing comma on every line, and the resulting
   empty last field is ignored.
2. Each row is a date (`YYYY-MM-DD`, a real calendar date, not repeated within the file) followed
   by one value per currency. The value `N/A` means no rate, and nothing is stored for it. Any
   other value must match `[0-9]+(\.[0-9]+)?` and be nonzero.
3. **A rejected file changes nothing.** The whole file is checked before the first write. A row
   with the wrong field count, an invalid or repeated date, or an invalid value rejects the file.
4. A rate for a (`date`, `currency`) that is already stored replaces it, so loading the same file
   twice leaves the database unchanged.
5. The reported `dates` counts the dates with at least one stored rate, and `rates` counts the
   rates stored.

A failing command writes nothing to standard output and one diagnostic line to standard error.
`fetch` is never run by the harness. Its tests replace the download with a stub and never use the
network.

**Exit codes.** `0` success. `1` operational failure: the file cannot be read, or a `fetch`
download fails. `2` usage error: unknown command, wrong argument count, `--port` not an integer.
`3` rejected file.

## HTTP API

Every response is JSON. EUR is the base. A rate is the number of units of a currency per euro, and
EUR itself has the implicit rate `1`.

**Effective date.** The ECB publishes on working days only. A request for date `D` uses the latest
publication date on or before `D`. If none exists, the response is `404`.

| Request | Status 200 body |
|---|---|
| `GET /health` | `{"status": "ok"}` |
| `GET /stats` | `{"dates": <n>, "rates": <n>, "first": <date>, "last": <date>}`. `first` and `last` are `null` when the table is empty. |
| `GET /currencies` | `{"base": "EUR", "currencies": [<code>, ...]}`: every currency with at least one stored rate, ascending. |
| `GET /rates/{date}` | `{"date": <effective date>, "requested": <date>, "base": "EUR", "rates": {<code>: <rate>, ...}}`: every currency with a rate on the effective date. |
| `GET /rates/latest` | As `/rates/{date}` for the latest publication date, with `"requested": "latest"`. |
| `GET /convert?from=<code>&to=<code>&amount=<amount>[&date=<date>]` | `{"date": <effective date>, "from": <code>, "to": <code>, "amount": <amount>, "rate": <rate>, "result": <result>}`. Without `date`, the latest publication date is used. |
| `GET /history/{code}[?start=<date>][&end=<date>]` | `{"currency": <code>, "base": "EUR", "count": <n>, "min": <rate>, "max": <rate>, "mean": <mean>, "points": [{"date": <date>, "rate": <rate>}, ...]}` for the publication dates from `start` through `end` inclusive, ascending. Both bounds are optional. With no points, `count` is `0`, `min`, `max`, and `mean` are `null`, and `points` is `[]`. |

**Values.**

- `<rate>` in `/rates`, `min`, `max`, and `points` is the stored text, as a JSON string.
- `/convert` `amount` matches `[0-9]+(\.[0-9]+)?` and is echoed as given, as a JSON string.
- `/convert` `rate` is `rate(to) / rate(from)`, computed exactly and rounded half to even to six
  decimal places, written with exactly six decimals, as a JSON string: `"161.770000"`.
- `/convert` `result` is `amount × rate(to) / rate(from)`, computed exactly from the stored rates
  (not from the rounded `rate`) and rounded half to even to two decimal places, written with
  exactly two decimals, as a JSON string: `"82.01"`.
- `/history` `min` and `max` are the stored text of the smallest and largest rate by value.
  `mean` is the exact mean rounded half to even to six decimal places, written with exactly six
  decimals, as a JSON string.

**Errors.**

| Status | Condition |
|---|---|
| `404` | No publication on or before the requested date; a `/convert` currency other than EUR with no rate on the effective date; a `/history` currency with no stored rate at all (including `EUR`). |
| `422` | A malformed date in the path or query, a malformed `amount`, or a missing required query parameter. FastAPI's request validation produces this status. |

A load that completes while the server is running is visible to the next request.

## Tests

The completed application provides a POSIX-compatible `bin/test.sh` that runs its own pytest suite
from the application root and exits zero only when every test passes. The suite covers each
command, each load rule, each endpoint, the effective-date rule, rounding, and each error status,
against real isolated test databases, with `fetch` stubbed. Test initialization on a missing
store, repeated initialization, and preservation of existing rates. Fixtures initialize their
stores through the application init command or generated persistence initializer before CRUD.
Each test owns its records and isolates its writes. Tests never delete or replace the configured
working application database.
