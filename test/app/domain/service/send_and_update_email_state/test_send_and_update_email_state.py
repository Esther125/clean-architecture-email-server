from unittest import IsolatedAsyncioTestCase

from src.app.domain.service.send_and_update_email_state.send_and_update_email_state import (
    SendAndUpdateEmailStateService,
    EmailNotSentError,
    EmailStateNotUpdatedError,
)
from src.app.port.inward.send_and_update_email_state.send_and_update_email_state_command import (
    SendAndUpdateEmailStateCommand,
)
from src.app.port.outward.send_email.send_email_command import SendEmailCommand
from src.app.port.outward.send_email.send_email_port import SendEmailPort
from src.app.port.outward.update_email_state.update_email_state_command import (
    UpdateEmailStateCommand,
)
from src.app.port.outward.update_email_state.update_email_state_port import (
    UpdateEmailStatePort,
)


class MockSendEmailAdapter(SendEmailPort):
    async def send_email(self, command: SendEmailCommand):
        pass


class MockUpdateEmailStateAdapter(UpdateEmailStatePort):
    async def update_state(self, command: UpdateEmailStateCommand):
        pass


class MockSendEmailAdapterWithError(SendEmailPort):
    async def send_email(self, command: SendEmailCommand):
        raise Exception()


class MockUpdateEmailStateAdapterWithError(UpdateEmailStatePort):
    async def update_state(self, command: UpdateEmailStateCommand):
        raise Exception()


class TestSendAndUpdateEmailStateService(IsolatedAsyncioTestCase):
    def setUp(self):
        self.command = SendAndUpdateEmailStateCommand(
            email_id="1",
            receivers=["test@example.com"],
            subject="Test Subject",
            content="Test Content",
            attachments=None,
        )

    async def test_send_and_update_email_state_success(self):
        send_email_adapter = MockSendEmailAdapter()
        update_email_state_adapter = MockUpdateEmailStateAdapter()
        service = SendAndUpdateEmailStateService(
            send_email_adapter, update_email_state_adapter
        )
        try:
            await service.send_and_update_email_state(self.command)
        except Exception as error:
            self.fail(f"Send and update email state failed with exception: {error}")

    async def test_send_and_update_email_state_failure_on_send(self):
        send_email_adapter_with_error = MockSendEmailAdapterWithError()
        update_email_state_adapter = MockUpdateEmailStateAdapter()
        service = SendAndUpdateEmailStateService(
            send_email_adapter_with_error, update_email_state_adapter
        )
        with self.assertRaises(EmailNotSentError):
            await service.send_and_update_email_state(self.command)

    async def test_send_and_update_email_state_failure_on_update(self):
        send_email_adapter = MockSendEmailAdapter()
        update_email_state_adapter_with_error = MockUpdateEmailStateAdapterWithError()
        service = SendAndUpdateEmailStateService(
            send_email_adapter, update_email_state_adapter_with_error
        )
        with self.assertRaises(EmailStateNotUpdatedError):
            await service.send_and_update_email_state(self.command)
