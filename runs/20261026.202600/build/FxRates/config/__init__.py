import os
from pathlib import Path

def database_dsn() -> str:
    return os.environ.get('DATABASE_URL') or os.environ.get('DATABASE_PATH') or str(Path('data/app.db'))
