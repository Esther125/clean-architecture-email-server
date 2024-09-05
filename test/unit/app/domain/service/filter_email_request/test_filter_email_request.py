from typing import List
from datetime import datetime
from unittest import IsolatedAsyncioTestCase

from src.app.domain.entity.email import Email
from src.app.domain.service.filter_email_request.filter_email_request import (
    FailedToFilterEmail,
    FilterEmailRequestService,
)
from src.app.port.inward.filter_email_request.filter_email_request_command import (
    FilterEmailRequestCommand,
)
from src.app.port.outward.filter_email.filter_email_command import FilterEmailCommand
from src.app.port.outward.filter_email.filter_email_port import FilterEmailPort


class MockFilterEmailAdapter(FilterEmailPort):
    async def filter_email(self, command: FilterEmailCommand) -> List[Email]:
        result_emails = [
            Email(
                email_id="test-id",
                is_sent=False,
                request_time=datetime(2024, 12, 12),
                sent_time=datetime(2024, 12, 12),
                receivers=["test@gmail.com"],
                subject="Test Subject",
                content="test content",
            )
        ]
        return result_emails


class MockFilterEmailAdatperFailed(FilterEmailPort):
    async def filter_email(self, command: FilterEmailCommand) -> List[Email]:
        raise Exception()


class TestFilterEmailRequest(IsolatedAsyncioTestCase):
    def setUp(self):
        self.request_command = FilterEmailRequestCommand(
            email_id=None,
            request_time_start=None,
            request_time_end=None,
            sent_time_start=None,
            sent_time_end=None,
            is_sent=True,
            receivers=None,
            subject=None,
            content=None,
            attachments_keyword=None,
        )

    async def test_filter_email_request_success(self) -> None:
        mock_filter_email_adapter = MockFilterEmailAdapter()
        filter_email_request_service = FilterEmailRequestService(
            mock_filter_email_adapter
        )
        result_emails = await filter_email_request_service.filter_email_request(
            self.request_command
        )
        assert isinstance(result_emails, list)
        assert isinstance(result_emails[0], Email)

    async def test_filter_email_request_failed(self) -> None:
        mock_filter_email_adapter_failed = MockFilterEmailAdatperFailed()
        filter_email_request_service = FilterEmailRequestService(
            mock_filter_email_adapter_failed
        )
        with self.assertRaises(FailedToFilterEmail):
            await filter_email_request_service.filter_email_request(
                self.request_command
            )
