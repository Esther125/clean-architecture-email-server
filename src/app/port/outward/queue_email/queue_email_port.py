from abc import ABC, abstractmethod
from src.app.port.outward.queue_email.queue_email_command import QueueEmailCommand


class QueueEmailPort(ABC):
    @abstractmethod
    async def queue_email(self, command: QueueEmailCommand) -> None:
        raise NotImplementedError