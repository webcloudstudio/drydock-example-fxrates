# Technology Stack

**Approved:** 2026-10-22

Technology decisions of record for this Target. One row per technology, naming the
Rigging best-practice file that governs building it.

A `—` in the Rigging column means no Rigging guidance exists for that technology; the
builder applies general best practice instead. Adding a row never requires a matching
Rigging file.

This file is owned by the UAT kit. It is seeded into the Target before `analyze`, which
never overwrites it, and `drydock plan` reads it to assign per-story `stack:` guidance.

| Technology | Rigging | Notes |
|---|---|---|
| Python | python.md | Implementation language; Python 3.11 or newer. |
| FastAPI | fastapi.md | JSON HTTP API, served by uvicorn on 127.0.0.1. |
| SQLite | sqlite.md | Database, reached through the shipped persistence library. |
| CLI | cli.md | The `fxrates` executable at the application root: `init`, `load`, `fetch`, `serve`. |
| pytest | python.md | Test runner behind `bin/test.sh`; FastAPI `TestClient` for the API. |
| ECB reference rates | — | Input format: the ECB `eurofxref-hist.csv` history file, downloaded as `eurofxref-hist.zip`. |
| Shell | common.md | POSIX sh for `bin/test.sh` and the supplied grader. |
