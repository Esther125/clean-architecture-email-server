import asyncio

from src.adapter.outward.persistence.update_email_state_adapter import (
    UpdateEmailStateAdapter,
)
from src.app.port.outward.update_email_state.update_email_state_command import (
    UpdateEmailStateCommand,
)


async def test_update_email_state():
    update_email_state_adapter = UpdateEmailStateAdapter()

    test_command = UpdateEmailStateCommand(email_id="test-id", is_sent=True)

    await update_email_state_adapter.update_state(test_command)
    print(f"Email Record has been updated successfully. (ID: {test_command.email_id})")


if __name__ == "__main__":
    asyncio.run(test_update_email_state())
