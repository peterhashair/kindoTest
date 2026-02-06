import uuid
from fastapi.testclient import TestClient
from unittest.mock import patch


def test_get_trips(client: TestClient):
    response = client.get("/trips")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["status"] == "success"
    assert isinstance(json_response["data"], list)


def test_create_trip(client: TestClient, test_data):
    school = test_data["school"]

    trip_data = {
        "name": "Trip to the Zoo",
        "description": "A fun day at the zoo",
        "price_in_cents": 2500,
        "school_id": str(school.id),
        "published": True,
        "destination": "City Zoo",
        "start_date": "2026-02-06T00:43:58.925Z",
        "end_date": "2026-02-05T00:43:58.925Z",
    }

    response = client.post("/trips/", json=trip_data)
    assert response.status_code == 400
    json_response = response.json()
    assert json_response["status"] == "error"
