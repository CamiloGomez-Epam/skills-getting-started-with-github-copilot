import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Deep-copy the in-memory activities before each test and restore after."""
    orig = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(orig)
