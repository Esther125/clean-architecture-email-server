from abc import ABC, abstractmethod

from src.app.port.inward.send_and_update_email_state.send_and_update_email_state_command import SendAndUpdateEmailStateCommand


class SendAndUpdateEmailStateUseCase(ABC):
    @abstractmethod
    def send_and_update_email_state(self, command: SendAndUpdateEmailStateCommand) -> bool:
        raise NotImplementedError
