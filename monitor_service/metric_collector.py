"""
Linux System Metrics Collector

Collects CPU, memory, and disk metrics using psutil.
"""

from typing import Any, Dict

import psutil


class MetricCollector:
    """Simple system metrics collector for Linux."""

    def collect_cpu_metrics(self) -> Dict[str, Any]:
        """Collect basic CPU metrics."""
        return {
            "cpu_usage": psutil.cpu_percent(interval=1),
            "cpu_count": psutil.cpu_count(logical=False),
            "per_core_usage": psutil.cpu_percent(interval=1, percpu=True),
            "frequency": {
                "current": psutil.cpu_freq().current,
                "min": psutil.cpu_freq().min,
                "max": psutil.cpu_freq().max,
            },
        }

    def collect_memory_metrics(self) -> Dict[str, Any]:
        """Collect basic memory metrics."""
        mem = psutil.virtual_memory()
        gb = 1024**3
        return {
            "total_gb": mem.total / gb,
            "used_gb": mem.used / gb,
            "free_gb": mem.free / gb,
            "percent": mem.percent,
        }

    def collect_disk_metrics(self) -> Dict[str, Any]:
        """Collect disk usage metrics for all partitions."""
        disk_metrics = {}
        for part in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(part.mountpoint)
                disk_metrics[part.mountpoint] = {
                    "total_gb": usage.total / (1024**3),
                    "used_gb": usage.used / (1024**3),
                    "free_gb": usage.free / (1024**3),
                    "percent": usage.percent,
                }
            except Exception:
                continue
        return disk_metrics


if __name__ == "__main__":
    collector = MetricCollector()
    print("CPU:", collector.collect_cpu_metrics())
    print("Memory:", collector.collect_memory_metrics())
    print("Disk:", collector.collect_disk_metrics())
