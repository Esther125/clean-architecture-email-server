from abc import ABC, abstractmethod
from typing import List

from src.app.domain.entity.email import Email
from src.app.port.outward.query_email.query_email_command import QueryEmailCommand


class QueryEmailPort(ABC):
    @abstractmethod
    async def query_email(self, command: QueryEmailCommand) -> List[Email]:
        raise NotImplementedError
