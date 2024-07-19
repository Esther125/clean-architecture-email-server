
from src.app.port.inward.queue_email.queue_email_command import QueueEmailCommand
from src.app.port.inward.queue_email.queue_email_use_case import QueueEmailUseCase
from src.app.port.outward.queuing_email.queuing_email_command import QueuingEmailCommand
from src.app.port.outward.queuing_email.queuing_email_port import QueuingEmailPort
from src.app.port.outward.save_email.save_email_command import SaveEmailCommand
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
        save_command = SaveEmailCommand(
            email_id = command.__email_id,
            receivers = command.__receivers,
            subject = command.__subject,
            content = command.__content,
            attachments = command.__attachments
        )
        self.__save_email_port.save_email(save_command)
        
        # Queue email
        queuing_command = QueuingEmailCommand(
            receivers = command.__receivers,
            subject = command.__subject,
            content = command.__content,
            attachments = command.__attachments
        )
        self.__queuing_email_port.queuing_email(queuing_command)