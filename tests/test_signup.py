"""
Tests for POST /activities/{activity_name}/signup endpoint.
Each test follows the AAA (Arrange-Act-Assert) pattern.
"""

from fastapi.testclient import TestClient


def test_signup_success(client: TestClient):
    """
    Should allow a new participant to sign up for an activity.
    """
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    
    # Verify participant was added to activity
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert email in activities_data[activity_name]["participants"]


def test_signup_activity_not_found(client: TestClient):
    """
    Should return 404 when trying to sign up for a non-existent activity.
    """
    # Arrange
    activity_name = "NonExistent Activity"
    email = "student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_signup_duplicate_email_fails(client: TestClient):
    """
    Should return 400 when a participant tries to sign up twice.
    """
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"].lower()


def test_signup_multiple_participants_same_activity(client: TestClient):
    """
    Should allow multiple different participants to sign up for the same activity.
    """
    # Arrange
    activity_name = "Programming Class"
    new_email_1 = "alice@mergington.edu"
    new_email_2 = "bob@mergington.edu"

    # Act
    response1 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_email_1}
    )
    response2 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_email_2}
    )

    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    participants = activities_data[activity_name]["participants"]
    assert new_email_1 in participants
    assert new_email_2 in participants


def test_signup_same_participant_different_activities(client: TestClient):
    """
    Should allow the same participant to sign up for different activities.
    """
    # Arrange
    email = "newstudent@mergington.edu"
    activity1 = "Chess Club"
    activity2 = "Programming Class"

    # Act
    response1 = client.post(
        f"/activities/{activity1}/signup",
        params={"email": email}
    )
    response2 = client.post(
        f"/activities/{activity2}/signup",
        params={"email": email}
    )

    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert email in activities_data[activity1]["participants"]
    assert email in activities_data[activity2]["participants"]
