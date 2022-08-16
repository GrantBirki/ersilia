import click
import json

from . import ersilia_cli
from .. import echo
from ...io.input import ExampleGenerator
from ... import ModelBase
from ...utils.cli_query import query_yes_no
from ...utils.exceptions.email_reporting import send_exception_report_email


def example_cmd():
    """Create example command"""

    # Example usage: ersilia example {MODEL} -n 10 [--file_name {FILE_NAME} --simple/--complete]
    @ersilia_cli.command(
        short_help="Generate input examples for the model of interest",
        help="This command generates input examples to be tested for the model of interest. The number of examples can be specified, as well as a file name. Simple inputs only contain the essential information, while complete inputs contain key and other fields, potentially.",
    )
    @click.argument("model", type=click.STRING)
    @click.option("--n_samples", "-n", default=5, type=click.INT)
    @click.option("--file_name", "-f", default=None, type=click.STRING)
    @click.option("--simple/--complete", "-s/-c", default=True)
    def example(model, n_samples, file_name, simple):
        try:
            model_id = ModelBase(model).model_id
            eg = ExampleGenerator(model_id)
            if file_name is None:
                echo(json.dumps(eg.example(n_samples, file_name, simple), indent=4))
            else:
                eg.example(n_samples, file_name, simple)
 
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