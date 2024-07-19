from abc import ABC, abstractmethod

from src.app.port.inward.send_email.send_email_command import SendEmailCommand

class SendEmailUseCase(ABC):
    @abstractmethod
    def send_email(self, command: SendEmailCommand):
        raise NotImplementedError
