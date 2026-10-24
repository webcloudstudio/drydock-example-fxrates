# Soundings

Per-assertion acceptance board, one row per Blueprint Programmatic Acceptance check.
`drydock plan` projects every assertion as `— UNVERIFIED`; `drydock score ac` sets the
Status column from deterministic proof results. A rerun of `drydock plan` resets Status to
`— UNVERIFIED`; rescore to refresh.

| Status | Blueprint | AC Id | Text | Binding | Baseline | Previously Passed | Last Block | Evidence | Verified At |
|---|---|---|---|---|---|---|---|---|---|
| ✓ PASS | ARCHITECTURE.md | architecture-imports | The declared application entry points and test clients are importable. | yes | VALID product-missing | yes | block-3 |  | 2026-10-24T17:56:15+00:00 |
| ✓ PASS | DATABASE.md | rates-get-round-trip | A rate can be retrieved by its date and currency key. | yes | VALID product-missing | yes | block-3 |  | 2026-10-24T17:56:15+00:00 |
| ✓ PASS | DATABASE.md | rates-list-date | Listing rates filters by publication date and returns currency order. | yes | VALID product-missing | yes | block-3 |  | 2026-10-24T17:56:15+00:00 |
| ✓ PASS | DATABASE.md | rates-upsert-replaces | Upserting the same date and currency replaces its stored text. | yes | VALID product-missing | yes | block-3 |  | 2026-10-24T17:56:15+00:00 |
| ✓ PASS | DATABASE.md | rates-delete-round-trip | Deleting a rate by date and currency removes that stored row. | yes | VALID product-missing | yes | block-3 |  | 2026-10-24T17:56:15+00:00 |
| ✓ PASS | FEATURE-Initialize.md | initialize-clears-rates | Initialization removes existing rates and produces no standard output. | yes | VALID baseline-red | yes | block-3 |  | 2026-10-24T17:56:15+00:00 |
| ~ PREPASSED | FEATURE-Initialize.md | initialize-repeat | Initialization can be run again after the rates table is empty. | yes | VALID existing-behavior | yes | block-3 | green at this block's baseline too, before its code existed — confirm the criterion exercises the story's work | 2026-10-24T17:56:15+00:00 |
| ✓ PASS | FEATURE-Load.md | load-stores-published-text | Loading a valid staged ECB file stores each non-N/A rate as published text and reports its date and rate counts. | yes | VALID baseline-red | yes | block-3 |  | 2026-10-24T17:56:15+00:00 |
| ✓ PASS | FEATURE-Load.md | load-replaces-matching-rate | Loading a file replaces a stored rate for the same date and currency with its published text. | yes | VALID baseline-red | yes | block-3 |  | 2026-10-24T17:56:15+00:00 |
| ✓ PASS | FEATURE-Load.md | load-rejects-invalid-file-atomically | An invalid staged file is rejected without changing existing rates. | yes | VALID baseline-red | yes | block-3 |  | 2026-10-24T17:56:15+00:00 |
| ✓ PASS | FEATURE-Fetch.md | fetch-download-is-stubbed | The fetch command loads a valid archive member using a stubbed download without opening a network connection. | yes | VALID baseline-red | yes | block-3 |  | 2026-10-24T17:56:15+00:00 |
| ✓ PASS | FEATURE-Fetch.md | fetch-rejects-download-error | A failed download returns the operational failure exit status. | yes | VALID baseline-red | yes | block-3 |  | 2026-10-24T17:56:15+00:00 |
| ✓ PASS | FEATURE-Rates.md | rates-effective-date | The date endpoint resolves a seeded date to the latest available publication and returns its stored rate text. | yes | VALID baseline-red | yes | block-3 |  | 2026-10-24T17:56:15+00:00 |
| ✓ PASS | FEATURE-Rates.md | rates-latest | The latest endpoint returns the newest publication and its stored rates. | yes | VALID baseline-red | yes | block-3 |  | 2026-10-24T17:56:15+00:00 |
| ~ PREPASSED | FEATURE-Rates.md | rates-no-publication | A date before every stored publication returns 404. | yes | VALID existing-behavior | yes | block-3 | green at this block's baseline too, before its code existed — confirm the criterion exercises the story's work | 2026-10-24T17:56:15+00:00 |
| ✓ PASS | FEATURE-Rates.md | rates-malformed-date | A malformed date returns 422. | yes | VALID baseline-red | yes | block-3 |  | 2026-10-24T17:56:15+00:00 |
| ✓ PASS | FEATURE-Currencies.md | currencies-route | The currencies route returns a successful JSON response with the EUR base and currency codes. | yes | VALID baseline-red | yes | block-3 |  | 2026-10-24T17:56:15+00:00 |
| ✓ PASS | FEATURE-Health-Stats.md | health-route | The health route responds successfully with a JSON object. | yes | VALID baseline-red | yes | block-3 |  | 2026-10-24T17:56:15+00:00 |
| ✓ PASS | FEATURE-Health-Stats.md | stats-route | The statistics route reports counts and date bounds from stored rate rows. | yes | VALID baseline-red | yes | block-3 |  | 2026-10-24T17:56:15+00:00 |
| ✓ PASS | FEATURE-History.md | history-bounded-points | History returns stored points within inclusive date bounds, in ascending order, with summary values. | yes | VALID baseline-red | yes | block-3 |  | 2026-10-24T17:56:15+00:00 |
| ✓ PASS | FEATURE-History.md | history-empty-range | An empty bounded history range returns empty points and null statistics. | yes | VALID baseline-red | yes | block-3 |  | 2026-10-24T17:56:15+00:00 |
| ~ PREPASSED | FEATURE-History.md | history-unknown-currency | A currency with no stored history returns 404. | yes | VALID existing-behavior | yes | block-3 | green at this block's baseline too, before its code existed — confirm the criterion exercises the story's work | 2026-10-24T17:56:15+00:00 |
| ✓ PASS | FEATURE-History.md | history-malformed-bound | A malformed history date bound returns 422. | yes | VALID baseline-red | yes | block-3 |  | 2026-10-24T17:56:15+00:00 |
| ✓ PASS | FEATURE-Convert.md | convert-exact-values | Conversion returns the supplied amount and the exact same-currency ratio with contract precision. | yes | VALID baseline-red | yes | block-3 |  | 2026-10-24T17:56:15+00:00 |
| ✓ PASS | FEATURE-Convert.md | convert-eur-base | EUR conversions use the implicit base rate and return the supplied amount rounded to the result precision. | yes | VALID baseline-red | yes | block-3 |  | 2026-10-24T17:56:15+00:00 |
| ✓ PASS | FEATURE-Convert.md | convert-invalid-amount | A malformed amount is rejected with 422. | yes | VALID baseline-red | yes | block-3 |  | 2026-10-24T17:56:15+00:00 |
| ✓ PASS | FEATURE-Convert.md | convert-missing-parameter | A missing required conversion parameter is rejected with 422. | yes | VALID baseline-red | yes | block-3 |  | 2026-10-24T17:56:15+00:00 |
| ~ PREPASSED | FEATURE-Convert.md | convert-unknown-currency | An unavailable currency is rejected with 404. | yes | VALID existing-behavior | yes | block-3 | green at this block's baseline too, before its code existed — confirm the criterion exercises the story's work | 2026-10-24T17:56:15+00:00 |
| ✓ PASS | FEATURE-Serve.md | serve-uses-port-and-stops | The serve command starts the API on the requested loopback port and exits after SIGTERM. | yes | VALID baseline-red | yes | block-3 |  | 2026-10-24T17:56:15+00:00 |
| ✓ PASS | FEATURE-CLI-Errors.md | cli-usage-error-status | Unknown commands and missing command arguments return the usage exit status. | yes | VALID baseline-red | yes | block-3 |  | 2026-10-24T17:56:15+00:00 |
| ✓ PASS | FEATURE-CLI-Errors.md | cli-operational-error-status | An unreadable input file returns the operational failure status. | yes | VALID baseline-red | yes | block-3 |  | 2026-10-24T17:56:15+00:00 |
| ~ PREPASSED | FEATURE-CLI-Errors.md | test-launcher | The project test launcher exits successfully when the project's tests pass. | yes | VALID existing-behavior | yes | block-3 | green at this block's baseline too, before its code existed — confirm the criterion exercises the story's work | 2026-10-24T17:56:15+00:00 |
| ✓ PASS | VERIFICATION.md | fxrates-full-conformance | The supplied end-to-end grader passes all of its checks. | yes | VALID baseline-red | yes | block-3 |  | 2026-10-24T17:56:15+00:00 |
