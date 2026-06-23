"""
Tests for DELETE /activities/{activity_name}/participants endpoint.
Each test follows the AAA (Arrange-Act-Assert) pattern.
"""

import pytest
from fastapi.testclient import TestClient


def test_unregister_success(client: TestClient):
    """
    Should allow a participant to be unregistered from an activity.
    """
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up in seed data

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    
    # Verify participant was removed from activity
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert email not in activities_data[activity_name]["participants"]


def test_unregister_activity_not_found(client: TestClient):
    """
    Should return 404 when trying to unregister from a non-existent activity.
    """
    # Arrange
    activity_name = "NonExistent Activity"
    email = "student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_unregister_participant_not_in_activity(client: TestClient):
    """
    Should return 404 when trying to unregister a participant who is not in the activity.
    """
    # Arrange
    activity_name = "Chess Club"
    email = "notamember@mergington.edu"  # Not signed up

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_unregister_removes_from_participants_list(client: TestClient):
    """
    Should ensure the participant is removed from the participants list after unregistering.
    """
    # Arrange
    activity_name = "Programming Class"
    email = "emma@mergington.edu"  # Already signed up in seed data
    
    # Verify they're in the list initially
    initial_response = client.get("/activities")
    initial_data = initial_response.json()
    assert email in initial_data[activity_name]["participants"]
    initial_count = len(initial_data[activity_name]["participants"])

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    
    # Verify they're no longer in the list
    final_response = client.get("/activities")
    final_data = final_response.json()
    assert email not in final_data[activity_name]["participants"]
    assert len(final_data[activity_name]["participants"]) == initial_count - 1


def test_unregister_twice_fails(client: TestClient):
    """
    Should return 404 when trying to unregister a participant twice.
    """
    # Arrange
    activity_name = "Chess Club"
    email = "daniel@mergington.edu"  # Already signed up in seed data

    # Act: First unregister should succeed
    response1 = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email}
    )

    # Assert: First unregister succeeds
    assert response1.status_code == 200

    # Act: Second unregister should fail
    response2 = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email}
    )

    # Assert: Second unregister fails with 404
    assert response2.status_code == 404
    data = response2.json()
    assert "detail" in data


def test_unregister_does_not_affect_other_activities(client: TestClient):
    """
    Should ensure unregistering from one activity does not affect other activities.
    """
    # Arrange
    participant = "emma@mergington.edu"  # Signed up for Programming Class
    activity1 = "Programming Class"
    activity2 = "Math Olympiad"
    
    # Sign participant up for a second activity
    client.post(
        f"/activities/{activity2}/signup",
        params={"email": participant}
    )

    # Act: Unregister from activity1
    response = client.delete(
        f"/activities/{activity1}/participants",
        params={"email": participant}
    )

    # Assert
    assert response.status_code == 200
    
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    
    # Verify removed from activity1
    assert participant not in activities_data[activity1]["participants"]
    
    # Verify still in activity2
    assert participant in activities_data[activity2]["participants"]
