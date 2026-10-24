# Sea Trials: FxRates

## Policy

| Consequence | On FAIL | On INCONCLUSIVE |
|---|---|---|
| blocks  | fail   | attest |
| scores  | score  | score  |
| attests | report | report |

## st-001: The supplied grader passes
Type: technical
Required: yes
Criterion: The completed fxrates shall make sh sources/run.sh exit zero; that script's exit status is the sole acceptance verdict.
Testability: deterministic
Consequence: blocks
Verification: proof
Command: ["sh", "sources/run.sh"]
Pattern: ubiquitous

## st-002: Test suite passes
Type: technical
Required: yes
Criterion: The application shall provide a POSIX-compatible bin/test.sh that exits zero when every automated test passes.
Testability: deterministic
Consequence: blocks
Verification: proof
Pattern: ubiquitous

## st-003: ECB history files load exactly and atomically
Type: behavioral
Required: yes
Criterion: When an ECB history file is loaded, the application shall store every non-N/A rate as published text, replace rates already stored for the same date and currency, and, if any row is invalid, exit 3 and store nothing.
Testability: deterministic
Consequence: blocks
Verification: proof
Pattern: event

## st-004: The service starts and reports health
Type: technical
Required: yes
Criterion: When fxrates serve --port is run, the application shall answer GET /health on 127.0.0.1 at that port with status 200 and {"status": "ok"}.
Testability: deterministic
Consequence: blocks
Verification: proof
Pattern: event

## st-005: Rates resolve to the effective publication date
Type: behavioral
Required: yes
Criterion: When rates or a conversion are requested for a date, the application shall use the latest publication date on or before it, and respond 404 when there is none.
Testability: deterministic
Consequence: blocks
Verification: proof
Pattern: event

## st-006: Conversions and history match the known answers
Type: behavioral
Required: yes
Criterion: The application shall compute /convert rates and results and /history statistics with exact decimal arithmetic rounded half to even, matching the known answers in sources/run.sh.
Testability: deterministic
Consequence: blocks
Verification: proof
Pattern: ubiquitous

## st-007: Invalid requests are refused with the right status
Type: behavioral
Required: yes
Criterion: If a request has a malformed date or amount or lacks a required parameter, then the application shall respond 422; if it names an unknown currency, then it shall respond 404.
Testability: deterministic
Consequence: blocks
Verification: proof
Pattern: unwanted

## st-008: Persistence goes through the shipped library
Type: technical
Required: yes
Criterion: The application shall reach the database only through the shipped persistence library, selected by DATABASE_URL, with rates stored as text and never as floating point.
Testability: judgeable
Consequence: scores
Verification: llm
Pattern: ubiquitous

## st-009: Tests never use the network
Type: technical
Required: yes
Criterion: The application's automated tests shall exercise fetch through a stubbed download and shall not open a network connection.
Testability: judgeable
Consequence: scores
Verification: llm
Pattern: ubiquitous
