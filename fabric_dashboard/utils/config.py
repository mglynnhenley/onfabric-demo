"""Configuration management for fabric_dashboard."""

import os
from pathlib import Path
from typing import Any, Optional

import yaml
from pydantic import ValidationError

from fabric_dashboard.models.schemas import Config


# Default configuration directory
CONFIG_DIR = Path.home() / ".fabric-dashboard"
CONFIG_FILE = CONFIG_DIR / "config.yaml"
DASHBOARDS_DIR = CONFIG_DIR / "dashboards"


def get_config_dir() -> Path:
    """Get the configuration directory path."""
    return CONFIG_DIR


def get_dashboards_dir() -> Path:
    """Get the dashboards output directory path."""
    return DASHBOARDS_DIR


def ensure_config_dir() -> None:
    """Ensure configuration directory exists."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    DASHBOARDS_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> Optional[Config]:
    """
    Load configuration from YAML file.

    Returns:
        Config object if file exists and is valid, None otherwise.
    """
    if not CONFIG_FILE.exists():
        return None

    try:
        with open(CONFIG_FILE, "r") as f:
            data = yaml.safe_load(f)

        if not data:
            return None

        # Try to create Config object
        config = Config(**data)
        return config

    except (yaml.YAMLError, ValidationError, IOError) as e:
        # If config is invalid, return None
        # Caller should handle this by prompting for new config
        return None


def save_config(config: Config) -> None:
    """
    Save configuration to YAML file.

    Args:
        config: Config object to save.
    """
    ensure_config_dir()

    # Convert Config to dict
    data = config.model_dump()

    with open(CONFIG_FILE, "w") as f:
        yaml.safe_dump(data, f, default_flow_style=False, sort_keys=False)


def get_config_from_env() -> Optional[Config]:
    """
    Try to load configuration from environment variables.

    Returns:
        Config object if environment variables are set, None otherwise.
    """
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    perplexity_key = os.getenv("PERPLEXITY_API_KEY")

    if not anthropic_key or not perplexity_key:
        return None

    try:
        config = Config(
            anthropic_api_key=anthropic_key,
            perplexity_api_key=perplexity_key,
            days_back=int(os.getenv("DAYS_BACK", "30")),
            debug=os.getenv("DEBUG", "false").lower() == "true",
            # External API keys for UI enrichment
            openweathermap_api_key=os.getenv("OPENWEATHERMAP_API_KEY") or None,
            youtube_api_key=os.getenv("YOUTUBE_API_KEY") or None,
            ticketmaster_api_key=os.getenv("TICKETMASTER_API_KEY") or None,
            mapbox_api_key=os.getenv("MAPBOX_API_KEY") or None,
        )
        return config
    except (ValidationError, ValueError):
        return None


def get_config() -> Optional[Config]:
    """
    Get configuration from file or environment variables.

    Priority:
    1. Environment variables (ANTHROPIC_API_KEY, PERPLEXITY_API_KEY)
    2. Config file (~/.fabric-dashboard/config.yaml)

    Returns:
        Config object if found, None otherwise.
    """
    # Try environment variables first (higher priority)
    config = get_config_from_env()
    if config:
        return config

    # Fall back to config file
    return load_config()


def update_config(**kwargs: Any) -> Config:
    """
    Update specific configuration values.

    Args:
        **kwargs: Configuration values to update.

    Returns:
        Updated Config object.

    Raises:
        ValueError: If no existing config found or update fails.
    """
    config = get_config()
    if not config:
        raise ValueError("No existing configuration found. Please run 'init' first.")

    # Update values
    data = config.model_dump()
    data.update(kwargs)

    # Create new config with updated values
    updated_config = Config(**data)

    # Save to file
    save_config(updated_config)

    return updated_config
