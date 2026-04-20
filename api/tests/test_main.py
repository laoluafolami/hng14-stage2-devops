import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch


@pytest.fixture
def mock_redis():
    """Return a mock Redis instance."""
    with patch("main.r") as mock_r:
        mock_r.ping.return_value = True
        mock_r.lpush.return_value = 1
        mock_r.hset.return_value = 1
        mock_r.hget.return_value = b"queued"
        yield mock_r


@pytest.fixture
def client(mock_redis):
    from main import app
    return TestClient(app)


def test_health_endpoint(client):
    """Test that /health returns ok without requiring Redis."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_job(client, mock_redis):
    """Test that POST /jobs creates a job and returns a job_id."""
    response = client.post("/jobs")
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert len(data["job_id"]) == 36  # UUID format


def test_get_job_found(client, mock_redis):
    """Test GET /jobs/{id} returns status when job exists."""
    mock_redis.hget.return_value = b"queued"
    response = client.get("/jobs/test-job-id-123")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "queued"
    assert data["job_id"] == "test-job-id-123"


def test_get_job_not_found(client, mock_redis):
    """Test GET /jobs/{id} returns error when job does not exist."""
    mock_redis.hget.return_value = None
    response = client.get("/jobs/nonexistent-id")
    assert response.status_code == 200
    data = response.json()
    assert "error" in data
    assert data["error"] == "not found"


def test_create_job_pushes_to_redis_queue(client, mock_redis):
    """Test that creating a job pushes to the correct Redis queue."""
    response = client.post("/jobs")
    assert response.status_code == 200
    job_id = response.json()["job_id"]
    mock_redis.lpush.assert_called_once_with("jobs", job_id)