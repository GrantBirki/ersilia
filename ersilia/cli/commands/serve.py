import click
import os
from ...utils import tmp_pid_file
from . import ersilia_cli
from .. import echo
from ... import ErsiliaModel
from ..messages import ModelNotFound
from ...utils.cli_query import query_yes_no
from ...utils.exceptions.email_reporting import send_exception_report_email



def serve_cmd():
    """Creates serve command"""
    # Example usage: ersilia serve {MODEL}
    @ersilia_cli.command(short_help="Serve model", help="Serve model")
    @click.argument("model", type=click.STRING)
    @click.option("--lake/--no-lake", is_flag=True, default=True)
    @click.option("--docker/--no-docker", is_flag=True, default=False)
    def serve(model, lake, docker):
        try:
            if docker:
                service_class = "docker"
            else:
                service_class = None
            mdl = ErsiliaModel(model, save_to_lake=lake, service_class=service_class)
            if not mdl.is_valid():
                ModelNotFound(mdl).echo()
            mdl.serve()
            if mdl.url is None:
                echo("No URL found. Service unsuccessful.", fg="red")
                return
            echo(
                ":rocket: Serving model {0}: {1}".format(mdl.model_id, mdl.slug), fg="green"
            )
            echo("")
            echo("   URL: {0}".format(mdl.url), fg="yellow")
            echo("   PID: {0}".format(mdl.pid), fg="yellow")
            echo("   SRV: {0}".format(mdl.scl), fg="yellow")
            echo("")
            echo(":backhand_index_pointing_right: Available APIs:", fg="blue")
            apis = mdl.get_apis()
            for api in apis:
                echo("   - {0}".format(api), fg="blue")

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