import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Basketball" in data
    assert "Tennis Club" in data


def test_signup_success():
    email = "newstudent@mergington.edu"
    response = client.post(f"/activities/Basketball/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for Basketball" in response.json()["message"]


def test_signup_duplicate():
    email = "alex@mergington.edu"
    response = client.post(f"/activities/Basketball/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_activity_full():
    # Fill up the activity
    activity = "Tennis Club"
    max_participants = 10
    for i in range(2, max_participants + 1):
        email = f"student{i}@mergington.edu"
        client.post(f"/activities/{activity}/signup?email={email}")
    # Try to add one more
    response = client.post(f"/activities/{activity}/signup?email=overflow@mergington.edu")
    assert response.status_code == 400
    assert "is full" in response.json()["detail"]
