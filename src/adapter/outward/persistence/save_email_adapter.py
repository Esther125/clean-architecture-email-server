import logging
from typing import Dict, List
from dotenv import load_dotenv

from src.adapter.outward.persistence.email_repository import EmailRepository
from src.app.port.outward.save_email.save_email_command import SaveEmailCommand
from src.app.port.outward.save_email.save_email_port import SaveEmailPort

logger = logging.getLogger(__name__)

load_dotenv()


class SaveEmailAdapter(SaveEmailPort):
    def __init__(self, repository: EmailRepository) -> None:
        self.repository = repository

    def generate_attachments_list(
        self, command: SaveEmailCommand
    ) -> List[Dict[str, str]]:
        attachments_list = (
            [
                {
                    "filename": attachment.filename,
                    "filetype": attachment.filetype,
                    "blobname": attachment.blobname,
                }
                for attachment in command.attachments
            ]
            if command.attachments
            else []
        )
        return attachments_list

    async def save_email(self, command: SaveEmailCommand) -> None:
        try:
            attachments_list = self.generate_attachments_list(command)
            await self.repository.save_document(
                document_id=command.email_id,
                data={
                    "email_id": command.email_id,
                    "is_sent": command.is_sent,
                    "request_time": command.request_time,
                    "sent_time": command.sent_time,
                    "receivers": command.receivers,
                    "subject": command.subject,
                    "content": command.content,
                    "attachments": attachments_list,
                },
            )
        except Exception as error:
            raise FailedToSaveEmailToFirestoreError(command.email_id, error)


class FailedToSaveEmailToFirestoreError(Exception):
    def __init__(self, email_id, error) -> None:
        self.email_id = email_id
        self.error = error
        self.message = (
            f"Failed to save email to Firestore. (ID: {email_id}) Error: {error}"
        )
        super().__init__(self.message)
