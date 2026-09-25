from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from restaurant_agent.core.config import get_settings
from restaurant_agent.main import create_app


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch) -> Generator[TestClient, None, None]:
    monkeypatch.setenv("APP_NAME", "Test Restaurant API")
    monkeypatch.setenv("APP_ENVIRONMENT", "test")
    get_settings.cache_clear()
    with TestClient(create_app()) as client:
        yield client
    get_settings.cache_clear()


def test_liveness(client: TestClient) -> None:
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "Test Restaurant API",
        "environment": "test",
    }


def test_readiness(client: TestClient) -> None:
    response = client.get("/health/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_openapi_document_is_available(client: TestClient) -> None:
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json()["info"]["title"] == "Test Restaurant API"
