"""Utility functions for the monitoring service."""

from pathlib import Path
from typing import Any, Dict

import yaml


def load_config(path: str = "config.yaml") -> Dict[str, Any]:
    """
    Load configuration from a YAML file.

    Args:
        path: Path to the configuration file

    Returns:
        Dictionary containing the configuration

    Raises:
        FileNotFoundError: If the configuration file doesn't exist
        yaml.YAMLError: If the YAML file is malformed
    """
    config_path = Path(path)

    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path}")

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing configuration file {path}: {e}")
