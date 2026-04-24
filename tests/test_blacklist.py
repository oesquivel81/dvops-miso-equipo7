import pytest
from unittest.mock import MagicMock, patch
import sys
import os

# Asegurar que el root del proyecto esté en el path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import health as health_module
from health import app


@pytest.fixture(autouse=True)
def mock_repository():
    """Reemplaza el repositorio real por un mock en cada prueba."""
    mock_repo = MagicMock()
    health_module.blacklist_service.repository = mock_repo
    yield mock_repo


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ─────────────────────────────────────────────
# GET /health
# ─────────────────────────────────────────────

class TestHealth:
    def test_health_returns_200(self, client):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_healthy(self, client):
        response = client.get("/health")
        assert b"healthy" in response.data


# ─────────────────────────────────────────────
# GET /blacklists/
# ─────────────────────────────────────────────

class TestGetAllBlacklist:
    def test_get_all_returns_200(self, client, mock_repository):
        mock_repository.get_all.return_value = []
        response = client.get("/blacklists/")
        assert response.status_code == 200

    def test_get_all_returns_status_ok(self, client, mock_repository):
        mock_repository.get_all.return_value = []
        response = client.get("/blacklists/")
        data = response.get_json()
        assert data["status"] == "ok"

    def test_get_all_returns_list_of_emails(self, client, mock_repository):
        mock_repository.get_all.return_value = [
            {"email": "test@example.com", "blocked_reason": "spam"}
        ]
        response = client.get("/blacklists/")
        data = response.get_json()
        assert len(data["data"]) == 1
        assert data["data"][0]["email"] == "test@example.com"

    def test_get_all_returns_empty_list(self, client, mock_repository):
        mock_repository.get_all.return_value = []
        response = client.get("/blacklists/")
        data = response.get_json()
        assert data["data"] == []


# ─────────────────────────────────────────────
# GET /blacklists/<email>
# ─────────────────────────────────────────────

class TestGetBlacklistByEmail:
    def test_get_existing_email_returns_200(self, client, mock_repository):
        mock_repository.get_by_email.return_value = {
            "email": "blocked@example.com",
            "blocked_reason": "spam"
        }
        response = client.get("/blacklists/blocked@example.com")
        assert response.status_code == 200

    def test_get_existing_email_returns_data(self, client, mock_repository):
        mock_repository.get_by_email.return_value = {
            "email": "blocked@example.com",
            "blocked_reason": "spam"
        }
        response = client.get("/blacklists/blocked@example.com")
        data = response.get_json()
        assert data["email"] == "blocked@example.com"

    def test_get_nonexistent_email_returns_404(self, client, mock_repository):
        mock_repository.get_by_email.return_value = None
        response = client.get("/blacklists/notfound@example.com")
        assert response.status_code == 404

    def test_get_nonexistent_email_returns_exists_false(self, client, mock_repository):
        mock_repository.get_by_email.return_value = None
        response = client.get("/blacklists/notfound@example.com")
        data = response.get_json()
        assert data["exists"] is False


# ─────────────────────────────────────────────
# POST /blacklists/
# ─────────────────────────────────────────────

class TestAddBlacklist:
    def test_post_valid_email_returns_201(self, client, mock_repository):
        mock_repository.add.return_value = None
        response = client.post("/blacklists/", json={
            "email": "new@example.com",
            "blacklisted": True
        })
        assert response.status_code == 201

    def test_post_valid_email_returns_message(self, client, mock_repository):
        mock_repository.add.return_value = None
        response = client.post("/blacklists/", json={
            "email": "new@example.com",
            "blacklisted": True
        })
        data = response.get_json()
        assert data["message"] == "Email added to blacklist"
        assert data["email"] == "new@example.com"

    def test_post_default_blacklisted_true(self, client, mock_repository):
        mock_repository.add.return_value = None
        response = client.post("/blacklists/", json={"email": "auto@example.com"})
        data = response.get_json()
        assert data["blacklisted"] is True

    def test_post_missing_email_returns_400(self, client, mock_repository):
        response = client.post("/blacklists/", json={"blacklisted": True})
        assert response.status_code == 400

    def test_post_missing_email_returns_error_message(self, client, mock_repository):
        response = client.post("/blacklists/", json={"blacklisted": True})
        data = response.get_json()
        assert "email is required" in data["error"]

    def test_post_calls_repository_add(self, client, mock_repository):
        mock_repository.add.return_value = None
        client.post("/blacklists/", json={"email": "call@example.com"})
        mock_repository.add.assert_called_once()
