from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr


class Attachment(BaseModel):
    filename: str
    filetype: str
    blobname: str


class Email(BaseModel):
    email_id: str
    is_sent: bool
    request_time: datetime
    sent_time: Optional[datetime] = None
    receivers: List[EmailStr]
    subject: str
    content: str
    attachments: Optional[List[Attachment]]


class FilterEmailResponse(BaseModel):
    message: str
    result_emails: List[Email]
