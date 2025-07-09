"""
Alerting module for Linux Resources Monitoring Service.
- Reads thresholds and alerting config from config.yaml
- Checks metrics and triggers alerts via email, Slack, or logs
- Implements a cooldown window to avoid duplicate alerts
"""

import logging
import smtplib
import time
from email.mime.text import MIMEText
from typing import Any, Dict

import requests

_last_alert_times = {}


def check_thresholds(metrics: Dict[str, float], config: Dict[str, Any]):
    """
    Check metrics against thresholds and trigger alerts if needed.
    Args:
        metrics: Dict of metric name to value (e.g., {'cpu': 95.0})
        config: Parsed config dict
    """
    alerting = config.get("alerting", {})
    cooldown = alerting.get("cooldown_seconds", 600)
    now = time.time()
    for metric, value in metrics.items():
        threshold = alerting.get(f"{metric}_threshold")
        if threshold is not None and value > threshold:
            last_time = _last_alert_times.get(metric, 0)
            if now - last_time > cooldown:
                msg = (
                    f"ALERT: {metric.upper()} is {value}, "
                    f"exceeds threshold {threshold}!"
                )
                send_alert(msg, alerting)
                _last_alert_times[metric] = now


def send_alert(message: str, alerting: Dict[str, Any]):
    """
    Send alert via enabled channels (email, Slack, logs).
    """
    if alerting.get("email", {}).get("enabled"):
        send_email_alert(message, alerting["email"])
    if alerting.get("slack", {}).get("enabled"):
        send_slack_alert(message, alerting["slack"])
    log_alert(message)


def send_email_alert(message: str, email_cfg: Dict[str, Any]):
    """
    Send an email alert using SMTP.
    """
    try:
        msg = MIMEText(message)
        msg["Subject"] = "Linux Resource Alert"
        msg["From"] = email_cfg["username"]
        msg["To"] = email_cfg["to"]
        with smtplib.SMTP(email_cfg["smtp_server"], email_cfg["smtp_port"]) as server:
            server.starttls()
            server.login(email_cfg["username"], email_cfg["password"])
            server.sendmail(email_cfg["username"], [email_cfg["to"]], msg.as_string())
    except Exception as e:
        logging.error(f"Failed to send email alert: {e}")


def send_slack_alert(message: str, slack_cfg: Dict[str, Any]):
    """
    Send a Slack alert using webhook.
    """
    try:
        payload = {"text": message}
        resp = requests.post(slack_cfg["webhook_url"], json=payload, timeout=5)
        if resp.status_code != 200:
            logging.error(f"Slack alert failed: {resp.text}")
    except Exception as e:
        logging.error(f"Failed to send Slack alert: {e}")


def log_alert(message: str):
    """
    Log the alert message.
    """
    logging.warning(message)
