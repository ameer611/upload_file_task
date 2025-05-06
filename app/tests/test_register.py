import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():
    response = client.post(
        "/register",
        json={"username": "newuser", "password": "newpassword123"}
    )
    
    assert response.status_code == 200
    assert response.json() == {"username": "newuser"}

def test_register_existing_user():
    # First registration
    client.post(
        "/register",
        json={"username": "existinguser", "password": "password123"}
    )
    
    # Attempt to register same user
    response = client.post(
        "/register",
        json={"username": "existinguser", "password": "password123"}
    )
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"

def test_register_short_password():
    response = client.post(
        "/register",
        json={"username": "shortpassuser", "password": "short"}
    )
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Password must be at least 8 characters"