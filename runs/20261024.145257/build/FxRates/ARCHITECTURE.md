# ARCHITECTURE: FxRates

## Module ownership

| Boundary | Owner | Responsibility |
|---|---|---|
| Configuration | `config` | Reads `DATABASE_URL`, then `DATABASE_PATH`, then `data/app.db`. |
| Persistence | generated `persistence` package | Owns database connections and declared repository operations. Application modules must not open drivers or issue SQL directly. |
| CLI | `cli` | Parses commands, invokes feature services, and writes command output and diagnostics. |
| API | `app_server` | Creates the FastAPI application and delegates route behavior to feature services. |
| ECB fetch | CLI fetch service | Downloads and extracts ECB data, then delegates CSV loading to shared load behavior. |

The root `fxrates` executable delegates to `cli.main`. Persisted ECB rates retain
their published text; arithmetic uses `decimal.Decimal`.
