from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_counts():
    response = client.get("/v0/counts/")
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["firm_count"] == 34
    assert response_data["user_count"] == 0
    assert response_data["vote_count"] == 0