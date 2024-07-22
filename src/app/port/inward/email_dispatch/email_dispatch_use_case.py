from abc import ABC, abstractmethod

from src.app.port.inward.email_dispatch.email_dispatch_command import EmailDispatchCommand


class EmailDispatchUseCase(ABC):
    """
    Interface for the process of email dispatch,
    which includes queuing emails for sending and storing them in a database.
    """
    @abstractmethod
    def dispatch_email(self, command: EmailDispatchCommand):
        raise NotImplementedError
