from datetime import datetime


class UpdateEmailStateCommand:
    def __init__(
        self,
        email_id: str,
        is_sent: bool = True,
    ):
        self.__email_id = email_id
        self.__sent_time = datetime.now()
        self.__is_sent = is_sent

    @property
    def email_id(self) -> str:
        return self.__email_id

    @property
    def sent_time(self) -> datetime:
        return self.__sent_time

    @property
    def is_sent(self) -> bool:
        return self.__is_sent
