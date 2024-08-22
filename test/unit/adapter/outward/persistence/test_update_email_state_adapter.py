from unittest import IsolatedAsyncioTestCase

from src.adapter.outward.persistence.update_email_state_adapter import (
    FailedToUpdateEmailStateInFirestoreError,
    UpdateEmailStateAdapter,
)
from src.app.port.outward.update_email_state.update_email_state_command import (
    UpdateEmailStateCommand,
)


class MockEmailRepositoryFailed:
    def document(self, email_id):
        raise Exception("Failed to get documents in Firestore.")


class TestUpdateEmailStateAdapter(IsolatedAsyncioTestCase):
    def setUp(self):
        self.email_repository_failed = MockEmailRepositoryFailed()
        self.update_email_state_adapter = UpdateEmailStateAdapter(
            repository=self.email_repository_failed
        )

    async def test_failed_to_update_state_in_firestore(self):
        with self.assertRaises(FailedToUpdateEmailStateInFirestoreError) as context:
            command = UpdateEmailStateCommand(email_id="test-id", is_sent=True)
            await self.update_email_state_adapter.update_state(command)

        assert "Failed to get documents in Firestore" in str(context.exception)
