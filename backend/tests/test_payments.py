from fastapi.testclient import TestClient


def test_payment_invalid(client: TestClient, test_data):
    booking = test_data["booking"]
    studentg = test_data["student"]
    parent = test_data["parent"]
    school = test_data["school"]

    payment_data_invalid_card = {
        "student_name": studentg.name,
        "parent_name": parent.name,
        "amount": round(booking.total_in_cents / 100, 2),
        "card_number": "invalidcardnumber",
        "expiry_date": "03/50",
        "cvv": "227",
        "school_id": str(school.id),
        "activity_id": str(booking.id),
    }

    response = client.post("/payments/process", json=payment_data_invalid_card)
    assert response.status_code == 400
    json_response = response.json()
    assert json_response["status"] == "error"
    assert "Invalid card number" in json_response["error"]

    payment_data_invalid_expiry = {
        "student_name": studentg.name,
        "parent_name": parent.name,
        "amount": round(booking.total_in_cents / 100, 2),
        "card_number": "1234123412341234",
        "expiry_date": "03/10",
        "cvv": "227",
        "school_id": str(school.id),
        "activity_id": str(booking.id),
    }

    response = client.post("/payments/process", json=payment_data_invalid_expiry)
    assert response.status_code == 400
    json_response = response.json()
    assert json_response["status"] == "error"
    assert "Card has expired" in json_response["error"]

    payment_data_invalid_cvv = {
        "student_name": studentg.name,
        "parent_name": parent.name,
        "amount": round(booking.total_in_cents / 100, 2),
        "card_number": "1234123412341234",
        "expiry_date": "03/50",
        "cvv": "1",
        "school_id": str(school.id),
        "activity_id": str(booking.id),
    }

    response = client.post("/payments/process", json=payment_data_invalid_cvv)
    assert response.status_code == 400
    json_response = response.json()
    assert json_response["status"] == "error"
    assert "Invalid CVV" in json_response["error"]


def test_sucess_payment(client: TestClient, test_data):
    booking = test_data["booking"]
    studentg = test_data["student"]
    parent = test_data["parent"]
    school = test_data["school"]

    payment_data = {
        "student_name": studentg.name,
        "parent_name": parent.name,
        "amount": round(booking.total_in_cents / 100, 2),
        "card_number": "1234123412341234",
        "expiry_date": "03/50",
        "cvv": "227",
        "school_id": str(school.id),
        "activity_id": str(booking.id),
    }

    response = client.post("/payments/process", json=payment_data)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["status"] == "success"
    assert "data" in json_response
    assert json_response["data"]["transaction_id"] is not None
