
from src.app.port.inward.email_delivery.email_delivery_command import EmailDeliveryCommand
from src.app.port.inward.email_delivery.email_delivery_use_case import EmailDeliveryUseCase
from src.app.port.outward.send_email.send_email_command import SendEmailCommand
from src.app.port.outward.send_email.send_email_port import SendEmailPort
from src.app.port.outward.update_email_state.update_email_state_command import UpdateEmailStateCommand
from src.app.port.outward.update_email_state.update_email_state_port import UpdateEmailStatePort

class EmailDeliveryService(EmailDeliveryUseCase):
    def __init__(self,
        send_email_adapter: SendEmailPort,
        update_email_state_adapter: UpdateEmailStatePort
    ):
        self.__send_email_adapter = send_email_adapter
        self.__update_email_state_adapter = update_email_state_adapter

    async def deliver_email(self, command: EmailDeliveryCommand):
        try:
            await self.send_email(command)
            await self.update_email_state(command)
            success = True  
        except Exception as err:
            print(f"Error delivering email with ID {command.email_id}: {err}")
            success = False  
        return success
        
    async def send_email(self, command: EmailDeliveryCommand):
        sending_command = SendEmailCommand(
            receivers = command.receivers,
            subject = command.subject,
            content = command.content,
            attachments = command.attachments
        )
        try:
            await self.__send_email_adapter.send_email(sending_command)
        
        except Exception as err:
            raise EmailSendingError(command.email_id) from err

    async def update_email_state(self, command: EmailDeliveryCommand):
        # Update `is_sent` attribute if sent successfully
        update_state_command = UpdateEmailStateCommand(
            email_id = command.email_id,
            is_sent = True
        )
        try:
            await self.__update_email_state_adapter.update_state(update_state_command)

        except Exception as err:
            raise UpdateEmailStateError(command.email_id) from err


class EmailSendingError(Exception):
    def __init__(self, email_id):
        self.email_id = email_id
        self.message = f"Failed to send the email with ID {email_id}."
        super().__init__(self.message)


class UpdateEmailStateError(Exception):
    def __init__(self, email_id):
        self.email_id = email_id
        self.message = f"Failed to update email state (is_sent = True) in the database with ID {email_id}."
        super().__init__(self.message)
