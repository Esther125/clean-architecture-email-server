import uuid
from fastapi import APIRouter, HTTPException, Depends
from dependency_injector.wiring import inject, Provide

from src.adapter.inward.web.send_email.send_email_schema import (
    QueueRequestWebInterface,
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
from src.app.port.inward.send_and_update_email_state.send_and_update_email_state_command import (
    SendAndUpdateEmailStateCommand,
)
from src.app.port.inward.send_and_update_email_state.send_and_update_email_state_use_case import (
    SendAndUpdateEmailStateUseCase,
)
from src.container import Container


router = APIRouter(prefix="/v1")


@router.post("/user/email", status_code=200, summary="For users to send emails.")
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
        success = await queue_and_save_email_service.queue_and_save_email(
            queue_and_save_email_command
        )

        if success is True:
            return SendEmailResponse(
                message="Successfully queue and save email.", email_id=email_id
            )
    except Exception as error:
        raise HTTPException(
            status_code=500, detail=f"Failed to queue and save email. Error: {error}"
        )


@router.post("/queue/email", status_code=200, summary="For queue to dequeue emails.")
@inject
async def handle_send_and_update_email_state_request(
    queue_request: QueueRequestWebInterface,
    send_and_update_email_state_service: SendAndUpdateEmailStateUseCase = Depends(
        Provide[Container.send_and_update_email_state_service]
    ),
):
    try:
        attachments = []
        if queue_request.attachments is not None:
            attachments = [
                Attachment(
                    filename=attach.filename,
                    filetype=attach.filetype,
                    blobname=attach.blobname,
                )
                for attach in queue_request.attachments
            ]

        send_and_update_email_state_command = SendAndUpdateEmailStateCommand(
            email_id=queue_request.email_id,
            receivers=queue_request.receivers,
            subject=queue_request.subject,
            content=queue_request.content,
            attachments=attachments,
        )
        success = await send_and_update_email_state_service.send_and_update_email_state(
            send_and_update_email_state_command
        )

        if success is True:
            return SendEmailResponse(
                message="Successfully send and update email state.",
                email_id=queue_request.email_id,
            )
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send and update email state. Error: {error}",
        )
