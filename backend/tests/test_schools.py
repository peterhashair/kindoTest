from fastapi.testclient import TestClient

def test_get_schools(client: TestClient):
    response = client.get("/schools")
    assert response.status_code == 200
    
    # The response should be wrapped
    json_response = response.json()
    assert json_response["status"] == "success"
    assert isinstance(json_response["data"], list)
    
    # Check if there's data, assuming the seeder ran
    if json_response["data"]:
        # Check the structure of the first school
        school = json_response["data"][0]
        assert "id" in school
        assert "name" in school
        assert school["name"] == "Test Academy" # From seeder
