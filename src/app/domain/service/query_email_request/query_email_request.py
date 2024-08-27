from typing import List
from src.app.domain.entity.email import Email
from src.app.port.inward.query_email_request.query_email_request_command import (
    QueryEmailRequestCommand,
)
from src.app.port.inward.query_email_request.query_email_request_use_case import (
    QueryEmailRequestUseCase,
)
from src.app.port.outward.query_email.query_email_command import QueryEmailCommand
from src.app.port.outward.query_email.query_email_port import QueryEmailPort


class QueryEmailRequestService(QueryEmailRequestUseCase):
    def __init__(self, query_email_adapter: QueryEmailPort):
        self.__query_email_adapter = query_email_adapter

    async def query_email_request(
        self, request_command: QueryEmailRequestCommand
    ) -> List[Email]:
        try:
            command = QueryEmailCommand(
                email_id=request_command.email_id,
                receivers=request_command.receivers,
                subject=request_command.subject,
                content=request_command.content,
                attachments=request_command.attachments,
            )
            result_emails = await self.__query_email_adapter.query_email(command)
            return result_emails
        except Exception as error:
            raise FailedToQueryEmail(error)


class FailedToQueryEmail(Exception):
    def __init__(self, error):
        self.error = error
        self.message = f"Failed to query email. Error: {error}"
        super().__init__(self.message)
