import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_spec_model():
    mock = MagicMock()
    mock.id = "123e4567-e89b-12d3-a456-426614174000"
    mock.title = "test_api.json"
    mock.format = "json"
    mock.created_at = "2026-04-17T12:00:00Z"
    return mock


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to API Doc Assistant!"}


@patch("app.api.upload.SpecificationService.process_and_save", new_callable=AsyncMock)
def test_upload_specification(mock_process_and_save, client, mock_spec_model):

    mock_process_and_save.return_value = mock_spec_model

    file_content = b'{"openapi": "3.0.0", "info": {"title": "Test"}, "paths": {}}'
    files = {"file": ("test_api.json", file_content, "application/json")}

    response = client.post("/api/v1/upload", files=files)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == mock_spec_model.id
    assert data["format"] == mock_spec_model.format
