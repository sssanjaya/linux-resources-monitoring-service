"""
Linux System Metrics Collector

Collects CPU, memory, and disk metrics using psutil.
Provides a method to periodically print these metrics.
"""

import time
from typing import Any, Dict

import psutil

from monitor_service.utils import load_config


class MetricCollector:
    """
    Simple system metrics collector for Linux.
    Provides methods to collect CPU, memory, and disk metrics.
    Loads configuration from config.yaml for:
      - metrics collection interval
      - cloud endpoint & credentials
      - threshold values for alerting
    """

    def __init__(self, config_path: str = "config.yaml"):
        self.config = load_config(config_path)
        self.interval = self.config.get("metrics", {}).get("interval")
        self.cloud_endpoint = self.config.get("cloud", {}).get("endpoint", "")
        self.cloud_api_key = self.config.get("cloud", {}).get("api_key", "")
        self.cpu_threshold = self.config.get("alerting", {}).get("cpu_threshold", 90)
        self.memory_threshold = self.config.get("alerting", {}).get(
            "memory_threshold", 80
        )
        self.disk_threshold = self.config.get("alerting", {}).get("disk_threshold", 80)

    def collect_cpu_metrics(self) -> Dict[str, Any]:
        """
        Collect basic CPU metrics.
        Returns a dictionary with CPU usage, count, per-core usage
        """
        return {
            "cpu_usage": psutil.cpu_percent(interval=1),
            "cpu_count": psutil.cpu_count(logical=True),
            "per_core_usage": psutil.cpu_percent(interval=1, percpu=True),
        }

    def collect_memory_metrics(self) -> Dict[str, Any]:
        """
        Collect basic memory metrics.
        Returns a dictionary with total, used, free memory
        (in GB, rounded to 2 decimal places), and percent used.
        """
        mem = psutil.virtual_memory()
        gb = 1024**3
        # GB values are rounded to 2 decimal places for readability
        return {
            "total_gb": round(mem.total / gb, 2),
            "used_gb": round(mem.used / gb, 2),
            "free_gb": round(mem.free / gb, 2),
            "percent": mem.percent,
        }

    def collect_disk_metrics(self) -> Dict[str, Any]:
        """
        Collect disk usage metrics for all partitions.
        Returns a dictionary with mountpoints as keys
        and disk usage info as values.
        GB values are rounded to 2 decimal places.
        """
        disk_metrics = {}
        gb = 1024**3
        for part in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(part.mountpoint)
                # GB values are rounded to 2 decimal places for readability
                disk_metrics[part.mountpoint] = {
                    "total_gb": round(usage.total / gb, 2),
                    "used_gb": round(usage.used / gb, 2),
                    "free_gb": round(usage.free / gb, 2),
                    "percent": usage.percent,
                }
            except Exception:
                continue
        return disk_metrics

    def monitor_periodically(self, interval: int = None) -> None:
        """
        Periodically collect and print system metrics every `interval` seconds.
        Press Ctrl+C to stop.
        Interval is loaded from config.yaml if not provided.
        """
        if interval is None:
            interval = self.interval
        print(f"Metrics collection every {interval} seconds. Press Ctrl+C to stop.")
        print(f"Cloud endpoint: {self.cloud_endpoint}")
        print(
            f"Alert thresholds: CPU={self.cpu_threshold}%, "
            f"Memory={self.memory_threshold}%, Disk={self.disk_threshold}%"
        )
        try:
            while True:
                cpu = self.collect_cpu_metrics()
                memory = self.collect_memory_metrics()
                disk = self.collect_disk_metrics()
                print("\n--- System Metrics ---")
                print("CPU:", cpu)
                print("Memory:", memory)
                print("Disk:", disk)
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\nStopped periodic metrics collection.")


if __name__ == "__main__":
    # Example usage: print metrics once
    collector = MetricCollector()
    print("CPU:", collector.collect_cpu_metrics())
    print("Memory:", collector.collect_memory_metrics())
    print("Disk:", collector.collect_disk_metrics())
    # Uncomment below to run periodic monitoring
    collector.monitor_periodically(interval=collector.interval)
