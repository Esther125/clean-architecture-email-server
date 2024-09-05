from email.message import EmailMessage
from unittest import IsolatedAsyncioTestCase, mock

from src.adapter.outward.send_email.storage_client import StorageClient
from src.adapter.outward.send_email.email_message_builder import (
    EmailMessageBuilder,
    FailedToBuildEmailMessage,
)
from src.app.domain.entity.email import Attachment
from src.app.port.outward.send_email.send_email_command import SendEmailCommand


class TestEmailMessageBuilder(IsolatedAsyncioTestCase):
    def setUp(self):
        self.message_builder = EmailMessageBuilder()
        self.storage_client = mock.Mock(spec=StorageClient)
        self.message_builder.storage_client = self.storage_client

    async def test_build_email_message_success(self):
        command = SendEmailCommand(
            email_id="test-id",
            receivers=["test@gmail.com"],
            subject="Test Subject",
            content="test content",
        )
        email_msg = await self.message_builder.build_email_message(command)
        assert isinstance(email_msg, EmailMessage)
        assert email_msg["From"] == self.message_builder.sender
        assert email_msg["To"] == "test@gmail.com"
        assert email_msg["Subject"] == "Test Subject"
        assert "test content" in email_msg.get_content()

    async def test_build_email_message_failed(self):
        self.message_builder._EmailMessageBuilder__add_attachments = mock.AsyncMock(
            side_effect=Exception("Failed to add attachments.")
        )
        command = SendEmailCommand(
            email_id="test-id",
            receivers=["test@gmail.com"],
            subject="Test Subject",
            content="test content",
            attachments=[
                Attachment(
                    filename="test-file",
                    filetype="application/json",
                    blobname="test.txt",
                )
            ],
        )
        with self.assertRaises(FailedToBuildEmailMessage):
            await self.message_builder.build_email_message(command)
