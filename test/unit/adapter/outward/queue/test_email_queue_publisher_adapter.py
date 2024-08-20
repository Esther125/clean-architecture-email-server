from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch
from src.adapter.outward.queue.email_queue_publisher_adapter import (
    EmailQueuePublisherAdapter,
    FailedToGenerateEmailMessageError,
)
from src.app.port.outward.queue_email.queue_email_command import QueueEmailCommand


class TestEmailQueuePublisherAdapter(IsolatedAsyncioTestCase):
    def setUp(self):
        self.queue_publisher_adapter = EmailQueuePublisherAdapter()

    async def test_generate_email_message_success(self) -> None:
        command = QueueEmailCommand(
            email_id="test-id",
            receivers=["test@gmail.com"],
            subject="Test Subject",
            content="Test Content",
        )
        result = self.queue_publisher_adapter.generate_email_message(command)
        self.assertIsInstance(result, bytes)

    async def test_generate_email_message_failed(self) -> None:
        command = QueueEmailCommand(
            email_id="test-id",
            receivers=["test@gmail.com"],
            subject="Test Subject",
            content="Test Content",
        )
        with patch("json.dumps", side_effect=Exception("Failed to parse to JSON.")):
            with self.assertRaises(FailedToGenerateEmailMessageError):
                self.queue_publisher_adapter.generate_email_message(command)
