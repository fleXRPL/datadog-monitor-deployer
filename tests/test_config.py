"""
Tests for configuration loading and validation.
"""
import os
import pytest
import tempfile
import yaml
import json
from datadog_monitor_deployer.utils.config import load_config

def test_load_yaml_config():
    """Test loading YAML configuration."""
    config = {
        "monitors": [
            {
                "name": "Test Monitor",
                "type": "metric alert",
                "query": "avg(last_5m):avg:system.cpu.user{*} > 80",
                "message": "Test message"
            }
        ]
    }
    
    with tempfile.NamedTemporaryFile(suffix=".yaml", mode="w", delete=False) as f:
        yaml.dump(config, f)
    
    try:
        loaded_config = load_config(f.name)
        assert loaded_config == config
    finally:
        os.unlink(f.name)

def test_load_json_config():
    """Test loading JSON configuration."""
    config = {
        "monitors": [
            {
                "name": "Test Monitor",
                "type": "metric alert",
                "query": "avg(last_5m):avg:system.cpu.user{*} > 80",
                "message": "Test message"
            }
        ]
    }
    
    with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as f:
        json.dump(config, f)
    
    try:
        loaded_config = load_config(f.name)
        assert loaded_config == config
    finally:
        os.unlink(f.name)

def test_invalid_file_format():
    """Test loading configuration with invalid file format."""
    with tempfile.NamedTemporaryFile(suffix=".txt", mode="w", delete=False) as f:
        f.write("invalid config")
    
    try:
        with pytest.raises(ValueError, match="Unsupported file format"):
            load_config(f.name)
    finally:
        os.unlink(f.name)

def test_missing_file():
    """Test loading configuration from non-existent file."""
    with pytest.raises(FileNotFoundError):
        load_config("nonexistent_file.yaml")

def test_invalid_yaml_syntax():
    """Test loading configuration with invalid YAML syntax."""
    with tempfile.NamedTemporaryFile(suffix=".yaml", mode="w", delete=False) as f:
        f.write("invalid: yaml: content: - [}")
    
    try:
        with pytest.raises(ValueError, match="Failed to parse configuration file"):
            load_config(f.name)
    finally:
        os.unlink(f.name)

def test_invalid_json_syntax():
    """Test loading configuration with invalid JSON syntax."""
    with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as f:
        f.write("{invalid json}")
    
    try:
        with pytest.raises(ValueError, match="Failed to parse configuration file"):
            load_config(f.name)
    finally:
        os.unlink(f.name)

def test_invalid_monitor_config():
    """Test loading configuration with invalid monitor structure."""
    config = {
        "monitors": [
            {
                "name": "Test Monitor",
                # Missing required fields
            }
        ]
    }
    
    with tempfile.NamedTemporaryFile(suffix=".yaml", mode="w", delete=False) as f:
        yaml.dump(config, f)
    
    try:
        with pytest.raises(ValueError, match="Invalid configuration format"):
            load_config(f.name)
    finally:
        os.unlink(f.name)

def test_empty_config():
    """Test loading empty configuration."""
    config = {}
    
    with tempfile.NamedTemporaryFile(suffix=".yaml", mode="w", delete=False) as f:
        yaml.dump(config, f)
    
    try:
        with pytest.raises(ValueError, match="Invalid configuration format"):
            load_config(f.name)
    finally:
        os.unlink(f.name)

def test_valid_complex_config():
    """Test loading valid complex configuration."""
    config = {
        "monitors": [
            {
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
        ]
    }
    
    with tempfile.NamedTemporaryFile(suffix=".yaml", mode="w", delete=False) as f:
        yaml.dump(config, f)
    
    try:
        loaded_config = load_config(f.name)
        assert loaded_config == config
    finally:
        os.unlink(f.name) 