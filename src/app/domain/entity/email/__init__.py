from datetime import datetime
from typing import List, Optional

from pydantic import EmailStr


class Attachment:
    def __init__(self, filename: str, filetype: str, blobname: str):
        self.filename = filename
        self.filetype = filetype
        self.blobname = blobname


class Email:
    def __init__(
        self,
        email_id: str,
        receivers: List[EmailStr],
        subject: str,
        content: str,
        attachments: Optional[List[Attachment]] = None,
    ):
        self.__email_id = email_id
        self.__receivers = receivers
        self.__subject = subject
        self.__content = content
        self.__attachments = attachments or []
        self.__timestamp = datetime.now()
        self.__is_sent = False

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

    @property
    def timestamp(self) -> datetime:
        return self.__timestamp

    @property
    def is_sent(self) -> bool:
        return self.__is_sent

    @is_sent.setter
    def is_sent(self, is_sent: bool):
        self.__is_sent = is_sent
