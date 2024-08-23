import os
from dotenv import load_dotenv
from google.cloud.firestore import AsyncClient

load_dotenv()


class DBClient(AsyncClient):
    def __new__(cls) -> AsyncClient:
        project_id = os.getenv("GCP_PROJECT_ID")
        database_id = os.getenv("GCP_FIRESTORE_DATABASE_ID")
        db = AsyncClient(
            project=project_id,
            database=database_id,
        )
        return db
