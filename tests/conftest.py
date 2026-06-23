"""
Shared fixtures and configuration for backend tests.
Enforces deterministic state reset before each test to prevent cross-test contamination.
"""

import pytest
import copy
from fastapi.testclient import TestClient
from src.app import app, activities


# Deep copy of original activities state for reset
_ORIGINAL_ACTIVITIES = copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Automatically reset activities to original state before each test.
    This ensures tests are isolated and order-independent.
    """
    activities.clear()
    activities.update(copy.deepcopy(_ORIGINAL_ACTIVITIES))
    yield
    # Cleanup after test
    activities.clear()
    activities.update(copy.deepcopy(_ORIGINAL_ACTIVITIES))


@pytest.fixture
def client():
    """
    Provides a TestClient instance for making requests to the app.
    Uses the reset_activities fixture for state isolation.
    """
    return TestClient(app)
