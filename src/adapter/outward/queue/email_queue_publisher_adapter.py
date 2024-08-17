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

    def generate_email_message(self, command: QueueEmailCommand) -> bytes:
        try:
            email = {
                "email_id": command.email_id,
                "receivers": command.receivers,
                "subject": command.subject,
                "content": command.content,
                "attachments": command.attachments,
            }
            email_message = json.dumps(email).encode("utf-8")
            return email_message
        except Exception:
            raise

    async def queue_email(self, command: QueueEmailCommand) -> None:
        try:
            email_message = self.generate_email_message(command)
            future = self.publisher.publish(self.topic_path, email_message)
            message_id = future.result()
            print(
                f"Successfully published the email message (ID: {message_id}) to pub/sub."
            )
        except Exception as error:
            raise FailedToPublishedEmailToQueueError(command.email_id, error)


class FailedToPublishedEmailToQueueError(Exception):
    def __init__(self, email_id, error) -> None:
        self.email_id = email_id
        self.error = error
        self.message = f"Failed to publish the email message (ID: {email_id}) to pub/sub. Error: {error}"
        super().__init__(self.message)


# Test block
# import asyncio

# async def publish_message():
#     try:
#         adapter = EmailQueuePublisherAdapter()
#         command = QueueEmailCommand(
#             email_id="test-id",
#             receivers=["test@gmail.com"],
#             subject="Test Subject",
#             content="Test Content"
#         )
#         await adapter.queue_email(command)
#     except Exception as e:
#         print(f"Failed: {e}")

# if __name__ == "__main__":
#     asyncio.run(publish_message())
