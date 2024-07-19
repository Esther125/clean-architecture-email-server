import abc

from src.app.port.inward.queue_email.queue_email_command import QueueEmailCommand


class QueueEmailUseCase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def queue_email(self, command: QueueEmailCommand):
        raise NotImplementedError
