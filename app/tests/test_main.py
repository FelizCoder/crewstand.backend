# pylint: disable=C0116

from fastapi.testclient import TestClient

from app.main import app
from app.utils.config import settings

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World. This is the swncrew backend"}


def test_swagger_ui_html():
    # Test default behavior
    response = client.get("/docs")
    assert response.status_code == 200
    assert "Swagger UI" in response.text
    assert "openapi.json" in response.text
    assert "/favicon.ico" in response.text
    assert settings.PROJECT_NAME in response.text
