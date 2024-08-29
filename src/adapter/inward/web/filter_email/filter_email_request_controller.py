from fastapi import APIRouter, HTTPException, Depends
from dependency_injector.wiring import inject, Provide

from src.adapter.inward.web.filter_email.filter_email_schema import (
    FilterEmailRequestWebInterface,
    FilterEmailResponse,
)
from src.app.port.inward.filter_email_request.filter_email_request_command import (
    FilterEmailRequestCommand,
)
from src.app.port.inward.filter_email_request.filter_email_request_use_case import (
    FilterEmailRequestUseCase,
)
from src.container import Container


router = APIRouter(prefix="/v1")


@router.post(
    "/filter-email-request", status_code=200, summary="For users to filter emails."
)
@inject
async def handle_filter_email_request(
    filter_email_request: FilterEmailRequestWebInterface,
    filter_email_request_service: FilterEmailRequestUseCase = Depends(
        Provide[Container.filter_email_request_service]
    ),
):
    try:
        filter_email_request_command = FilterEmailRequestCommand(
            email_id=filter_email_request.email_id,
            request_time_start=filter_email_request.request_time_start,
            request_time_end=filter_email_request.request_time_end,
            sent_time_start=filter_email_request.sent_time_start,
            sent_time_end=filter_email_request.sent_time_end,
            is_sent=filter_email_request.is_sent,
            receivers=filter_email_request.receivers,
            subject=filter_email_request.subject,
            content=filter_email_request.content,
            attachments_blobname=filter_email_request.attachments_blobname,
        )
        result_emails = await filter_email_request_service.filter_email_request(
            filter_email_request_command
        )
        return FilterEmailResponse(
            message="Successfully filter emails.", result_emails=result_emails
        )
    except Exception as error:
        raise HTTPException(
            status_code=500, detail=f"Failed to filter emails. Error: {error}"
        )
