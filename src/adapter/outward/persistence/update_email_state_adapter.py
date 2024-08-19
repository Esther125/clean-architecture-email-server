import os
import logging
from google.cloud import firestore
from google.oauth2 import service_account
from google.cloud.firestore_v1 import FieldFilter


from src.app.port.outward.update_email_state.update_email_state_command import (
    UpdateEmailStateCommand,
)
from src.app.port.outward.update_email_state.update_email_state_port import (
    UpdateEmailStatePort,
)

logger = logging.getLogger(__name__)


class UpdateEmailStateAdapter(UpdateEmailStatePort):
    def __init__(self) -> None:
        self.credentials = service_account.Credentials.from_service_account_file(
            os.getenv("GCP_SERVICE_ACCOUNT_SECRET_PATH")
        )
        self.project_id = os.getenv("GCP_PROJECT_ID")
        self.database_id = os.getenv("GCP_FIRESTORE_DATABASE_ID")
        self.db = firestore.AsyncClient(self.project_id, self.database_id)

    async def update_state(self, command: UpdateEmailStateCommand) -> None:
        try:
            doc_ref = (
                self.db.collection("emails")
                .where(filter=FieldFilter("email_id", "==", command.email_id))
                .stream()
            )
            await doc_ref.update({"is_sent": command.is_sent})
            logger.info(
                f"Successfully update the email state. (Email ID: {command.email_id})"
            )
        except Exception as error:
            raise FailedToUpdateEmailStateInFirestoreError(command.email_id, error)


class FailedToUpdateEmailStateInFirestoreError(Exception):
    def __int__(self, email_id, error) -> None:
        self.email_id = email_id
        self.error = error
        self.message = f"Failed to update email state in Firestore. (ID: {email_id}) Error: {error}"
        super().__init__(self.message)
