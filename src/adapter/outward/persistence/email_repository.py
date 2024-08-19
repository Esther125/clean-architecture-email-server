import os
from dotenv import load_dotenv
from google.cloud import firestore

from src.app.port.outward.save_email.save_email_command import SaveEmailCommand
from src.app.port.outward.save_email.save_email_port import SaveEmailPort

load_dotenv()


class EmailRepository(SaveEmailPort):
    def __init__(self) -> None:
        self.project_id = os.getenv("GCP_PROJECT_ID")
        self.database_id = os.getenv("GCP_FIRESTORE_DATABASE_ID")
        self.db = firestore.AsyncClient(self.project_id, self.database_id)

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
