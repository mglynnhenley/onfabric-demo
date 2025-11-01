"""
Application configuration using pydantic-settings.

Supports both mock mode (default) and real API integration.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    # Mock mode (default to True for easy demos)
    mock_mode: bool = True

    # OnFabric API
    onfabric_api_key: Optional[str] = None
    onfabric_api_url: str = "https://api.onfabric.com"

    # Enrichment APIs (optional)
    weather_api_key: Optional[str] = None
    search_api_key: Optional[str] = None

    # Application config
    backend_port: int = 8000
    frontend_port: int = 3000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


# Global settings instance
settings = Settings()
