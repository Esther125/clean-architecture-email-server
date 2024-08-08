from src.app.port.inward.send_and_update_email_state.send_and_update_email_state_command import (
    SendAndUpdateEmailStateCommand,
)
from src.app.port.inward.send_and_update_email_state.send_and_update_email_state_use_case import (
    SendAndUpdateEmailStateUseCase,
)
from src.app.port.outward.send_email.send_email_command import SendEmailCommand
from src.app.port.outward.send_email.send_email_port import SendEmailPort
from src.app.port.outward.update_email_state.update_email_state_command import (
    UpdateEmailStateCommand,
)
from src.app.port.outward.update_email_state.update_email_state_port import (
    UpdateEmailStatePort,
)


class SendAndUpdateEmailStateService(SendAndUpdateEmailStateUseCase):
    def __init__(
        self,
        send_email_adapter: SendEmailPort,
        update_email_state_adapter: UpdateEmailStatePort,
    ):
        self.__send_email_adapter = send_email_adapter
        self.__update_email_state_adapter = update_email_state_adapter

    async def send_and_update_email_state(
        self, command: SendAndUpdateEmailStateCommand
    ) -> bool:
        try:
            success = False
            await self.send_email(command)
            await self.update_email_state(command)
            success = True
        except Exception:
            raise
        return success

    async def send_email(self, command: SendAndUpdateEmailStateCommand) -> None:
        try:
            send_command = SendEmailCommand(
                email_id=command.email_id,
                receivers=command.receivers,
                subject=command.subject,
                content=command.content,
                attachments=command.attachments,
            )
            await self.__send_email_adapter.send_email(send_command)
        except Exception as error:
            raise EmailNotSentError(command.email_id, error)

    async def update_email_state(self, command: SendAndUpdateEmailStateCommand) -> None:
        try:
            # Update `is_sent` attribute to True if sent successfully
            update_state_command = UpdateEmailStateCommand(
                email_id=command.email_id, is_sent=True
            )
            await self.__update_email_state_adapter.update_state(update_state_command)
        except Exception as error:
            raise EmailStateNotUpdatedError(command.email_id, error)


class EmailNotSentError(Exception):
    def __init__(self, email_id, send_error):
        self.email_id = email_id
        self.send_error = send_error
        self.message = (
            f"Email ID: {email_id} failed to be sent. Send Error: {send_error}"
        )
        super().__init__(self.message)


class EmailStateNotUpdatedError(Exception):
    def __init__(self, email_id, update_error):
        self.email_id = email_id
        self.update_error = update_error
        self.message = f"The state of Email ID: {email_id} failed to be updated. Update Error: {update_error}"
        super().__init__(self.message)
