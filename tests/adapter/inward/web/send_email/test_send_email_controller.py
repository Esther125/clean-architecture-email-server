from fastapi.testclient import TestClient
from unittest import TestCase
from src.main import app


class TestSendEmailEndpoint(TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_queue_and_save_email(self):
        response = self.client.post(
            "/v1/user/email",
            headers={"Content-Type": "application/json"},
            json={
                "receivers": ["test@gmail.com"],
                "subject": "Test Subject",
                "content": "test content",
            },
        )
        assert response.status_code == 200
        result = response.json()
        assert result["email_id"], "email_id should not be null"
        assert isinstance(result["email_id"], str), "email_id should be a string"

    def test_queue_and_save_email_failed(self):
        pass

    def test_send_and_update_email(self):
        response = self.client.post(
            "/v1/queue/email",
            headers={"Content-Type": "application/json"},
            json={
                "email_id": "test",
                "receivers": ["test@gmail.com"],
                "subject": "Test Subject",
                "content": "test content",
            },
        )
        assert response.status_code == 200
        result = response.json()
        assert result["email_id"], "email_id should not be null"
        assert isinstance(result["email_id"], str), "email_id should be a string"

    def test_send_and_update_email_failed(self):
        pass
