from abc import ABC, abstractmethod

from src.app.port.outward.sending_email.sending_email_command import SendingEmailCommand


class SendingEmailPort(ABC):
    @abstractmethod
    def sending_email(self, command: SendingEmailCommand):
        raise NotImplementedError