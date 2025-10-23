"""Tests for OAuth flow manager."""

import pytest
from unittest.mock import Mock, patch
from fabric_dashboard.mcp.oauth_flow import OAuthFlowManager


def test_oauth_flow_manager_initialization():
    """Test that OAuth flow manager initializes with config."""
    manager = OAuthFlowManager()

    assert hasattr(manager, "config")
    assert hasattr(manager, "get_authorization_url")
    assert hasattr(manager, "exchange_code_for_token")


def test_get_authorization_url_returns_valid_url():
    """Test that authorization URL is generated correctly."""
    manager = OAuthFlowManager()

    auth_url = manager.get_authorization_url()

    assert isinstance(auth_url, str)
    assert auth_url.startswith("https://")
    assert "oauth" in auth_url.lower() or "authorize" in auth_url.lower()


@patch("fabric_dashboard.mcp.oauth_flow.OAuth2Session")
def test_exchange_code_for_token_calls_fetch_token(mock_session):
    """Test that code exchange calls OAuth2Session.fetch_token()."""
    # Mock OAuth2Session behavior
    mock_instance = Mock()
    mock_instance.fetch_token.return_value = {
        "access_token": "test_token_123",
        "token_type": "Bearer",
        "expires_in": 3600,
    }
    mock_session.return_value = mock_instance

    manager = OAuthFlowManager()
    token = manager.exchange_code_for_token("test_auth_code")

    assert token is not None
    assert "access_token" in token
    assert token["access_token"] == "test_token_123"
