import abc

from src.app.port.inward.send_email.send_email_command import SendEmailCommand

class SendEmailUseCase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def send_email(self, command: SendEmailCommand):
        raise NotImplementedError
