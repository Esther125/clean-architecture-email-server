
import asyncio
from src.app.port.inward.save_and_queue_email.save_and_queue_email_command import SaveAndQueueEmailCommand
from src.app.port.inward.save_and_queue_email.save_and_queue_email_use_case import SaveAndQueueEmailUseCase
from src.app.port.outward.queuing_email.queuing_email_command import QueuingEmailCommand
from src.app.port.outward.queuing_email.queuing_email_port import QueuingEmailPort
from src.app.port.outward.save_email.save_email_command import SaveEmailCommand
from src.app.port.outward.save_email.save_email_port import SaveEmailPort


class SaveAndQueueEmailService(SaveAndQueueEmailUseCase):
    def __init__(self,
        save_email_port: SaveEmailPort,
        queuing_email_port: QueuingEmailPort
    ):
        self.__save_email_port = save_email_port
        self.__queuing_email_port = queuing_email_port
    
    async def save_and_queue_email(self, command: SaveAndQueueEmailCommand):
        # Asynchronously save to DB and enqueue the email
        results = await asyncio.gather(
            self.save_email,
            self.queue_email,
            return_exceptions = True
        )

        db_error = None
        queue_error = None

        for result in results:
            if isinstance(result, EmailNotSavedError):
                db_error = result
            elif isinstance(result, QueuingError):
                queue_error = result

        if db_error and queue_error:
            raise EmailSaveAndQueueError(command.email_id)
        elif db_error:
            raise EmailNotSavedError(command.email_id)
        elif queue_error:
            raise QueuingError(command.email_id)

    async def save_email(self,command: QueueEmailCommand):
        try:
            save_command = SaveEmailCommand(
                email_id = command.email_id,
                receivers = command.receivers,
                subject = command.subject,
                content = command.content,
                attachments = command.attachments
            )
            self.__save_email_port.save_email(save_command)
        
        except EmailNotSavedError:
            raise

    async def queue_email(self,command: QueueEmailCommand):
        try:
            queuing_command = QueuingEmailCommand(
                receivers = command.receivers,
                subject = command.subject,
                content = command.content,
                attachments = command.attachments
            )
            self.__queuing_email_port.queuing_email(queuing_command),

        except QueuingError:
            raise


class EmailNotSavedError(Exception):
    def __init__(self, email_id):
        self.email_id = email_id
        self.message = f"Email ID: {email_id} failed to save to the database."
        super().__init__(self.message)


class QueuingError(Exception):
    def __init__(self, email_id):
        self.email_id = email_id
        self.message = f"Email ID: {email_id} failed to send to the queue."
        super().__init__(self.message)


class EmailSaveAndQueueError(Exception):
    def __init__(self, email_id):
        self.email_id = email_id
        self.message = f"Email ID: {email_id} failed to save to the database and send to the queue."
        super().__init__(self.message)