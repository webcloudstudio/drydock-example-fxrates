<!-- Compacted from ARCHITECTURE.md sha256=f277db47b49b73dbb6a00804908c5d41b3e6510719d9eaee12d6905babe44656 on 2026-10-27 by drydock build agent -->

Project: pyproject.toml (requires-python >=3.11; deps fastapi, uvicorn, httpx2; dev group pytest; [tool.pytest.ini_options] testpaths=["tests"], pythonpath=["."]); committed uv.lock; .venv created by uv.
Package: fxrates_app (import name fxrates_app).
Test command: sh bin/test.sh (exit = pytest -q status). Tests live in tests/, conftest.py provides project_root fixture and blocks socket connect/create_connection.
Module ownership (spec): persistence -> only module importing a DB driver (generated); config -> DATABASE_URL, DATABASE_PATH; ecb -> pure CSV parsing; fetch -> download_archive(url) sole network call; rates/history/convert -> db.rates.<op> only; cli -> dispatch, exit codes 0/1/2/3, diagnostics to stderr; app_server -> create_app factory and module-level app.
Exit codes: 0 success, 1 operational failure, 2 usage error, 3 rejected file.
