import asyncio

from src.adapter.outward.send_email.send_email_adapter import SendEmailAdapter
from src.app.domain.entity.email import Attachment
from src.app.port.outward.send_email.send_email_command import SendEmailCommand


async def main():
    email_adapter = SendEmailAdapter()

    attachment = Attachment(
        filename="example.rtf", filetype="application/rtf", blobname="example.rtf"
    )
    command = SendEmailCommand(
        email_id="test123",
        receivers=["friday50523@gmail.com"],
        subject="Test Email",
        content="This is a test email sent from the SendEmailAdapter script.",
        attachments=[attachment],
    )

    try:
        await email_adapter.send_email(command)
        print("Email sent successfully.")

    except Exception as e:
        print(f"An error occurred while sending the email: {e}")


if __name__ == "__main__":
    asyncio.run(main())
