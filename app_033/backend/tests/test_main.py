import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_predict():
    response = client.post("/api/v1/predict", json={"data": [1, 2, 3]})
    assert response.status_code == 200
    assert "prediction" in response.json()
