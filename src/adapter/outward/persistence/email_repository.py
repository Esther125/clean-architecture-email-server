from src.app.port.outward.save_email.save_email_command import SaveEmailCommand
from src.app.port.outward.save_email.save_email_port import SaveEmailPort


class EmailRepository(SaveEmailPort):
    def __init__(self) -> None:
        pass

    async def save_email(self, command: SaveEmailCommand) -> None:
        pass
