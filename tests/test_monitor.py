"""
Tests for the Monitor class.
"""
import pytest
from datadog_monitor_deployer.core.monitor import Monitor

def test_monitor_creation():
    """Test basic monitor creation."""
    monitor = Monitor(
        name="Test Monitor",
        type="metric alert",
        query="avg(last_5m):avg:system.cpu.user{*} > 80",
        message="Test message"
    )
    
    assert monitor.name == "Test Monitor"
    assert monitor.type == "metric alert"
    assert monitor.query == "avg(last_5m):avg:system.cpu.user{*} > 80"
    assert monitor.message == "Test message"
    assert monitor.tags == []
    assert monitor.options == {}
    assert monitor.priority is None
    assert monitor.restricted_roles is None

def test_monitor_with_options():
    """Test monitor creation with options."""
    options = {
        "notify_no_data": True,
        "no_data_timeframe": 10,
        "thresholds": {
            "critical": 80,
            "warning": 70
        }
    }
    
    monitor = Monitor(
        name="Test Monitor",
        type="metric alert",
        query="avg(last_5m):avg:system.cpu.user{*} > 80",
        message="Test message",
        options=options
    )
    
    assert monitor.options == options

def test_monitor_to_dict():
    """Test conversion of monitor to dictionary."""
    monitor = Monitor(
        name="Test Monitor",
        type="metric alert",
        query="avg(last_5m):avg:system.cpu.user{*} > 80",
        message="Test message",
        tags=["env:test"],
        priority=1
    )
    
    monitor_dict = monitor.to_dict()
    
    assert monitor_dict["name"] == "Test Monitor"
    assert monitor_dict["type"] == "metric alert"
    assert monitor_dict["query"] == "avg(last_5m):avg:system.cpu.user{*} > 80"
    assert monitor_dict["message"] == "Test message"
    assert monitor_dict["tags"] == ["env:test"]
    assert monitor_dict["priority"] == 1

def test_monitor_from_dict():
    """Test creation of monitor from dictionary."""
    monitor_dict = {
        "name": "Test Monitor",
        "type": "metric alert",
        "query": "avg(last_5m):avg:system.cpu.user{*} > 80",
        "message": "Test message",
        "tags": ["env:test"],
        "priority": 1
    }
    
    monitor = Monitor.from_dict(monitor_dict)
    
    assert monitor.name == "Test Monitor"
    assert monitor.type == "metric alert"
    assert monitor.query == "avg(last_5m):avg:system.cpu.user{*} > 80"
    assert monitor.message == "Test message"
    assert monitor.tags == ["env:test"]
    assert monitor.priority == 1

def test_monitor_validation():
    """Test monitor validation."""
    # Valid monitor
    monitor = Monitor(
        name="Test Monitor",
        type="metric alert",
        query="avg(last_5m):avg:system.cpu.user{*} > 80",
        message="Test message"
    )
    assert monitor.validate() is True
    
    # Invalid monitor - missing name
    with pytest.raises(ValueError, match="Monitor name is required"):
        Monitor(
            name="",
            type="metric alert",
            query="avg(last_5m):avg:system.cpu.user{*} > 80",
            message="Test message"
        ).validate()
    
    # Invalid monitor - missing type
    with pytest.raises(ValueError, match="Monitor type is required"):
        Monitor(
            name="Test Monitor",
            type="",
            query="avg(last_5m):avg:system.cpu.user{*} > 80",
            message="Test message"
        ).validate()
    
    # Invalid monitor - missing query
    with pytest.raises(ValueError, match="Monitor query is required"):
        Monitor(
            name="Test Monitor",
            type="metric alert",
            query="",
            message="Test message"
        ).validate()
    
    # Invalid monitor - missing message
    with pytest.raises(ValueError, match="Monitor message is required"):
        Monitor(
            name="Test Monitor",
            type="metric alert",
            query="avg(last_5m):avg:system.cpu.user{*} > 80",
            message=""
        ).validate() 