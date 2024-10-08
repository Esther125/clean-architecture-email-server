from asyncio import to_thread
import asyncio
import os
from email.message import EmailMessage
from typing import List

from src.adapter.outward.send_email.storage_client import StorageClient
from src.app.port.outward.send_email.send_email_command import SendEmailCommand


class EmailMessageBuilder:
    def __init__(self) -> None:
        self.storage_client = StorageClient()
        self.sender = str(os.getenv("EMAIL_SENDER"))

    async def async_download_attachment(self, blob_name):
        return await to_thread(
            self.storage_client.download_attachment, blob_name=blob_name
        )

    async def __add_attachments(
        self, email_msg: EmailMessage, attachments: List
    ) -> None:
        download_tasks = [
            self.async_download_attachment(attachment.blobname)
            for attachment in attachments
        ]
        downloaded_files = await asyncio.gather(*download_tasks)
        for file_content, attachment in zip(downloaded_files, attachments):
            maintype, subtype = attachment.filetype.split("/", 1)
            email_msg.add_attachment(
                file_content,
                maintype=maintype,
                subtype=subtype,
                filename=attachment.filename,
            )

    async def build_email_message(self, command: SendEmailCommand) -> EmailMessage:
        try:
            email_msg = EmailMessage()
            email_msg["From"] = self.sender
            email_msg["To"] = command.receivers
            email_msg["Subject"] = command.subject
            email_msg.set_content(command.content)

            if len(command.attachments) != 0:
                await self.__add_attachments(email_msg, command.attachments)
            return email_msg
        except Exception as error:
            raise FailedToBuildEmailMessage(error)


class FailedToBuildEmailMessage(Exception):
    def __init__(self, error) -> None:
        self.error = error
        self.message = f"Failed to build email message. Error: {error}"
        super().__init__(self.message)
