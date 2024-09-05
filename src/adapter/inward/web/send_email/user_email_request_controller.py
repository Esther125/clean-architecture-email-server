import logging
import uuid
from fastapi import APIRouter, HTTPException, Depends
from dependency_injector.wiring import inject, Provide

from src.adapter.inward.web.send_email.send_email_schema import (
    SendEmailResponse,
    UserRequestWebInterface,
)
from src.app.domain.entity.email import Attachment
from src.app.port.inward.queue_and_save_email.queue_and_save_email_command import (
    QueueAndSaveEmailCommand,
)
from src.app.port.inward.queue_and_save_email.queue_and_save_email_use_case import (
    QueueAndSaveEmailUseCase,
)
from src.container import Container


logger = logging.getLogger(__name__)


router = APIRouter(prefix="/v1")


@router.post(
    "/user-email-request", status_code=200, summary="For users to send emails."
)
@inject
async def handle_queue_and_save_email_request(
    user_request: UserRequestWebInterface,
    queue_and_save_email_service: QueueAndSaveEmailUseCase = Depends(
        Provide[Container.queue_and_save_email_service]
    ),
):
    try:
        email_id = str(uuid.uuid4())
        attachments = []
        if user_request.attachments is not None:
            attachments = [
                Attachment(
                    filename=attach.filename,
                    filetype=attach.filetype,
                    blobname=attach.blobname,
                )
                for attach in user_request.attachments
            ]

        queue_and_save_email_command = QueueAndSaveEmailCommand(
            email_id=email_id,
            receivers=user_request.receivers,
            subject=user_request.subject,
            content=user_request.content,
            attachments=attachments,
        )
        await queue_and_save_email_service.queue_and_save_email(
            queue_and_save_email_command
        )

        return SendEmailResponse(
            message="Successfully queue and save email.", email_id=email_id
        )
    except Exception as error:
        logger.error(f"Failed to queue and save email. Error: {error}")
        raise HTTPException(
            status_code=500, detail=f"Failed to queue and save email. Error: {error}"
        )
