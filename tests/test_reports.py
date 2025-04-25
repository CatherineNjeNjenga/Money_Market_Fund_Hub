from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_reports():
    response = client.get("/v0/reports/?skip=0&limit=1000")
    print(response)
    assert response.status_code == 200
    assert len(response.json()) == 544

# test /v0/reports/ with changed date
def test_read_reports_by_date():
    response = client.get(
        "/v0/reports/?skip=0&limit=1000&minimum_last_changed_date=2025-04-24"
    )
    assert response.status_code == 200
    assert len(response.json()) == 544