from typing import List
from src.app.domain.entity.email import Email
from src.app.port.inward.filter_email_request.filter_email_request_command import (
    FilterEmailRequestCommand,
)
from src.app.port.inward.filter_email_request.filter_email_request_use_case import (
    FilterEmailRequestUseCase,
)
from src.app.port.outward.filter_email.filter_email_command import FilterEmailCommand
from src.app.port.outward.filter_email.filter_email_port import FilterEmailPort


class FilterEmailRequestService(FilterEmailRequestUseCase):
    def __init__(self, filter_email_adapter: FilterEmailPort):
        self.__filter_email_adapter = filter_email_adapter

    async def filter_email_request(
        self, request_command: FilterEmailRequestCommand
    ) -> List[Email]:
        try:
            command = FilterEmailCommand(
                email_id=request_command.email_id,
                request_time_start=request_command.request_time_start,
                request_time_end=request_command.request_time_end,
                sent_time_start=request_command.sent_time_start,
                sent_time_end=request_command.sent_time_end,
                is_sent=request_command.is_sent,
                receivers=request_command.receivers,
                subject=request_command.subject,
                content=request_command.content,
                attachments_blobname=request_command.attachments_blobname,
            )
            result_emails = await self.__filter_email_adapter.filter_email(command)
            return result_emails
        except Exception as error:
            raise FailedToFilterEmail(error)


class FailedToFilterEmail(Exception):
    def __init__(self, error):
        self.error = error
        self.message = f"Failed to filter email. Error: {error}"
        super().__init__(self.message)
