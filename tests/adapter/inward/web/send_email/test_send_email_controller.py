from fastapi.testclient import TestClient
from unittest import TestCase
from src.main import app


class TestSendEmailEndpoint(TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_dispatch_email(self):
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
        assert result["message"] == "Successfully dispatched the email request."

    def test_deliver_email(self):
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
        assert result["message"] == "Successfully delivered the email request."
