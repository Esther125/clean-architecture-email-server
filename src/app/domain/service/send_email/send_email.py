
from src.app.port.inward.send_email.send_email_command import SendEmailCommand
from src.app.port.inward.send_email.send_email_use_case import SendEmailUseCase
from src.app.port.outward.save_email.save_email_port import SaveEmailPort
from src.app.port.outward.sending_email.sending_email_port import SendingEmailPort
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
        # TODO: mapping
        result = self.__sending_email_port.sending_email()

        # update is_sent attribute if sent successfully
        if result:
            self.__update_email_state_port.update_state()
        else:
            raise EmailNotSendError
            

class EmailNotSendError(Exception):
    def __init__(self):
        self.message = f"Email failed to send."
        super().__init__(self.message)
