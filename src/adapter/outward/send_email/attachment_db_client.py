import os
import logging
from dotenv import load_dotenv
from google.cloud.storage import Client

load_dotenv()

logger = logging.getLogger(__name__)


class AttachmentDBClient(Client):
    def __init__(self) -> None:
        self.client = Client()
        self.attachment_bucket_name = os.getenv("GCP_CLOUD_STORAGE_BUCKET_NAME")
        self.attachment_bucket = self.bucket(self.attachment_bucket_name)

    def download_attachment(self, blob_name: str) -> bytes:
        try:
            attachment = self.attachment_bucket.blob(blob_name)
            logger.info(
                "Successfully download the attachment from Cloud Storage. (Blobname: {blob_name})"
            )
            return attachment.download_as_bytes()
        except Exception as error:
            logger.error(
                f"Failed to download the attachment from Cloud Storage. (Blobname: {blob_name}) Error: {error}"
            )
            raise error
