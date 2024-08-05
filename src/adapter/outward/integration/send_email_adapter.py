from src.app.port.outward.send_email.send_email_command import SendEmailCommand
from src.app.port.outward.send_email.send_email_port import SendEmailPort


class SendEmailAdapter(SendEmailPort):
    def __init__(self) -> None:
        pass

    async def send_email(self, command: SendEmailCommand) -> None:
        pass
