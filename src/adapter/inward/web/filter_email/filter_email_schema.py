from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr

from src.app.domain.entity.email import Email


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
