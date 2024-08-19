from unittest import IsolatedAsyncioTestCase

from src.adapter.outward.persistence.email_repository import EmailRepository
from src.app.domain.entity.email import Attachment
from src.app.port.outward.save_email.save_email_command import SaveEmailCommand


class TestEmailRepository(IsolatedAsyncioTestCase):
    def setUp(self):
        self.email_repository = EmailRepository()

    def test_generate_attachments_list_success(self) -> None:
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
        result = self.email_repository.generate_attachments_list(command)
        expected_result = [
            {"filename": "file1.txt", "filetype": "text/plain", "blobname": "blob1"},
            {"filename": "file2.txt", "filetype": "text/plain", "blobname": "blob2"},
        ]
        assert result == expected_result
