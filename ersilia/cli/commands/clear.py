from . import ersilia_cli
from ...utils.clear import Clearer
from ...utils.exceptions.exceptions import ErsiliaError
from ...utils.exceptions.clear_exceptions import ClearErsiliaError


def clear_cmd():
    """Clears all contents related to Ersilia available in the local computer"""
    # Example usage: ersilia setup
    @ersilia_cli.command(
        short_help="Clear ersilia",
        help="Clears all contents related to Ersilia available in the local computer.",
    )
    def clear():
        try:
            cl = Clearer()
            cl.clear()

        except ErsiliaError as E:
            raise E
        except Exception as E:
            # TODO: ensure that the exception is properly logged here to save stacktrace
            raise ClearErsiliaError