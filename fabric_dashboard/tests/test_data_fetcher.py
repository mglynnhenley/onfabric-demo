"""Tests for data fetcher module."""

from fabric_dashboard.core.data_fetcher import DataFetcher
from fabric_dashboard.models.schemas import UserData


def test_data_fetcher_mock_mode():
    """Test DataFetcher in mock mode."""
    fetcher = DataFetcher(mock_mode=True)
    assert fetcher.mock_mode is True
    assert fetcher.mcp_client is None


def test_data_fetcher_real_mode():
    """Test DataFetcher in real mode."""
    fetcher = DataFetcher(mock_mode=False)
    assert fetcher.mock_mode is False
    assert fetcher.mcp_client is not None


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
    """Test that real mode falls back to mock data when MCP not implemented."""
    fetcher = DataFetcher(mock_mode=False)

    # This should fall back to mock data since MCP raises NotImplementedError
    user_data = fetcher.fetch_user_data(days_back=30)

    # Should still return data via fallback
    assert user_data is not None
    assert isinstance(user_data, UserData)
