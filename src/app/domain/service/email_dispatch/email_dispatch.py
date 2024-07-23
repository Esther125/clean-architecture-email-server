
import asyncio
from src.app.port.inward.email_dispatch.email_dispatch_command import EmailDispatchCommand
from src.app.port.inward.email_dispatch.email_dispatch_use_case import EmailDispatchUseCase
from src.app.port.outward.queue_email.queue_email_command import QueueEmailCommand
from src.app.port.outward.queue_email.queue_email_port import QueueEmailPort
from src.app.port.outward.save_email.save_email_command import SaveEmailCommand
from src.app.port.outward.save_email.save_email_port import SaveEmailPort


class EmailDispatchService(EmailDispatchUseCase):
    def __init__(self,
        save_email_port: SaveEmailPort,
        queue_email_port: QueueEmailPort
    ):
        self.__save_email_port = save_email_port
        self.__queue_email_port = queue_email_port
    
    async def dispatch_email(self, command: EmailDispatchCommand):
        # Asynchronously save the email to DB and enqueue the email
        results = await asyncio.gather(
            self.save_email(command),
            self.queue_email(command),
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
            raise EmailSaveAndQueueError(command.email_id, db_error, queue_error)
        elif db_error:
            raise db_error  
        elif queue_error:
            raise queue_error  
        
    async def save_email(self,command: EmailDispatchCommand):
        try:
            save_command = SaveEmailCommand(
                email_id = command.email_id,
                receivers = command.receivers,
                subject = command.subject,
                content = command.content,
                attachments = command.attachments
            )
            await self.__save_email_port.save_email(save_command)
        
        except Exception as err:
            raise EmailNotSavedError(command.email_id) from err

    async def queue_email(self,command: EmailDispatchCommand):
        try:
            queue_command = QueueEmailCommand(
                receivers = command.receivers,
                subject = command.subject,
                content = command.content,
                attachments = command.attachments
            )
            await self.__queue_email_port.queue_email(queue_command)

        except Exception as err:
            raise QueuingError(command.email_id) from err


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
    def __init__(self, email_id, db_error, queue_error):
        self.email_id = email_id
        self.db_error = db_error
        self.queue_error = queue_error
        self.message = f"Email ID: {email_id} failed to save to the database and send to the queue. DB Error: {db_error}, Queue Error: {queue_error}"
        super().__init__(self.message)