"""
Linux System Metrics Collector

This module provides a comprehensive system monitoring solution using psutil.
It collects CPU, memory, and disk metrics with proper error handling and logging.

Author: SRE Team
Version: 1.0.0
"""

import gc
import logging
import signal
import threading
import time
import tracemalloc
from datetime import datetime
from typing import Any, Dict

import psutil


class MetricCollector:
    """
    A class to collect system metrics from Linux systems.

    This class provides methods to gather CPU, memory, and disk metrics
    using the psutil library. It includes error handling, logging, and
    structured data collection for monitoring purposes.

    Attributes:
        logger: A logging instance for recording events and errors
        performance_stats: Dictionary to store performance statistics
        memory_tracker: Flag to enable memory tracking
        shutdown_event: Threading event to signal shutdown
        running: Flag to track if monitoring is running
    """

    def __init__(self, enable_memory_tracking: bool = False):
        """
        Initialize the MetricCollector with logging setup.

        Args:
            enable_memory_tracking: If True, enables memory leak detection
        """
        self.setup_logging()
        self.performance_stats = {
            "cpu_collection_times": [],
            "memory_collection_times": [],
            "disk_collection_times": [],
            "total_collections": 0,
            "errors": 0,
            "start_time": datetime.now(),
            "shutdown_time": None,
        }
        self.memory_tracker = enable_memory_tracking
        self.shutdown_event = threading.Event()
        self.running = False

        if self.memory_tracker:
            tracemalloc.start()
            self.logger.info("Memory tracking enabled")

        # Setup signal handlers for graceful shutdown
        self._setup_signal_handlers()

    def _setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown."""
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        # On Windows, also handle SIGBREAK
        if hasattr(signal, "SIGBREAK"):
            signal.signal(signal.SIGBREAK, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """
        Handle shutdown signals gracefully.

        Args:
            signum: Signal number
            frame: Current stack frame
        """
        signal_name = signal.Signals(signum).name
        self.logger.info(
            f"Received signal {signal_name} ({signum}), initiating graceful shutdown..."
        )
        print(f"\n🛑 Received {signal_name} signal. Initiating graceful shutdown...")

        # Set shutdown event to stop the monitoring loop
        self.shutdown_event.set()

    def setup_logging(self):
        """
        Configure logging for the metric collector.

        Sets up basic logging configuration with timestamp, log level,
        and message format. This helps in debugging and monitoring
        the collector's operation.
        """
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger(__name__)

    def _measure_performance(self, func_name: str, func):
        """
        Measure performance of a function execution.

        Args:
            func_name: Name of the function being measured
            func: Function to execute and measure

        Returns:
            tuple: (result, execution_time)
        """
        start_time = time.time()
        start_memory = tracemalloc.get_traced_memory()[0] if self.memory_tracker else 0

        try:
            result = func()
            execution_time = time.time() - start_time

            if self.memory_tracker:
                end_memory = tracemalloc.get_traced_memory()[0]
                memory_used = end_memory - start_memory
                self.logger.debug(
                    f"{func_name} took {execution_time:.3f}s, used {memory_used} bytes"
                )

            # Store performance stats
            if func_name == "cpu_metrics":
                self.performance_stats["cpu_collection_times"].append(execution_time)
            elif func_name == "memory_metrics":
                self.performance_stats["memory_collection_times"].append(execution_time)
            elif func_name == "disk_metrics":
                self.performance_stats["disk_collection_times"].append(execution_time)

            return result, execution_time

        except Exception as e:
            execution_time = time.time() - start_time
            self.performance_stats["errors"] += 1
            self.logger.error(f"{func_name} failed after {execution_time:.3f}s: {e}")
            return None, execution_time

    def collect_cpu_metrics(self):
        """
        Collect comprehensive CPU metrics from the system.

        Gathers CPU utilization (overall and per-core), CPU count,
        and frequency information using psutil.

        Returns:
            dict: A dictionary containing CPU metrics with keys:
                - cpu_usage: Overall CPU usage percentage
                - cpu_count: Number of logical CPU cores
                - per_core_usage: List of CPU usage per core
                - frequency: Dictionary with current, min, max frequencies
            None: If an error occurs during collection

        Raises:
            Exception: Logs any errors that occur during metric collection
        """

        def _collect_cpu():
            # Get overall CPU usage (waits 1 second for accurate measurement)
            cpu_usage = psutil.cpu_percent(interval=1)

            # Get number of logical CPU cores
            cpu_count = psutil.cpu_count(logical=True)

            # Get per-core CPU usage
            per_core_cpu_usage = psutil.cpu_percent(interval=1, percpu=True)

            # Get CPU frequency information
            cpu_freq = psutil.cpu_freq()

            return {
                "cpu_usage": cpu_usage,
                "cpu_count": cpu_count,
                "per_core_usage": per_core_cpu_usage,
                "frequency": {
                    "current": cpu_freq.current,
                    "min": cpu_freq.min,
                    "max": cpu_freq.max,
                },
            }

        result, execution_time = self._measure_performance("cpu_metrics", _collect_cpu)

        if result is None:
            self.logger.error(
                f"Error collecting CPU metrics after {execution_time:.3f}s"
            )
            return None

        return result

    def collect_memory_metrics(self):
        """
        Collect memory usage metrics from the system.

        Gathers total, used, and free memory information along with
        usage percentage using psutil's virtual_memory() function.

        Returns:
            dict: A dictionary containing memory metrics with keys:
                - total_gb: Total memory in gigabytes
                - used_gb: Used memory in gigabytes
                - free_gb: Free memory in gigabytes
                - percent: Memory usage percentage
            None: If an error occurs during collection

        Raises:
            Exception: Logs any errors that occur during metric collection
        """

        def _collect_memory():
            # Get virtual memory information
            memory = psutil.virtual_memory()

            # Convert bytes to gigabytes for readability
            bytes_to_gb = 1024**3

            return {
                "total_gb": memory.total / bytes_to_gb,
                "used_gb": memory.used / bytes_to_gb,
                "free_gb": memory.free / bytes_to_gb,
                "percent": memory.percent,
            }

        result, execution_time = self._measure_performance(
            "memory_metrics", _collect_memory
        )

        if result is None:
            self.logger.error(
                f"Error collecting memory metrics after {execution_time:.3f}s"
            )
            return None

        return result

    def collect_disk_metrics(self):
        """
        Collect disk usage metrics for all accessible filesystems.

        Iterates through all disk partitions and collects usage information
        for each accessible filesystem. Handles permission errors gracefully.

        Returns:
            list: A list of dictionaries, each containing disk metrics with keys:
                - device: Device name (e.g., '/dev/sda1')
                - mountpoint: Mount point path (e.g., '/')
                - total_gb: Total disk space in gigabytes
                - used_gb: Used disk space in gigabytes
                - free_gb: Free disk space in gigabytes
                - percent: Disk usage percentage
            None: If an error occurs during collection

        Note:
            Skips filesystems that require elevated permissions or are not accessible.
        """

        def _collect_disk():
            disk_data = []

            # Iterate through all disk partitions
            for partition in psutil.disk_partitions():
                try:
                    # Get disk usage for this partition
                    partition_usage = psutil.disk_usage(partition.mountpoint)

                    # Convert bytes to gigabytes
                    bytes_to_gb = 1024**3

                    disk_data.append(
                        {
                            "device": partition.device,
                            "mountpoint": partition.mountpoint,
                            "total_gb": partition_usage.total / bytes_to_gb,
                            "used_gb": partition_usage.used / bytes_to_gb,
                            "free_gb": partition_usage.free / bytes_to_gb,
                            "percent": partition_usage.percent,
                        }
                    )

                except PermissionError:
                    # Log warning for permission-denied filesystems
                    self.logger.warning(
                        f"No permission to access {partition.mountpoint}"
                    )
                    continue
                except Exception as e:
                    # Log error for other partition access issues
                    self.logger.error(
                        f"Error accessing partition {partition.device}: {e}"
                    )
                    continue

            return disk_data

        result, execution_time = self._measure_performance(
            "disk_metrics", _collect_disk
        )

        if result is None:
            self.logger.error(
                f"Error collecting disk metrics after {execution_time:.3f}s"
            )
            return None

        return result

    def collect_final_metrics(self):
        """
        Collect final metrics before shutdown.

        This method collects one final set of metrics and logs them
        for shutdown analysis.

        Returns:
            dict: Final metrics collection
        """
        self.logger.info("Collecting final metrics before shutdown...")
        print("\n📊 Collecting final metrics...")

        final_metrics = {
            "timestamp": datetime.now().isoformat(),
            "cpu": self.collect_cpu_metrics(),
            "memory": self.collect_memory_metrics(),
            "disk": self.collect_disk_metrics(),
        }

        # Log final metrics
        self.logger.info(f"Final metrics collected: {final_metrics}")

        return final_metrics

    def cleanup(self):
        """
        Perform cleanup operations before shutdown.

        This method handles all cleanup tasks including:
        - Stopping memory tracking
        - Final garbage collection
        - Logging final statistics
        """
        self.logger.info("Starting cleanup process...")
        print("\n🧹 Performing cleanup...")

        # Record shutdown time
        self.performance_stats["shutdown_time"] = datetime.now()

        # Stop memory tracking if enabled
        if self.memory_tracker:
            tracemalloc.stop()
            self.logger.info("Memory tracking stopped")

        # Force garbage collection
        gc.collect()
        self.logger.info("Garbage collection completed")

        # Log final statistics
        self._log_final_statistics()

        self.logger.info("Cleanup completed successfully")
        print("✅ Cleanup completed")

    def _log_final_statistics(self):
        """Log final statistics for the monitoring session."""
        stats = self.get_performance_stats()

        # Calculate runtime
        runtime = (
            self.performance_stats["shutdown_time"]
            - self.performance_stats["start_time"]
        )

        self.logger.info("=" * 60)
        self.logger.info("FINAL MONITORING SESSION STATISTICS")
        self.logger.info("=" * 60)
        self.logger.info(f"Session Duration: {runtime}")
        self.logger.info(f"Total Collections: {stats['total_collections']}")
        self.logger.info(f"Errors: {stats['errors']} ({stats['error_rate']:.1f}%)")

        if "avg_cpu_time" in stats:
            self.logger.info(
                f"Average CPU Collection Time: {stats['avg_cpu_time']:.3f}s"
            )
        if "avg_memory_time" in stats:
            self.logger.info(
                f"Average Memory Collection Time: {stats['avg_memory_time']:.3f}s"
            )
        if "avg_disk_time" in stats:
            self.logger.info(
                f"Average Disk Collection Time: {stats['avg_disk_time']:.3f}s"
            )

        self.logger.info("=" * 60)

    def get_performance_stats(self) -> Dict[str, Any]:
        """
        Get performance statistics for the metric collector.

        Returns:
            dict: Performance statistics including:
                - Average collection times for each metric type
                - Total number of collections
                - Number of errors
                - Memory usage (if tracking enabled)
        """
        stats = {
            "total_collections": self.performance_stats["total_collections"],
            "errors": self.performance_stats["errors"],
            "error_rate": (
                self.performance_stats["errors"]
                / max(self.performance_stats["total_collections"], 1)
            )
            * 100,
        }

        # Calculate averages
        if self.performance_stats["cpu_collection_times"]:
            stats["avg_cpu_time"] = sum(
                self.performance_stats["cpu_collection_times"]
            ) / len(self.performance_stats["cpu_collection_times"])
        if self.performance_stats["memory_collection_times"]:
            stats["avg_memory_time"] = sum(
                self.performance_stats["memory_collection_times"]
            ) / len(self.performance_stats["memory_collection_times"])
        if self.performance_stats["disk_collection_times"]:
            stats["avg_disk_time"] = sum(
                self.performance_stats["disk_collection_times"]
            ) / len(self.performance_stats["disk_collection_times"])

        # Add memory tracking if enabled
        if self.memory_tracker:
            current_memory = tracemalloc.get_traced_memory()
            stats["memory_usage"] = {
                "current": current_memory[0],
                "peak": current_memory[1],
            }

        return stats

    def print_metrics(self, cpu_data, memory_data, disk_data):
        """
        Print collected metrics in a formatted, human-readable way.

        Displays all collected metrics with proper formatting and handles
        cases where metric collection failed.

        Args:
            cpu_data (dict): CPU metrics dictionary or None
            memory_data (dict): Memory metrics dictionary or None
            disk_data (list): List of disk metrics dictionaries or None
        """
        # Print header with timestamp
        print("\n" + "=" * 60)
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

        # Print CPU metrics
        if cpu_data:
            print(f"CPU Usage: {cpu_data['cpu_usage']}%")
            print(f"Number of CPUs: {cpu_data['cpu_count']}")
            print(f"Per-Core Usage: {cpu_data['per_core_usage']}")
            print(f"CPU Frequency: {cpu_data['frequency']['current']:.2f} MHz")
        else:
            print("CPU metrics: Error collecting data")

        # Print memory metrics
        if memory_data:
            print(f"Total Memory: {memory_data['total_gb']:.2f} GB")
            print(f"Used Memory: {memory_data['used_gb']:.2f} GB")
            print(f"Free Memory: {memory_data['free_gb']:.2f} GB")
            print(f"Memory Usage: {memory_data['percent']}%")
        else:
            print("Memory metrics: Error collecting data")

        # Print disk metrics
        if disk_data:
            print("\nDisk Usage:")
            for disk in disk_data:
                print(f"Filesystem: {disk['device']}")
                print(f"  Mount Point: {disk['mountpoint']}")
                print(f"  Total: {disk['total_gb']:.2f} GB")
                print(f"  Used: {disk['used_gb']:.2f} GB")
                print(f"  Free: {disk['free_gb']:.2f} GB")
                print(f"  Usage: {disk['percent']}%")
                print()
        else:
            print("Disk metrics: Error collecting data")

    def run_monitoring(self, interval=5):
        """
        Run continuous monitoring with specified collection interval.

        Starts a continuous monitoring loop that collects metrics at regular
        intervals. Handles graceful shutdown on keyboard interrupt or signals.

        Args:
            interval (int): Time interval between metric collections in seconds.
                          Default is 5 seconds.

        Note:
            To stop monitoring, press Ctrl+C (SIGINT) or send SIGTERM.
        """
        self.running = True
        self.logger.info(f"Starting metric collection with {interval}s interval")
        print(f"🚀 Starting monitoring with {interval}s interval...")
        print("Press Ctrl+C to stop gracefully")

        try:
            while self.running and not self.shutdown_event.is_set():
                # Collect all metrics
                cpu_data = self.collect_cpu_metrics()
                memory_data = self.collect_memory_metrics()
                disk_data = self.collect_disk_metrics()

                # Update collection count
                self.performance_stats["total_collections"] += 1

                # Print results
                self.print_metrics(cpu_data, memory_data, disk_data)

                # Print performance stats every 10 collections
                if self.performance_stats["total_collections"] % 10 == 0:
                    self._print_performance_summary()

                # Wait before next collection (with shutdown check)
                if not self.shutdown_event.is_set():
                    print(f"Waiting {interval} seconds...")
                    # Wait in smaller intervals to check for shutdown
                    for _ in range(interval):
                        if self.shutdown_event.wait(1):
                            break

        except KeyboardInterrupt:
            self.logger.info("Received KeyboardInterrupt, initiating graceful shutdown")
            print("\n🛑 Received interrupt signal. Shutting down gracefully...")
        except Exception as e:
            self.logger.error(f"Unexpected error during monitoring: {e}")
            print(f"❌ Unexpected error occurred: {e}")
        finally:
            self._graceful_shutdown()

    def _graceful_shutdown(self):
        """Perform graceful shutdown sequence."""
        self.running = False
        self.logger.info("Starting graceful shutdown sequence...")
        print("\n🔄 Starting graceful shutdown...")

        try:
            # Collect final metrics
            self.collect_final_metrics()

            # Print final performance summary
            self._print_final_performance_summary()

            # Perform cleanup
            self.cleanup()

            self.logger.info("Graceful shutdown completed successfully")
            print("✅ Graceful shutdown completed successfully!")

        except Exception as e:
            self.logger.error(f"Error during graceful shutdown: {e}")
            print(f"❌ Error during shutdown: {e}")
        finally:
            # Ensure cleanup happens even if there are errors
            if self.memory_tracker:
                try:
                    tracemalloc.stop()
                except Exception:
                    pass

    def _print_performance_summary(self):
        """Print a summary of performance statistics."""
        stats = self.get_performance_stats()
        print("\n" + "-" * 40)
        print("PERFORMANCE SUMMARY")
        print("-" * 40)
        print(f"Total Collections: {stats['total_collections']}")
        print(f"Errors: {stats['errors']} ({stats['error_rate']:.1f}%)")

        if "avg_cpu_time" in stats:
            print(f"Avg CPU Collection Time: {stats['avg_cpu_time']:.3f}s")
        if "avg_memory_time" in stats:
            print(f"Avg Memory Collection Time: {stats['avg_memory_time']:.3f}s")
        if "avg_disk_time" in stats:
            print(f"Avg Disk Collection Time: {stats['avg_disk_time']:.3f}s")

        if self.memory_tracker and "memory_usage" in stats:
            current_mb = stats["memory_usage"]["current"] / (1024 * 1024)
            peak_mb = stats["memory_usage"]["peak"] / (1024 * 1024)
            print(f"Memory Usage: {current_mb:.1f}MB (Peak: {peak_mb:.1f}MB)")

        print("-" * 40)

    def _print_final_performance_summary(self):
        """Print final performance summary when monitoring stops."""
        print("\n" + "=" * 50)
        print("FINAL PERFORMANCE SUMMARY")
        print("=" * 50)
        self._print_performance_summary()

        # Calculate runtime
        if self.performance_stats["shutdown_time"]:
            runtime = (
                self.performance_stats["shutdown_time"]
                - self.performance_stats["start_time"]
            )
            print(f"Total Runtime: {runtime}")

        # Force garbage collection
        gc.collect()
        if self.memory_tracker:
            final_memory = tracemalloc.get_traced_memory()
            final_mb = final_memory[0] / (1024 * 1024)
            print(f"Final Memory Usage: {final_mb:.1f}MB")

        print("=" * 50)


def main():
    """
    Main function to run the metric collector.

    Creates a MetricCollector instance and starts monitoring
    with a 5-second interval and memory tracking enabled.
    """
    # Enable memory tracking for development/debugging
    collector = MetricCollector(enable_memory_tracking=True)
    collector.run_monitoring(interval=5)


# Entry point for the script
if __name__ == "__main__":
    main()
