# FXRATES

- Short description: Drydock uat - FxRates is the web-service kit and the first to exercise FastAPI. The source is an original brief for a currency rates service: a command line loads the European Central Bank euro reference rate history into SQLite, and a FastAPI JSON API serves rates by date (resolved to the latest publication on or before it), conversions between any two currencies with exact decimal rounding, and a currency's history. The supplied grader, sources/run.sh, loads real ECB files for January 2025 plus two February dates, starts the server on a free local port, and makes 35 checks of command output and HTTP status and JSON body. Run with drydock uat FxRates. Source Repo: none, the brief is original to this kit; data from the ECB euro foreign exchange reference rates.
- Status: PLAN CREATED

1 of 4 receipt claims proven. Open `index.html` for the linked proof kit; verify it with `sha256sum -c SHA256SUMS`.

## Receipt

| Claim | Verdict | Recorded outcome | Proof |
|---|---|---|---|
| Lifecycle completed | FAIL | 10 lifecycle commands executed; the run ended at 10-after-plan-workspace-status. | [result.json](result.json) |
| External conformance suite passed | UNPROVEN | No external test command is defined for this project. | — |
| Release score passed | UNPROVEN | No release score was recorded for this run. | — |
| Integrity verification passed | PASS | 242 files digested; verify with sha256sum -c SHA256SUMS. | [SHA256SUMS](SHA256SUMS) |

## Run facts

- Drydock: `0.8.0` (commit `42f14d1c98175da55a553cf557fa0259751ff79e`)
- Provider and model: `codex` / `gpt-6-luna`
- Platform: `Linux-6.6.87.2-microsoft-standard-WSL2-x86_64-with-glibc2.35` on Python `3.12.13`
- Run: `20261024.183153`
- Elapsed: 390.2s
- LLM calls: 13
- Tokens: cached 152,320; uncached 315,474; output 21,755
- LLM elapsed: 203.4s
- Build passes: 0; repairs: not recorded
- Conformance: no external suite defined
- Advisory scores: none recorded

## RUN SUMMARY

- Input specification: [`sources/INSTRUCTIONS.md`](sources/INSTRUCTIONS.md)
- Delivered Code: [`build/FxRates/`](build/FxRates)
- Test Results: not recorded for this run.

## Shortfall

- Failure: FxRates: stopped at plan-repair: acceptance criteria still cannot run after one repair pass

## Commands

| # | Command | Exit | Elapsed | Output |
|---|---|---|---|---|
| 01-init | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python -m drydock init FxRates` | 0 | 3.6s | [stdout](evidence/commands/01-init.stdout.log) · [stderr](evidence/commands/01-init.stderr.log) |
| 02-import-sources | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python -m drydock import FxRates sources --format markdown` | 0 | 7.4s | [stdout](evidence/commands/02-import-sources.stdout.log) · [stderr](evidence/commands/02-import-sources.stderr.log) |
| 03-analyze | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python -m drydock analyze FxRates` | 0 | 39.6s | [stdout](evidence/commands/03-analyze.stdout.log) · [stderr](evidence/commands/03-analyze.stderr.log) · [llm](evidence/commands/03-analyze.llm.log) |
| 04-plan | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python -m drydock plan FxRates --override` | 0 | 216.2s | [stdout](evidence/commands/04-plan.stdout.log) · [stderr](evidence/commands/04-plan.stderr.log) · [llm](evidence/commands/04-plan.llm.log) |
| 05-plan-verify | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python -m drydock plan verify FxRates` | 1 | 27.0s | [stdout](evidence/commands/05-plan-verify.stdout.log) · [stderr](evidence/commands/05-plan-verify.stderr.log) |
| 06-plan-repair | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python -m drydock plan repair FxRates` | 1 | 59.0s | [stdout](evidence/commands/06-plan-repair.stdout.log) · [stderr](evidence/commands/06-plan-repair.stderr.log) · [llm](evidence/commands/06-plan-repair.llm.log) |
| 07-plan-verify-after-repair | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python -m drydock plan verify FxRates` | 1 | 24.0s | [stdout](evidence/commands/07-plan-verify-after-repair.stdout.log) · [stderr](evidence/commands/07-plan-verify-after-repair.stderr.log) |
| 08-after-plan-build-status | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python -m drydock build status FxRates` | 0 | 3.8s | [stdout](evidence/commands/08-after-plan-build-status.stdout.log) · [stderr](evidence/commands/08-after-plan-build-status.stderr.log) |
| 09-after-plan-target-status | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python -m drydock status FxRates` | 0 | 3.1s | [stdout](evidence/commands/09-after-plan-target-status.stdout.log) · [stderr](evidence/commands/09-after-plan-target-status.stderr.log) |
| 10-after-plan-workspace-status | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python -m drydock status` | 0 | 1.7s | [stdout](evidence/commands/10-after-plan-workspace-status.stdout.log) · [stderr](evidence/commands/10-after-plan-workspace-status.stderr.log) |

## Evidence

- [`evidence/commands/`](evidence/commands) — stdout and stderr of every command
- [`evidence/prompts/`](evidence/prompts) — the assembled prompt for every LLM call
- [`evidence/provider_raw/`](evidence/provider_raw) — unmodified provider transcripts
- [`evidence/llm_logs/`](evidence/llm_logs) — call banners and token accounting
- [`result.json`](result.json) — the machine-readable record of this run
