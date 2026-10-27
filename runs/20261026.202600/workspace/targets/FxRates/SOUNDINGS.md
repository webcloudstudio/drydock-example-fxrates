# Soundings

Per-assertion acceptance board, one row per Blueprint Programmatic Acceptance check.
`drydock plan` projects every assertion as `— UNVERIFIED`; `drydock score ac` sets the
Status column from deterministic proof results. A rerun of `drydock plan` resets Status to
`— UNVERIFIED`; rescore to refresh.

| Status | Blueprint | AC Id | Text | Binding | Baseline | Previously Passed | Last Block | Evidence | Verified At |
|---|---|---|---|---|---|---|---|---|---|
| ✓ PASS | ARCHITECTURE.md | architecture-service-boundary | The application provides an importable services boundary for shared CLI and API behavior. | yes | VALID baseline-red | yes | block-6 |  | 2026-10-26T21:16:43+00:00 |
| ✓ PASS | DATABASE.md | rates-upsert | The repository stores a rate and replaces the value for the same date and currency. | yes |  | yes | block-6 |  | 2026-10-26T21:16:43+00:00 |
| ✓ PASS | DATABASE.md | rates-by-date | The repository returns the stored rates for a requested publication date. | yes |  | yes | block-6 |  | 2026-10-26T21:16:43+00:00 |
| ✓ PASS | DATABASE.md | rates-publications-through | The repository returns stored publications on or before the requested date in descending date order. | yes |  | yes | block-6 |  | 2026-10-26T21:16:43+00:00 |
| ✓ PASS | DATABASE.md | rates-history | The repository returns a currency's rates within inclusive optional date bounds in ascending date order. | yes |  | yes | block-6 |  | 2026-10-26T21:16:43+00:00 |
| ✓ PASS | DATABASE.md | rates-list | The repository lists stored rates with their published text. | yes |  | yes | block-6 |  | 2026-10-26T21:16:43+00:00 |
| ✓ PASS | FEATURE-AppServer.md | app-server-factory | The application factory and published test client are importable and construct the declared FastAPI interfaces. | yes |  | yes | block-6 |  | 2026-10-26T21:16:43+00:00 |
| ✓ PASS | FEATURE-CLI.md | cli-foundation-interfaces | The CLI entry point and in-process runner expose the published callable interfaces. | yes |  | yes | block-6 |  | 2026-10-26T21:16:43+00:00 |
| ✓ PASS | FEATURE-Load.md | load-valid-file | Loading the supplied January history succeeds and reports the fixture-derived date and rate counts. | yes | VALID baseline-red | yes | block-6 |  | 2026-10-26T21:16:43+00:00 |
| ✓ PASS | FEATURE-Load.md | load-rejects-atomically | A rejected CSV file leaves the rates it would otherwise have changed untouched. | yes | VALID baseline-red | yes | block-6 |  | 2026-10-26T21:16:43+00:00 |
| ✓ PASS | FEATURE-Load.md | load-replaces-published-text | Loading a valid file stores its rate text exactly and replaces a matching stored rate. | yes | VALID baseline-red | yes | block-6 |  | 2026-10-26T21:16:43+00:00 |
| ✗ FAIL | FEATURE-Init.md | init-clears-store | The init command succeeds and leaves the rates repository empty. | yes | VALID baseline-red | yes | block-6 | assert code == 0 → AssertionError | 2026-10-26T21:16:43+00:00 |
| ✓ PASS | FEATURE-Init.md | init-rejects-extra-arguments | The init command rejects an unexpected argument with the usage exit status. | yes | VALID baseline-red | yes | block-6 |  | 2026-10-26T21:16:43+00:00 |
| ✓ PASS | FEATURE-Currencies.md | currencies-list-sorted | The endpoint lists currencies present in the store in ascending order. | yes | VALID baseline-red | yes | block-6 |  | 2026-10-26T21:16:43+00:00 |
| ✓ PASS | FEATURE-Currencies.md | currencies-base | The endpoint identifies EUR as the base currency. | yes | VALID baseline-red | yes | block-6 |  | 2026-10-26T21:16:43+00:00 |
| ✓ PASS | FEATURE-LatestRates.md | latest-rates-response | The latest-rates route returns the stored rates for the latest publication. | yes | VALID baseline-red | yes | block-6 |  | 2026-10-26T21:16:43+00:00 |
| ✗ FAIL | FEATURE-LatestRates.md | latest-rates-empty | The latest-rates route returns 404 when there is no publication. | yes | VALID existing-behavior | yes | block-6 | assert web_client().get("/rates/latest").status_code == 404 → AssertionError | 2026-10-26T21:16:43+00:00 |
| ✓ PASS | FEATURE-Stats.md | stats-derive-from-store | The statistics endpoint reflects rates inserted through the repository. | yes | VALID baseline-red | yes | block-6 |  | 2026-10-26T21:16:43+00:00 |
| ✗ FAIL | FEATURE-Stats.md | stats-empty-store | The statistics endpoint reports null date bounds when the rates store is empty. | yes | VALID baseline-red | yes | block-6 | assert code == 0 → AssertionError | 2026-10-26T21:16:43+00:00 |
| ✓ PASS | FEATURE-Rates.md | rates-effective-date | The route resolves a requested date to the latest available publication and returns its stored rates. | yes | VALID baseline-red | yes | block-6 |  | 2026-10-26T21:16:43+00:00 |
| ✓ PASS | FEATURE-Rates.md | rates-errors | The route returns the declared errors for a missing effective publication and a malformed date. | yes | VALID baseline-red | yes | block-6 |  | 2026-10-26T21:16:43+00:00 |
| ✓ PASS | FEATURE-History.md | history-range-and-statistics | The history endpoint returns bounded points and statistics derived from the seeded rates. | yes | VALID baseline-red | yes | block-6 |  | 2026-10-26T21:16:43+00:00 |
| ✓ PASS | FEATURE-History.md | history-empty-range-and-errors | The history endpoint distinguishes an empty range from a currency with no history and rejects malformed bounds. | yes | VALID baseline-red | yes | block-6 |  | 2026-10-26T21:16:43+00:00 |
| ✓ PASS | FEATURE-Convert.md | convert-decimal-and-rounding | The conversion endpoint echoes its input amount and calculates its rate and result from the fixture rates with the specified rounding. | yes | VALID baseline-red | yes | block-6 |  | 2026-10-26T21:16:43+00:00 |
| ✓ PASS | FEATURE-Convert.md | convert-validation-and-unknown-currency | The conversion endpoint rejects missing or malformed inputs and returns 404 for a currency without a rate. | yes | VALID baseline-red | yes | block-6 |  | 2026-10-26T21:16:43+00:00 |
| ✓ PASS | FEATURE-Health.md | health-response | The health endpoint responds successfully with the documented JSON body. | yes | VALID baseline-red | yes | block-6 |  | 2026-10-26T21:16:43+00:00 |
| ✓ PASS | FEATURE-Health.md | health-method | An unsupported method is refused by the health route. | yes | VALID baseline-red | yes | block-6 |  | 2026-10-26T21:16:43+00:00 |
| ✓ PASS | FEATURE-CLI-Errors.md | cli-usage-errors | Usage errors return status 2 and produce no standard output. | yes | VALID baseline-red | yes | block-6 |  | 2026-10-26T21:16:43+00:00 |
| ✓ PASS | FEATURE-CLI-Errors.md | cli-operational-errors | File read failures return status 1 and rejected CSV files return status 3. | yes | VALID baseline-red | yes | block-6 |  | 2026-10-26T21:16:43+00:00 |
| ✓ PASS | FEATURE-Fetch.md | fetch-stubbed-success | Fetch loads the CSV from a stubbed ECB archive and reports its fixture-derived counts. | yes | VALID baseline-red | yes | block-6 |  | 2026-10-26T21:16:43+00:00 |
| ✓ PASS | FEATURE-Fetch.md | fetch-stubbed-failure | A failed stubbed download returns the operational failure status without standard output. | yes | VALID baseline-red | yes | block-6 |  | 2026-10-26T21:16:43+00:00 |
| ~ PREPASSED | FEATURE-Tests.md | test-suite-passes | The project's test launcher completes successfully. | yes | VALID existing-behavior | yes | block-6 | green at this block's baseline too, before its code existed — confirm the criterion exercises the story's work | 2026-10-26T21:16:43+00:00 |
| ✓ PASS | FEATURE-Grader.md | grader-complete | The complete supplied grader passes. | yes | VALID baseline-red | yes | block-6 |  | 2026-10-26T21:16:43+00:00 |
