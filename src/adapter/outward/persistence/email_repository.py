import os
import logging
from typing import Dict, List
from dotenv import load_dotenv
from google.oauth2 import service_account
from google.cloud import firestore

from src.app.port.outward.save_email.save_email_command import SaveEmailCommand
from src.app.port.outward.save_email.save_email_port import SaveEmailPort

logger = logging.getLogger(__name__)

load_dotenv()


class EmailRepository(SaveEmailPort):
    def __init__(self) -> None:
        self.credentials = service_account.Credentials.from_service_account_file(
            os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        )
        self.project_id = os.getenv("GCP_PROJECT_ID")
        self.database_id = os.getenv("GCP_FIRESTORE_DATABASE_ID")
        self.db = firestore.AsyncClient(
            project=self.project_id,
            database=self.database_id,
            credentials=self.credentials,
        )

    def generate_attachments_list(
        self, command: SaveEmailCommand
    ) -> List[Dict[str, str]]:
        try:
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
        except Exception:
            raise

    async def save_email(self, command: SaveEmailCommand) -> None:
        try:
            attachments_list = self.generate_attachments_list(command)
            doc_ref = self.db.collection("emails").document(command.email_id)
            await doc_ref.set(
                {
                    "email_id": command.email_id,
                    "is_sent": command.is_sent,
                    "receivers": command.receivers,
                    "subject": command.subject,
                    "content": command.content,
                    "attachments": attachments_list,
                }
            )
            logger.info(
                f"Successfully save the email to Firestore. (Email ID: {command.email_id})"
            )
        except Exception as error:
            raise FailedToSaveEmailToFirestoreError(command.email_id, error)


class FailedToSaveEmailToFirestoreError(Exception):
    def __int__(self, email_id, error) -> None:
        self.email_id = email_id
        self.error = error
        self.message = (
            f"Failed to save email to Firestore. (ID: {email_id}) Error: {error}"
        )
        super().__init__(self.message)
