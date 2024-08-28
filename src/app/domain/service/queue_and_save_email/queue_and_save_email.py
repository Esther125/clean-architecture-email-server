import asyncio
from src.app.port.inward.queue_and_save_email.queue_and_save_email_command import (
    QueueAndSaveEmailCommand,
)
from src.app.port.inward.queue_and_save_email.queue_and_save_email_use_case import (
    QueueAndSaveEmailUseCase,
)
from src.app.port.outward.queue_email.queue_email_command import QueueEmailCommand
from src.app.port.outward.queue_email.queue_email_port import QueueEmailPort
from src.app.port.outward.save_email.save_email_command import SaveEmailCommand
from src.app.port.outward.save_email.save_email_port import SaveEmailPort


class QueueAndSaveEmailService(QueueAndSaveEmailUseCase):
    def __init__(
        self, save_email_adapter: SaveEmailPort, queue_email_adapter: QueueEmailPort
    ):
        self.__save_email_adapter = save_email_adapter
        self.__queue_email_adapter = queue_email_adapter

    async def queue_and_save_email(self, command: QueueAndSaveEmailCommand) -> None:
        db_error, queue_error = await asyncio.gather(
            self.save_email(command), self.queue_email(command), return_exceptions=True
        )
        if db_error and queue_error:
            raise EmailSaveAndQueueError(command.email_id, db_error, queue_error)
        elif db_error:
            raise db_error
        elif queue_error:
            raise queue_error
        else:
            return

    async def save_email(self, command: QueueAndSaveEmailCommand) -> None:
        try:
            save_command = SaveEmailCommand(
                email_id=command.email_id,
                request_time=command.request_time,
                receivers=command.receivers,
                subject=command.subject,
                content=command.content,
                attachments=command.attachments,
            )
            await self.__save_email_adapter.save_email(save_command)
        except Exception as error:
            raise EmailNotSavedError(command.email_id, error)

    async def queue_email(self, command: QueueAndSaveEmailCommand) -> None:
        try:
            queue_command = QueueEmailCommand(
                email_id=command.email_id,
                receivers=command.receivers,
                subject=command.subject,
                content=command.content,
                attachments=command.attachments,
            )
            await self.__queue_email_adapter.queue_email(queue_command)
        except Exception as error:
            raise EmailNotQueuedError(command.email_id, error)


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
        self.message = (
            f"Email ID: {email_id} failed to be queued. Queue Error: {queue_error}"
        )
        super().__init__(self.message)


class EmailSaveAndQueueError(Exception):
    def __init__(self, email_id, db_error, queue_error):
        self.email_id = email_id
        self.db_error = db_error
        self.queue_error = queue_error
        self.message = f"Email ID: {email_id} failed to be saved and queued. DB Error: {db_error}, Queue Error: {queue_error}"
        super().__init__(self.message)
