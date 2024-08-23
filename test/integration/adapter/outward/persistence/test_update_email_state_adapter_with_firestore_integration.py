# import os
# import unittest
# from src.adapter.outward.persistence.db_client import DBClient
# from src.adapter.outward.persistence.email_repository import EmailRepository
# from src.adapter.outward.persistence.save_email_adapter import SaveEmailAdapter
# from src.adapter.outward.persistence.update_email_state_adapter import (
#     UpdateEmailStateAdapter,
# )
# from src.app.port.outward.save_email.save_email_command import SaveEmailCommand
# from src.app.port.outward.update_email_state.update_email_state_command import (
#     UpdateEmailStateCommand,
# )


# class TestUpdateEmailStateAdapterWithFirestoreIntegration(
#     unittest.IsolatedAsyncioTestCase
# ):
#     async def asyncSetUp(self):
#         os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8081"
#         self.db_client = DBClient()
#         self.email_repo = EmailRepository(client=self.db_client)
#         self.save_email_adapter = SaveEmailAdapter(repository=self.email_repo)
#         self.test_command = SaveEmailCommand(
#             email_id="test-id",
#             receivers=["test@gmail.com"],
#             subject="Test Subject",
#             content="test content",
#         )
#         await self.save_email_adapter.save_email(self.test_command)
#         self.update_email_state_adapter = UpdateEmailStateAdapter(
#             repository=self.email_repo
#         )

#     async def test_update_document_state(self):
#         test_command = UpdateEmailStateCommand(email_id="test-id", is_sent=True)
#         await self.update_email_state_adapter.update_state(test_command)
#         doc_ref = self.email_repo.get_document(test_command.email_id)
#         doc_snapshot = await doc_ref.get()
#         assert doc_snapshot.exists is True

#         doc_data = doc_snapshot.to_dict()
#         assert doc_data["is_sent"] is True

#     async def asyncTearDown(self):
#         doc_ref = self.email_repo.get_document("test-id")
#         await doc_ref.delete()
#         os.environ.pop("FIRESTORE_EMULATOR_HOST", None)
