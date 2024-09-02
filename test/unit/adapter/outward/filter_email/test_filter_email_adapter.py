from datetime import datetime
from unittest import IsolatedAsyncioTestCase, mock

from src.adapter.outward.filter_email.filter_email_adapter import (
    FailedToFilterEmailError,
    FilterEmailAdapter,
)
from src.adapter.outward.filter_email.query_builder import QueryBuilder
from src.app.port.outward.filter_email.filter_email_command import FilterEmailCommand


class TestFilterEmailAdapter(IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_query_builder = mock.Mock(spec=QueryBuilder)
        self.filter_email_adapter = FilterEmailAdapter()
        self.filter_email_adapter.query_builder = self.mock_query_builder
        self.command = FilterEmailCommand(
            request_time_start=datetime(2002, 12, 5),
            request_time_end=datetime(2003, 8, 8),
        )

    async def test_filter_email_failed(self):
        self.filter_email_adapter.query_builder.build_query.side_effect = Exception(
            "Failed to filter email."
        )
        with self.assertRaises(FailedToFilterEmailError):
            await self.filter_email_adapter.filter_email(self.command)
