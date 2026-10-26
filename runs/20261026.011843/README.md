# FXRATES

- Short description: Drydock uat - FxRates is the web-service kit and the first to exercise FastAPI. The source is an original brief for a currency rates service: a command line loads the European Central Bank euro reference rate history into SQLite, and a FastAPI JSON API serves rates by date (resolved to the latest publication on or before it), conversions between any two currencies with exact decimal rounding, and a currency's history. The supplied grader, sources/run.sh, loads real ECB files for January 2025 plus two February dates, starts the server on a free local port, and makes 35 checks of command output and HTTP status and JSON body. Run with drydock uat FxRates. Source Repo: none, the brief is original to this kit; data from the ECB euro foreign exchange reference rates.
- Status: SCORE AC — FAILED

2 of 4 receipt claims proven. Open `index.html` for the linked proof kit; verify it with `sha256sum -c SHA256SUMS`.

## Receipt

| Claim | Verdict | Recorded outcome | Proof |
|---|---|---|---|
| Lifecycle completed | FAIL | 19 lifecycle commands executed; the run ended at 19-score-release. | [result.json](result.json) |
| External conformance suite passed | PASS | sh sources/run.sh exited 0. | [evidence/commands/16-test.stdout.log](evidence/commands/16-test.stdout.log) |
| Release score passed | FAIL | drydock score release exited 1. | [evidence/commands/19-score-release.stdout.log](evidence/commands/19-score-release.stdout.log) |
| Integrity verification passed | PASS | 1,432 files digested; verify with sha256sum -c SHA256SUMS. | [SHA256SUMS](SHA256SUMS) |

## Run facts

- Drydock: `0.8.0` (commit `1c5d9b8a39ac7ef55ed8cf87e5c8ad61c6cf2e4d`)
- Provider and model: `codex` / `gpt-6-luna`
- Platform: `Linux-6.6.87.2-microsoft-standard-WSL2-x86_64-with-glibc2.35` on Python `3.12.13`
- Run: `20261026.011843`
- Elapsed: 885.6s
- LLM calls: 14
- Tokens: cached 1,246,080; uncached 411,839; output 34,122
- LLM elapsed: 464.2s
- Build passes: 1; repairs: 6 attempts allowed
- Conformance: passed
- Advisory scores: acceptance=exit 1, build-report=exit 0, release=exit 1

## RUN SUMMARY

- Input specification: [`sources/INSTRUCTIONS.md`](sources/INSTRUCTIONS.md)
- Delivered Code: [`build/FxRates/`](build/FxRates)
- Test Results: [`evidence/commands/16-test.stdout.log`](evidence/commands/16-test.stdout.log)

## Shortfall

- Failure: execution PASS, acceptance FAIL

## Commands

| # | Command | Exit | Elapsed | Output |
|---|---|---|---|---|
| 01-init | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python -m drydock init FxRates` | 0 | 3.6s | [stdout](evidence/commands/01-init.stdout.log) · [stderr](evidence/commands/01-init.stderr.log) |
| 02-import-sources | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python -m drydock import FxRates sources --format markdown` | 0 | 6.3s | [stdout](evidence/commands/02-import-sources.stdout.log) · [stderr](evidence/commands/02-import-sources.stderr.log) |
| 03-analyze | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python -m drydock analyze FxRates` | 0 | 37.7s | [stdout](evidence/commands/03-analyze.stdout.log) · [stderr](evidence/commands/03-analyze.stderr.log) · [llm](evidence/commands/03-analyze.llm.log) |
| 04-plan | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python -m drydock plan FxRates --override` | 0 | 237.2s | [stdout](evidence/commands/04-plan.stdout.log) · [stderr](evidence/commands/04-plan.stderr.log) · [llm](evidence/commands/04-plan.llm.log) |
| 05-plan-verify | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python -m drydock plan verify FxRates` | 0 | 23.9s | [stdout](evidence/commands/05-plan-verify.stdout.log) · [stderr](evidence/commands/05-plan-verify.stderr.log) |
| 06-after-plan-build-status | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python -m drydock build status FxRates` | 0 | 2.4s | [stdout](evidence/commands/06-after-plan-build-status.stdout.log) · [stderr](evidence/commands/06-after-plan-build-status.stderr.log) |
| 07-after-plan-target-status | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python -m drydock status FxRates` | 0 | 2.4s | [stdout](evidence/commands/07-after-plan-target-status.stdout.log) · [stderr](evidence/commands/07-after-plan-target-status.stderr.log) |
| 08-after-plan-workspace-status | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python -m drydock status` | 0 | 1.5s | [stdout](evidence/commands/08-after-plan-workspace-status.stdout.log) · [stderr](evidence/commands/08-after-plan-workspace-status.stderr.log) |
| 09-initial-ready | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python -m drydock status FxRates --ready` | 0 | 2.9s | [stdout](evidence/commands/09-initial-ready.stdout.log) · [stderr](evidence/commands/09-initial-ready.stderr.log) |
| 10-initial-build-1 | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python -m drydock build FxRates --override --repair-attempts 6` | 0 | 398.6s | [stdout](evidence/commands/10-initial-build-1.stdout.log) · [stderr](evidence/commands/10-initial-build-1.stderr.log) · [llm](evidence/commands/10-initial-build-1.llm.log) |
| 11-initial-ready | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python -m drydock status FxRates --ready` | 1 | 2.7s | [stdout](evidence/commands/11-initial-ready.stdout.log) · [stderr](evidence/commands/11-initial-ready.stderr.log) |
| 12-initial-complete | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python -m drydock status FxRates --check` | 1 | 1.8s | [stdout](evidence/commands/12-initial-complete.stdout.log) · [stderr](evidence/commands/12-initial-complete.stderr.log) |
| 13-after-initial-build-build-status | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python -m drydock build status FxRates` | 0 | 2.1s | [stdout](evidence/commands/13-after-initial-build-build-status.stdout.log) · [stderr](evidence/commands/13-after-initial-build-build-status.stderr.log) |
| 14-after-initial-build-target-status | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python -m drydock status FxRates` | 0 | 2.2s | [stdout](evidence/commands/14-after-initial-build-target-status.stdout.log) · [stderr](evidence/commands/14-after-initial-build-target-status.stderr.log) |
| 15-after-initial-build-workspace-status | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python -m drydock status` | 0 | 1.4s | [stdout](evidence/commands/15-after-initial-build-workspace-status.stdout.log) · [stderr](evidence/commands/15-after-initial-build-workspace-status.stderr.log) |
| 16-test | `sh sources/run.sh` | 0 | 15.2s | [stdout](evidence/commands/16-test.stdout.log) · [stderr](evidence/commands/16-test.stderr.log) |
| 17-score-acceptance | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python -m drydock score ac FxRates` | 1 | 49.6s | [stdout](evidence/commands/17-score-acceptance.stdout.log) · [stderr](evidence/commands/17-score-acceptance.stderr.log) |
| 18-score-build-report | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python -m drydock score build FxRates` | 0 | 1.5s | [stdout](evidence/commands/18-score-build-report.stdout.log) · [stderr](evidence/commands/18-score-build-report.stderr.log) |
| 19-score-release | `/mnt/c/Users/barlo/projects/drydock/.venv/bin/python -m drydock score release FxRates` | 1 | 86.2s | [stdout](evidence/commands/19-score-release.stdout.log) · [stderr](evidence/commands/19-score-release.stderr.log) · [llm](evidence/commands/19-score-release.llm.log) |

## Evidence

- [`evidence/commands/`](evidence/commands) — stdout and stderr of every command
- [`evidence/prompts/`](evidence/prompts) — the assembled prompt for every LLM call
- [`evidence/provider_raw/`](evidence/provider_raw) — unmodified provider transcripts
- [`evidence/llm_logs/`](evidence/llm_logs) — call banners and token accounting
- [`result.json`](result.json) — the machine-readable record of this run
