"""Lets `python -m cli` run the dispatcher; the launcher `fxrates` uses this form."""

import sys

from cli import main

sys.exit(main())
