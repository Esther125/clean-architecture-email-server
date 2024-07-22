
from src.app.port.inward.email_delivery.email_delivery_command import EmailDeliveryCommand
from src.app.port.inward.email_delivery.email_delivery_use_case import EmailDeliveryUseCase
from src.app.port.outward.send_email.send_email_command import SendEmailCommand
from src.app.port.outward.send_email.send_email_port import SendEmailPort
from src.app.port.outward.update_email_state.update_email_state_command import UpdateEmailStateCommand
from src.app.port.outward.update_email_state.update_email_state_port import UpdateEmailStatePort

class EmailDeliveryService(EmailDeliveryUseCase):
    def __init__(self,
        send_email_port: SendEmailPort,
        update_email_state_port: UpdateEmailStatePort
    ):
        self.__send_email_port = send_email_port
        self.__update_email_state_port = update_email_state_port

    def send_and_update_email_state(self, command: EmailDeliveryCommand):
        # Send email
        try:
            sending_command = SendEmailCommand(
                receivers = command.receivers,
                subject = command.subject,
                content = command.content,
                attachments = command.attachments
            )
            self.__send_email_port.send_email(sending_command)
        
        except EmailSendingError:
            raise

        # Update is_sent attribute if sent successfully
        try:
            update_state_command = UpdateEmailStateCommand(
                email_id = command.email_id,
                is_sent = True
            )
            self.__update_email_state_port.update_state(update_state_command)

        except UpdateEmailStateError:
            raise

class EmailSendingError(Exception):
    def __init__(self):
        self.message = f"Failed to send the email."
        super().__init__(self.message)


class UpdateEmailStateError(Exception):
    def __init__(self):
        self.message = f"Failed to update email state (is_sent = True)in the database."
        super().__init__(self.message)
