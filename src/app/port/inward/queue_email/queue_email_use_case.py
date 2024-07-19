from abc import ABC, abstractmethod

from src.app.port.inward.queue_email.queue_email_command import QueueEmailCommand


class QueueEmailUseCase(ABC):
    @abstractmethod
    def queue_email(self, command: QueueEmailCommand):
        raise NotImplementedError
