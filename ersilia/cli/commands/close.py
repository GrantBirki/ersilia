from . import ersilia_cli
from .. import echo
from ... import ErsiliaModel
from ...core.session import Session
from ...utils.cli_query import query_yes_no
from ...utils.exceptions.email_reporting import send_exception_report_email


def close_cmd():
    # Example usage: ersilia close {MODEL}
    @ersilia_cli.command(short_help="Close model", help="Close model")
    def close():
        try:
            session = Session(config_json=None)
            model_id = session.current_model_id()
            service_class = session.current_service_class()
            if model_id is None:
                echo("No model was served")
                return
            mdl = ErsiliaModel(model_id, service_class=service_class)
            mdl.close()
            echo(":no_entry: Model {0} closed".format(mdl.model_id), fg="green")

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