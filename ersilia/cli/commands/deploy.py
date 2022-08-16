import click

from . import ersilia_cli
from .. import echo
from ...contrib.deploy import Deployer
from ... import ModelBase

from ...utils.cli_query import query_yes_no
from ...utils.exceptions.email_reporting import send_exception_report_email


def deploy_cmd():
    """Creates deploy command"""

    # Example usage: ersilia deploy {MODEL}
    @ersilia_cli.command(
        short_help="Deploy model to the cloud",
        help="Deploy model in a cloud service. "
        "This option is only for developers and requires credentials.",
    )
    @click.argument("model", type=click.STRING)
    @click.option("--cloud", default="heroku", type=click.STRING)
    def deploy(model, cloud):
        try:
            model_id = ModelBase(model).model_id
            dp = Deployer(cloud=cloud)
            if dp.dep is None:
                click.echo(click.style("Please enter a valid cloud option", fg="red"))
                click.echo(
                    click.style(
                        "Only 'heroku' and 'local' are available for the moment...",
                        fg="yellow",
                    )
                )
                return
            dp.deploy(model_id)
    
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
