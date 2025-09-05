"""Unit tests for webook module."""

import pytest
from fastapi.testclient import TestClient

from app.webhook import subscribe_app


@pytest.fixture
def client_fixture():
    """A test client for the webhook app."""
    with TestClient(subscribe_app) as c:
        yield c


def test_health_check(client_fixture):
    """Test health check endpoint."""
    response = client_fixture.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_webhook(client_fixture):
    """Test webhook endpoint."""
    response = client_fixture.post("/webhook", json={"key": "value"})
    assert response.status_code == 200
    assert response.json() == {"status": "success"}
