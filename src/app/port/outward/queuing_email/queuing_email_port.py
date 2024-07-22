from abc import ABC, abstractmethod
from src.app.port.outward.queuing_email.queuing_email_command import QueuingEmailCommand


class QueuingEmailPort(ABC):
    @abstractmethod
    async def queuing_email(self, command: QueuingEmailCommand):
        raise NotImplementedError