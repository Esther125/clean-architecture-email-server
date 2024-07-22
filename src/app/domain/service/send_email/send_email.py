
from src.app.port.inward.send_email.send_email_command import SendEmailCommand
from src.app.port.inward.send_email.send_email_use_case import SendEmailUseCase
from src.app.port.outward.sending_email.sending_email_command import SendingEmailCommand
from src.app.port.outward.sending_email.sending_email_port import SendingEmailPort
from src.app.port.outward.update_email_state.update_email_state_command import UpdateEmailStateCommand
from src.app.port.outward.update_email_state.update_email_state_port import UpdateEmailStatePort

class SendEmailService(SendEmailUseCase):
    def __init__(self,
        sending_email_port: SendingEmailPort,
        update_email_state_port: UpdateEmailStatePort
    ):
        self.__sending_email_port = sending_email_port
        self.__update_email_state_port = update_email_state_port

    def send_email(self, command: SendEmailCommand):
        # Send email
        try:
            sending_command = SendingEmailCommand(
                receivers = command.receivers,
                subject = command.subject,
                content = command.content,
                attachments = command.attachments
            )
            self.__sending_email_port.sending_email(sending_command)
        
        except EmailSendingError as error:
            raise

        # Update is_sent attribute if sent successfully
        try:
            update_state_command = UpdateEmailStateCommand(
                email_id = command.email_id,
                is_sent = True
            )
            self.__update_email_state_port.update_state(update_state_command)

        except UpdateEmailStateError as error:
            raise

class EmailSendingError(Exception):
    def __init__(self):
        self.message = f"Failed to send the email."
        super().__init__(self.message)


class UpdateEmailStateError(Exception):
    def __init__(self):
        self.message = f"Failed to update email state (is_sent = True)in the database."
        super().__init__(self.message)
