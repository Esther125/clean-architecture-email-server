from fastapi.testclient import TestClient
from unittest import IsolatedAsyncioTestCase, mock
from src.adapter.outward.filter_email.filter_email_adpter import FilterEmailAdapter
from src.app.domain.service.filter_email_request.filter_email_request import (
    FailedToFilterEmail,
    FilterEmailRequestService,
)
from src.main import app


class TestFilterEmailRequestEndpoint(IsolatedAsyncioTestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.mock_filter_email_adapter = mock.Mock(spec=FilterEmailAdapter)
        self.mock_filter_email_request_service = mock.Mock(
            spec=FilterEmailRequestService
        )

    async def test_filter_email(self):
        with app.container.filter_email_adapter.override(
            self.mock_filter_email_adapter
        ), app.container.filter_email_request_service.override(
            self.mock_filter_email_request_service
        ):
            response = self.client.get("/v1/email?request_time_start=2023-09-15")
            assert response.status_code == 200
            result = response.json()
            assert "Successfully filter emails" in result["message"]

    async def test_filter_email_failed(self):
        self.mock_filter_email_request_service.filter_email_request.side_effect = (
            FailedToFilterEmail(error="Failed to filter emails.")
        )
        with app.container.filter_email_adapter.override(
            self.mock_filter_email_adapter
        ), app.container.filter_email_request_service.override(
            self.mock_filter_email_request_service
        ):
            response = self.client.get("/v1/email?is_sent=True")
            assert response.status_code == 500
            exception = response.json()
            assert "Failed to filter emails" in exception["detail"]
