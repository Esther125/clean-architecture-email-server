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


class FilterEmailRequestWebInterface(BaseModel):
    email_id: Optional[str] = None
    request_time_start: Optional[datetime] = None
    request_time_end: Optional[datetime] = None
    sent_time_start: Optional[datetime] = None
    sent_time_end: Optional[datetime] = None
    is_sent: Optional[bool] = None
    receivers: Optional[EmailStr] = None
    subject: Optional[str] = None
    content: Optional[str] = None
    attachments_blobname: Optional[str] = None


class FilterEmailResponse(BaseModel):
    message: str
    result_emails: List[Email]
