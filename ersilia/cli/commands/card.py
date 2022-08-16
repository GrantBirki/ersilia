import click
import json

from . import ersilia_cli
from ...hub.content.card import ModelCard, LakeCard
from ...serve.schema import ApiSchema
from ... import ModelBase
from ...utils.exceptions.exceptions import ErsiliaError
from ...utils.exceptions.card_exceptions import CardErsiliaError


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
    def card(model, schema, lake):
        try:
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

        except ErsiliaError as E:
            raise E
        except Exception as E:
            # TODO: ensure that the exception is properly logged here to save stacktrace
            raise CardErsiliaError