"""
Linux Resources Monitoring Service Package

A comprehensive system monitoring solution for Linux systems.
Provides CPU, memory, and disk metric collection with alerting capabilities.

Author: SRE Team
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "SRE Team"
__description__ = "Linux system monitoring service"

# Import main classes for easy access
from .metric_collector import MetricCollector

# Define what gets imported with "from monitor_service import *"
__all__ = [
    "MetricCollector",
]

# Package initialization
print(f"Loading {__description__} v{__version__}...")
