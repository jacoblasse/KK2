import pytest
from fastapi.testclient import TestClient

@pytest.fixture(autouse=True)
def reset_state():
    from app import data
    data.dataset = None
    yield

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


def test_stats_without_data(client):
    response = client.get("/data/stats")
    assert response.status_code == 404


def test_stats_with_data(client):
    csv_content = "name,age\nJacob,22\nKevin,21"
    files = {"file": ("test.csv", csv_content)}
    client.post("/data/upload", files=files)

    response = client.get("/data/stats")
    assert response.status_code == 200
    stats = response.json()["stats"]
    assert "age" in stats
    assert stats["age"]["count"] == 2
    assert stats["age"]["mean"] == 21.5

def test_ai_ask_with_mocked_chain(client, monkeypatch):
    csv_content = "name,age\nJacob,22\nKevin,21"
    files = {"file": ("test.csv", csv_content)}
    client.post("/data/upload", files=files)

    from app.chain.steps import ResponseParserOutput

    class FakeChain:
        def invoke(self, input):
            return ResponseParserOutput(prompt = "", answer="The average age is 21.5")
        
    import app.main
    monkeypatch.setattr(app.main, "oraklet", FakeChain())

    response = client.post("/ai/ask", json={"question": "What is the average age?"})

    assert response.status_code == 200
    data = response.json()
    assert data["question"] == "What is the average age?"
    assert data["answer"] == "The average age is 21.5"