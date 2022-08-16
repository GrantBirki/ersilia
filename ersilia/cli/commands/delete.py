import click
import csv

from . import ersilia_cli
from .. import echo
from ...hub.delete.delete import ModelFullDeleter
from ... import ModelBase
from ...utils.cli_query import query_yes_no
from ...utils.exceptions.email_reporting import send_exception_report_email


def delete_cmd():
    """Create delete command"""

    def _delete(md, model_id):
        md.delete(model_id)

    # Example usage: ersilia delete {MODEL}
    @ersilia_cli.command(
        short_help="Delete model from local computer",
        help="Delete model from local computer. The BentoML bundle is deleted, as well as the files stored in "
        "the EOS directory and the Pip-installed package",
    )
    @click.argument("model", type=click.STRING)
    def delete(model):
        try:
            model_id = ModelBase(model).model_id
            md = ModelFullDeleter()
            if md.needs_delete(model_id):
                echo("Deleting model {0}".format(model_id))
                _delete(md, model_id)
                echo(
                    ":collision: Model {0} deleted successfully!".format(model_id),
                    fg="green",
                )
            else:
                echo(
                    ":person_tipping_hand: Model {0} is not available locally. No delete is necessary".format(
                        model_id
                    ),
                    fg="yellow",
                )

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
