"""
Linux System Metrics Collector

Collects CPU, memory, and disk metrics using psutil.
Provides a method to periodically print these metrics.
"""

import json
import logging
import socket
import time
from datetime import datetime, timezone
from typing import Any, Dict

import psutil
import requests
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

from monitor_service.utils import load_config


class MetricCollector:
    """
    Simple system metrics collector for Linux.
    Provides methods to collect CPU, memory, and disk metrics.
    Loads configuration from config.yaml for:
      - metrics collection interval
      - cloud endpoint & credentials
      - threshold values for alerting
    Adds:
      - Structured JSON logging (timestamp, level, message)
      - Robust error handling and retries
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
        self.logger = self._setup_logger()

    def _setup_logger(self):
        logger = logging.getLogger("MetricCollector")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(JSONLogFormatter())
        if not logger.hasHandlers():
            logger.addHandler(handler)
        return logger

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

    def send_metrics(self, metrics: dict) -> None:
        """
        Send metrics to the configured cloud endpoint as a JSON payload.
        Includes timestamp and hostname. Logs success or error.
        """
        if not self.cloud_endpoint:
            self.logger.warning(
                {"event": "no_cloud_endpoint", "msg": "No cloud endpoint configured."}
            )
            return
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "hostname": socket.gethostname(),
            "metrics": metrics,
        }
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.cloud_api_key,
        }
        try:
            response = requests.post(
                self.cloud_endpoint, json=payload, headers=headers, timeout=5
            )
            response.raise_for_status()
            self.logger.info({"event": "metrics_sent", "response": response.json()})
        except Exception as e:
            self.logger.error({"event": "send_error", "error": str(e)})

    def _get_influxdb_config(self):
        """
        Get InfluxDB configuration.
        """
        return self.config.get("influxdb", {})

    def _format_point(self, metric_type, values, hostname, ts):
        """
        Format a single metric point for InfluxDB.
        """
        point = Point(metric_type).tag("host", hostname).time(ts)
        for k, v in values.items():
            if k == "per_core_usage" and isinstance(v, list):
                for i, core_usage in enumerate(v):
                    point = point.field(f"core_{i}", float(core_usage))
            elif isinstance(v, (int, float)):
                point = point.field(k, float(v))
        return point

    def _format_disk_points(self, values, hostname, ts):
        """
        Format disk metric points for InfluxDB.
        """
        points = []
        for mount, stats in values.items():
            point = Point("disk").tag("host", hostname).tag("mount", mount).time(ts)
            for k, v in stats.items():
                point = point.field(k, float(v) if isinstance(v, (int, float)) else 0)
            points.append(point)
        return points

    def write_metrics_influxdb(self, metrics: dict) -> None:
        """
        Write metrics to InfluxDB if configured.
        """
        influx_conf = self._get_influxdb_config()
        url = influx_conf.get("url")
        token = influx_conf.get("token")
        org = influx_conf.get("org")
        bucket = influx_conf.get("bucket")
        if not (url and token and org and bucket):
            self.logger.warning(
                {"event": "no_influxdb_config", "msg": "No InfluxDB config provided."}
            )
            return
        try:
            with InfluxDBClient(url=url, token=token, org=org) as client:
                write_api = client.write_api(write_options=SYNCHRONOUS)
                ts = datetime.now(timezone.utc)
                hostname = socket.gethostname()
                for metric_type, values in metrics.items():
                    if metric_type == "disk":
                        points = self._format_disk_points(values, hostname, ts)
                        write_api.write(bucket=bucket, org=org, record=points)
                    else:
                        point = self._format_point(metric_type, values, hostname, ts)
                        write_api.write(bucket=bucket, org=org, record=point)
                self.logger.info(
                    {"event": "metrics_written_influxdb", "bucket": bucket}
                )
        except Exception as e:
            self.logger.error({"event": "influxdb_error", "error": str(e)})

    def _collect_and_send_metrics(self):
        """
        Collect all metrics and send them to the configured endpoints.
        """
        cpu = self.collect_cpu_metrics()
        memory = self.collect_memory_metrics()
        disk = self.collect_disk_metrics()
        self.logger.info(
            {
                "event": "metrics_collected",
                "cpu": cpu,
                "memory": memory,
                "disk": disk,
            }
        )
        metrics = {
            "cpu": cpu,
            "memory": memory,
            "disk": disk,
        }
        self.send_metrics(metrics)
        self.write_metrics_influxdb(metrics)

    def monitor_periodically(self, interval: int = None) -> None:
        """
        Periodically collect and print system metrics every `interval` seconds.
        Press Ctrl+C to stop.
        Interval is loaded from config.yaml if not provided.
        Logs metrics and errors in structured JSON format.
        Retries metric collection up to 3 times on error.
        """
        if interval is None:
            interval = self.interval
        self.logger.info(
            {
                "event": "start_monitoring",
                "interval": interval,
                "cloud_endpoint": self.cloud_endpoint,
                "alert_thresholds": {
                    "cpu": self.cpu_threshold,
                    "memory": self.memory_threshold,
                    "disk": self.disk_threshold,
                },
            }
        )
        try:
            while True:
                for attempt in range(1, 4):
                    try:
                        self._collect_and_send_metrics()
                        break
                    except Exception as e:
                        self.logger.error(
                            {
                                "event": "collection_error",
                                "error": str(e),
                                "attempt": attempt,
                            }
                        )
                        if attempt == 3:
                            self.logger.error(
                                {
                                    "event": "max_retries_exceeded",
                                    "error": str(e),
                                }
                            )
                        else:
                            time.sleep(2)
                time.sleep(interval)
        except KeyboardInterrupt:
            self.logger.info({"event": "stopped"})


class JSONLogFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        # If the message is a dict, merge it
        if isinstance(record.msg, dict):
            log_record.update(record.msg)
        return json.dumps(log_record)


if __name__ == "__main__":
    # Example usage: print metrics once
    collector = MetricCollector()
    collector.logger.info(
        {
            "event": "single_collection",
            "cpu": collector.collect_cpu_metrics(),
            "memory": collector.collect_memory_metrics(),
            "disk": collector.collect_disk_metrics(),
        }
    )
    # Uncomment below to run periodic monitoring
    collector.monitor_periodically(interval=collector.interval)
