from unittest import IsolatedAsyncioTestCase
from unittest.mock import Mock

from src.adapter.outward.persistence.email_repository import EmailRepository
from src.adapter.outward.persistence.update_email_state_adapter import (
    FailedToUpdateEmailStateInFirestoreError,
    UpdateEmailStateAdapter,
)
from src.app.port.outward.update_email_state.update_email_state_command import (
    UpdateEmailStateCommand,
)


class TestUpdateEmailStateAdapter(IsolatedAsyncioTestCase):
    def setUp(self):
        self.email_repository = Mock(spec=EmailRepository)
        self.update_email_state_adapter = UpdateEmailStateAdapter(
            repository=self.email_repository
        )

    async def test_failed_to_update_state_in_firestore(self):
        self.email_repository.update_document.side_effect = Exception(
            "Failed to update the document."
        )

        with self.assertRaises(FailedToUpdateEmailStateInFirestoreError) as context:
            command = UpdateEmailStateCommand(email_id="test-id", is_sent=True)
            await self.update_email_state_adapter.update_state(command)

        assert "Failed to update the document" in str(context.exception)
