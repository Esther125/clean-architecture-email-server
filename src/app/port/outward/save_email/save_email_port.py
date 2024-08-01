from abc import ABC, abstractmethod

from src.app.port.outward.save_email.save_email_command import SaveEmailCommand 

class SaveEmailPort(ABC):
    @abstractmethod
    async def save_email(self, command: SaveEmailCommand) -> None:
        raise NotImplementedError