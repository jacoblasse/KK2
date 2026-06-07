import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    from app.main import app
    return TestClient(app)

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_upload_data(client):
    csv_content = "name,age\nJacob,22\nKevin,21"
    files = {"file": ("test.csv", csv_content)}
    response = client.post("/data/upload", files=files)

    assert response.status_code == 200
    data = response.json()
    assert data["rows"] == 2
    assert data["columns"] == ["name", "age"]
    assert "dtypes" in data


def test_upload_invalid_file(client):
    files = {"file": ("test.txt", "This is not a CSV file.")}
    response = client.post("/data/upload", files=files)

    assert response.status_code == 400
    assert "csv" in response.json()["detail"].lower()