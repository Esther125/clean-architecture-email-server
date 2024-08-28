from typing import List
from src.app.domain.entity.email import Email
from src.app.port.outward.filter_email.filter_email_command import FilterEmailCommand
from src.app.port.outward.filter_email.filter_email_port import FilterEmailPort


class FilterEmailAdapter(FilterEmailPort):
    async def filter_email(self, command: FilterEmailCommand) -> List[Email]:
        result_emails = [
            Email(
                email_id="test-id",
                receivers=["test@gmail.com"],
                subject="Test Subject",
                content="test content",
            )
        ]
        return result_emails
