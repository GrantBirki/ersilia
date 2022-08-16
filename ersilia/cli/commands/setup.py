import click
from .. import echo
from . import ersilia_cli
from ...utils.installers import base_installer, 
from ...utils.cli_query import query_yes_no
from ...utils.exceptions.email_reporting import send_exception_report_email


def setup_cmd():
    """Creates setup command"""
    # Example usage: ersilia setup
    @ersilia_cli.command(
        short_help="Setup ersilia",
        help="Setup ersilia, including building a model-server image, a base environment (eos), rdkit, etc.",
    )
    @click.option(
        "--base",
        is_flag=True,
        default=False,
        help="Install only bare-minimum dependencies.",
    )
    @click.option(
        "--full",
        is_flag=True,
        default=True,
        help="Install all the necessary dependencies.",
    )
    def setup(base=False, full=True):
        try:
            if base:
                base_installer()
            elif full:
                full_installer()
            else:
                pass
        
        except Exception as E:
            text = ":triangular_flag: Something went wrong with Ersilia...\n\n"
            text += "{}\n\n".format(self.__class__.__name__)
            echo(text)
            echo("Error message:\n")
            echo(":prohibited: " + str(E), fg="red")
            text = "If this error message is not helpful, open an issue at:\n"
            text += " - https://github.com/ersilia-os/ersilia\n"
            text += "Or feel free to reach out to us at:\n"
            text += " - hello[at]ersilia.io\n\n"
            text += "If you haven't, try to run your command in verbose mode (-v in the CLI)\n\n"
            echo(text)
        
            if query_yes_no("Would you like to report this error to Ersilia?"):
                send_exception_report_email(E)

            if query_yes_no("Would you like to access the log?"):
                print("No log info")
                # TODO: execute cli logic for [y/n] query and write log to a file

