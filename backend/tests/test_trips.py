import uuid
from fastapi.testclient import TestClient
from unittest.mock import patch

def test_get_trips(client: TestClient):
    response = client.get("/trips")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["status"] == "success"
    assert isinstance(json_response["data"], list)


