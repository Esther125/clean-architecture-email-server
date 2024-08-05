from src.app.port.outward.update_email_state.update_email_state_command import (
    UpdateEmailStateCommand,
)
from src.app.port.outward.update_email_state.update_email_state_port import (
    UpdateEmailStatePort,
)


class UpdateEmailStateAdapter(UpdateEmailStatePort):
    def __init__(self) -> None:
        pass

    async def update_state(self, command: UpdateEmailStateCommand) -> None:
        pass
