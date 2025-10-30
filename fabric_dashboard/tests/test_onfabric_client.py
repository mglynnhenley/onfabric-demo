"""Tests for OnFabric API client."""

import os
from unittest.mock import patch

import pytest
import requests
import responses

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


@responses.activate
def test_get_tapestries_success():
    """Test fetching tapestries from API."""
    responses.add(
        responses.GET,
        "https://api.onfabric.io/api/v1/tapestries",
        json=[
            {
                "id": "tapestry_123",
                "fabric_user_id": "user_456",
                "created_at": "2025-10-16T15:14:29.219809",
                "updated_at": "2025-10-16T15:14:29.219809"
            }
        ],
        status=200
    )

    with patch.dict(os.environ, {
        "ONFABRIC_BEARER_TOKEN": "test_token",
        "ONFABRIC_TAPESTRY_ID": "tapestry_123"
    }):
        client = OnFabricAPIClient()
        tapestries = client.get_tapestries()

        assert len(tapestries) == 1
        assert tapestries[0]["id"] == "tapestry_123"


@responses.activate
def test_get_tapestries_api_error():
    """Test get_tapestries handles API errors."""
    responses.add(
        responses.GET,
        "https://api.onfabric.io/api/v1/tapestries",
        json={"error": "Unauthorized"},
        status=401
    )

    with patch.dict(os.environ, {
        "ONFABRIC_BEARER_TOKEN": "invalid_token",
        "ONFABRIC_TAPESTRY_ID": "tapestry_123"
    }):
        client = OnFabricAPIClient()

        with pytest.raises(requests.HTTPError):
            client.get_tapestries()
