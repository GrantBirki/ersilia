import click

from .. import echo
from . import ersilia_cli
from ...hub.content.catalog import ModelCatalog
from ...hub.content.search import ModelSearcher
from ...hub.content.table_update import table
from ...utils.cli_query import query_yes_no
from ...utils.exceptions.email_reporting import send_exception_report_email


def catalog_cmd():
    """Creates catalog command"""
    # Example usage: ersilia catalog
    @ersilia_cli.command(help="List a catalog of models")
    @click.option(
        "-l",
        "--local",
        is_flag=True,
        default=False,
        help="Show catalog of models available in the local computer",
    )
    @click.option(
        "-t",
        "--text",
        default=None,
        type=click.STRING,
        help="Shows the  model related to input keyword",
    )
    @click.option(
        "-m",
        "--mode",
        default=None,
        type=click.STRING,
        help="Shows the  model trained via input mode",
    )
    @click.option(
        "-n", "--next", is_flag=True, default=False, help="Shows the next table"
    )
    @click.option(
        "-p", "--previous", is_flag=True, default=False, help="Shows previous table"
    )
    def catalog(
        local=False, search=None, text=None, mode=None, next=False, previous=False
    ):
        try:
            mc = ModelCatalog()
            if not (local or text or mode):
                catalog = mc.hub()
                if not (next or previous):
                    catalog = table(catalog).initialise()

                if next:
                    catalog = table(catalog).next_table()

                if previous:
                    catalog = table(catalog).prev_table()

            if local:
                catalog = mc.local()

            if text:
                catalog = mc.hub()
                catalog = ModelSearcher(catalog).search_text(text)
            if mode:
                catalog = mc.hub()
                catalog = ModelSearcher(catalog).search_mode(mode)
            click.echo(catalog)

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