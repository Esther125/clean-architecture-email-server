from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock

from src.adapter.outward.filter_email.query_builder import (
    FailedToBuildQuery,
    QueryBuilder,
)
from src.app.port.outward.filter_email.filter_email_command import FilterEmailCommand


class TestQueryBuilder(IsolatedAsyncioTestCase):
    def setUp(self):
        self.query_builder = QueryBuilder()
        self.command = FilterEmailCommand(
            email_id="test-id",
        )

    async def test_build_query_success(self) -> None:
        query, params = await self.query_builder.build_query(self.command)
        assert "email_id = @email_id" in query
        assert params["email_id"] == "test-id"

    async def test_build_query_failed(self) -> None:
        self.query_builder._QueryBuilder__format_params = AsyncMock(
            side_effect=Exception("Failed to bulid query.")
        )
        with self.assertRaises(FailedToBuildQuery):
            await self.query_builder.build_query(self.command)
