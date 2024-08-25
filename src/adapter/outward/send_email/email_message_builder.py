import os
from email.message import EmailMessage
from typing import List

from src.adapter.outward.send_email.attachment_db_client import AttachmentDBClient
from src.app.port.outward.send_email.send_email_command import SendEmailCommand


class EmailMessageBuilder:
    def __init__(self) -> None:
        self.attachment_db_client = AttachmentDBClient()
        self.sender = str(os.getenv("EMAIL_SENDER"))

    def __add_attachments(self, email_msg: EmailMessage, attachments: List) -> None:
        for attachment in attachments:
            file_content = self.attachment_db_client.download_attachment(
                blob_name=attachment.blobname
            )
            maintype, subtype = attachment.filetype.split("/", 1)
            email_msg.add_attachment(
                file_content,
                maintype=maintype,
                subtype=subtype,
                filename=attachment.filename,
            )

    def build_email_message(self, command: SendEmailCommand) -> EmailMessage:
        try:
            email_msg = EmailMessage()
            email_msg["From"] = self.sender
            email_msg["To"] = command.receivers
            email_msg["Subject"] = command.subject
            email_msg.set_content(command.content)

            if not command.attachments:
                self.__add_attachments(email_msg, command.attachments)
            return email_msg
        except Exception as error:
            raise FailedToBuildEmailMessage(error)


class FailedToBuildEmailMessage(Exception):
    def __init__(self, error) -> None:
        self.error = error
        self.message = f"Failed to build email message. Error: {error}"
        super().__init__(self.message)
