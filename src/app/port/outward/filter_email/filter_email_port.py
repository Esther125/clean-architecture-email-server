from abc import ABC, abstractmethod
from typing import List

from src.app.domain.entity.email import Email
from src.app.port.outward.filter_email.filter_email_command import FilterEmailCommand


class FilterEmailPort(ABC):
    @abstractmethod
    async def filter_email(self, command: FilterEmailCommand) -> List[Email]:
        raise NotImplementedError
