
from src.app.domain.entity.email import Email
from src.app.port.inward.queue_email.queue_email_command import QueueEmailCommand
from src.app.port.inward.queue_email.queue_email_use_case import QueueEmailUseCase
from src.app.port.outward.queuing_email.queuing_email_port import QueuingEmailPort
from src.app.port.outward.save_email.save_email_port import SaveEmailPort


class QueueEmailService(QueueEmailUseCase):
    def __init__(self,
        save_email_port: SaveEmailPort,
        queuing_email_port: QueuingEmailPort
    ):
        self.__save_email_port = save_email_port
        self.__queuing_email_port = queuing_email_port
    
    def queue_email(self, command: QueueEmailCommand):
        # Save email to DB
        # TODO: mapping
        self.__save_email_port.save_email()
        # Queue eamil
        self.__queuing_email_port.queuing_email()