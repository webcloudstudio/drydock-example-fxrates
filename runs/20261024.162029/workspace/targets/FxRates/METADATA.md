# AUTHORITATIVE PROJECT METADATA — FIELDS SHOULD BE CURRENT

name: FxRates
display_name: drydock FxRates Uat Case
short_description: Drydock uat - FxRates is the web-service kit and the first to exercise FastAPI. The source is an original brief for a currency rates service: a command line loads the European Central Bank euro reference rate history into SQLite, and a FastAPI JSON API serves rates by date (resolved to the latest publication on or before it), conversions between any two currencies with exact decimal rounding, and a currency's history. The supplied grader, sources/run.sh, loads real ECB files for January 2025 plus two February dates, starts the server on a free local port, and makes 35 checks of command output and HTTP status and JSON body. Run with drydock uat FxRates. Source Repo: none, the brief is original to this kit; data from the ECB euro foreign exchange reference rates.
stack: Python
version: 0.03
build_state: analyzed
build_sub_state: complete
last_analyzed: 2026-10-24
last_planned: 
last_built: 
build_dir: 
brand: 
git_repo: 
release_tag: 
updated: 2026-10-24T16:21:12+00:00
