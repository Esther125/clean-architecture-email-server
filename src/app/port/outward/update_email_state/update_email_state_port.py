from abc import ABC, abstractmethod

from src.app.port.outward.update_email_state.update_email_state_command import UpdateEmailStateCommand

class UpdateEmailStatePort(ABC):
    @abstractmethod
    async def update_state(self, command: UpdateEmailStateCommand):
        raise NotImplementedError