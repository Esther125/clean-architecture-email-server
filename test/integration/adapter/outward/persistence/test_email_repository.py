import os
import unittest

from src.adapter.outward.persistence.db_client import DBClient
from src.adapter.outward.persistence.email_repository import EmailRepository


class TestEmailRepository(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8081"
        self.db_client = DBClient()
        self.email_repo = EmailRepository(client=self.db_client)

    async def test_save_document(self):
        await self.email_repo.save_document(
            document_id="test-id",
            data={
                "email_id": "test-id",
                "receivers": ["test@example.com"],
                "subject": "Test Subject",
                "content": "This is a test email.",
                "is_sent": False,
            },
        )
        doc_ref = self.email_repo.get_document("test-id")
        doc_snapshot = await doc_ref.get()
        self.assertTrue(doc_snapshot.exists)

    async def test_update_document(self):
        await self.email_repo.save_document(
            document_id="test-id",
            data={
                "email_id": "test-id",
                "receivers": ["test@example.com"],
                "subject": "Test Subject",
                "content": "This is a test email.",
                "is_sent": False,
            },
        )
        await self.email_repo.update_document(
            document_id="test-id", data={"is_sent": True}
        )
        doc_ref = self.email_repo.get_document("test-id")
        doc_snapshot = await doc_ref.get()
        assert doc_snapshot.exists is True

        doc_data = doc_snapshot.to_dict()
        assert doc_data["is_sent"] is True

    async def asyncTearDown(self):
        doc_ref = self.email_repo.get_document("test-id")
        await doc_ref.delete()
        os.environ.pop("FIRESTORE_EMULATOR_HOST", None)
