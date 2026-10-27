# Application Architecture

## Module ownership

| Module | Owns | Allowed dependencies |
| --- | --- | --- |
| `cli` | The `fxrates` executable, argument handling, command dispatch, and diagnostics. | Feature services, configuration |
| `app_server` | FastAPI application factory and HTTP route registration. | Feature services, configuration |
| `services` | ECB CSV validation and loading, fetching, store initialization, rate queries, and exact decimal calculations. | `persistence`, configuration, standard library |
| `persistence` | Generated relational layer and shipped database library. | Database engine and schema |
| `config` | Resolving the database location. | Standard library |

HTTP handlers call services. CLI commands call services. Services call generated persistence operations through the shipped persistence library. Only the persistence boundary reaches the database; application modules do not open database drivers directly.

The load workflow validates the complete input file before its first write. Fetch extracts the archive CSV and uses the same validation and loading path. Rates remain ECB-published text in storage and responses; calculations use `decimal.Decimal`.

## Technology roles

| Technology | Role |
| --- | --- |
| Python 3.11 or newer | Application, CLI, services, and tests |
| FastAPI | JSON HTTP API |
| uvicorn | Serves the API on `127.0.0.1` |
| SQLite | Local rates store, accessed only through the shipped persistence library |
| pytest | Offline automated tests |
| FastAPI `TestClient` | In-process API checks |

Database location precedence is `DATABASE_URL`, then `DATABASE_PATH`, then `data/app.db`.
