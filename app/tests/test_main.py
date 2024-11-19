# pylint: disable=C0116

from fastapi.testclient import TestClient
import pytest

from app.main import app
from app.utils.config import settings


@pytest.fixture(name="client")
def setup_test_client():
    with TestClient(app) as client:
        yield client


def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.url == "http://testserver/docs"


def test_swagger_ui_html(client):
    # Test default behavior
    response = client.get("/docs")
    assert response.status_code == 200
    assert "Swagger UI" in response.text
    assert "openapi.json" in response.text
    assert "/favicon.ico" in response.text
    assert settings.PROJECT_NAME in response.text
