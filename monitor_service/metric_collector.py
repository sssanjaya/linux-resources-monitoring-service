"""
Linux System Metrics Collector

Collects CPU, memory, and disk metrics using psutil.
Provides a method to periodically print these metrics.
"""

import time
from typing import Any, Dict

import psutil


class MetricCollector:
    """
    Simple system metrics collector for Linux.
    Provides methods to collect CPU, memory, and disk metrics.
    """

    def collect_cpu_metrics(self) -> Dict[str, Any]:
        """Collect basic CPU metrics."""
        return {
            "cpu_usage": psutil.cpu_percent(interval=1),
            "cpu_count": psutil.cpu_count(logical=True),
            "per_core_usage": psutil.cpu_percent(interval=1, percpu=True),
        }

    def collect_memory_metrics(self) -> Dict[str, Any]:
        """
        Collect basic memory metrics.
        Returns a dictionary with total, used, free memory (in GB), and percent used.
        """
        mem = psutil.virtual_memory()
        gb = 1024**3
        return {
            "total_gb": mem.total / gb,
            "used_gb": mem.used / gb,
            "free_gb": mem.free / gb,
            "percent": mem.percent,
        }

    def collect_disk_metrics(self) -> Dict[str, Any]:
        """
        Collect disk usage metrics for all partitions.
        Returns a dictionary with mountpoints as keys and disk usage info as values.
        """
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

    def monitor_periodically(self, interval: int = 5) -> None:
        """
        Periodically collect and print system metrics every `interval` seconds.
        Press Ctrl+C to stop.
        """
        print(f"metrics collection every {interval} seconds. Press Ctrl+C to stop.")
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
    # collector.monitor_periodically(interval=5)
