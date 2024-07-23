from unittest import IsolatedAsyncioTestCase
from unittest.mock import Mock

from src.app.domain.service.email_delivery.email_delivery import EmailDeliveryService, EmailSendingError, UpdateEmailStateError
from src.app.port.inward.email_delivery.email_delivery_command import EmailDeliveryCommand
from src.app.port.outward.send_email.send_email_port import SendEmailPort
from src.app.port.outward.update_email_state.update_email_state_port import UpdateEmailStatePort

class TestEmailDeliveryService(IsolatedAsyncioTestCase):
    def setUp(self):
        self.send_email_port = Mock(spec=SendEmailPort)
        self.update_email_state_port = Mock(spec=UpdateEmailStatePort)
        self.service = EmailDeliveryService(self.send_email_port, self.update_email_state_port)
        self.command = EmailDeliveryCommand(
            email_id = "1",
            receivers = ["test@example.com"],
            subject = "Test Subject",
            content = "Test Content",
            attachments = None
        )

    async def test_email_delivery_success(self):
        self.send_email_port.send_email.return_value = None
        self.update_email_state_port.update_state.return_value = None

        await self.service.deliver_email(self.command)

        self.send_email_port.send_email.assert_called_once()
        self.update_email_state_port.update_state.assert_called_once()
    
    async def test_email_delivery_failure_on_send(self):
        self.send_email_port.send_email.side_effect = EmailSendingError(email_id="1")

        with self.assertRaises(EmailSendingError):
            await self.service.deliver_email(self.command)
        
        self.update_email_state_port.update_state.assert_not_called()

    async def test_email_delivery_failure_on_update(self):
        self.send_email_port.send_email.return_value = None 
        self.update_email_state_port.update_state.side_effect = UpdateEmailStateError(email_id="1")

        with self.assertRaises(UpdateEmailStateError):
            await self.service.deliver_email(self.command)
        
        self.send_email_port.send_email.assert_called_once()
