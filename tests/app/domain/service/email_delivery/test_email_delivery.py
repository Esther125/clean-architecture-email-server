from unittest import IsolatedAsyncioTestCase
from unittest.mock import Mock

from src.app.domain.service.email_delivery.email_delivery import EmailDeliveryService, EmailSendingError, UpdateEmailStateError
from src.app.port.inward.email_delivery.email_delivery_command import EmailDeliveryCommand
from src.app.port.outward.send_email.send_email_command import SendEmailCommand
from src.app.port.outward.send_email.send_email_port import SendEmailPort
from src.app.port.outward.update_email_state.update_email_state_command import UpdateEmailStateCommand
from src.app.port.outward.update_email_state.update_email_state_port import UpdateEmailStatePort


class SendEmailAdapter(SendEmailPort):
    async def send_email(self, command: SendEmailCommand):
        pass


class UpdateEmailStateAdapter(UpdateEmailStatePort):
    async def update_state(self, command: UpdateEmailStateCommand):
        pass


class SendEmailAdapterWithError(SendEmailPort):
    async def send_email(self, command: SendEmailCommand):
        raise Exception()
    

class UpdateEmailStateAdapterWithError(UpdateEmailStatePort):
    async def update_state(self, command: UpdateEmailStateCommand):
        raise Exception()


class TestEmailDeliveryService(IsolatedAsyncioTestCase):
    def setUp(self):
        self.command = EmailDeliveryCommand(
            email_id = "1",
            receivers = ["test@example.com"],
            subject = "Test Subject",
            content = "Test Content",
            attachments = None
        )

    async def test_email_delivery_success(self):
        send_email_adapter = SendEmailAdapter()
        update_email_state_adapter = UpdateEmailStateAdapter()
        service = EmailDeliveryService(send_email_adapter, update_email_state_adapter)
        success = await service.deliver_email(self.command)
        self.assertTrue(success, "Email delivery should succeed")

    async def test_email_delivery_failure_on_send(self):
        send_email_adapter_with_error = SendEmailAdapterWithError()
        update_email_state_adapter = UpdateEmailStateAdapter()
        service = EmailDeliveryService(send_email_adapter_with_error, update_email_state_adapter)
        with self.assertRaises(EmailSendingError):
            await service.deliver_email(self.command)
        
    async def test_email_delivery_failure_on_update(self):
        send_email_adapter = SendEmailAdapter()
        update_email_state_adapter_with_error = UpdateEmailStateAdapterWithError()
        service = EmailDeliveryService(send_email_adapter, update_email_state_adapter_with_error)
        with self.assertRaises(UpdateEmailStateError):
            await service.deliver_email(self.command)
    