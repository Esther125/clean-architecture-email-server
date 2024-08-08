from abc import ABC, abstractmethod

from src.app.port.outward.send_email.send_email_command import SendEmailCommand


class SendEmailPort(ABC):
    @abstractmethod
    async def send_email(self, command: SendEmailCommand) -> None:
        raise NotImplementedError
