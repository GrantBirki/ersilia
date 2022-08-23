import click
import time

import os
from . import ersilia_cli
from ...hub.fetch.fetch import ModelFetcher
from ... import ModelBase

from .. import echo
from ...utils.cli_query import query_yes_no
from ...utils.exceptions.email_reporting import send_exception_report_email

def fetch_cmd():
    """Create fetch commmand"""

    def _fetch(mf, model_id):
        mf.fetch(model_id)

    # Example usage: ersilia fetch {MODEL}
    @ersilia_cli.command(
        short_help="Fetch model from Ersilia Model Hub",
        help="Fetch model from EOS repository. Model files are downloaded from GitHub and model data are "
        "downloaded from a file storage system such as the Open Science Framework. Model is downloaded to "
        "an EOS folder, then packed to a BentoML bundle",
    )
    @click.argument("model", type=click.STRING)
    @click.option("--mode", "-m", default=None, type=click.STRING)
    @click.option("--dockerize/--not-dockerize", default=False)
    def fetch(model, mode, dockerize):
        try:
            mdl = ModelBase(model)
            model_id = mdl.model_id
            # TODO: Move the commented code
            # url = "https://github.com/ersilia-os/{0}.git/info/lfs".format(model_id)
            # cmd = "echo " + url + "| perl -ne 'print $1 if m!([^/]+/[^/]+?)(?:\.git)?$!' | xargs -I{} curl -s -k https://api.github.com/repos/'{}' | grep size"
            # echo(
            #    "The disk storage of this model in KB is"
            # )
            # print (
            #    os.system(cmd)
            # )
            echo(
                ":down_arrow:  Fetching model {0}: {1}".format(model_id, mdl.slug),
                fg="blue",
            )
            mf = ModelFetcher(mode=mode, dockerize=dockerize)
            _fetch(mf, model_id)
            echo(":thumbs_up: Model {0} fetched successfully!".format(model_id), fg="green")

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

            # # TODO: add access to log information
            # if query_yes_no("Would you like to access the log?"):
            #     print("No log info")
