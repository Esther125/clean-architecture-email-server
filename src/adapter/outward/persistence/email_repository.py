import logging
from src.adapter.outward.persistence.db_client import DBClient

logger = logging.getLogger(__name__)


class EmailRepository:
    def __init__(self, client: DBClient) -> None:
        self.client = client

    def get_document(self, document_id: str):
        return self.client.collection("emails").document(document_id)  # type: ignore[attr-defined]

    async def save_document(self, document_id: str, data: dict):
        try:
            document = self.get_document(document_id)
            await document.set(data)
            logger.info(
                f"Successfully save the email to Firestore. (Document ID: {document_id})"
            )
        except Exception as error:
            logger.error(
                f"Failed to save email to Firestore. (Email ID: {document_id}) Error: {error}"
            )
            raise error

    async def update_document(self, document_id: str, data: dict):
        try:
            document = self.get_document(document_id)
            await document.set(data, merge=True)
            logger.info(
                f"Successfully update the email state in Firestore. (Document ID: {document_id})"
            )
        except Exception as error:
            logger.error(
                f"Failed to update the email state in Firestore. (Email ID: {document_id}) Error: {error}"
            )
            raise error
