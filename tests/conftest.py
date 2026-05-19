import pytest
from fastapi.testclient import TestClient

from run import app

@pytest.fixture
def client():
    return TestClient(app)