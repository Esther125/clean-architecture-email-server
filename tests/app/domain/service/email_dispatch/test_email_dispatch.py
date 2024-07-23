from unittest import IsolatedAsyncioTestCase

from src.app.domain.service.email_dispatch.email_dispatch import EmailDispatchService, EmailNotSavedError, EmailSaveAndQueueError, QueuingError
from src.app.port.inward.email_dispatch.email_dispatch_command import EmailDispatchCommand
from src.app.port.outward.queue_email.queue_email_command import QueueEmailCommand
from src.app.port.outward.queue_email.queue_email_port import QueueEmailPort
from src.app.port.outward.save_email.save_email_command import SaveEmailCommand
from src.app.port.outward.save_email.save_email_port import SaveEmailPort


class MockSaveEmailAdapter(SaveEmailPort):
    def __init__(self, raise_exception = False):
        self.raise_exception = raise_exception

    async def save_email(self, command: SaveEmailCommand):
        if self.raise_exception:
            raise Exception()


class MockQueueEmailAdapter(QueueEmailPort):
    def __init__(self, raise_exception = False):
        self.raise_exception = raise_exception

    async def queue_email(self, command: QueueEmailCommand):
        if self.raise_exception:
            raise Exception()

    
class TestEmailDispatchService(IsolatedAsyncioTestCase):
    def setUp(self):
        self.save_email_adapter = MockSaveEmailAdapter()
        self.queue_email_adapter = MockQueueEmailAdapter()
        self.service = EmailDispatchService(self.save_email_adapter, self.queue_email_adapter)
        self.command = EmailDispatchCommand(
            email_id = "1",
            receivers = ["test@example.com"],
            subject = "Test Subject",
            content = "Test Content",
            attachments = None
        )

    async def test_email_dispatch_success(self):
        success = await self.service.dispatch_email(self.command)
        self.assertTrue(success, "Email dispatch should succeed")

    async def test_email_dispatch_failure_on_save(self):
        self.save_email_adapter.raise_exception = True
        with self.assertRaises(EmailNotSavedError):
            await self.service.dispatch_email(self.command)

    async def test_email_dispatch_failure_on_queue(self): 
        self.queue_email_adapter.raise_exception = True
        with self.assertRaises(QueuingError):
            await self.service.dispatch_email(self.command)

    async def test_email_dispatch_failure_on_both(self):
        self.save_email_adapter.raise_exception = True
        self.queue_email_adapter.raise_exception = True
        with self.assertRaises(EmailSaveAndQueueError):
            await self.service.dispatch_email(self.command)
