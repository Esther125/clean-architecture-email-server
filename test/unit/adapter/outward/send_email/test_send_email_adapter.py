from unittest import IsolatedAsyncioTestCase, mock

from src.adapter.outward.send_email.email_message_builder import EmailMessageBuilder
from src.adapter.outward.send_email.send_email_adapter import (
    FailedToSendEmailWithSMTPServer,
    SendEmailAdapter,
)
from src.app.port.outward.send_email.send_email_command import SendEmailCommand


class TestSendEmailAdpater(IsolatedAsyncioTestCase):
    def setUp(self):
        self.send_email_adapter = SendEmailAdapter()
        self.email_builder = mock.Mock(spec=EmailMessageBuilder)
        self.send_email_adapter.email_builder = self.email_builder

    async def test_send_email_failed(self) -> None:
        self.email_builder.build_email_message.side_effect = Exception(
            "Failed to build email message."
        )
        with self.assertRaises(FailedToSendEmailWithSMTPServer):
            command = SendEmailCommand(
                email_id="test-id",
                receivers=["test@gmail.com"],
                subject="Test Subject",
                content="test content",
            )
            await self.send_email_adapter.send_email(command)
