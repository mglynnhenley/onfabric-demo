"""Tests for OAuth flow manager - Device Code Flow."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from fabric_dashboard.mcp.oauth_flow import OAuthFlowManager


def test_oauth_flow_manager_initialization():
    """Test that OAuth flow manager initializes with config."""
    manager = OAuthFlowManager()

    assert hasattr(manager, "config")
    assert hasattr(manager, "request_device_code")
    assert hasattr(manager, "poll_for_token")


@patch("fabric_dashboard.mcp.oauth_flow.requests.post")
def test_request_device_code_success(mock_post):
    """Test that device code request returns expected data."""
    # Mock successful device code response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "device_code": "device_xyz",
        "user_code": "ABCD-1234",
        "verification_uri": "https://auth.onfabric.io/activate",
        "interval": 5,
        "expires_in": 600
    }
    mock_post.return_value = mock_response

    manager = OAuthFlowManager()
    result = manager.request_device_code()

    assert result is not None
    assert result["device_code"] == "device_xyz"
    assert result["user_code"] == "ABCD-1234"
    assert result["verification_uri"] == "https://auth.onfabric.io/activate"
    assert result["interval"] == 5


@patch("fabric_dashboard.mcp.oauth_flow.requests.post")
def test_request_device_code_failure(mock_post):
    """Test that device code request handles errors."""
    # Mock failed response
    mock_response = Mock()
    mock_response.status_code = 400
    mock_post.return_value = mock_response

    manager = OAuthFlowManager()
    result = manager.request_device_code()

    assert result is None


@patch("fabric_dashboard.mcp.oauth_flow.requests.post")
@patch("fabric_dashboard.mcp.oauth_flow.time.sleep")
def test_poll_for_token_success(mock_sleep, mock_post):
    """Test successful token polling."""
    # First call: pending, Second call: success
    pending_response = Mock()
    pending_response.status_code = 400
    pending_response.json.return_value = {"error": "authorization_pending"}

    success_response = Mock()
    success_response.status_code = 200
    success_response.json.return_value = {
        "access_token": "test_token",
        "token_type": "Bearer",
        "expires_in": 3600
    }

    mock_post.side_effect = [pending_response, success_response]

    manager = OAuthFlowManager()
    token = manager.poll_for_token("device_code_xyz", interval=1)

    assert token is not None
    assert token["access_token"] == "test_token"
    assert mock_sleep.called


@patch("fabric_dashboard.mcp.oauth_flow.requests.post")
def test_poll_for_token_declined(mock_post):
    """Test polling when user declines authorization."""
    # User declined
    declined_response = Mock()
    declined_response.status_code = 400
    declined_response.json.return_value = {"error": "access_denied"}
    mock_post.return_value = declined_response

    manager = OAuthFlowManager()
    token = manager.poll_for_token("device_code_xyz", interval=1)

    assert token is None
