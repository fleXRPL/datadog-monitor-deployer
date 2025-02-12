"""
Logging utility for the Datadog Monitor Deployer.
"""
import logging
import sys
from typing import Optional

def setup_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Set up and configure logger.
    
    Args:
        name: Logger name (defaults to package name)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name or "datadog_monitor_deployer")
    
    # Only configure if no handlers are set
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # Format
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
        
        # Don't propagate to root logger
        logger.propagate = False
    
    return logger 