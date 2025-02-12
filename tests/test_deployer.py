"""
Tests for the MonitorDeployer class.
"""
import os
import pytest
from unittest.mock import patch, MagicMock
import yaml
from datadog_monitor_deployer.core.deployer import MonitorDeployer
from datadog_monitor_deployer.core.monitor import Monitor

@pytest.fixture
def test_config():
    """Load test configuration."""
    config_path = os.path.join(os.path.dirname(__file__), "test_config.yaml")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

@pytest.fixture
def mock_datadog():
    """Mock Datadog API client."""
    with patch("datadog_monitor_deployer.core.deployer.api") as mock_api:
        yield mock_api

def test_deployer_initialization(mock_datadog):
    """Test deployer initialization."""
    deployer = MonitorDeployer()
    assert deployer is not None
    mock_datadog.Monitor.get_all.assert_called_once()

def test_deployer_validation_error():
    """Test deployer validation with invalid config."""
    deployer = MonitorDeployer()
    
    with pytest.raises(ValueError):
        deployer.validate_config({"invalid": "config"})
        
    with pytest.raises(ValueError):
        deployer.validate_config({"monitors": "not_a_list"})

def test_deployer_deploy_new_monitor(mock_datadog, test_config):
    """Test deploying a new monitor."""
    mock_datadog.Monitor.get_all.return_value = []
    mock_datadog.Monitor.create.return_value = {"id": "test-id-1"}
    
    deployer = MonitorDeployer()
    results = deployer.deploy(test_config)
    
    assert len(results) == 2
    mock_datadog.Monitor.create.assert_called()
    assert not mock_datadog.Monitor.update.called

def test_deployer_update_existing_monitor(mock_datadog, test_config):
    """Test updating an existing monitor."""
    existing_monitor = {
        "id": "test-id-1",
        "name": "Test CPU Monitor"
    }
    mock_datadog.Monitor.get_all.return_value = [existing_monitor]
    mock_datadog.Monitor.update.return_value = {"id": "test-id-1", "updated": True}
    
    deployer = MonitorDeployer()
    results = deployer.deploy(test_config)
    
    assert len(results) == 2
    mock_datadog.Monitor.update.assert_called()

def test_deployer_list_monitors(mock_datadog):
    """Test listing monitors."""
    mock_monitors = [
        {"id": "1", "name": "Test Monitor 1", "type": "metric alert", "tags": ["env:test"]},
        {"id": "2", "name": "Test Monitor 2", "type": "service check", "tags": ["env:prod"]}
    ]
    mock_datadog.Monitor.get_all.return_value = mock_monitors
    
    deployer = MonitorDeployer()
    
    # Test listing all monitors
    monitors = deployer.list_monitors()
    assert len(monitors) == 2
    
    # Test filtering by name
    monitors = deployer.list_monitors(name="Monitor 1")
    assert len(monitors) == 1
    assert monitors[0]["name"] == "Test Monitor 1"
    
    # Test filtering by tags
    monitors = deployer.list_monitors(tags=["env:test"])
    assert len(monitors) == 1
    assert monitors[0]["tags"] == ["env:test"]

def test_deployer_delete_monitor(mock_datadog):
    """Test deleting a monitor."""
    deployer = MonitorDeployer()
    deployer.delete_monitor("test-id")
    
    mock_datadog.Monitor.delete.assert_called_once_with("test-id")

def test_deployer_api_error(mock_datadog):
    """Test handling of API errors."""
    mock_datadog.Monitor.get_all.side_effect = Exception("API Error")
    
    with pytest.raises(ConnectionError):
        MonitorDeployer()

@pytest.mark.parametrize("monitor_id,expected_calls", [
    ("specific-id", 1),  # Test with specific monitor ID
    (None, 0)           # Test without monitor ID
])
def test_deployer_get_specific_monitor(mock_datadog, monitor_id, expected_calls):
    """Test getting a specific monitor."""
    mock_datadog.Monitor.get.return_value = {"id": "specific-id", "name": "Test Monitor"}
    mock_datadog.Monitor.get_all.return_value = []
    
    deployer = MonitorDeployer()
    monitors = deployer.list_monitors(monitor_id=monitor_id)
    
    assert len(monitors) > 0 if monitor_id else len(monitors) == 0
    assert mock_datadog.Monitor.get.call_count == expected_calls 