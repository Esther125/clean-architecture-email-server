from abc import ABC, abstractmethod

from src.app.port.inward.save_and_queue_email.save_and_queue_email_command import SaveAndQueueEmailCommand


class SaveAndQueueEmailUseCase(ABC):
    @abstractmethod
    def queue_email(self, command: SaveAndQueueEmailCommand):
        raise NotImplementedError
