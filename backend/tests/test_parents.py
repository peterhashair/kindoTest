from fastapi.testclient import TestClient


def test_get_parents(client: TestClient):
    response = client.get("/parents")
    assert response.status_code == 200

    json_response = response.json()
    assert json_response["status"] == "success"
    assert isinstance(json_response["data"], list)

    # Check for seeded data
    if json_response["data"]:
        parent = json_response["data"][0]
        assert "id" in parent
        assert "name" in parent
        assert parent["name"] == "Test Parent"  # From seeder
