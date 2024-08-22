import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from google.cloud import firestore

load_dotenv()


class DBClient:
    def __new__(cls) -> firestore.AsyncClient:
        credentials = service_account.Credentials.from_service_account_file(
            os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        )
        project_id = os.getenv("GCP_PROJECT_ID")
        database_id = os.getenv("GCP_FIRESTORE_DATABASE_ID")
        db = firestore.AsyncClient(
            project=project_id,
            database=database_id,
            credentials=credentials,
        )
        return db
