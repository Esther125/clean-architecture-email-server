import asyncio

from src.adapter.outward.queue.email_queue_publisher_adapter import (
    EmailQueuePublisherAdapter,
)
from src.app.port.outward.queue_email.queue_email_command import QueueEmailCommand


async def publish_message():
    try:
        adapter = EmailQueuePublisherAdapter()
        command = QueueEmailCommand(
            email_id="test-id",
            receivers=["test@gmail.com"],
            subject="Test Subject",
            content="Test Content",
        )
        await adapter.queue_email(command)
    except Exception as e:
        print(f"Failed: {e}")


if __name__ == "__main__":
    asyncio.run(publish_message())
