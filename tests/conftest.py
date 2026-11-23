import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app

_initial_activities = copy.deepcopy(activities)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    # Restore in place so the app keeps referencing the same dict
    activities.clear()
    activities.update(copy.deepcopy(_initial_activities))
    yield
