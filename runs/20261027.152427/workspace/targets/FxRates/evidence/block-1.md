# Evidence: Block 1 · Foundational (block-1)

- block type: block
- date: 2026-10-27
- resulting state: closed/verified
- story points (combined assembled cost): 7689
- execution id: 20261027.154003.460Z-26552b9d

## Stories built
- Stand up the Python project root, environment, dependency manifest, package layout, and test runner. (foundation-python) [story]

## Acceptance tooling authorization
- ARCHITECTURE.md#arch-project-manifest: executable=python3; scope=test; authorization=existing Target environment
- ARCHITECTURE.md#arch-package-imports: executable=python3; scope=test; authorization=existing Target environment
- ARCHITECTURE.md#arch-no-driver-import: executable=python3; scope=test; authorization=existing Target environment
- ARCHITECTURE.md#arch-pytest-runs: executable=python3; scope=test; authorization=existing Target environment

## Reusable compacts
- ARCHITECTURE_compact.md

## Stacked context
- implements: python.md (SP 1166)
- compass: COMPASS.md (SP 1152)
- implements: ARCHITECTURE.md (SP 2398)
- stack: common.md (SP 2776)

## Build directory changes
- .gitignore
- bin/test.sh
- fxrates_app/__init__.py
- pyproject.toml
- tests/conftest.py
- tests/test_foundation.py
- uv.lock

## Pre-build acceptance observation
- RED: arch-project-manifest (ARCHITECTURE.md)
  intent: The project root declares a Python requirement and the stack dependencies, commits a lockfile, and has a pytest conftest.
  return code: 1
  stderr:
    --- drydock: values at failure ---
      name = 'fastapi'
      lowered = '[project]\nname = "fxrates"\nversion = "0.1.0"\nrequires-python = ">=3.11"\ndependencies = []\n'
    --- drydock: end values ---
    Traceback (most recent call last):
      File "arch-project-manifest.py", line 10, in <module>
        assert name in lowered, name
               ^^^^^^^^^^^^^^^
    AssertionError: fastapi
- RED: arch-package-imports (ARCHITECTURE.md)
  intent: The interpreter is Python 3.11 or newer and the application package imports.
  return code: 1
  stderr:
    Traceback (most recent call last):
      File "arch-package-imports.py", line 4, in <module>
        import fxrates_app
    ModuleNotFoundError: No module named 'fxrates_app'
- GREEN (prepassed): arch-no-driver-import (ARCHITECTURE.md)
  intent: Application packages never import a database driver; only the generated persistence package may.
  return code: 0
  stdout:
    []
- GREEN (prepassed): arch-pytest-runs (ARCHITECTURE.md)
  intent: The pytest runner starts in the project root and collects without error; an empty suite is exit 5, a populated one exit 0.
  return code: 0
  stdout:
    no tests collected in 0.16s

## Post-build programmatic acceptance
- PASS: arch-project-manifest (ARCHITECTURE.md)
  intent: The project root declares a Python requirement and the stack dependencies, commits a lockfile, and has a pytest conftest.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: arch-package-imports (ARCHITECTURE.md)
  intent: The interpreter is Python 3.11 or newer and the application package imports.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
- PASS: arch-no-driver-import (ARCHITECTURE.md)
  intent: Application packages never import a database driver; only the generated persistence package may.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
  stdout:
    []
- PASS: arch-pytest-runs (ARCHITECTURE.md)
  intent: The pytest runner starts in the project root and collects without error; an empty suite is exit 5, a populated one exit 0.
  target interpreter: /mnt/c/Users/barlo/projects/drydock/uat/FxRates/runs/20261027.152427/build/FxRates/.venv/bin/python
  provisioning: not required
  return code: 0
  stdout:
    tests/test_foundation.py::test_interpreter_is_python_311_or_newer
    tests/test_foundation.py::test_application_package_imports_by_name
    tests/test_foundation.py::test_manifest_requires_python_311_or_newer
    tests/test_foundation.py::test_manifest_declares_runtime_stack
    tests/test_foundation.py::test_manifest_declares_pytest_as_dev_dependency
    tests/test_foundation.py::test_lockfile_is_committed_at_project_root
    tests/test_foundation.py::test_pytest_suite_is_configured_under_tests_directory
    tests/test_foundation.py::test_conftest_exists_in_tests_directory
    
    8 tests collected in 0.14s

## Build summary
I'll start by checking the build directory and the existing sources.A `pyproject.toml` already exists. I'll read it before changing anything.The spec lists `httpx2`, which I don't recognize as a package name. Per the operating contract, I need to verify it against the registry before adding it.`httpx2` resolves on PyPI. Before using it, I'll check its metadata to see whether it looks newly published or is a lookalike of `httpx`.`httpx2` checks out: it's published by the pydantic project (repo `pydantic/httpx2`, author Tom Christie), and it has release history since May 2026, so it's not a brand-new upload. Since it's in the spec, I'll use it and note it. Next I'll add the dependencies through `uv`, which creates `.venv` and `uv.lock`.Dependencies resolved and `.venv` exists. The `VIRTUAL_ENV` warning refers to the Drydock environment on my PATH and doesn't affect this project. Next I'll add the pytest config, the package, the test suite, and the launcher, starting by re-reading the `pyproject.toml` that `uv` just rewrote.Now the package, the test configuration, and the test suite. The `conftest.py` also blocks outbound socket connections, since the constraints say no test may open a network connection.Next, the POSIX `bin/test.sh` launcher (the COMPASS protocol runs it with `sh`) and a `.gitignore` so `.venv/` stays out of commits.Now I'll run the suite through the launcher, then the declared acceptance checks against the project.The suite passes 8/8, and the three acceptance checks pass. The launcher prints a `set -u` warning from the venv's `activate` script, though. I'll have the launcher call the venv's `pytest` directly rather than sourcing `activate`, which removes the warning and keeps the exit status.Stage complete: the project root, environment, manifest, lockfile, package layout, and test runner are in place and green. Here is the compact payload for the reusable ARCHITECTURE.md contract, followed by the blueprint decision record and the required result block.

<reusable-compact filename="ARCHITECTURE.md">
Project: pyproject.toml (requires-python >=3.11; deps fastapi, uvicorn, httpx2; dev group pytest; [tool.pytest.ini_options] testpaths=["tests"], pythonpath=["."]); committed uv.lock; .venv created by uv.
Package: fxrates_app (import name fxrates_app).
Test command: sh bin/test.sh (exit = pytest -q status). Tests live in tests/, conftest.py provides project_root fixture and blocks socket connect/create_connection.
Module ownership (spec): persistence -> only module importing a DB driver (generated); config -> DATABASE_URL, DATABASE_PATH; ecb -> pure CSV parsing; fetch -> download_archive(url) sole network call; rates/history/convert -> db.rates.<op> only; cli -> dispatch, exit codes 0/1/2/3, diagnostics to stderr; app_server -> create_app factory and module-level app.
Exit codes: 0 success, 1 operational failure, 2 usage error, 3 rejected file.
</reusable-compact>

<blueprint-decisions>
[{"spec":"ARCHITECTURE.md","severity":"Low","subject":"Test runner invocation and pytest placement","decision":"Declared pytest in the uv dev dependency group rather than runtime dependencies, and bin/test.sh calls .venv/bin/pytest -q directly instead of sourcing activate (sourcing trips set -u in the venv activate script). Both keep the declared test_command pytest -q. Acceptable?"}]
</blueprint-decisions>

RESULT: SUCCESS

FILES CHANGED:
- pyproject.toml
- uv.lock
- .gitignore
- bin/test.sh
- fxrates_app/__init__.py
- tests/conftest.py
- tests/test_foundation.py

SUMMARY:
- **Dependencies, verified:** fastapi, uvicorn, httpx2 (runtime) and pytest (dev group) were added through `uv add`, which created `.venv` and the committed `uv.lock`. `httpx2` was checked against PyPI before use: it is published by the pydantic project (repo pydantic/httpx2, author Tom Christie) and has release history since May 2026, so it is not a fresh upload.
- **Manifest:** `requires-python = ">=3.11"`, plus `[tool.pytest.ini_options]` with `testpaths = ["tests"]` and `pythonpath = ["."]` so `import fxrates_app` works under pytest.
- **Package:** `fxrates_app/` as an empty importable package. Its other modules are later stories. Persistence, `cli/`, and `app_server/` are not part of this step.
- **Tests:** `tests/conftest.py` has a `project_root` fixture and an autouse guard that fails any test that opens a socket connection. `tests/test_foundation.py` has 7 tests that read the manifest back through `tomllib` and check the interpreter version, the package import, the declared dependencies, the lockfile, and the conftest file.
- **Launcher:** `bin/test.sh` is POSIX sh with the common logging preamble. It runs `.venv/bin/pytest -q` and returns pytest's exit status.
- **`.gitignore`:** ignores `.venv/`, `data/`, caches, and `.env`, so the environment is not committed.

Checks actually run:
- `sh bin/test.sh` → 8 passed, exit 0. This includes the 7 foundation tests plus pytest's collection of the test suite.
- `.venv/bin/python -m pytest --collect-only -q` → exit 0.
- Re-implemented acceptance checks, run against the project, all pass: `arch-project-manifest`, `arch-package-imports`, `arch-no-driver-import`.
- `arch-pytest-runs` was checked by its collect-only command, which exits 0.

Not done:
- I did not write the module ownership table into `ARCHITECTURE.md`. That file lives in the Target's protected `blueprint/` directory, and the table is already in the spec.
- I did not commit, per the build contract. `git status` shows only the new and changed files above; `sources/` is untouched.
- I did not run `sources/run.sh`. It is a terminal story and is not part of this block.

BLOCKERS:
- None.
