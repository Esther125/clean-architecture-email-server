import base64
import json
import uuid
from fastapi import APIRouter, HTTPException, Depends, Request
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


async def parse_queue_resquest(request: Request) -> QueueRequestWebInterface:
    try:
        raw_body = await request.body()
        json_body = json.loads(raw_body.decode("utf-8"))
        encoded_data = json_body["message"]["data"]
        decoded_data = base64.b64decode(encoded_data).decode("utf-8")
        queue_request = QueueRequestWebInterface.model_validate_json(decoded_data)
        return queue_request
    except Exception as error:
        raise FailedToParseQueueRequestError(error)


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
        raise HTTPException(
            status_code=500, detail=f"Failed to queue and save email. Error: {error}"
        )


@router.post(
    "/queue-email-request", status_code=200, summary="For queue to dequeue emails."
)
@inject
async def handle_send_and_update_email_state_request(
    request: Request,
    send_and_update_email_state_service: SendAndUpdateEmailStateUseCase = Depends(
        Provide[Container.send_and_update_email_state_service]
    ),
):
    try:
        queue_request = await parse_queue_resquest(request)

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
        await send_and_update_email_state_service.send_and_update_email_state(
            send_and_update_email_state_command
        )

        return SendEmailResponse(
            message="Successfully send and update email state.",
            email_id=queue_request.email_id,
        )
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send and update email state. Error: {error}",
        )


class FailedToParseQueueRequestError(Exception):
    def __init__(self, error) -> None:
        self.error = error
        self.message = f"Failed to parse queue request. Error: {error}"
        super().__init__(self.message)
