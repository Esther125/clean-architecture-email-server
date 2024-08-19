import os
import logging
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

    async def save_email(self, command: SaveEmailCommand) -> None:
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

        doc_ref = self.db.collection("emails").document()
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
