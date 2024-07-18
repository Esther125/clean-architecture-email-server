import os
from typing import List
from dotenv import load_dotenv
from pydantic import EmailStr

from src.app.domain.entity.email import Attachment

load_dotenv()

class ExecuteSendEmailCommand:
    def __init__(self,
        receivers: List[EmailStr],
        subject: str,
        content: str,
        attachments: List[Attachment] | None
    ):
        self.__sender = os.getenv("SENDER_EMAIL"),
        self.__password = os.getenv("SENDER_PASSWORD"),
        self.__receivers = receivers
        self.__subject = subject
        self.__content = content
        self.__attachments = attachments

    @property
    def sender(self) -> List[EmailStr]:
         return self.__sender
    
    @property
    def password(self) -> str:
         return self.__password
    
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
    
    @attachments.setter
    def attachments(self, attachments: List[Attachment]):
         self.__attachments = attachments