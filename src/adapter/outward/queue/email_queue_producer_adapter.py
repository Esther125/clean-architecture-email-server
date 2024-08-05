from src.app.port.outward.queue_email.queue_email_command import QueueEmailCommand
from src.app.port.outward.queue_email.queue_email_port import QueueEmailPort


class EmailQueueProducerAdapter(QueueEmailPort):
    def __init__(self) -> None:
        pass

    async def queue_email(self, command: QueueEmailCommand) -> None:
        pass
