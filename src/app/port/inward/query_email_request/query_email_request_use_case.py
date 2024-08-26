from abc import ABC, abstractmethod

from src.app.port.inward.query_email_request.query_email_request_command import (
    QueryEmailRequestCommand,
)


class QueryEmailRequestUseCase(ABC):
    @abstractmethod
    async def query_email_request(self, command: QueryEmailRequestCommand) -> None:
        raise NotImplementedError
