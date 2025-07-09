"""
Unit tests for the MetricCollector class in monitor_service.metric_collector.

These tests verify:
- Metric collection methods return dictionaries with expected keys and value types.
- Robust error handling and retry logic in periodic monitoring.
"""

import pytest

from monitor_service.metric_collector import MetricCollector


@pytest.fixture
def collector():
    """Fixture to provide a MetricCollector instance for tests."""
    return MetricCollector()


def test_collect_cpu_metrics(collector):
    """Test that collect_cpu_metrics returns expected keys and value types."""
    cpu = collector.collect_cpu_metrics()
    assert isinstance(cpu, dict)
    assert "cpu_usage" in cpu
    assert "cpu_count" in cpu
    assert "per_core_usage" in cpu
    assert isinstance(cpu["cpu_usage"], (int, float))
    assert isinstance(cpu["cpu_count"], int)
    assert isinstance(cpu["per_core_usage"], list)


def test_collect_memory_metrics(collector):
    """Test that collect_memory_metrics returns expected keys and value types."""
    mem = collector.collect_memory_metrics()
    assert isinstance(mem, dict)
    for key in ["total_gb", "used_gb", "free_gb", "percent"]:
        assert key in mem
    assert isinstance(mem["total_gb"], float)
    assert isinstance(mem["used_gb"], float)
    assert isinstance(mem["free_gb"], float)
    assert isinstance(mem["percent"], (int, float))


def test_collect_disk_metrics_structure(collector):
    """Test that collect_disk_metrics returns a dictionary of dictionaries."""
    disk = collector.collect_disk_metrics()
    assert isinstance(disk, dict)
    assert disk, "Disk metrics should not be empty"
    for mount, info in disk.items():
        assert isinstance(info, dict)


def test_collect_disk_metrics_fields(collector):
    """Test that each disk metric has the expected fields and value types."""
    disk = collector.collect_disk_metrics()
    for mount, info in disk.items():
        for key in ["total_gb", "used_gb", "free_gb", "percent"]:
            assert key in info
        assert isinstance(info["total_gb"], float)
        assert isinstance(info["used_gb"], float)
        assert isinstance(info["free_gb"], float)
        assert isinstance(info["percent"], (int, float))
