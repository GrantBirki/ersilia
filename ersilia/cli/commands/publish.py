import click

from . import ersilia_cli
from .. import echo
from ...publish.publish import ModelPublisher
from ...publish.lake import LakeStorer
from ... import ModelBase
from ...utils.cli_query import query_yes_no
from ...utils.exceptions.email_reporting import send_exception_report_email


def publish_cmd():
    """Create publish commmand"""

    def _publish(mf, model_id):
        mf.publish(model_id)

    # Example usage: ersilia publish {STEP} {MODEL}
    @ersilia_cli.command(
        short_help="Publish model", help="Contribute a model to the Ersilia Model Hub"
    )
    @click.argument("step", type=click.STRING)
    @click.argument("model", type=click.STRING)
    def publish(step, model):

        try: 
            model_id = ModelBase(model).model_id
            mp = ModelPublisher(model_id, config_json=None, credentials_json=None)
            ls = LakeStorer(model_id, config_json=None, credentials_json=None)
            if step == "create":
                mp.create()
            elif step == "rebase":
                mp.rebase()
            elif step == "push":
                mp.push()
            elif step == "store":
                ls.store()
            elif step == "test":
                mp.test()
            else:
                echo(
                    "Step {0} is not valid. Please choose one of 'create', 'rebase', 'push', 'store' and 'test'",
                    fg="red",
                )
            echo(
                ":thumbs_up: Publishing step {0} for model {1} done successfully!".format(
                    step, model_id
                ),
                fg="green",
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


        
