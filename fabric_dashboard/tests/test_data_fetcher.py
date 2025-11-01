"""
Tests for data fetching from OnFabric API.

Tests data retrieval and transformation:
- API client initialization
- Mock data loading (default)
- Real API calls (when configured)
- Error handling

How to run:
    # With mock data (default)
    pytest fabric_dashboard/tests/test_data_fetcher.py -v

    # With real API (requires ONFABRIC_API_KEY in .env)
    MOCK_MODE=false pytest fabric_dashboard/tests/test_data_fetcher.py -v
"""

from unittest.mock import Mock, patch

from fabric_dashboard.core.data_fetcher import DataFetcher
from fabric_dashboard.models.schemas import UserData


def test_data_fetcher_mock_mode():
    """Test DataFetcher in mock mode."""
    fetcher = DataFetcher(mock_mode=True)
    assert fetcher.mock_mode is True
    assert fetcher.api_client is None


def test_data_fetcher_real_mode():
    """Test DataFetcher in real mode."""
    with patch("fabric_dashboard.core.data_fetcher.OnFabricAPIClient"):
        fetcher = DataFetcher(mock_mode=False)
        assert fetcher.mock_mode is False
        assert fetcher.api_client is not None


def test_fetch_mock_data():
    """Test fetching data from mock fixtures."""
    fetcher = DataFetcher(mock_mode=True)
    user_data = fetcher.fetch_user_data()

    assert user_data is not None
    assert isinstance(user_data, UserData)
    assert user_data.connection_id == "conn_abc123def456"
    assert len(user_data.interactions) == 15
    assert user_data.persona.writing_style == "analytical yet accessible, with enthusiasm for complex systems and interdisciplinary connections"


def test_fetch_mock_data_interactions():
    """Test that mock data interactions are properly structured."""
    fetcher = DataFetcher(mock_mode=True)
    user_data = fetcher.fetch_user_data()

    assert user_data is not None
    interactions = user_data.interactions

    # Check first interaction (Instagram post)
    first = interactions[0]
    assert first["platform"] == "instagram"
    assert first["type"] == "post"
    assert "AI safety" in first["content"]
    assert first["engagement"] is not None
    assert first["engagement"]["likes"] == 145
    assert "AI" in first["topics"]

    # Check search interaction
    search = next(i for i in interactions if i["type"] == "search")
    assert search["platform"] == "google"
    assert search["query"] is not None
    assert "startup fundraising" in search["query"]


def test_fetch_mock_data_summary():
    """Test that summary is properly loaded from mock data."""
    fetcher = DataFetcher(mock_mode=True)
    user_data = fetcher.fetch_user_data()

    assert user_data is not None
    summary = user_data.summary

    assert summary.total_interactions == 15
    assert summary.days_analyzed == 9
    assert "instagram" in summary.platforms
    assert "google" in summary.platforms
    assert "pinterest" in summary.platforms
    assert "AI and technology" in summary.top_themes


def test_fetch_mock_data_persona():
    """Test that persona is properly loaded from mock data."""
    fetcher = DataFetcher(mock_mode=True)
    user_data = fetcher.fetch_user_data()

    assert user_data is not None
    persona = user_data.persona

    assert persona.writing_style == "analytical yet accessible, with enthusiasm for complex systems and interdisciplinary connections"
    assert "AI safety and ethics" in persona.interests
    assert "Sustainable technology" in persona.interests
    assert persona.activity_level == "high"
    assert persona.professional_context == "tech entrepreneur interested in AI and sustainability"
    assert persona.tone_preference == "thoughtful and engaging with occasional technical depth"
    assert persona.age_range == "28-35"
    assert persona.content_depth_preference == "balanced"


def test_context_manager():
    """Test DataFetcher as context manager."""
    with DataFetcher(mock_mode=True) as fetcher:
        user_data = fetcher.fetch_user_data()
        assert user_data is not None
        assert len(user_data.interactions) == 15


def test_fetch_real_mode_fallback():
    """Test that real mode handles API errors gracefully."""
    with patch("fabric_dashboard.core.data_fetcher.OnFabricAPIClient") as mock_client_class:
        mock_client = Mock()
        mock_client.tapestry_id = "test_tapestry"
        # Simulate API error
        mock_client.get_threads.side_effect = Exception("API Error")
        mock_client_class.return_value = mock_client

        fetcher = DataFetcher(mock_mode=False)
        user_data = fetcher.fetch_user_data(days_back=30)

        # Should return None on error
        assert user_data is None


def test_data_fetcher_uses_api_client():
    """Test DataFetcher initializes with OnFabric API client."""
    with patch("fabric_dashboard.core.data_fetcher.OnFabricAPIClient") as mock_client:
        fetcher = DataFetcher(mock_mode=False)

        # Should create API client instead of MCP client
        mock_client.assert_called_once()
        assert fetcher.api_client is not None
        assert not hasattr(fetcher, "mcp_client")


def test_fetch_from_api_calls_client():
    """Test _fetch_from_api method calls API client methods."""
    with patch("fabric_dashboard.core.data_fetcher.OnFabricAPIClient") as mock_client_class:
        mock_client = Mock()
        mock_client.tapestry_id = "test_tapestry_123"
        mock_client.get_threads.return_value = [
            {"id": "thread_1", "content": "Test", "asat": "2025-10-27T12:00:00"}
        ]
        mock_client.get_summaries.return_value = [
            {"id": "summary_1", "summary": "Test summary"}
        ]
        mock_client_class.return_value = mock_client

        fetcher = DataFetcher(mock_mode=False)
        user_data = fetcher.fetch_user_data(days_back=30)

        # Should call API client methods
        mock_client.get_threads.assert_called_once_with("test_tapestry_123")
        mock_client.get_summaries.assert_called_once_with("test_tapestry_123")

        # Should return UserData
        assert user_data is not None
        assert len(user_data.interactions) > 0
