"""Tests for OAuth configuration."""

import pytest
from fabric_dashboard.mcp.oauth_config import OAuthConfig


def test_oauth_config_has_required_fields():
    """Test that OAuthConfig has all required OAuth fields."""
    config = OAuthConfig()

    assert hasattr(config, "client_id")
    assert hasattr(config, "authorization_url")
    assert hasattr(config, "token_url")
    assert hasattr(config, "redirect_uri")
    assert hasattr(config, "scopes")


def test_oauth_config_redirect_uri_is_localhost():
    """Test that redirect URI points to localhost for local auth server."""
    config = OAuthConfig()

    assert config.redirect_uri.startswith("http://localhost:")
    assert "/callback" in config.redirect_uri


def test_oauth_config_scopes_not_empty():
    """Test that OAuth scopes are configured."""
    config = OAuthConfig()

    assert isinstance(config.scopes, list)
    assert len(config.scopes) > 0
