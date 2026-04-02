from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Identifiers API"}

def test_get_identifiers():
    response = client.get("/identifiers")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_identifier():
    response = client.get("/identifiers/88823141")
    assert response.status_code in [200, 404]

def test_create_identifier():
    data = {
        "identifier_name": "99999999",
        "description": "Test Product",
        "identifier_type": "Test Type"
    }
    response = client.post("/identifiers", json=data)
    assert response.status_code in [200, 400]