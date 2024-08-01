from typing import List
from pydantic import EmailStr

from src.app.domain.entity.email import Attachment


class SendAndUpdateEmailStateCommand:
    def __init__(
        self, 
        email_id: str,
        receivers: List[EmailStr],
        subject: str,
        content: str,
        attachments: List[Attachment] | None
    ):
        self.__email_id = email_id
        self.__receivers = receivers
        self.__subject = subject
        self.__content = content
        self.__attachments = attachments
    
    @property
    def email_id(self) -> str:
         return self.__email_id

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
 