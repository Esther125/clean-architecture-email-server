from abc import ABC, abstractmethod

from src.app.port.inward.queue_and_save_email.queue_and_save_email_command import QueueAndSaveEmailCommand


class QueueAndSaveEmailUseCase(ABC):
    @abstractmethod
    def queue_and_save_email(self, command: QueueAndSaveEmailCommand) -> bool:
        raise NotImplementedError
