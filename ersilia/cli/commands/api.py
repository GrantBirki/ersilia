import click
import json
import types

from . import ersilia_cli
from .. import echo
from ... import ErsiliaModel
from ...core.session import Session
from ...utils.cli_query import query_yes_no
from ...utils.exceptions.email_reporting import send_exception_report_email


def api_cmd():
    """Create api command"""
    # Example usage: ersilia api {API_NAME} -i {INPUT} [-o {OUTPUT} -b {BATCH_SIZE}]
    @ersilia_cli.command(
        short_help="Run API on a served model", help="Run API on a served model"
    )
    @click.argument("api_name", required=False, default=None, type=click.STRING)
    @click.option("-i", "--input", "input", required=True, type=click.STRING)
    @click.option(
        "-o", "--output", "output", required=False, default=None, type=click.STRING
    )
    @click.option(
        "-b", "--batch_size", "batch_size", required=False, default=100, type=click.INT
    )
    def api(api_name, input, output, batch_size):
        try: 
            session = Session(config_json=None)
            model_id = session.current_model_id()
            service_class = session.current_service_class()
            if model_id is None:
                echo(
                    "No model seems to be served. Please run 'ersilia serve ...' before.",
                    fg="red",
                )
                return
            mdl = ErsiliaModel(model_id, service_class=service_class, config_json=None)
            result = mdl.api(
                api_name=api_name, input=input, output=output, batch_size=batch_size
            )
            if isinstance(result, types.GeneratorType):
                for result in mdl.api(
                    api_name=api_name, input=input, output=output, batch_size=batch_size
                ):
                    if result is not None:
                        echo(json.dumps(result, indent=4))
                    else:
                        echo("Something went wrong", fg="red")
            else:
                echo(result)

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