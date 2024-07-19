
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
        sending_command = SendingEmailCommand(
            receivers = command.__receivers,
            subject = command.__subject,
            content = command.__content,
            attachments = command.__attachments
        )
        result = self.__sending_email_port.sending_email(sending_command)

        # Update is_sent attribute if sent successfully
        update_state_command = UpdateEmailStateCommand(
            email_id = command.__email_id,
            is_sent = True
        )
        
        if result:
            self.__update_email_state_port.update_state(update_state_command)
        else:
            raise EmailNotSendError
            

class EmailNotSendError(Exception):
    def __init__(self):
        self.message = f"Failed to send email."
        super().__init__(self.message)
