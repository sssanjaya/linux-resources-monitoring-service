import socket
from datetime import datetime, timezone

from fastapi.testclient import TestClient

from monitor_service.cloud_ingestion import app


def test_receive_metrics():
    """
    Test that the /api/metrics endpoint accepts a valid payload and returns status ok.
    """
    client = TestClient(app)
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "hostname": socket.gethostname(),
        "metrics": {
            "cpu": {
                "cpu_usage": 10,
                "cpu_count": 4,
                "per_core_usage": [10, 10, 10, 10],
            },
            "memory": {"total_gb": 8, "used_gb": 4, "free_gb": 4, "percent": 50},
            "disk": {
                "/": {"total_gb": 100, "used_gb": 50, "free_gb": 50, "percent": 50}
            },
        },
    }
    response = client.post("/api/metrics", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "received_at" in data
    assert data["hostname"] == payload["hostname"]


def test_root_endpoint():
    """
    Test that the root endpoint returns API information.
    """
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Linux Resources Monitoring API"
    assert data["version"] == "1.0.0"
    assert "endpoints" in data
    assert "health" in data["endpoints"]
    assert "metrics" in data["endpoints"]


def test_health_check():
    """
    Test basic health check endpoint.
    """
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert data["version"] == "1.0.0"
    assert "uptime" in data
    assert isinstance(data["uptime"], (int, float))


def test_readiness_check():
    """
    Test readiness check endpoint.
    """
    client = TestClient(app)
    response = client.get("/health/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert "timestamp" in data
    assert data["version"] == "1.0.0"
    assert "uptime" in data


def test_liveness_check():
    """
    Test liveness check endpoint.
    """
    client = TestClient(app)
    response = client.get("/health/live")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "alive"
    assert "timestamp" in data
    assert data["version"] == "1.0.0"
    assert "uptime" in data


def test_detailed_health_check_status_and_basic_info():
    """
    Test that the detailed health check
    returns the correct status and basic information.
    """
    client = TestClient(app)
    response = client.get("/health/detailed")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert data["version"] == "1.0.0"
    assert "uptime" in data


def test_detailed_health_check_system_info():
    """
    Test the structure and content of the system_info field
    in the detailed health check.
    """
    client = TestClient(app)
    response = client.get("/health/detailed")
    assert response.status_code == 200
    data = response.json()
    assert "system_info" in data
    system_info = data["system_info"]
    assert "hostname" in system_info
    assert "platform" in system_info
    assert "cpu_count" in system_info
    assert "cpu_percent" in system_info


def test_detailed_health_check_memory_usage():
    """
    Test the structure and content of the memory_usage field
    in the detailed health check.
    """
    client = TestClient(app)
    response = client.get("/health/detailed")
    assert response.status_code == 200
    data = response.json()
    assert "memory_usage" in data
    memory_usage = data["memory_usage"]
    assert "total_gb" in memory_usage
    assert "used_gb" in memory_usage
    assert "percent" in memory_usage


def test_detailed_health_check_disk_usage():
    """
    Test the structure and content of the disk_usage field
    in the detailed health check.
    """
    client = TestClient(app)
    response = client.get("/health/detailed")
    assert response.status_code == 200
    data = response.json()
    assert "disk_usage" in data
    disk_usage = data["disk_usage"]
    assert "total_gb" in disk_usage
    assert "used_gb" in disk_usage
    assert "percent" in disk_usage


def test_health_check_response_model():
    """
    Test that health check responses match the expected Pydantic model structure.
    """
    client = TestClient(app)

    # Test basic health check model
    response = client.get("/health")
    data = response.json()
    required_fields = ["status", "timestamp", "version", "uptime"]
    for field in required_fields:
        assert field in data

    # Test detailed health check model
    response = client.get("/health/detailed")
    data = response.json()
    required_fields = [
        "status",
        "timestamp",
        "version",
        "uptime",
        "system_info",
        "memory_usage",
        "disk_usage",
    ]
    for field in required_fields:
        assert field in data
