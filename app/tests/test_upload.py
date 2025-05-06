import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def auth_token():
    # Simulate login to get token
    response = client.post(
        "/token",
        json={"username": "testuser", "password": "testpassword"}
    )
    return response.json().get("access_token")

def test_upload_file(auth_token):
    with open("test.jpg", "rb") as file:
        response = client.post(
            "/upload",
            files={"file": ("test.jpg", file, "image/jpeg")},
            headers={"Authorization": f"Bearer {auth_token}"}
        )
    
    assert response.status_code == 200
    assert "file_id" in response.json()
    assert "file_url" in response.json()
    assert "filename" in response.json()