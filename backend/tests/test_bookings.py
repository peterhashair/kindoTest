from fastapi.testclient import TestClient
import uuid


# We need to create a trip first to be able to create a booking
def test_create_booking(client: TestClient):
    # 1. Get existing trips, parent, and student from the test DB setup
    trip_response = client.get("/trips")
    trip_id = trip_response.json()["data"][0]["id"]

    parent_response = client.get("/parents")
    parent_id = parent_response.json()["data"][0]["id"]

    student_response = client.get(f"/students/parent/{parent_id}")
    student_id = student_response.json()["data"][0]["id"]

    # 2. Create a new trip for the booking
    booking_data = {
        "description": "Museum Visit",
        "trip_id": trip_id,
        "student_id": student_id,
        "parent_id": parent_id,
    }

    create_response = client.post("/bookings/", json=booking_data)
    assert create_response.status_code == 200

    booking = create_response.json()["data"]

    assert "id" in booking

    # 3. Test get_or_create: creating the same booking again should return the same one
    retry_response = client.post("/bookings/", json=booking_data)
    assert retry_response.status_code == 200
    retry_booking = retry_response.json()["data"]
    assert retry_booking["id"] == booking["id"]

    # 4. Test get bookings by parent ID
    get_by_parent_response = client.get(f"/bookings/parent/{parent_id}")
    assert get_by_parent_response.status_code == 200
    parent_bookings = get_by_parent_response.json()["data"]
    assert isinstance(parent_bookings, list)
    assert len(parent_bookings) > 0
