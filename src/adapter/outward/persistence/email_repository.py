from google.cloud import firestore
from src.adapter.outward.persistence.db_client import DBClient


class EmailRepository:
    def __new__(cls, client: DBClient) -> firestore.AsyncClient:
        client = client
        return client.collection("emails")  # type: ignore[attr-defined]
