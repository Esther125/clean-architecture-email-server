
from src.app.port.inward.send_email.send_email_command import SendEmailCommand
from src.app.port.inward.send_email.send_email_use_case import SendEmailUseCase
from src.app.port.outward.execute_send_email.execute_send_email_port import ExecuteSendEmailPort
from src.app.port.outward.save_email.save_email_port import SaveEmailPort
from src.app.port.outward.update_email_state.update_email_state_port import UpdateEmailStatePort

class SendEmailService(SendEmailUseCase):
    def __init__(self,
        save_email_port: SaveEmailPort,
        execute_send_email_port: ExecuteSendEmailPort,
        update_email_state_port: UpdateEmailStatePort
    ):
        self.__save_email_port = save_email_port
        self.__execute_send_email_port = execute_send_email_port
        self.__update_email_state_port = update_email_state_port

    def send_email(self, command: SendEmailCommand):
        self.__save_email_port.save_email(command)
        result = self.__execute_send_email_port.execute_send_email(command)

        if result:
            self.__update_email_state_port.update_state(command)
        else:
            raise EmailNotSendError
            

class EmailNotSendError(Exception):
    def __init__(self):
        self.message = f"Email failed to send."
        super().__init__(self.message)
