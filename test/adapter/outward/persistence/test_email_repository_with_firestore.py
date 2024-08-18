import asyncio

from src.app.port.outward.save_email.save_email_command import SaveEmailCommand
from src.app.domain.entity.email import Attachment
from src.adapter.outward.persistence.email_repository import EmailRepository


async def test_save_email():
    email_repo = EmailRepository()

    sample_attachment = Attachment(
        filename="test_file.txt", filetype="text/plain", blobname="test_blob_name"
    )

    test_command = SaveEmailCommand(
        email_id="test-id-123",
        receivers=["test@example.com"],
        subject="Test Subject",
        content="This is a test email.",
        attachments=[sample_attachment],
    )

    await email_repo.save_email(test_command)
    print("Email Record has been saved successfully. (ID: {test_command.email_id})")


if __name__ == "__main__":
    asyncio.run(test_save_email())
