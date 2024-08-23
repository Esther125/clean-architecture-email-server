import os
import unittest

from src.adapter.outward.persistence.db_client import DBClient
from src.adapter.outward.persistence.save_email_adapter import SaveEmailAdapter
from src.app.port.outward.save_email.save_email_command import SaveEmailCommand
from src.app.domain.entity.email import Attachment
from src.adapter.outward.persistence.email_repository import EmailRepository


class TestEmailRepositoryWithFirestoreIntegration(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8081"
        self.db_client = DBClient()
        self.email_repo = EmailRepository(client=self.db_client)
        self.save_email_adapter = SaveEmailAdapter(repository=self.email_repo)

    async def test_save_document(self):
        sample_attachment = Attachment(
            filename="test_file.txt", filetype="text/plain", blobname="test_blob_name"
        )
        test_command = SaveEmailCommand(
            email_id="test-id",
            receivers=["test@example.com"],
            subject="Test Subject",
            content="This is a test email.",
            attachments=[sample_attachment],
        )
        await self.save_email_adapter.save_email(test_command)
        doc_ref = self.email_repo.get_document(test_command.email_id)
        doc_snapshot = await doc_ref.get()
        self.assertTrue(doc_snapshot.exists)

    async def asyncTearDown(self):
        doc_ref = self.email_repo.get_document("test-id")
        await doc_ref.delete()
        os.environ.pop("FIRESTORE_EMULATOR_HOST", None)
