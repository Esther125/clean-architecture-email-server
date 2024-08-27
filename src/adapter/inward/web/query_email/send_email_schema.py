from typing import List, Optional

from pydantic import BaseModel, EmailStr


class Attachment(BaseModel):
    filename: str
    filetype: str
    blobname: str


class UserRequestWebInterface(BaseModel):
    receivers: List[EmailStr]
    subject: str
    content: str
    attachments: Optional[List[Attachment]] = None


class QueueRequestWebInterface(BaseModel):
    email_id: str
    receivers: List[EmailStr]
    subject: str
    content: str
    attachments: Optional[List[Attachment]] = None


class SendEmailResponse(BaseModel):
    message: str
    email_id: str
