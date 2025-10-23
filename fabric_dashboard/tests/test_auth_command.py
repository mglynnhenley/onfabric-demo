"""Tests for auth CLI command."""

import pytest
from click.testing import CliRunner
from unittest.mock import Mock, patch
from fabric_dashboard.commands.auth import auth


def test_auth_command_exists():
    """Test that auth command is defined."""
    assert auth is not None
    assert callable(auth)


@patch("fabric_dashboard.commands.auth.OAuthFlowManager")
@patch("fabric_dashboard.commands.auth.TokenStorage")
def test_auth_command_runs_oauth_flow(mock_storage, mock_flow):
    """Test that auth command runs OAuth flow and saves token."""
    # Mock successful OAuth flow
    mock_flow_instance = Mock()
    mock_flow_instance.run_interactive_flow.return_value = {
        "access_token": "test_token",
        "token_type": "Bearer",
    }
    mock_flow.return_value = mock_flow_instance

    # Mock token storage
    mock_storage_instance = Mock()
    mock_storage_instance.has_token.return_value = False
    mock_storage.return_value = mock_storage_instance

    # Run command
    runner = CliRunner()
    result = runner.invoke(auth)

    # Check that OAuth flow was run
    mock_flow_instance.run_interactive_flow.assert_called_once()

    # Check that token was saved
    mock_storage_instance.save_token.assert_called_once()

    # Check command succeeded
    assert result.exit_code == 0


@patch("fabric_dashboard.commands.auth.OAuthFlowManager")
def test_auth_command_handles_oauth_failure(mock_flow):
    """Test that auth command handles OAuth flow failure gracefully."""
    # Mock failed OAuth flow
    mock_flow_instance = Mock()
    mock_flow_instance.run_interactive_flow.return_value = None
    mock_flow.return_value = mock_flow_instance

    # Run command
    runner = CliRunner()
    result = runner.invoke(auth)

    # Check command failed
    assert result.exit_code != 0
