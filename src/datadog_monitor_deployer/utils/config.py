"""
Configuration loading and validation utilities.
"""
import os
from typing import Dict, Any
import yaml
import json
from pathlib import Path
from jsonschema import validate
from ..schemas.monitor import MONITOR_SCHEMA

def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load and validate configuration from file.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Parsed configuration dictionary
        
    Raises:
        ValueError: If configuration is invalid
    """
    path = Path(config_path)
    
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    # Load configuration based on file extension
    try:
        if path.suffix.lower() in ['.yml', '.yaml']:
            with open(path, 'r') as f:
                config = yaml.safe_load(f)
        elif path.suffix.lower() == '.json':
            with open(path, 'r') as f:
                config = json.load(f)
        else:
            raise ValueError(f"Unsupported file format: {path.suffix}")
            
    except Exception as e:
        raise ValueError(f"Failed to parse configuration file: {str(e)}")
    
    # Validate against schema
    try:
        validate(instance=config, schema=MONITOR_SCHEMA)
    except Exception as e:
        raise ValueError(f"Invalid configuration format: {str(e)}")
    
    return config 