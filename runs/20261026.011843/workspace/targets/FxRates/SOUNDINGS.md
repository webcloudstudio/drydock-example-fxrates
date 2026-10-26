# Soundings

Per-assertion acceptance board, one row per Blueprint Programmatic Acceptance check.
`drydock plan` projects every assertion as `— UNVERIFIED`; `drydock score ac` sets the
Status column from deterministic proof results. A rerun of `drydock plan` resets Status to
`— UNVERIFIED`; rescore to refresh.

| Status | Blueprint | AC Id | Text | Binding | Baseline | Previously Passed | Last Block | Evidence | Verified At |
|---|---|---|---|---|---|---|---|---|---|
| ✓ PASS | ARCHITECTURE.md | architecture-imports | The application factory and CLI entry point are importable. | yes | VALID product-missing | yes | block-3 |  | 2026-10-26T01:31:09+00:00 |
| ✓ PASS | DATABASE.md | rates-upsert | The rates upsert operation replaces an existing date and currency rate and returns the stored row. | yes | VALID product-missing | yes | block-3 |  | 2026-10-26T01:31:09+00:00 |
| ✓ PASS | DATABASE.md | rates-effective-rates | Effective-date lookup returns stored rows on or before its bound in descending date order. | yes | VALID product-missing | yes | block-3 |  | 2026-10-26T01:31:09+00:00 |
| ✓ PASS | DATABASE.md | rates-by-date | Date lookup returns the stored rows for the requested date. | yes | VALID product-missing | yes | block-3 |  | 2026-10-26T01:31:09+00:00 |
| ✓ PASS | DATABASE.md | rates-history | Currency history returns matching rows in ascending date order within its inclusive bounds. | yes | VALID product-missing | yes | block-3 |  | 2026-10-26T01:31:09+00:00 |
| ✓ PASS | DATABASE.md | rates-list | The rates list operation reads back all rows created by the criterion in declared date and currency order. | yes | VALID product-missing | yes | block-3 |  | 2026-10-26T01:31:09+00:00 |
| ✗ FAIL | FEATURE-DatabaseInitialization.md | init-empty | Initialization clears existing rates and leaves the table empty. | yes |  |  |  | assert exit_code == 0 → AssertionError | 2026-10-26T01:31:09+00:00 |
| ✓ PASS | FEATURE-DatabaseInitialization.md | init-usage | Initialization accepts no extra arguments and unknown commands return the declared usage status. | yes |  |  |  |  | 2026-10-26T01:31:09+00:00 |
| ✓ PASS | FEATURE-HistoryLoading.md | load-valid-fixture | Loading the staged January fixture preserves source rate text and stores every non-N/A cell. | yes |  |  |  |  | 2026-10-26T01:31:09+00:00 |
| ✓ PASS | FEATURE-HistoryLoading.md | load-repeat | Loading the same file twice leaves the rates table unchanged. | yes |  |  |  |  | 2026-10-26T01:31:09+00:00 |
| ✓ PASS | FEATURE-HistoryLoading.md | load-rejection-atomic | An invalid rate rejects the complete file without storing its valid first row. | yes |  |  |  |  | 2026-10-26T01:31:09+00:00 |
| ✓ PASS | FEATURE-HistoryLoading.md | load-missing-file | A missing input file is an operational failure. | yes |  |  |  |  | 2026-10-26T01:31:09+00:00 |
| ✗ FAIL | FEATURE-ServiceOverview.md | overview-routes | Health, statistics, and currencies routes are reachable and reflect persisted state. | yes |  |  |  | ModuleNotFoundError: No module named 'app_server.testing' | 2026-10-26T01:31:09+00:00 |
| ✗ FAIL | FEATURE-ServiceOverview.md | stats-empty-contract | Statistics expose the declared null bounds when the rates table is empty. | yes |  |  |  | ModuleNotFoundError: No module named 'app_server.testing' | 2026-10-26T01:31:09+00:00 |
| ✗ FAIL | FEATURE-EffectiveRates.md | effective-rate-routes | Both effective-rate routes return successful responses for dates backed by rates. | yes |  |  |  | ModuleNotFoundError: No module named 'app_server.testing' | 2026-10-26T01:31:09+00:00 |
| ✗ FAIL | FEATURE-EffectiveRates.md | effective-rate-errors | A malformed requested date is rejected, and a date before all stored rates is not found. | yes |  |  |  | ModuleNotFoundError: No module named 'app_server.testing' | 2026-10-26T01:31:09+00:00 |
| ✗ FAIL | FEATURE-CurrencyHistory.md | history-route | The history route returns stored points in ascending date order for the requested currency and range. | yes |  |  |  | ModuleNotFoundError: No module named 'app_server.testing' | 2026-10-26T01:31:09+00:00 |
| ✗ FAIL | FEATURE-CurrencyHistory.md | history-summary-and-empty | History reports the count and extrema of stored points and represents a valid empty period with null statistics. | yes |  |  |  | ModuleNotFoundError: No module named 'app_server.testing' | 2026-10-26T01:31:09+00:00 |
| ✗ FAIL | FEATURE-CurrencyHistory.md | history-errors | History rejects malformed date bounds and an unavailable currency. | yes |  |  |  | ModuleNotFoundError: No module named 'app_server.testing' | 2026-10-26T01:31:09+00:00 |
| ✗ FAIL | FEATURE-CurrencyConversion.md | conversion-route | The conversion route returns a successful response and echoes the supplied amount and currency codes. | yes |  |  |  | ModuleNotFoundError: No module named 'app_server.testing' | 2026-10-26T01:31:09+00:00 |
| ✗ FAIL | FEATURE-CurrencyConversion.md | conversion-rounding | The conversion rate and result use exact source rates and half-even rounding at their specified precisions. | yes |  |  |  | ModuleNotFoundError: No module named 'app_server.testing' | 2026-10-26T01:31:09+00:00 |
| ✗ FAIL | FEATURE-CurrencyConversion.md | conversion-errors | The conversion route rejects a missing or malformed amount and returns not found for an unavailable currency. | yes |  |  |  | ModuleNotFoundError: No module named 'app_server.testing' | 2026-10-26T01:31:09+00:00 |
| ✓ PASS | FEATURE-HistoryFetch.md | fetch-stubbed | The fetch command loads a ZIP archive supplied by a stub without accessing the network. | yes |  |  |  |  | 2026-10-26T01:31:09+00:00 |
| ✗ FAIL | FEATURE-HistoryFetch.md | fetch-operational-error | A failed archive download returns the operational failure exit code. | yes |  |  |  | assert code == 1 → AssertionError | 2026-10-26T01:31:09+00:00 |
| ✓ PASS | FEATURE-TestRunner.md | test-runner-exits-successfully | The project test runner exits successfully when run from the application root after implementation stories are complete. | yes |  |  |  |  | 2026-10-26T01:31:09+00:00 |
| ✓ PASS | FEATURE-EndToEndVerification.md | supplied-grader | The supplied end-to-end grader passes the complete application. | yes |  |  |  |  | 2026-10-26T01:31:09+00:00 |
