from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock

from src.app.domain.service.queue_email.queue_email import QueueEmailService, EmailNotSavedError, EmailSaveAndQueueError, QueuingError
from src.app.port.outward.save_email.save_email_port import SaveEmailPort
from src.app.port.outward.queuing_email.queuing_email_port import QueuingEmailPort
from src.app.port.inward.queue_email.queue_email_command import QueueEmailCommand

class TestQueueEmailService(IsolatedAsyncioTestCase):
    def setUp(self):
        self.save_email_port = AsyncMock(spec=SaveEmailPort)
        self.queuing_email_port = AsyncMock(spec=QueuingEmailPort)
        self.service = QueueEmailService(self.save_email_port, self.queuing_email_port)
        self.command = QueueEmailCommand(
            email_id = "1",
            receivers = ["test@example.com"],
            subject = "Test Subject",
            content = "Test Content",
            attachments = None
        )

    async def test_queue_email_success(self):
        self.save_email_port.save_email.return_value = None  
        self.queuing_email_port.queuing_email.return_value = None  

        await self.service.queue_email(self.command)

        self.save_email_port.save_email.assert_called_once()
        self.queuing_email_port.queuing_email.assert_called_once()

    async def test_queue_email_fail_to_save_email(self):
        self.save_email_port.save_email.side_effect = EmailNotSavedError(email_id="1")

        with self.assertRaises(EmailNotSavedError):
            await self.service.queue_email(self.command)

    async def test_queue_email_fail_to_queue_email(self):
        self.queuing_email_port.queuing_email.side_effect = QueuingError(email_id="1")
        
        with self.assertRaises(QueuingError):
            await self.service.queue_email(self.command)

    async def test_queue_email_both_failed(self):
        self.save_email_port.save_email.side_effect = EmailNotSavedError(email_id="1")
        self.queuing_email_port.queuing_email.side_effect = QueuingError(email_id="1")
        
        with self.assertRaises(EmailSaveAndQueueError):
            await self.service.queue_email(self.command)

