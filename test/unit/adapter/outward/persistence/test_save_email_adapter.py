from unittest import IsolatedAsyncioTestCase

from src.adapter.outward.persistence.email_repository import DBClient, EmailRepository
from src.adapter.outward.persistence.save_email_adapter import (
    FailedToSaveEmailToFirestoreError,
    SaveEmailAdapter,
)
from src.app.domain.entity.email import Attachment
from src.app.port.outward.save_email.save_email_command import SaveEmailCommand


class MockEmailRepositoryFailed:
    def document(self, email_id):
        raise Exception("Failed to get documents in Firestore.")


class TestSaveEmailAdapter(IsolatedAsyncioTestCase):
    def test_generate_attachments_list_success(self) -> None:
        self.db_client = DBClient()
        self.email_repository = EmailRepository(self.db_client)
        self.save_email_adapter = SaveEmailAdapter(repository=self.email_repository)

        command = SaveEmailCommand(
            email_id="test-id",
            receivers=["test@gmail.com"],
            subject="Test Subject",
            content="Test content",
            attachments=[
                Attachment(
                    filename="file1.txt", filetype="text/plain", blobname="blob1"
                ),
                Attachment(
                    filename="file2.txt", filetype="text/plain", blobname="blob2"
                ),
            ],
        )
        result = self.save_email_adapter.generate_attachments_list(command)
        expected_result = [
            {"filename": "file1.txt", "filetype": "text/plain", "blobname": "blob1"},
            {"filename": "file2.txt", "filetype": "text/plain", "blobname": "blob2"},
        ]
        assert result == expected_result

    async def test_failed_to_send_email_to_firestore(self) -> None:
        self.email_repository_failed = MockEmailRepositoryFailed()
        self.save_email_adapter = SaveEmailAdapter(
            repository=self.email_repository_failed
        )
        with self.assertRaises(FailedToSaveEmailToFirestoreError) as context:
            command = SaveEmailCommand(
                email_id="test-id",
                receivers=["test@gmail.com"],
                subject="Test Subject",
                content="Test content",
                attachments=[
                    Attachment(
                        filename="file1.txt", filetype="text/plain", blobname="blob1"
                    )
                ],
            )
            await self.save_email_adapter.save_email(command)
        assert "Failed to get documents in Firestore" in str(context.exception)
