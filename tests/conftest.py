import pytest
from fastapi.testclient import TestClient
from faker import Faker
from random import randint

from run import app
from app.core.config import settings

fake = Faker()

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def password():
    return settings.admin_password

@pytest.fixture
def fake_user():
    data = {
        'name': fake.first_name(),
        'age': randint(1, 120),
        'email': fake.email()
    }
    return data