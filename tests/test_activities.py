"""
Tests for GET /activities endpoint.
Each test follows the AAA (Arrange-Act-Assert) pattern.
"""

import pytest
from fastapi.testclient import TestClient


def test_get_activities_returns_all_activities(client: TestClient):
    """
    Should return a 200 response with all activities as a dict.
    """
    # Arrange: client is ready (from fixture)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0  # Should have seed data


def test_get_activities_response_structure(client: TestClient):
    """
    Each activity in the response should have required fields.
    """
    # Arrange: client is ready

    # Act
    response = client.get("/activities")

    # Assert
    data = response.json()
    required_fields = {"description", "schedule", "max_participants", "participants"}
    
    for activity_name, activity_data in data.items():
        assert isinstance(activity_name, str)
        assert all(field in activity_data for field in required_fields)
        assert isinstance(activity_data["participants"], list)
        assert isinstance(activity_data["max_participants"], int)


def test_get_activities_participants_are_strings(client: TestClient):
    """
    Each participant in the list should be a string email.
    """
    # Arrange: client is ready

    # Act
    response = client.get("/activities")

    # Assert
    data = response.json()
    for activity_name, activity_data in data.items():
        for participant in activity_data["participants"]:
            assert isinstance(participant, str)
            assert "@" in participant  # Basic email format check
