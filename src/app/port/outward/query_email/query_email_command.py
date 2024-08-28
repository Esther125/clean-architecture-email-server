from datetime import datetime
from typing import List, Optional
from pydantic import EmailStr


class QueryEmailCommand:
    def __init__(
        self,
        email_id: Optional[str] = None,
        request_time_start: Optional[datetime] = None,
        request_time_end: Optional[datetime] = None,
        sent_time_start: Optional[datetime] = None,
        sent_time_end: Optional[datetime] = None,
        is_sent: Optional[bool] = None,
        receivers: Optional[List[EmailStr]] = None,
        subject: Optional[str] = None,
        content: Optional[str] = None,
        attachments_blobname: Optional[List[str]] = None,
    ):
        self.__email_id = email_id
        self.__request_time_start = request_time_start
        self.__request_time_end = request_time_end
        self.__sent_time_start = sent_time_start
        self.__sent_time_end = sent_time_end
        self.__is_sent = is_sent
        self.__receivers = receivers or []
        self.__subject = subject
        self.__content = content
        self.__attachments_blobname = attachments_blobname

    @property
    def email_id(self) -> Optional[str]:
        return self.__email_id

    @property
    def request_time_start(self) -> Optional[datetime]:
        return self.__request_time_start

    @property
    def request_time_end(self) -> Optional[datetime]:
        return self.__request_time_end

    @property
    def sent_time_start(self) -> Optional[datetime]:
        return self.__sent_time_start

    @property
    def sent_time_end(self) -> Optional[datetime]:
        return self.__sent_time_end

    @property
    def is_sent(self) -> Optional[bool]:
        return self.__is_sent

    @property
    def receivers(self) -> Optional[List[EmailStr]]:
        return self.__receivers

    @property
    def subject(self) -> Optional[str]:
        return self.__subject

    @property
    def content(self) -> Optional[str]:
        return self.__content

    @property
    def attachments_blobname(self) -> Optional[List[str]]:
        return self.__attachments_blobname
