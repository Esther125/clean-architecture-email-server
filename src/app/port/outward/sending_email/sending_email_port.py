import abc

from src.app.port.outward.sending_email.sending_email_command import SendingEmailCommand


class SendingEmailPort(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def sending_email(self, command: SendingEmailCommand):
        raise NotImplementedError