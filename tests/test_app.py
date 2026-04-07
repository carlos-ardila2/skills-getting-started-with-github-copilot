"""Backend FastAPI tests for the Mergington High School API."""

from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities_returns_expected_data():
    # Arrange
    expected_keys = {"Chess Club", "Programming Class", "Gym Class"}

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert expected_keys.issubset(set(data.keys()))
    assert all("description" in activity for activity in data.values())


def test_signup_new_student_adds_participant():
    # Arrange
    activity_name = "Chess Club"
    email = "teststudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )

    # Assert
    assert response.status_code == 200
    body = response.json()
    assert "Signed up" in body["message"]

    activity_response = client.get("/activities")
    participants = activity_response.json()[activity_name]["participants"]
    assert email in participants


def test_signup_duplicate_student_records_duplicate_entry():
    # Arrange
    activity_name = "Programming Class"
    email = "duplicate@mergington.edu"

    # Act
    response_first = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    response_second = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )

    # Assert
    assert response_first.status_code == 200
    assert response_second.status_code == 400

    participants = client.get("/activities").json()[activity_name]["participants"]
    assert participants.count(email) == 1
