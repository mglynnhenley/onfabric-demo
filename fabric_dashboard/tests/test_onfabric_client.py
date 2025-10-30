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


@responses.activate
def test_get_threads_success():
    """Test fetching threads from API."""
    mock_threads = [
        {
            "id": "thread_1",
            "provider": "instagram",
            "content": "Posted photo",
            "asat": "2025-10-27T18:37:28"
        },
        {
            "id": "thread_2",
            "provider": "google",
            "content": "Searched for AI",
            "asat": "2025-10-26T12:00:00"
        }
    ]

    responses.add(
        responses.GET,
        "https://api.onfabric.io/api/v1/tapestries/tapestry_123/threads",
        json=mock_threads,
        status=200
    )

    with patch.dict(os.environ, {
        "ONFABRIC_BEARER_TOKEN": "test_token",
        "ONFABRIC_TAPESTRY_ID": "tapestry_123"
    }):
        client = OnFabricAPIClient()
        threads = client.get_threads("tapestry_123")

        assert len(threads) == 2
        assert threads[0]["id"] == "thread_1"
        assert threads[1]["provider"] == "google"


@responses.activate
def test_get_threads_not_found():
    """Test get_threads handles 404 errors."""
    responses.add(
        responses.GET,
        "https://api.onfabric.io/api/v1/tapestries/invalid_id/threads",
        json={"error": "Tapestry not found"},
        status=404
    )

    with patch.dict(os.environ, {
        "ONFABRIC_BEARER_TOKEN": "test_token",
        "ONFABRIC_TAPESTRY_ID": "tapestry_123"
    }):
        client = OnFabricAPIClient()

        with pytest.raises(requests.HTTPError):
            client.get_threads("invalid_id")


@responses.activate
def test_get_summaries_success():
    """Test fetching summaries from API."""
    mock_summaries = [
        {
            "id": "summary_1",
            "provider": "instagram",
            "summary": "Posted 5 photos this week",
            "week_start": "2025-10-21"
        }
    ]

    responses.add(
        responses.GET,
        "https://api.onfabric.io/api/v1/tapestries/tapestry_123/summaries?page_size=10&direction=desc&provider=instagram",
        json=mock_summaries,
        status=200
    )

    with patch.dict(os.environ, {
        "ONFABRIC_BEARER_TOKEN": "test_token",
        "ONFABRIC_TAPESTRY_ID": "tapestry_123"
    }):
        client = OnFabricAPIClient()
        summaries = client.get_summaries(
            "tapestry_123",
            provider="instagram",
            page_size=10,
            direction="desc"
        )

        assert len(summaries) == 1
        assert summaries[0]["provider"] == "instagram"


@responses.activate
def test_get_summaries_custom_params():
    """Test get_summaries with custom parameters."""
    responses.add(
        responses.GET,
        "https://api.onfabric.io/api/v1/tapestries/tapestry_123/summaries?page_size=20&direction=asc&provider=google",
        json=[],
        status=200
    )

    with patch.dict(os.environ, {
        "ONFABRIC_BEARER_TOKEN": "test_token",
        "ONFABRIC_TAPESTRY_ID": "tapestry_123"
    }):
        client = OnFabricAPIClient()
        summaries = client.get_summaries(
            "tapestry_123",
            provider="google",
            page_size=20,
            direction="asc"
        )

        assert summaries == []


@responses.activate
def test_client_auto_discovers_tapestry_id():
    """Test client auto-discovers tapestry ID when not in env."""
    responses.add(
        responses.GET,
        "https://api.onfabric.io/api/v1/tapestries",
        json=[
            {"id": "discovered_tapestry_123", "fabric_user_id": "user_456"},
            {"id": "second_tapestry_456", "fabric_user_id": "user_456"}
        ],
        status=200
    )

    with patch.dict(os.environ, {"ONFABRIC_BEARER_TOKEN": "test_token"}, clear=True):
        client = OnFabricAPIClient()

        # Should auto-discover and use first tapestry
        assert client.tapestry_id == "discovered_tapestry_123"


@responses.activate
def test_client_auto_discovery_warns_multiple_tapestries():
    """Test client warns when multiple tapestries found."""
    responses.add(
        responses.GET,
        "https://api.onfabric.io/api/v1/tapestries",
        json=[
            {"id": "tapestry_1", "fabric_user_id": "user_456"},
            {"id": "tapestry_2", "fabric_user_id": "user_456"}
        ],
        status=200
    )

    with patch.dict(os.environ, {"ONFABRIC_BEARER_TOKEN": "test_token"}, clear=True):
        with patch("fabric_dashboard.utils.logger.warning") as mock_warning:
            client = OnFabricAPIClient()

            # Should warn about multiple tapestries
            mock_warning.assert_called()
            assert "multiple tapestries" in str(mock_warning.call_args).lower()


@responses.activate
def test_client_auto_discovery_no_tapestries():
    """Test client raises error when no tapestries found."""
    responses.add(
        responses.GET,
        "https://api.onfabric.io/api/v1/tapestries",
        json=[],
        status=200
    )

    with patch.dict(os.environ, {"ONFABRIC_BEARER_TOKEN": "test_token"}, clear=True):
        with pytest.raises(ValueError, match="No tapestries found"):
            OnFabricAPIClient()
