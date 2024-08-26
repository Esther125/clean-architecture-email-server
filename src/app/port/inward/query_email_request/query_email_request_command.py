from typing import List, Optional
from pydantic import EmailStr

from src.app.domain.entity.email import Attachment


class QueryEmailRequestCommand:
    def __init__(
        self,
        email_id: Optional[str] = None,
        receivers: Optional[List[EmailStr]] = None,
        subject: Optional[str] = None,
        content: Optional[str] = None,
        attachments: Optional[List[Attachment]] = None,
    ):
        self.__email_id = email_id
        self.__receivers = receivers or []
        self.__subject = subject
        self.__content = content
        self.__attachments = attachments or []

    @property
    def email_id(self) -> Optional[str]:
        return self.__email_id

    @property
    def receivers(self) -> List[EmailStr]:
        return self.__receivers

    @property
    def subject(self) -> Optional[str]:
        return self.__subject

    @property
    def content(self) -> Optional[str]:
        return self.__content

    @property
    def attachments(self) -> List[Attachment]:
        return self.__attachments
