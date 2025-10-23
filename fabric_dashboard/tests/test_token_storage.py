"""Tests for OAuth token storage."""

import os
import tempfile
from pathlib import Path
import pytest
from fabric_dashboard.mcp.token_storage import TokenStorage


@pytest.fixture
def temp_env_file():
    """Create temporary .env file for testing."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
        f.write("# Test env file\n")
        f.write("EXISTING_VAR=value\n")
        temp_path = f.name

    yield temp_path

    # Cleanup
    if os.path.exists(temp_path):
        os.unlink(temp_path)


def test_token_storage_initialization():
    """Test that token storage can be initialized."""
    storage = TokenStorage()

    assert hasattr(storage, "save_token")
    assert hasattr(storage, "load_token")
    assert hasattr(storage, "has_token")


def test_save_token_creates_env_entries(temp_env_file):
    """Test that saving token adds entries to .env file."""
    storage = TokenStorage(env_file=temp_env_file)

    test_token = {
        "access_token": "test_access_token_123",
        "token_type": "Bearer",
        "expires_in": 3600,
    }

    storage.save_token(test_token)

    # Read .env file and check contents (set_key adds quotes)
    with open(temp_env_file, "r") as f:
        contents = f.read()

    assert "ONFABRIC_ACCESS_TOKEN" in contents
    assert "test_access_token_123" in contents
    assert "ONFABRIC_TOKEN_TYPE" in contents
    assert "Bearer" in contents


def test_load_token_reads_from_env(temp_env_file):
    """Test that loading token reads from .env file."""
    # Add token to env file
    with open(temp_env_file, "a") as f:
        f.write("ONFABRIC_ACCESS_TOKEN=saved_token_456\n")
        f.write("ONFABRIC_TOKEN_TYPE=Bearer\n")

    storage = TokenStorage(env_file=temp_env_file)
    token = storage.load_token()

    assert token is not None
    assert token["access_token"] == "saved_token_456"
    assert token["token_type"] == "Bearer"


def test_has_token_returns_false_when_no_token(temp_env_file):
    """Test that has_token returns False when no token exists."""
    # Clear any existing env var from previous tests
    if "ONFABRIC_ACCESS_TOKEN" in os.environ:
        del os.environ["ONFABRIC_ACCESS_TOKEN"]

    storage = TokenStorage(env_file=temp_env_file)

    assert storage.has_token() is False


def test_has_token_returns_true_when_token_exists(temp_env_file):
    """Test that has_token returns True when token exists."""
    # Add token to env file
    with open(temp_env_file, "a") as f:
        f.write("ONFABRIC_ACCESS_TOKEN=token_exists\n")

    storage = TokenStorage(env_file=temp_env_file)

    assert storage.has_token() is True
