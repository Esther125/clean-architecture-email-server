
import asyncio
from src.app.port.inward.queue_and_save_email.queue_and_save_email_command import QueueAndSaveEmailCommand
from src.app.port.inward.queue_and_save_email.queue_and_save_email_use_case import QueueAndSaveEmailUseCase
from src.app.port.outward.queue_email.queue_email_command import QueueEmailCommand
from src.app.port.outward.queue_email.queue_email_port import QueueEmailPort
from src.app.port.outward.save_email.save_email_command import SaveEmailCommand
from src.app.port.outward.save_email.save_email_port import SaveEmailPort


class QueueAndSaveEmailService(QueueAndSaveEmailUseCase):
    def __init__(self,
        save_email_adapter: SaveEmailPort,
        queue_email_adapter: QueueEmailPort
    ):
        self.__save_email_adapter = save_email_adapter
        self.__queue_email_adapter = queue_email_adapter
    
    async def queue_and_save_email(self, command: QueueAndSaveEmailCommand) -> bool:
        success = False
        results = await asyncio.gather(
            self.save_email(command),
            self.queue_email(command),
            return_exceptions = True
        )

        if results == [True, True]:
            success = True
        elif results[0] == True: # save email success but queue email failed
            raise results[1]
        elif results[1] == True: # queue email success but save email failed
            raise results[0]
        else:
            raise EmailSaveAndQueueError(command.email_id, results[0], results[1])
        return success

    async def save_email(self,command: QueueAndSaveEmailCommand) -> bool:
        try:
            save_command = SaveEmailCommand(
                email_id = command.email_id,
                receivers = command.receivers,
                subject = command.subject,
                content = command.content,
                attachments = command.attachments
            )
            result = await self.__save_email_adapter.save_email(save_command)
            return result 
        except Exception as err:
            raise EmailNotSavedError(command.email_id, err)
        
    async def queue_email(self,command: QueueAndSaveEmailCommand) -> bool:
        try:
            queue_command = QueueEmailCommand(
                email_id = command.email_id,
                receivers = command.receivers,
                subject = command.subject,
                content = command.content,
                attachments = command.attachments
            )
            result = await self.__queue_email_adapter.queue_email(queue_command)
            return result
        except Exception as err:
            raise EmailNotQueuedError(command.email_id, err)


class EmailNotSavedError(Exception):
    def __init__(self, email_id, db_error):
        self.email_id = email_id
        self.db_error = db_error
        self.message = f"Email ID: {email_id} failed to be saved. DB Error: {db_error}"
        super().__init__(self.message)

 
class EmailNotQueuedError(Exception):
    def __init__(self, email_id, queue_error):
        self.email_id = email_id
        self.queue_error = queue_error
        self.message = f"Email ID: {email_id} failed to be queued. Queue Error: {queue_error}"
        super().__init__(self.message)


class EmailSaveAndQueueError(Exception):
    def __init__(self, email_id, db_error, queue_error):
        self.email_id = email_id
        self.db_error = db_error
        self.queue_error = queue_error
        self.message = f"Email ID: {email_id} failed to be saved and queued. DB Error: {db_error}, Queue Error: {queue_error}"
        super().__init__(self.message)