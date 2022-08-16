import smtplib, ssl
from datetime import datetime

smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = "ersilia_errors@gmail.com"
password = '*******' # insecure: the password will be visible from the code. Is this permissible?

sender_email = "ersilia_errors@gmail.com"
receiver_email = "ersilia_errors@gmail.com"

def send_exception_report_email(E:Exception, log_text:str = ""):
    # get date/time info for message
    datetime_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.starttls(context=context) # Secure the connection
        server.login(sender_email, password)

        message = f"Subject: Exception {type(E)}: {datetime_str}\n\n"
        message += f"{str(E)}\n\n"
        message += log_text
        server.sendmail(sender_email, receiver_email, message)

    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit() 