"""Tests for OAuth local redirect server."""

import pytest
from fabric_dashboard.mcp.oauth_server import LocalRedirectServer


def test_redirect_server_initialization():
    """Test that redirect server can be initialized."""
    server = LocalRedirectServer(port=8080)

    assert server.port == 8080
    assert server.authorization_code is None


def test_redirect_server_has_wait_for_callback_method():
    """Test that server has method to wait for OAuth callback."""
    server = LocalRedirectServer(port=8080)

    assert hasattr(server, "wait_for_callback")
    assert callable(server.wait_for_callback)
