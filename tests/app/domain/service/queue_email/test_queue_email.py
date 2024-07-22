import unittest
from unittest.mock import AsyncMock

from src.app.domain.service.queue_email.queue_email import QueueEmailService, EmailNotSavedError, EmailSaveAndQueueError, QueuingError
from src.app.port.outward.save_email.save_email_port import SaveEmailPort
from src.app.port.outward.queuing_email.queuing_email_port import QueuingEmailPort
from src.app.port.inward.queue_email.queue_email_command import QueueEmailCommand

class TestQueueEmailService(unittest.IsolatedAsyncioTestCase):

    async def test_queue_email_success(self):
        save_email_port = AsyncMock(spec=SaveEmailPort)
        queuing_email_port = AsyncMock(spec=QueuingEmailPort)

        service = QueueEmailService(save_email_port, queuing_email_port)

        command = QueueEmailCommand(
            email_id = "1",
            receivers = ["test@example.com"],
            subject = "Test Subject",
            content = "Test Content",
            attachments = None
        )

        save_email_port.save_email.return_value = None  
        queuing_email_port.queuing_email.return_value = None  

        await service.queue_email(command)

        save_email_port.save_email.assert_called_once()
        queuing_email_port.queuing_email.assert_called_once()

    async def test_queue_email_fail_to_save_email(self):
        save_email_port = AsyncMock(spec=SaveEmailPort)
        queuing_email_port = AsyncMock(spec=QueuingEmailPort)
        service = QueueEmailService(save_email_port, queuing_email_port)
        command = QueueEmailCommand(
            email_id="1",
            receivers=["test@example.com"],
            subject="Test Subject",
            content="Test Content",
            attachments=[]
        )

        save_email_port.save_email.side_effect = EmailNotSavedError(email_id="1")

        with self.assertRaises(EmailNotSavedError):
            await service.queue_email(command)

    async def test_queue_email_fail_to_queue_email(self):
        save_email_port = AsyncMock(spec=SaveEmailPort)
        queuing_email_port = AsyncMock(spec=QueuingEmailPort)
        service = QueueEmailService(save_email_port, queuing_email_port)
        command = QueueEmailCommand(
            email_id="1",
            receivers=["test@example.com"],
            subject="Test Subject",
            content="Test Content",
            attachments=[]
        )

        queuing_email_port.queuing_email.side_effect = QueuingError(email_id="1")
        
        with self.assertRaises(QueuingError):
            await service.queue_email(command)

    async def test_queue_email_both_failed(self):
        save_email_port = AsyncMock(spec=SaveEmailPort)
        queuing_email_port = AsyncMock(spec=QueuingEmailPort)
        service = QueueEmailService(save_email_port, queuing_email_port)
        command = QueueEmailCommand(
            email_id="1",
            receivers=["test@example.com"],
            subject="Test Subject",
            content="Test Content",
            attachments=[]
        )
        
        save_email_port.save_email.side_effect = EmailNotSavedError(email_id="1")
        queuing_email_port.queuing_email.side_effect = QueuingError(email_id="1")
        
        with self.assertRaises(EmailSaveAndQueueError):
            await service.queue_email(command)

if __name__ == '__main__':
    unittest.main()
