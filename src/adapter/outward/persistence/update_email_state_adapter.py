import logging

from src.adapter.outward.persistence.email_repository import EmailRepository
from src.app.port.outward.update_email_state.update_email_state_command import (
    UpdateEmailStateCommand,
)
from src.app.port.outward.update_email_state.update_email_state_port import (
    UpdateEmailStatePort,
)

logger = logging.getLogger(__name__)


class UpdateEmailStateAdapter(UpdateEmailStatePort):
    def __init__(self, repository: EmailRepository) -> None:
        self.repository = repository

    async def update_state(self, command: UpdateEmailStateCommand) -> None:
        try:
            await self.repository.update_document(
                document_id=command.email_id, data={"is_sent": command.is_sent}
            )
        except Exception as error:
            raise FailedToUpdateEmailStateInFirestoreError(command.email_id, error)


class FailedToUpdateEmailStateInFirestoreError(Exception):
    def __int__(self, email_id, error) -> None:
        self.email_id = email_id
        self.error = error
        self.message = f"Failed to update email state in Firestore. (ID: {email_id}) Error: {error}"
        super().__init__(self.message)
