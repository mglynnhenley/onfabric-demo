"""Tests for MCP client OAuth integration."""

import pytest
from unittest.mock import Mock, patch
from fabric_dashboard.mcp.client import MCPClient


@patch("fabric_dashboard.mcp.client.TokenStorage")
def test_mcp_client_loads_token_on_connect(mock_storage):
    """Test that MCPClient loads OAuth token when connecting."""
    # Mock token storage
    mock_storage_instance = Mock()
    mock_storage_instance.load_token.return_value = {
        "access_token": "test_token_123",
        "token_type": "Bearer",
    }
    mock_storage.return_value = mock_storage_instance

    # Create client and connect
    client = MCPClient(server_name="onfabric")
    result = client.connect()

    # Verify token was loaded
    mock_storage_instance.load_token.assert_called_once()

    # Verify token is stored in client
    assert hasattr(client, "access_token")
    assert client.access_token == "test_token_123"

    # Connection should succeed
    assert result is True


@patch("fabric_dashboard.mcp.client.TokenStorage")
def test_mcp_client_fails_when_no_token(mock_storage):
    """Test that MCPClient fails to connect when no token exists."""
    # Mock no token
    mock_storage_instance = Mock()
    mock_storage_instance.load_token.return_value = None
    mock_storage.return_value = mock_storage_instance

    # Create client and try to connect
    client = MCPClient(server_name="onfabric")
    result = client.connect()

    # Connection should fail
    assert result is False


def test_mcp_client_has_is_authenticated_method():
    """Test that MCPClient has method to check authentication status."""
    client = MCPClient(server_name="onfabric")

    assert hasattr(client, "is_authenticated")
    assert callable(client.is_authenticated)
