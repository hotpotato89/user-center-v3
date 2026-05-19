import pytest
from fastapi.testclient import TestClient

from run import app

from app.core.config import settings

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def password():
    return settings.admin_password