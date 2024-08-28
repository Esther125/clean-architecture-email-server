from abc import ABC, abstractmethod
from typing import List

from src.app.domain.entity.email import Email
from src.app.port.inward.filter_email_request.filter_email_request_command import (
    FilterEmailRequestCommand,
)


class FilterEmailRequestUseCase(ABC):
    @abstractmethod
    async def filter_email_request(
        self, command: FilterEmailRequestCommand
    ) -> List[Email]:
        raise NotImplementedError
