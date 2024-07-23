from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock

from src.app.domain.service.email_dispatch.email_dispatch import EmailDispatchService, EmailNotSavedError, EmailSaveAndQueueError, QueuingError
from src.app.port.inward.email_dispatch.email_dispatch_command import EmailDispatchCommand
from src.app.port.outward.queue_email.queue_email_port import QueueEmailPort
from src.app.port.outward.save_email.save_email_port import SaveEmailPort

class TestEmailDispatchService(IsolatedAsyncioTestCase):
    def setUp(self):
        self.save_email_port = AsyncMock(spec=SaveEmailPort)
        self.queue_email_port = AsyncMock(spec=QueueEmailPort)
        self.service = EmailDispatchService(self.save_email_port, self.queue_email_port)
        self.command = EmailDispatchCommand(
            email_id = "1",
            receivers = ["test@example.com"],
            subject = "Test Subject",
            content = "Test Content",
            attachments = None
        )

    async def test_email_dispatch_success(self):
        self.save_email_port.save_email.return_value = None  
        self.queue_email_port.queue_email.return_value = None  

        await self.service.dispatch_email(self.command)

        self.save_email_port.save_email.assert_called_once()
        self.queue_email_port.queue_email.assert_called_once()

    async def test_email_dispatch_failure_on_save(self):
        self.save_email_port.save_email.side_effect = EmailNotSavedError(email_id="1")

        with self.assertRaises(EmailNotSavedError):
            await self.service.dispatch_email(self.command)

    async def test_email_dispatch_failure_on_queue(self):
        self.queue_email_port.queue_email.side_effect = QueuingError(email_id="1")
        
        with self.assertRaises(QueuingError):
            await self.service.dispatch_email(self.command)

    async def test_email_dispatch_failure_on_both(self):
        self.save_email_port.save_email.side_effect = EmailNotSavedError(email_id="1")
        self.queue_email_port.queue_email.side_effect = QueuingError(email_id="1")
        
        with self.assertRaises(EmailSaveAndQueueError):
            await self.service.dispatch_email(self.command)
