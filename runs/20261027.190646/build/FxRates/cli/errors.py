"""Expected failures a command raises. Each class carries the exit code the dispatcher returns."""


class OperationalError(Exception):
    """The command ran but could not complete its work."""

    exit_code = 1


class UsageError(Exception):
    """The command line was not a valid invocation."""

    exit_code = 2


class RejectedFile(Exception):
    """An input file was refused before any of its content was written."""

    exit_code = 3
