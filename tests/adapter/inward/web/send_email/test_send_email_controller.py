from fastapi.testclient import TestClient
from unittest import IsolatedAsyncioTestCase, mock
from src.adapter.outward.persistence.email_repository import EmailRepository
from src.adapter.outward.queue.email_queue_producer_adapter import (
    EmailQueueProducerAdapter,
)
from src.app.domain.service.queue_and_save_email.queue_and_save_email import (
    QueueAndSaveEmailService,
)
from src.app.domain.service.send_and_update_email_state.send_and_update_email_state import (
    SendAndUpdateEmailStateService,
)
from src.app.port.outward.send_email.send_email_port import SendEmailPort
from src.app.port.outward.update_email_state.update_email_state_port import (
    UpdateEmailStatePort,
)
from src.main import app


class TestSendEmailEndpoint(IsolatedAsyncioTestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.mock_save_email_adapter = mock.Mock(spec=EmailRepository)
        self.mock_queue_email_adapter = mock.Mock(spec=EmailQueueProducerAdapter)
        self.mock_queue_and_save_email_service = mock.Mock(
            spec=QueueAndSaveEmailService
        )

        self.mock_send_email_adapter = mock.Mock(spec=SendEmailPort)
        self.mock_update_email_state_adapter = mock.Mock(spec=UpdateEmailStatePort)
        self.mock_send_and_update_email_state_service = mock.Mock(
            spec=SendAndUpdateEmailStateService
        )

    async def test_queue_and_save_email(self):
        self.mock_queue_and_save_email_service.queue_and_save_email.return_value = True

        with app.container.save_email_adapter.override(
            self.mock_save_email_adapter
        ), app.container.queue_email_adapter.override(
            self.mock_queue_email_adapter
        ), app.container.queue_and_save_email_service.override(
            self.mock_queue_and_save_email_service
        ):
            response = self.client.post(
                "/v1/user/email",
                headers={"Content-Type": "application/json"},
                json={
                    "receivers": ["test@gmail.com"],
                    "subject": "Test Subject",
                    "content": "test content",
                },
            )
            assert response.status_code == 200
            result = response.json()
            assert result["email_id"], "email_id should not be null"

    async def test_queue_and_save_email_failed(self):
        self.mock_queue_and_save_email_service.queue_and_save_email.return_value = False

        with app.container.save_email_adapter.override(
            self.mock_save_email_adapter
        ), app.container.queue_email_adapter.override(
            self.mock_queue_email_adapter
        ), app.container.queue_and_save_email_service.override(
            self.mock_queue_and_save_email_service
        ):
            response = self.client.post(
                "/v1/user/email",
                headers={"Content-Type": "application/json"},
                json={
                    "receivers": ["test@gmail.com"],
                    "subject": "Test Subject",
                    # missing content field
                },
            )
            assert response.status_code == 422  # Unprocessable Entity Error

    async def test_send_and_update_email_state(self):
        self.mock_send_and_update_email_state_service.send_and_update_email_state.return_value = True

        with app.container.send_email_adapter.override(
            self.mock_send_email_adapter
        ), app.container.update_email_state_adapter.override(
            self.mock_update_email_state_adapter
        ), app.container.send_and_update_email_state_service.override(
            self.mock_send_and_update_email_state_service
        ):
            response = self.client.post(
                "/v1/queue/email",
                headers={"Content-Type": "application/json"},
                json={
                    "email_id": "test-id",
                    "receivers": ["test@gmail.com"],
                    "subject": "Test Subject",
                    "content": "test content",
                },
            )
            assert response.status_code == 200
            result = response.json()
            assert result["email_id"], "email_id should not be null"

    async def test_send_and_update_email_state_failed(self):
        self.mock_send_and_update_email_state_service.send_and_update_email_state.return_value = False

        with app.container.send_email_adapter.override(
            self.mock_send_email_adapter
        ), app.container.update_email_state_adapter.override(
            self.mock_update_email_state_adapter
        ), app.container.send_and_update_email_state_service.override(
            self.mock_send_and_update_email_state_service
        ):
            response = self.client.post(
                "/v1/queue/email",
                headers={"Content-Type": "application/json"},
                json={
                    "email_id": "test-id",
                    # missing receivers field
                    "subject": "Test Subject",
                    "content": "test content",
                },
            )
            assert response.status_code == 422
