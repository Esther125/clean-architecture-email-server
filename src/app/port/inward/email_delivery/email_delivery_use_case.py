from abc import ABC, abstractmethod

from src.app.port.inward.email_delivery.email_delivery_command import EmailDeliveryCommand


class EmailDeliveryUseCase(ABC):
    """
    Interface for the process of email delivery,
    which includes sending the email and updating the database to mark the 'is_sent' field as true.
    """
    @abstractmethod
    def deliver_email(self, command: EmailDeliveryCommand):
        raise NotImplementedError
