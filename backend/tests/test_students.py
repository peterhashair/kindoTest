from fastapi.testclient import TestClient

def test_create_and_get_student(client: TestClient):
    # Get parent and school IDs first
    parent_response = client.get("/parents")
    parent_id = parent_response.json()["data"][0]["id"]
    
    school_response = client.get("/schools")
    school_id = school_response.json()["data"][0]["id"]

    # Create a new student
    new_student_data = {
        "name": "Sammy Doe",
        "gender":"male",
        "dob": "2010-01-01",
        "parent_ids": [parent_id]
    }
    create_response = client.post("/students/", json=new_student_data)
    assert create_response.status_code == 200
    created_student = create_response.json()["data"]
    assert created_student["name"] == new_student_data["name"]
    assert "id" in created_student

    # Get the student by parent_id
    get_response = client.get(f"/students/parent/{parent_id}")
    assert get_response.status_code == 200
    students = get_response.json()["data"]
    assert isinstance(students, list)
    assert len(students) > 0
    assert students[1]["name"] == "Sammy Doe"
