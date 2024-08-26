from abc import ABC, abstractmethod

from src.app.port.outward.query_email.query_email_command import QueryEmailCommand


class QueryEmailPort(ABC):
    @abstractmethod
    async def query_email(self, command: QueryEmailCommand) -> None:
        raise NotImplementedError
