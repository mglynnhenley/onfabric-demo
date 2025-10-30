"""Tests for OnFabric API client."""

import os
from unittest.mock import patch

import pytest

from fabric_dashboard.api.onfabric_client import OnFabricAPIClient


def test_client_initialization_with_env_vars():
    """Test client initializes with valid env vars."""
    with patch.dict(os.environ, {
        "ONFABRIC_BEARER_TOKEN": "test_token_123",
        "ONFABRIC_TAPESTRY_ID": "test_tapestry_456"
    }):
        client = OnFabricAPIClient()
        assert client.bearer_token == "test_token_123"
        assert client.tapestry_id == "test_tapestry_456"
        assert client.base_url == "https://api.onfabric.io/api/v1"


def test_client_initialization_missing_token():
    """Test client raises error when token missing."""
    with patch.dict(os.environ, {"ONFABRIC_TAPESTRY_ID": "test_tapestry_456"}, clear=True):
        with pytest.raises(ValueError, match="ONFABRIC_BEARER_TOKEN not found"):
            OnFabricAPIClient()
