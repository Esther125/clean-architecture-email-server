import os
from google.cloud import firestore
from google.cloud.firestore_v1 import FieldFilter


from src.app.port.outward.update_email_state.update_email_state_command import (
    UpdateEmailStateCommand,
)
from src.app.port.outward.update_email_state.update_email_state_port import (
    UpdateEmailStatePort,
)


class UpdateEmailStateAdapter(UpdateEmailStatePort):
    def __init__(self) -> None:
        self.project_id = os.getenv("GCP_PROJECT_ID")
        self.database_id = os.getenv("GCP_FIRESTORE_DATABASE_ID")
        self.db = firestore.AsyncClient(self.project_id, self.database_id)

    async def update_state(self, command: UpdateEmailStateCommand) -> None:
        doc_ref = (
            self.db.collection("emails")
            .where(filter=FieldFilter("email_id", "==", command.email_id))
            .stream()
        )
        await doc_ref.update({"is_sent": command.is_sent})
