"""Tests for OAuth configuration."""

import pytest
from fabric_dashboard.mcp.oauth_config import OAuthConfig


def test_oauth_config_has_required_fields():
    """Test that OAuthConfig has all required OAuth fields for Device Flow."""
    config = OAuthConfig()

    assert hasattr(config, "client_id")
    assert hasattr(config, "device_code_url")
    assert hasattr(config, "token_url")
    assert hasattr(config, "verification_uri")
    assert hasattr(config, "scopes")
    assert hasattr(config, "default_poll_interval")


def test_oauth_config_uses_auth_onfabric_domain():
    """Test that OAuth URLs use auth.onfabric.io domain."""
    config = OAuthConfig()

    assert "auth.onfabric.io" in config.device_code_url
    assert "auth.onfabric.io" in config.token_url
    assert "auth.onfabric.io" in config.verification_uri


def test_oauth_config_scopes_not_empty():
    """Test that OAuth scopes are configured."""
    config = OAuthConfig()

    assert isinstance(config.scopes, list)
    assert len(config.scopes) > 0
