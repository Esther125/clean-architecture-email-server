from datetime import datetime
from typing import List, Optional

from pydantic import EmailStr

from src.app.domain.entity.email import Attachment


class SaveEmailCommand:
    def __init__(
        self,
        email_id: str,
        request_time: datetime,
        receivers: List[EmailStr],
        subject: str,
        content: str,
        attachments: Optional[List[Attachment]] = None,
    ):
        self.__email_id = email_id
        self.__is_sent = False
        self.__request_time = request_time
        self.__sent_time = None
        self.__receivers = receivers
        self.__subject = subject
        self.__content = content
        self.__attachments = attachments or []

    @property
    def email_id(self) -> str:
        return self.__email_id

    @property
    def is_sent(self) -> bool:
        return self.__is_sent

    @property
    def request_time(self) -> datetime:
        return self.__request_time

    @property
    def sent_time(self) -> datetime | None:
        return self.__sent_time

    @property
    def receivers(self) -> List[EmailStr]:
        return self.__receivers

    @property
    def subject(self) -> str:
        return self.__subject

    @property
    def content(self) -> str:
        return self.__content

    @property
    def attachments(self) -> List[Attachment]:
        return self.__attachments
