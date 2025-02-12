"""
Shared test fixtures and configuration.
"""
import os
import pytest
from unittest.mock import patch
import yaml

@pytest.fixture
def sample_monitor_dict():
    """Return a sample monitor dictionary."""
    return {
        "name": "Test Monitor",
        "type": "metric alert",
        "query": "avg(last_5m):avg:system.cpu.user{*} > 80",
        "message": "Test message",
        "tags": ["env:test", "service:test"],
        "priority": 1,
        "options": {
            "notify_no_data": True,
            "no_data_timeframe": 10,
            "thresholds": {
                "critical": 80,
                "warning": 70,
                "ok": 60
            }
        }
    }

@pytest.fixture
def sample_config():
    """Return a sample configuration dictionary."""
    return {
        "monitors": [
            {
                "name": "Test CPU Monitor",
                "type": "metric alert",
                "query": "avg(last_5m):avg:system.cpu.user{*} > 90",
                "message": "Test CPU alert",
                "tags": ["env:test"],
                "priority": 3,
                "options": {
                    "notify_no_data": True,
                    "thresholds": {
                        "critical": 90,
                        "warning": 80
                    }
                }
            }
        ]
    }

@pytest.fixture
def mock_env_vars():
    """Mock environment variables."""
    with patch.dict(os.environ, {
        "DD_API_KEY": "test-api-key",
        "DD_APP_KEY": "test-app-key",
        "DD_ENV": "test"
    }):
        yield

@pytest.fixture
def temp_config_file(sample_config, tmp_path):
    """Create a temporary configuration file."""
    config_file = tmp_path / "test_config.yaml"
    with open(config_file, "w") as f:
        yaml.dump(sample_config, f)
    return str(config_file)

@pytest.fixture
def mock_api_response():
    """Return mock API response data."""
    return {
        "id": "test-monitor-id",
        "name": "Test Monitor",
        "type": "metric alert",
        "query": "avg(last_5m):avg:system.cpu.user{*} > 80",
        "message": "Test message",
        "tags": ["env:test"],
        "options": {
            "notify_no_data": True,
            "thresholds": {
                "critical": 80,
                "warning": 70
            }
        },
        "overall_state": "OK",
        "created": "2024-02-11T00:00:00.000Z",
        "modified": "2024-02-11T00:00:00.000Z"
    } 