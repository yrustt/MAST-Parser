import os
import smtplib
import ssl

from email.message import EmailMessage
from io import StringIO


class LastFamousPersonEmailSender:
    def send(self, csv: StringIO):
        msg = self._create_email_message(csv)
        context = ssl.create_default_context()

        smtp_host = os.environ.get("SMTP_HOST")
        smtp_port = int(os.environ.get("SMTP_PORT"))
        smtp_username = os.environ.get("SMTP_USERNAME")
        smtp_password = os.environ.get("SMTP_PASSWORD")

        with smtplib.SMTP_SSL(
            host=smtp_host, port=smtp_port, context=context
        ) as smtp_server:
            smtp_server.login(smtp_username, smtp_password)
            smtp_server.send_message(msg)

    def _create_email_message(self, csv: StringIO) -> EmailMessage:
        msg = EmailMessage()

        msg["To"] = os.environ.get("NOTIFY_EMAIL")
        msg["From"] = os.environ.get("NOREPLY_EMAIL")
        msg["Subject"] = "Новые умершие известные люди"

        msg.set_content("Смотрите вложение со списком умерших известных людей.")
        msg.add_attachment(
            csv.getvalue().encode("utf-8"),
            maintype="text/csv",
            subtype="csv",
            filename="new_deads.csv",
        )

        return msg
