import time
from unittest.mock import patch

import pytest

from monitor_service import alerts


@pytest.fixture
def alerting_config():
    return {
        "cpu_threshold": 90,
        "memory_threshold": 80,
        "disk_threshold": 80,
        "cooldown_seconds": 2,  # seconds
        "slack": {"enabled": True, "webhook_url": "http://fake"},
        "email": {
            "enabled": True,
            "smtp_server": "smtp",
            "smtp_port": 25,
            "username": "u",
            "password": "p",
            "to": "t",
        },
        "log": {"enabled": True},
    }


def test_threshold_triggers_alert(monkeypatch, alerting_config):
    triggered = {}

    def fake_send_alert(msg, alerting):
        triggered["called"] = True

    monkeypatch.setattr(alerts, "send_alert", fake_send_alert)
    # Should trigger alert
    alerts.check_thresholds(
        {"cpu": 95}, {"alerting": alerting_config}, {"hostname": "host"}
    )
    assert triggered.get("called")


def test_threshold_no_alert_below(monkeypatch, alerting_config):
    triggered = {}

    def fake_send_alert(msg, alerting):
        triggered["called"] = True

    monkeypatch.setattr(alerts, "send_alert", fake_send_alert)
    # Should NOT trigger alert
    alerts.check_thresholds(
        {"cpu": 50}, {"alerting": alerting_config}, {"hostname": "host"}
    )
    assert not triggered.get("called", False)


def test_cooldown_prevents_alert(monkeypatch, alerting_config):
    alerts._last_alert_times = {}  # Reset cooldown state
    call_count = {"count": 0}

    def fake_send_alert(msg, alerting):
        call_count["count"] += 1

    monkeypatch.setattr(alerts, "send_alert", fake_send_alert)
    # First call triggers
    alerts.check_thresholds(
        {"cpu": 95}, {"alerting": alerting_config}, {"hostname": "host"}
    )
    # Second call within cooldown should not trigger
    alerts.check_thresholds(
        {"cpu": 96}, {"alerting": alerting_config}, {"hostname": "host"}
    )
    assert call_count["count"] == 1
    # Wait for cooldown
    time.sleep(alerting_config["cooldown_seconds"])
    # Should trigger again
    alerts.check_thresholds(
        {"cpu": 97}, {"alerting": alerting_config}, {"hostname": "host"}
    )
    assert call_count["count"] == 2


def test_send_slack_alert(monkeypatch, alerting_config):
    with patch("monitor_service.alerts.requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.text = "ok"
        alerts.send_slack_alert("test message", alerting_config["slack"])
        mock_post.assert_called_once()


def test_send_email_alert(monkeypatch, alerting_config):
    with patch("smtplib.SMTP") as mock_smtp:
        instance = mock_smtp.return_value.__enter__.return_value
        alerts.send_email_alert("test message", alerting_config["email"])
        instance.sendmail.assert_called_once()


def test_log_alert(monkeypatch):
    with patch("logging.warning") as mock_warn:
        alerts.log_alert("test log")
        mock_warn.assert_called_once_with("test log")
