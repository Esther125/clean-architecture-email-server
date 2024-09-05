from unittest import IsolatedAsyncioTestCase

from src.app.domain.service.queue_and_save_email.queue_and_save_email import (
    QueueAndSaveEmailService,
    EmailNotQueuedError,
    EmailNotSavedError,
    EmailSaveAndQueueError,
)
from src.app.port.inward.queue_and_save_email.queue_and_save_email_command import (
    QueueAndSaveEmailCommand,
)
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


class TestQueueAndSaveEmailService(IsolatedAsyncioTestCase):
    def setUp(self):
        self.command = QueueAndSaveEmailCommand(
            email_id="1",
            receivers=["test@example.com"],
            subject="Test Subject",
            content="Test Content",
            attachments=None,
        )

    async def test_queue_and_save_email_success(self):
        save_email_adapter = MockSaveEmailAdapter()
        queue_email_adapter = MockQueueEmailAdapter()
        service = QueueAndSaveEmailService(save_email_adapter, queue_email_adapter)
        assert await service.queue_and_save_email(self.command) is None

    async def test_queue_and_save_email_failure_on_save(self):
        save_email_adapter_with_error = MockSaveEmailAdapterWithError()
        queue_email_adapter = MockQueueEmailAdapter()
        service = QueueAndSaveEmailService(
            save_email_adapter_with_error, queue_email_adapter
        )
        with self.assertRaises(EmailNotSavedError):
            await service.queue_and_save_email(self.command)

    async def test_queue_and_save_email_failure_on_queue(self):
        save_email_adapter = MockSaveEmailAdapter()
        queue_email_adapter_with_error = MockQueueEmailAdapterWithError()
        service = QueueAndSaveEmailService(
            save_email_adapter, queue_email_adapter_with_error
        )
        with self.assertRaises(EmailNotQueuedError):
            await service.queue_and_save_email(self.command)

    async def test_queue_and_save_email_failure_on_both(self):
        save_email_adapter_with_error = MockSaveEmailAdapterWithError()
        queue_email_adapter_with_error = MockQueueEmailAdapterWithError()
        service = QueueAndSaveEmailService(
            save_email_adapter_with_error, queue_email_adapter_with_error
        )
        with self.assertRaises(EmailSaveAndQueueError):
            await service.queue_and_save_email(self.command)
