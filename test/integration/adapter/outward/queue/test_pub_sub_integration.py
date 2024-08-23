import os
import unittest
from google.cloud import pubsub_v1

from src.adapter.outward.queue.email_queue_publisher_adapter import (
    EmailQueuePublisherAdapter,
)
from src.app.port.outward.queue_email.queue_email_command import QueueEmailCommand


class TestPubSubIntegration(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        os.environ["PUBSUB_EMULATOR_HOST"] = "localhost:8085"
        self.adapter = EmailQueuePublisherAdapter()
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()
        self.topic_path = self.adapter.topic_path
        self.publisher.create_topic(request={"name": self.topic_path})
        self.subscription_path = self.subscriber.subscription_path(
            os.getenv("GCP_PROJECT_ID"), "test-subscription"
        )
        self.subscriber.create_subscription(
            request={"name": self.subscription_path, "topic": self.topic_path}
        )

    async def test_publish_message(self):
        command = QueueEmailCommand(
            email_id="test-id",
            receivers=["test@gmail.com"],
            subject="Test Subject",
            content="Test Content",
        )
        await self.adapter.queue_email(command)
        response = self.subscriber.pull(
            subscription=self.subscription_path, max_messages=1, timeout=10
        )
        messages = response.received_messages
        assert len(messages) == 1

    def tearDown(self):
        self.publisher.delete_topic(request={"topic": self.topic_path})
        self.subscriber.delete_subscription(
            request={"subscription": self.subscription_path}
        )
        os.environ.pop("PUBSUB_EMULATOR_HOST", None)
