"""
Command-line interface for the Datadog Monitor Deployer.
"""

import os
import sys
from typing import Optional

import click
from dotenv import load_dotenv

from .core.deployer import MonitorDeployer
from .utils.config import load_config
from .utils.logger import setup_logger

logger = setup_logger()


def validate_credentials() -> bool:
    """Validate that required Datadog credentials are set."""
    required_vars = ["DD_API_KEY", "DD_APP_KEY"]
    missing = [var for var in required_vars if not os.getenv(var)]

    if missing:
        click.echo(f"Error: Missing required environment variables: {', '.join(missing)}")
        click.echo("Please set them using environment variables or .env file")
        return False
    return True


@click.group()
@click.version_option()
def main():
    """Datadog Monitor Deployer - Manage your Datadog monitors as code."""
    # Load environment variables from .env file if it exists
    load_dotenv()

    if not validate_credentials():
        sys.exit(1)


@main.command()
@click.argument("config_file", type=click.Path(exists=True))
@click.option("--dry-run", is_flag=True, help="Validate configuration without deploying")
def deploy(config_file: str, dry_run: bool):
    """Deploy monitors from configuration file."""
    try:
        config = load_config(config_file)
        deployer = MonitorDeployer()

        if dry_run:
            click.echo("Performing dry run...")
            deployer.validate_config(config)
            click.echo("Configuration is valid!")
            return

        result = deployer.deploy(config)
        click.echo(f"Successfully deployed {len(result)} monitors!")

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@main.command()
@click.argument("monitor_id", required=False)
@click.option("--name", help="Filter monitors by name")
@click.option("--tag", multiple=True, help="Filter monitors by tags")
def list(monitor_id: Optional[str], name: Optional[str], tag: tuple):
    """List existing monitors."""
    try:
        deployer = MonitorDeployer()
        monitors = deployer.list_monitors(monitor_id, name, list(tag))

        for monitor in monitors:
            click.echo(f"ID: {monitor['id']}")
            click.echo(f"Name: {monitor['name']}")
            click.echo(f"Type: {monitor['type']}")
            click.echo(f"Tags: {', '.join(monitor.get('tags', []))}")
            click.echo("-" * 50)

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@main.command()
@click.argument("monitor_id")
def delete(monitor_id: str):
    """Delete a monitor by ID."""
    try:
        deployer = MonitorDeployer()
        deployer.delete_monitor(monitor_id)
        click.echo(f"Successfully deleted monitor {monitor_id}")

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@main.command()
@click.argument("config_file", type=click.Path(exists=True))
def validate(config_file: str):
    """Validate monitor configuration file."""
    try:
        config = load_config(config_file)
        deployer = MonitorDeployer()
        deployer.validate_config(config)
        click.echo("Configuration is valid!")

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
