
class UpdateEmailStateCommand:
    def __init__(self,
        email_id: int,
        is_sent: bool = True
    ):
        self.__email_id = email_id
        self.__is_sent = is_sent
    
    @property
    def email_id(self) -> int:
        return self.__email_id

    @property
    def is_sent(self) -> bool:
        return self.__is_sent
    
