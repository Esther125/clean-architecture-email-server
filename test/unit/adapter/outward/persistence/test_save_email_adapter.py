from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock

from src.adapter.outward.persistence.email_repository import EmailRepository
from src.adapter.outward.persistence.save_email_adapter import (
    FailedToSaveEmailToFirestoreError,
    SaveEmailAdapter,
)
from src.app.domain.entity.email import Attachment
from src.app.port.outward.save_email.save_email_command import SaveEmailCommand


class TestSaveEmailAdapter(IsolatedAsyncioTestCase):
    def test_generate_attachments_list_success(self) -> None:
        self.email_repository = AsyncMock(spec=EmailRepository)
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

    async def test_failed_to_save_email_to_firestore(self) -> None:
        self.email_repository = AsyncMock(spec=EmailRepository)
        self.save_email_adapter = SaveEmailAdapter(repository=self.email_repository)
        self.email_repository.save_document.side_effect = Exception(
            "Failed to save the document in Firestore"
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
        assert "Failed to save the document in Firestore" in str(context.exception)
