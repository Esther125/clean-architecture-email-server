import abc

from src.app.port.outward.queuing_email.queuing_email_command import QueuingEmailCommand


class QueuingEmailPort(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def queuing_email(self, command: QueuingEmailCommand):
        raise NotImplementedError