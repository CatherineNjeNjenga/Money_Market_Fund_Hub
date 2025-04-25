from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# test the root/health check endpoint
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Money Market Fund Hub API health check successful"}

# test /v0/firms/
def test_read_firms():
    response = client.get("/v0/firms/?skip=0&limit=100")
    assert response.status_code == 200
    assert len(response.json()) == 34

def test_read_firms_by_name():
    response = client.get("/v0/firms/?firm_name=Ndovu Money Market Fund")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0].get("firm_id") == 26

# test /v0/firms/{firm_id}/
def test_read_firms_with_id():
    response = client.get("/v0/firms/1/")
    assert response.status_code == 200
    assert response.json().get("firm_id") == 1