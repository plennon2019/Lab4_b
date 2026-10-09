import pytest
from fastapi.testclient import TestClient
from app.main import app, users

@pytest.fixture(autouse=True)
def clear_users():
    users.clear()

@pytest.fixture
def client():
    return TestClient(app)