"""
Tests for the command-line interface.
"""

import os
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from datadog_monitor_deployer.cli import main, validate_credentials


@pytest.fixture
def cli_runner():
    """Fixture for CLI testing."""
    return CliRunner()


@pytest.fixture
def mock_env_vars():
    """Mock environment variables."""
    with patch.dict(
        os.environ,
        {
            "DD_API_KEY": "test-api-key",
            "DD_APP_KEY": "test-app-key",
        },
        clear=True,
    ):
        yield


@pytest.fixture
def mock_deployer():
    """Mock MonitorDeployer."""
    with patch("datadog_monitor_deployer.cli.MonitorDeployer") as mock:
        mock_instance = mock.return_value
        mock_instance.deploy.return_value = [{"id": "test-id", "name": "Test Monitor"}]
        mock_instance.list_monitors.return_value = [
            {
                "id": "1",
                "name": "Test Monitor 1",
                "type": "metric alert",
                "tags": ["env:test"],
            }
        ]
        yield mock_instance


def test_validate_credentials_success(mock_env_vars):
    """Test credential validation with valid credentials."""
    assert validate_credentials() is True


def test_validate_credentials_failure():
    """Test credential validation with missing credentials."""
    with patch.dict(os.environ, {}, clear=True):
        assert validate_credentials() is False


def test_main_without_credentials(cli_runner):
    """Test main command without credentials."""
    with patch.dict(os.environ, {}, clear=True):
        result = cli_runner.invoke(main, ["list"])
        assert result.exit_code == 1
        assert "Missing required environment variables" in result.output


def test_deploy_command_success(cli_runner, tmp_path):
    """Test successful monitor deployment."""
    with patch.dict(os.environ, {"DD_API_KEY": "test", "DD_APP_KEY": "test"}):
        with patch("datadog_monitor_deployer.cli.MonitorDeployer") as mock:
            mock_instance = mock.return_value
            mock_instance.deploy.return_value = [{"id": "1", "name": "Test"}]
            config_file = tmp_path / "test_config.yaml"
            config_file.write_text("monitors:\n  - name: Test\n    type: metric alert\n    query: test\n    message: test")

            result = cli_runner.invoke(main, ["deploy", str(config_file)])
            assert result.exit_code == 0
            assert "Successfully deployed" in result.output
            mock_instance.deploy.assert_called_once()


def test_deploy_command_dry_run(cli_runner, tmp_path):
    """Test deploy command with dry-run option."""
    with patch.dict(os.environ, {"DD_API_KEY": "test", "DD_APP_KEY": "test"}):
        with patch("datadog_monitor_deployer.cli.MonitorDeployer") as mock:
            mock_instance = mock.return_value
            config_file = tmp_path / "test_config.yaml"
            config_file.write_text("monitors:\n  - name: Test\n    type: metric alert\n    query: test\n    message: test")

            result = cli_runner.invoke(main, ["deploy", str(config_file), "--dry-run"])
            assert result.exit_code == 0
            assert "Performing dry run" in result.output
            mock_instance.validate_config.assert_called_once()


def test_deploy_command_invalid_file(cli_runner, mock_env_vars):
    """Test deploy command with non-existent file."""
    result = cli_runner.invoke(main, ["deploy", "nonexistent.yaml"])
    assert result.exit_code == 2
    assert "Path" in result.output


def test_delete_command(cli_runner):
    """Test deleting a monitor."""
    with patch.dict(os.environ, {"DD_API_KEY": "test", "DD_APP_KEY": "test"}):
        with patch("datadog_monitor_deployer.cli.MonitorDeployer") as mock:
            mock_instance = mock.return_value
            result = cli_runner.invoke(main, ["delete", "test-id"])
            assert result.exit_code == 0
            assert "Successfully deleted" in result.output
            mock_instance.delete_monitor.assert_called_once_with("test-id")


def test_validate_command_success(cli_runner, mock_env_vars, mock_deployer, tmp_path):
    """Test successful configuration validation."""
    config_file = tmp_path / "test_config.yaml"
    config_file.write_text(
        """
monitors:
  - name: "Test Monitor"
    type: "metric alert"
    query: "avg(last_5m):avg:system.cpu.user{*} > 80"
    message: "Test message"
"""
    )

    result = cli_runner.invoke(main, ["validate", str(config_file)])
    assert result.exit_code == 0
    assert "Configuration is valid" in result.output
    mock_deployer.validate_config.assert_called_once()


def test_validate_command_invalid_config(cli_runner, mock_env_vars, mock_deployer, tmp_path):
    """Test validation with invalid configuration."""
    config_file = tmp_path / "invalid_config.yaml"
    config_file.write_text("invalid: yaml: content")

    result = cli_runner.invoke(main, ["validate", str(config_file)])
    assert result.exit_code == 1
    assert "Error" in result.output


def test_error_handling_deploy(cli_runner, tmp_path):
    """Test error handling during deployment."""
    with patch.dict(os.environ, {"DD_API_KEY": "test", "DD_APP_KEY": "test"}):
        with patch("datadog_monitor_deployer.cli.MonitorDeployer") as mock:
            config_file = tmp_path / "test_config.yaml"
            config_file.write_text("monitors:\n  - name: Test\n    type: metric alert\n    query: test\n    message: test")

            mock_instance = mock.return_value
            mock_instance.deploy.side_effect = Exception("Test error")
            result = cli_runner.invoke(main, ["deploy", str(config_file)])
            assert result.exit_code == 1
            assert "Error" in result.output


def test_error_handling_list(cli_runner):
    """Test error handling during list operation."""
    with patch.dict(os.environ, {"DD_API_KEY": "test", "DD_APP_KEY": "test"}):
        with patch("datadog_monitor_deployer.cli.MonitorDeployer") as mock:
            mock_instance = mock.return_value
            mock_instance.list_monitors.side_effect = Exception("Test error")
            result = cli_runner.invoke(main, ["list"])
            assert result.exit_code == 1
            assert "Error" in result.output


def test_error_handling_delete(cli_runner):
    """Test error handling during delete operation."""
    with patch.dict(os.environ, {"DD_API_KEY": "test", "DD_APP_KEY": "test"}):
        with patch("datadog_monitor_deployer.cli.MonitorDeployer") as mock:
            mock_instance = mock.return_value
            mock_instance.delete_monitor.side_effect = Exception("Test error")
            result = cli_runner.invoke(main, ["delete", "test-id"])
            assert result.exit_code == 1
            assert "Error" in result.output
