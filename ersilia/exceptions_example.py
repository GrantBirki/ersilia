from tkinter import E
from ersilia.utils.exceptions import ErsiliaError


try:

except ErsiliaError as E:
    # do you want to see the log?
    # do you want to report?
    raise E

except Exception E:
    # do you want to see the log?
    # do you want to report?
    raise E


class PrepareException(ErsiliaError):
    message = "error occured when running prepare module in cli command fetch"

Questions for Miquel:
1. walk us through ErsiliaBase--what does it do/mean?
2. what does the Silencer class encapsulate?
