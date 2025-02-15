"""
Core deployer class for managing Datadog monitors.
"""

from typing import Any, Dict, List, Optional

from datadog import api, initialize

from ..utils.logger import setup_logger
from .monitor import Monitor

logger = setup_logger()


class MonitorDeployer:
    """
    Class for deploying and managing Datadog monitors.
    """

    def __init__(self):
        """Initialize the Datadog API client."""
        initialize()
        self._validate_api_connection()

    def _validate_api_connection(self):
        """Validate connection to Datadog API."""
        try:
            api.Monitor.get_all()
        except Exception as e:
            logger.error("Failed to connect to Datadog API")
            raise ConnectionError(f"Failed to connect to Datadog API: {str(e)}")

    def deploy(self, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Deploy monitors from configuration.

        Args:
            config: Dictionary containing monitor configurations

        Returns:
            List of created/updated monitors
        """
        self.validate_config(config)
        results = []

        for monitor_config in config.get("monitors", []):
            monitor = Monitor.from_dict(monitor_config)

            # Check if monitor already exists
            existing = self._find_existing_monitor(monitor.name)

            try:
                if existing:
                    # Update existing monitor
                    result = api.Monitor.update(existing["id"], **monitor.to_dict())
                    logger.info(f"Updated monitor: {monitor.name}")
                else:
                    # Create new monitor
                    result = api.Monitor.create(**monitor.to_dict())
                    logger.info(f"Created monitor: {monitor.name}")

                results.append(result)

            except Exception as e:
                logger.error(f"Failed to deploy monitor {monitor.name}: {str(e)}")
                raise

        return results

    def _find_existing_monitor(self, name: str) -> Optional[Dict[str, Any]]:
        """Find existing monitor by name."""
        monitors = api.Monitor.get_all()
        return next((m for m in monitors if m["name"] == name), None)

    def list_monitors(
        self,
        monitor_id: Optional[str] = None,
        name: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        List monitors with optional filtering.

        Args:
            monitor_id: Specific monitor ID to retrieve
            name: Filter monitors by name
            tags: Filter monitors by tags

        Returns:
            List of monitors matching criteria
        """
        if monitor_id:
            return [api.Monitor.get(monitor_id)]

        monitors = api.Monitor.get_all()

        # Apply filters
        if name:
            monitors = [m for m in monitors if name.lower() in m["name"].lower()]

        if tags:
            monitors = [m for m in monitors if any(tag in m.get("tags", []) for tag in tags)]

        return monitors

    def delete_monitor(self, monitor_id: str):
        """Delete a monitor by ID."""
        try:
            api.Monitor.delete(monitor_id)
            logger.info(f"Deleted monitor: {monitor_id}")
        except Exception as e:
            logger.error(f"Failed to delete monitor {monitor_id}: {str(e)}")
            raise

    def validate_config(self, config: Dict[str, Any]):
        """
        Validate monitor configuration.

        Args:
            config: Dictionary containing monitor configurations

        Raises:
            ValueError: If configuration is invalid
        """
        if not isinstance(config, dict):
            raise ValueError("Configuration must be a dictionary")

        if "monitors" not in config:
            raise ValueError("Configuration must contain 'monitors' key")

        if not isinstance(config["monitors"], list):
            raise ValueError("'monitors' must be a list")

        # Validate each monitor configuration
        for monitor_config in config["monitors"]:
            try:
                monitor = Monitor.from_dict(monitor_config)
                monitor.validate()
            except Exception as e:
                raise ValueError(f"Invalid monitor configuration: {str(e)}")

        logger.info("Configuration validation successful")
