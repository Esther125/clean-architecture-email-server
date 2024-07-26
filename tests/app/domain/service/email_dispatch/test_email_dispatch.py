from unittest import IsolatedAsyncioTestCase

from src.app.domain.service.email_dispatch.email_dispatch import EmailDispatchService, EmailNotSavedError, EmailSaveAndQueueError, QueuingError
from src.app.port.inward.email_dispatch.email_dispatch_command import EmailDispatchCommand
from src.app.port.outward.queue_email.queue_email_command import QueueEmailCommand
from src.app.port.outward.queue_email.queue_email_port import QueueEmailPort
from src.app.port.outward.save_email.save_email_command import SaveEmailCommand
from src.app.port.outward.save_email.save_email_port import SaveEmailPort


class MockSaveEmailAdapter(SaveEmailPort):
    async def save_email(self, command: SaveEmailCommand):
        pass


class MockQueueEmailAdapter(QueueEmailPort):
    async def queue_email(self, command: QueueEmailCommand):
        pass


class MockSaveEmailAdapterWithError(SaveEmailPort):
    async def save_email(self, command: SaveEmailCommand):
        raise Exception()


class MockQueueEmailAdapterWithError(QueueEmailPort):
    async def queue_email(self, command: QueueEmailCommand):
        raise Exception()
    

class TestEmailDispatchService(IsolatedAsyncioTestCase):
    def setUp(self):
        self.command = EmailDispatchCommand(
            email_id = "1",
            receivers = ["test@example.com"],
            subject = "Test Subject",
            content = "Test Content",
            attachments = None
        )

    async def test_email_dispatch_success(self):
        save_email_adapter = MockSaveEmailAdapter()
        queue_email_adapter = MockQueueEmailAdapter()
        service = EmailDispatchService(save_email_adapter, queue_email_adapter)
        success = await service.dispatch_email(self.command)
        self.assertTrue(success, "Email dispatch should succeed")

    async def test_email_dispatch_failure_on_save(self):
        save_email_adapter_with_error = MockSaveEmailAdapterWithError()
        queue_email_adapter = MockQueueEmailAdapter()
        service = EmailDispatchService(save_email_adapter_with_error, queue_email_adapter)
        with self.assertRaises(EmailNotSavedError):
            await service.dispatch_email(self.command)

    async def test_email_dispatch_failure_on_queue(self): 
        save_email_adapter = MockSaveEmailAdapter()
        queue_email_adapter_with_error = MockQueueEmailAdapterWithError()
        service = EmailDispatchService(save_email_adapter, queue_email_adapter_with_error)
        with self.assertRaises(QueuingError):
            await service.dispatch_email(self.command)

    async def test_email_dispatch_failure_on_both(self):
        save_email_adapter_with_error = MockSaveEmailAdapterWithError()
        queue_email_adapter_with_error = MockQueueEmailAdapterWithError()
        service = EmailDispatchService(save_email_adapter_with_error, queue_email_adapter_with_error)
        with self.assertRaises(EmailSaveAndQueueError):
            await service.dispatch_email(self.command)
