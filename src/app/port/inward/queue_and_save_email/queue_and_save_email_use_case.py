from abc import ABC, abstractmethod
from typing import Any, Awaitable

from src.app.port.inward.queue_and_save_email.queue_and_save_email_command import (
    QueueAndSaveEmailCommand,
)


class QueueAndSaveEmailUseCase(ABC):
    @abstractmethod
    def queue_and_save_email(self, command: QueueAndSaveEmailCommand) -> Awaitable[Any]:
        raise NotImplementedError
