import os
from dotenv import load_dotenv
from google.cloud import firestore

load_dotenv()


class DBClient:
    def __new__(cls) -> firestore.AsyncClient:
        project_id = os.getenv("GCP_PROJECT_ID")
        database_id = os.getenv("GCP_FIRESTORE_DATABASE_ID")
        db = firestore.AsyncClient(
            project=project_id,
            database=database_id,
        )
        return db
