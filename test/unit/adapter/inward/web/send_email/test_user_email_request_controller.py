from fastapi.testclient import TestClient
from unittest import IsolatedAsyncioTestCase, mock
from src.adapter.outward.persistence.email_repository import EmailRepository
from src.adapter.outward.queue.email_queue_publisher_adapter import (
    EmailQueuePublisherAdapter,
)
from src.app.domain.service.queue_and_save_email.queue_and_save_email import (
    EmailNotQueuedError,
    QueueAndSaveEmailService,
)
from src.main import app


class TestUserEmailRequestEndpoint(IsolatedAsyncioTestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.mock_save_email_adapter = mock.Mock(spec=EmailRepository)
        self.mock_queue_email_adapter = mock.Mock(spec=EmailQueuePublisherAdapter)
        self.mock_queue_and_save_email_service = mock.Mock(
            spec=QueueAndSaveEmailService
        )

    async def test_queue_and_save_email(self):
        with app.container.save_email_adapter.override(
            self.mock_save_email_adapter
        ), app.container.queue_email_adapter.override(
            self.mock_queue_email_adapter
        ), app.container.queue_and_save_email_service.override(
            self.mock_queue_and_save_email_service
        ):
            response = self.client.post(
                "/v1/user-email-request",
                headers={"Content-Type": "application/json"},
                json={
                    "receivers": ["test@gmail.com"],
                    "subject": "Test Subject",
                    "content": "test content",
                },
            )
            assert response.status_code == 200
            result = response.json()
            assert result["email_id"] is not None

    async def test_queue_and_save_email_failed_on_invalid_request_data(self):
        with app.container.save_email_adapter.override(
            self.mock_save_email_adapter
        ), app.container.queue_email_adapter.override(
            self.mock_queue_email_adapter
        ), app.container.queue_and_save_email_service.override(
            self.mock_queue_and_save_email_service
        ):
            response = self.client.post(
                "/v1/user-email-request",
                headers={"Content-Type": "application/json"},
                json={
                    "receivers": ["test@gmail.com"],
                    "subject": "Test Subject",
                    # missing content field
                },
            )
            assert response.status_code == 422

    async def test_queue_and_save_email_failed_on_internal_server_error(self):
        self.mock_queue_and_save_email_service.queue_and_save_email.side_effect = (
            EmailNotQueuedError(
                queue_error="Queue connection failed", email_id="test-id"
            )
        )
        with app.container.save_email_adapter.override(
            self.mock_save_email_adapter
        ), app.container.queue_email_adapter.override(
            self.mock_queue_email_adapter
        ), app.container.queue_and_save_email_service.override(
            self.mock_queue_and_save_email_service
        ):
            response = self.client.post(
                "/v1/user-email-request",
                headers={"Content-Type": "application/json"},
                json={
                    "email_id": "test-id",
                    "receivers": ["test@gmail.com"],
                    "subject": "Test Subject",
                    "content": "test content",
                },
            )
            assert response.status_code == 500
            result = response.json()
            assert "Failed to queue and save email" in result["detail"]
