import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

from src.app.port.outward.send_email.send_email_command import SendEmailCommand
from src.app.port.outward.send_email.send_email_port import SendEmailPort

load_dotenv()


class SendEmailAdapter(SendEmailPort):
    def __init__(self) -> None:
        self.smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
        self.sender = str(os.getenv("EMAIL_SENDER"))
        self.password = str(os.getenv("APP_PASSWORD"))

    def build_email_message(self, command: SendEmailCommand) -> EmailMessage:
        try:
            email_msg = EmailMessage()
            email_msg["From"] = self.sender
            email_msg["To"] = command.receivers
            email_msg["Subject"] = command.subject
            email_msg.set_content(command.content)
            return email_msg
        except Exception as error:
            raise FailedToBuildEmailMessage(error)

    async def send_email(self, command: SendEmailCommand) -> None:
        try:
            with self.smtp_server as smtp:
                email_msg = self.build_email_message(command)
                smtp.starttls()
                smtp.login(self.sender, self.password)
                smtp.send_message(email_msg)
        except Exception as error:
            raise FailedToSendEmailWithSMTPServer(error, command.email_id)


class FailedToBuildEmailMessage(Exception):
    def __init__(self, error) -> None:
        self.error = error
        self.message = f"Failed to build email message. Error: {error}"
        super().__init__(self.message)


class FailedToSendEmailWithSMTPServer(Exception):
    def __init__(self, error, email_id) -> None:
        self.error = error
        self.email_id = email_id
        self.message = (
            f"Failed to send email with SMTP server. (ID: {email_id}) Error: {error}"
        )
        super().__init__(self.message)
