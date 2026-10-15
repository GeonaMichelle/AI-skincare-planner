import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "AI Skin Intelligence & Personalized Skincare Planner"
    assert data["version"] == "1.0.0"
    assert data["api_prefix"] == "/api/v1"

def test_frontend_serving():
    response = client.get("/")
    assert response.status_code in [200, 404] # Depending on if frontend exists in test env

def test_unauthorized_access():
    response = client.get("/api/v1/profiles/me")
    assert response.status_code == 401

def test_login_invalid_credentials():
    response = client.post("/api/v1/auth/login", json={
        "email": "invalid@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
