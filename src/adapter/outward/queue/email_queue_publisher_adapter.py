import json
import os
from dotenv import load_dotenv
from google.cloud import pubsub_v1

from src.app.port.outward.queue_email.queue_email_command import QueueEmailCommand
from src.app.port.outward.queue_email.queue_email_port import QueueEmailPort

load_dotenv()


class EmailQueuePublisherAdapter(QueueEmailPort):
    def __init__(self) -> None:
        self.project_id = os.getenv("GCP_PROJECT_ID")
        self.topic_id = os.getenv("GCP_PUB_SUB_TOPIC_ID")
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(self.project_id, self.topic_id)

    async def queue_email(self, command: QueueEmailCommand) -> None:
        try:
            email_message = {
                "email_id": command.email_id,
                "receivers": command.receivers,
                "subject": command.subject,
                "content": command.content,
                "attachments": command.attachments,
            }
            data = json.dumps(email_message).encode("utf-8")
            await self.publisher.publish(self.topic_path, data)
        except Exception:
            raise
