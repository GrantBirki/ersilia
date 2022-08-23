import click
import json

from .. import echo
from . import ersilia_cli
from ...hub.content.card import ModelCard, LakeCard
from ...serve.schema import ApiSchema
from ... import ModelBase
from ...utils.cli_query import query_yes_no
from ...utils.exceptions.email_reporting import send_exception_report_email

from ...utils.exceptions.exceptions import ErsiliaError

def card_cmd():
    """Creates card command"""
    # Example usage: ersilia card {MODEL}
    @ersilia_cli.command(
        short_help="Get model info card",
        help="Get model info card from Ersilia Model Hub.",
    )
    @click.argument("model", type=click.STRING)
    @click.option(
        "-s", "--schema", is_flag=True, default=False, help="Show schema of the model"
    )
    @click.option(
        "-l",
        "--lake",
        is_flag=True,
        default=False,
        help="Show the properties of the data lake",
    )
    @click.option(
        "-x",
        "--trigger",
        is_flag=True,
        default=False,
        help="Trigger exception",
    )
    def card(model, schema, lake, trigger):
        # try:
        if not trigger:
            mdl = ModelBase(model)
            model_id = mdl.model_id
            if schema:
                mc = ModelCard()
                click.echo(mc.get(model_id, as_json=True))
                return
            if lake:
                mc = LakeCard()
                click.echo(mc.get(model_id, as_json=True))
                return
            ac = ApiSchema(model_id, config_json=None)
            click.echo(json.dumps(ac.get(), indent=4))

        else:
        # except Exception as E:
            E = ErsiliaError
            text = ":triangular_flag: Something went wrong with Ersilia...\n\n"
            # text += "{}\n\n".format(self.__class__.__name__)
            text += "{}\n\n".format(E.__name__)
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