import logging
from src.adapter.outward.send_email.attachment_db_client import AttachmentDBClient

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    TEST_BLOB_NAME = "example.rtf"
    try:
        client = AttachmentDBClient()
    except Exception as e:
        logger.error(f"Failed to initialize AttachmentDBClient: {e}")
        exit(1)

    try:
        data = client.download_attachment(TEST_BLOB_NAME)
        print("DATA: ", data)
        if data:
            logger.info(f"Download successful. Size of data: {len(data)} bytes.")
        else:
            logger.warning("Download completed, but no data was returned.")

    except Exception as error:
        logger.error(f"An error occurred during the download: {error}")
