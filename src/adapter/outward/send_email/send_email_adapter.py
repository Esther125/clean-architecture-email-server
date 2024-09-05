import os
import smtplib
from dotenv import load_dotenv

from src.adapter.outward.send_email.email_message_builder import EmailMessageBuilder
from src.app.port.outward.send_email.send_email_command import SendEmailCommand
from src.app.port.outward.send_email.send_email_port import SendEmailPort


load_dotenv(override=True)


class SendEmailAdapter(SendEmailPort):
    def __init__(self) -> None:
        self.smtp_server = str(os.getenv("SMTP_SERVER", "smtp.gmail.com"))
        self.smtp_port = int(os.getenv("SMTP_PORT", 587))
        self.sender = str(os.getenv("EMAIL_SENDER"))
        self.password = str(os.getenv("APP_PASSWORD"))
        self.email_builder = EmailMessageBuilder()

    async def send_email(self, command: SendEmailCommand) -> None:
        try:
            email_msg = await self.email_builder.build_email_message(command)
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as smtp:
                smtp.starttls()
                smtp.login(self.sender, self.password)
                smtp.send_message(email_msg)
        except Exception as error:
            raise FailedToSendEmailWithSMTPServer(error, command.email_id)


class FailedToSendEmailWithSMTPServer(Exception):
    def __init__(self, error, email_id) -> None:
        self.error = error
        self.email_id = email_id
        self.message = (
            f"Failed to send email with SMTP server. (ID: {email_id}) Error: {error}"
        )
        super().__init__(self.message)
