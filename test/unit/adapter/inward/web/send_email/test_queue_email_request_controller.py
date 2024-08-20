import base64
import json
from unittest import IsolatedAsyncioTestCase, mock

from fastapi.testclient import TestClient
from src.app.domain.service.send_and_update_email_state.send_and_update_email_state import (
    EmailStateNotUpdatedError,
    SendAndUpdateEmailStateService,
)
from src.app.port.outward.send_email.send_email_port import SendEmailPort
from src.app.port.outward.update_email_state.update_email_state_port import (
    UpdateEmailStatePort,
)
from src.main import app


class TestQueueEmailRequestEndpoint(IsolatedAsyncioTestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.mock_send_email_adapter = mock.Mock(spec=SendEmailPort)
        self.mock_update_email_state_adapter = mock.Mock(spec=UpdateEmailStatePort)
        self.mock_send_and_update_email_state_service = mock.Mock(
            spec=SendAndUpdateEmailStateService
        )

    async def test_send_and_update_email_state(self):
        with app.container.send_email_adapter.override(
            self.mock_send_email_adapter
        ), app.container.update_email_state_adapter.override(
            self.mock_update_email_state_adapter
        ), app.container.send_and_update_email_state_service.override(
            self.mock_send_and_update_email_state_service
        ):
            data = json.dumps(
                {
                    "email_id": "test-id",
                    "receivers": ["test@gmail.com"],
                    "subject": "Test Subject",
                    "content": "test content",
                }
            ).encode("utf-8")
            encoded_data = base64.b64encode(data).decode("utf-8")

            request_body = {
                "deliveryAttempt": 5,
                "message": {
                    "data": encoded_data,
                    "messageId": "test-message-id",
                    "message_id": "test-message-id",
                    "publishTime": "test-time",
                    "publish_time": "test-time",
                },
                "subscription": "projects/tw-rd-de-milecoolab-dev/subscriptions/email-server-incoming-sub",
            }

            response = self.client.post(
                "/v1/queue-email-request",
                headers={"Content-Type": "application/json"},
                json=request_body,
            )
            assert response.status_code == 200
            result = response.json()
            assert result["email_id"] is not None

    async def test_send_and_update_email_state_failed_on_parse_queue_request(self):
        with app.container.send_email_adapter.override(
            self.mock_send_email_adapter
        ), app.container.update_email_state_adapter.override(
            self.mock_update_email_state_adapter
        ), app.container.send_and_update_email_state_service.override(
            self.mock_send_and_update_email_state_service
        ):
            request_body = {
                "deliveryAttempt": 5,
                "message": {
                    # lack of data field
                    "messageId": "test-message-id",
                    "message_id": "test-message-id",
                    "publishTime": "test-time",
                    "publish_time": "test-time",
                },
                "subscription": "projects/tw-rd-de-milecoolab-dev/subscriptions/email-server-incoming-sub",
            }
            response = self.client.post(
                "/v1/queue-email-request",
                headers={"Content-Type": "application/json"},
                json=request_body,
            )
            assert response.status_code == 500
            result = response.json()
            assert "Failed to parse queue request" in result["detail"]

    async def test_send_and_update_email_state_failed_on_internal_server_error(self):
        self.mock_send_and_update_email_state_service.send_and_update_email_state.side_effect = EmailStateNotUpdatedError(
            update_error="Database connection failed", email_id="test-id"
        )
        with app.container.send_email_adapter.override(
            self.mock_send_email_adapter
        ), app.container.update_email_state_adapter.override(
            self.mock_update_email_state_adapter
        ), app.container.send_and_update_email_state_service.override(
            self.mock_send_and_update_email_state_service
        ):
            data = json.dumps(
                {
                    "email_id": "test-id",
                    "receivers": ["test@gmail.com"],
                    "subject": "Test Subject",
                    "content": "test content",
                }
            ).encode("utf-8")
            encoded_data = base64.b64encode(data).decode("utf-8")

            request_body = {
                "deliveryAttempt": 5,
                "message": {
                    "data": encoded_data,
                    "messageId": "test-message-id",
                    "message_id": "test-message-id",
                    "publishTime": "test-time",
                    "publish_time": "test-time",
                },
                "subscription": "projects/tw-rd-de-milecoolab-dev/subscriptions/email-server-incoming-sub",
            }

            response = self.client.post(
                "/v1/queue-email-request",
                headers={"Content-Type": "application/json"},
                json=request_body,
            )
            assert response.status_code == 500
            result = response.json()
            assert "Failed to send and update email state" in result["detail"]
