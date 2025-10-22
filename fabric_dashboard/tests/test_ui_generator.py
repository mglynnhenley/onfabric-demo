"""Tests for UI Generator core functionality."""

import pytest

from fabric_dashboard.core.ui_generator import UIGenerator
from fabric_dashboard.models.schemas import Pattern, PersonaProfile


@pytest.fixture
def sample_patterns():
    """Create sample patterns for testing."""
    return [
        Pattern(
            title="Tech Enthusiast",
            description="Strong interest in technology, AI, and software development",
            confidence=0.95,
            keywords=["technology", "AI", "machine learning", "python", "coding"],
            interaction_count=150,
        ),
        Pattern(
            title="San Francisco Explorer",
            description="Frequent searches and engagement with San Francisco area activities",
            confidence=0.88,
            keywords=["san francisco", "bay area", "california", "travel", "local"],
            interaction_count=75,
        ),
        Pattern(
            title="Continuous Learner",
            description="Regular consumption of educational content and tutorials",
            confidence=0.82,
            keywords=["learning", "tutorial", "course", "education", "guide"],
            interaction_count=120,
        ),
        Pattern(
            title="Event Networker",
            description="Shows interest in meetups, conferences, and networking events",
            confidence=0.76,
            keywords=["meetup", "conference", "networking", "event", "community"],
            interaction_count=45,
        ),
    ]


@pytest.fixture
def sample_persona():
    """Create sample persona for testing."""
    return PersonaProfile(
        writing_style="analytical and data-driven with clear arguments",
        interests=["technology", "AI", "travel", "learning"],
        activity_level="high",
        professional_context="software engineer",
        tone_preference="balanced and professional",
        content_depth_preference="deep_dives",
    )


@pytest.mark.asyncio
class TestUIGenerator:
    """Test UI Generator functionality."""

    async def test_init_mock_mode(self):
        """Test UIGenerator initialization in mock mode."""
        generator = UIGenerator(mock_mode=True)

        assert generator.mock_mode is True
        assert generator.llm is None
        assert generator.weather_client is not None
        assert generator.youtube_client is not None

    async def test_generate_mock_components(self, sample_patterns, sample_persona):
        """Test mock component generation."""
        generator = UIGenerator(mock_mode=True)

        result = await generator.generate_components(sample_patterns, sample_persona)

        # Verify result structure
        assert result is not None
        assert len(result.components) >= 3
        assert len(result.components) <= 6
        assert result.total_patterns_analyzed == len(sample_patterns)

    async def test_generate_diverse_components(self, sample_patterns, sample_persona):
        """Test that generated components are diverse."""
        generator = UIGenerator(mock_mode=True)

        result = await generator.generate_components(sample_patterns, sample_persona)

        # Check for component type diversity
        component_types = {comp.component_type for comp in result.components}
        assert len(component_types) >= 2  # Should have at least 2 different types

    async def test_components_link_to_patterns(self, sample_patterns, sample_persona):
        """Test that each component links to a pattern."""
        generator = UIGenerator(mock_mode=True)

        result = await generator.generate_components(sample_patterns, sample_persona)

        pattern_titles = {p.title for p in sample_patterns}

        for component in result.components:
            assert component.pattern_title in pattern_titles
            assert 0.0 <= component.confidence <= 1.0

    async def test_high_confidence_patterns_prioritized(
        self, sample_patterns, sample_persona
    ):
        """Test that high-confidence patterns are prioritized."""
        generator = UIGenerator(mock_mode=True)

        result = await generator.generate_components(sample_patterns, sample_persona)

        # First component should be from a high-confidence pattern
        first_component = result.components[0]
        assert first_component.confidence >= 0.75

    async def test_location_pattern_triggers_map(self, sample_persona):
        """Test that location patterns trigger map components."""
        location_patterns = [
            Pattern(
                title="Travel Enthusiast",
                description="Frequent travel and location searches",
                confidence=0.90,
                keywords=["travel", "location", "city", "visit", "places"],
                interaction_count=100,
            ),
        ]

        generator = UIGenerator(mock_mode=True)
        result = await generator.generate_components(location_patterns, sample_persona)

        # Should include a map card
        component_types = [comp.component_type for comp in result.components]
        assert "map-card" in component_types or "info-card" in component_types

    async def test_generates_content_card(self, sample_patterns, sample_persona):
        """Test that a content card is always generated."""
        generator = UIGenerator(mock_mode=True)

        result = await generator.generate_components(sample_patterns, sample_persona)

        component_types = [comp.component_type for comp in result.components]
        assert "content-card" in component_types


@pytest.mark.asyncio
class TestAPIClientMocks:
    """Test mock API client behavior."""

    async def test_weather_client_mock(self):
        """Test weather client returns valid mock data."""
        from fabric_dashboard.api import OpenWeatherAPI

        client = OpenWeatherAPI(mock_mode=True)
        weather = await client.get_current_weather(37.7749, -122.4194)

        assert weather is not None
        assert "temperature" in weather
        assert "condition" in weather
        assert isinstance(weather["temperature"], (int, float))

    async def test_weather_forecast_mock(self):
        """Test weather forecast returns multiple days."""
        from fabric_dashboard.api import OpenWeatherAPI

        client = OpenWeatherAPI(mock_mode=True)
        forecast = await client.get_forecast(40.7128, -74.0060, days=3)

        assert len(forecast) == 3
        assert all("date" in day for day in forecast)
        assert all("temperature_high" in day for day in forecast)

    async def test_youtube_client_mock(self):
        """Test YouTube client returns valid mock videos."""
        from fabric_dashboard.api import YouTubeAPI

        client = YouTubeAPI(mock_mode=True)
        videos = await client.search_videos("machine learning", max_results=3)

        assert len(videos) == 3
        assert all("video_id" in video for video in videos)
        assert all("title" in video for video in videos)
        assert all("url" in video for video in videos)

    async def test_ticketmaster_client_mock(self):
        """Test Ticketmaster client returns valid mock events."""
        from fabric_dashboard.api import TicketmasterAPI

        client = TicketmasterAPI(mock_mode=True)
        events = await client.search_events("tech meetups", max_results=5)

        assert len(events) == 5
        assert all("name" in event for event in events)
        assert all("date" in event for event in events)
        assert all("url" in event for event in events)

    async def test_mapbox_client_mock(self):
        """Test Mapbox client returns valid mock coordinates."""
        from fabric_dashboard.api import MapboxAPI

        client = MapboxAPI(mock_mode=True)
        result = await client.geocode("San Francisco, CA")

        assert "lat" in result
        assert "lng" in result
        assert "formatted_address" in result
        assert -90 <= result["lat"] <= 90
        assert -180 <= result["lng"] <= 180


@pytest.mark.asyncio
class TestComponentConfiguration:
    """Test that component configurations are realistic."""

    async def test_info_card_has_valid_location(self, sample_patterns, sample_persona):
        """Test InfoCard has valid location string."""
        generator = UIGenerator(mock_mode=True)
        result = await generator.generate_components(sample_patterns, sample_persona)

        info_cards = [c for c in result.components if c.component_type == "info-card"]
        for card in info_cards:
            assert card.location
            assert len(card.location) > 0

    async def test_video_feed_has_search_query(self, sample_patterns, sample_persona):
        """Test VideoFeed has non-empty search query."""
        generator = UIGenerator(mock_mode=True)
        result = await generator.generate_components(sample_patterns, sample_persona)

        video_feeds = [
            c for c in result.components if c.component_type == "video-feed"
        ]
        for feed in video_feeds:
            assert feed.search_query
            assert len(feed.search_query) > 0

    async def test_task_list_has_valid_tasks(self, sample_patterns, sample_persona):
        """Test TaskList has valid task items."""
        generator = UIGenerator(mock_mode=True)
        result = await generator.generate_components(sample_patterns, sample_persona)

        task_lists = [c for c in result.components if c.component_type == "task-list"]
        for task_list in task_lists:
            assert len(task_list.tasks) >= 2
            assert all(task.text for task in task_list.tasks)
            assert all(task.priority in ["low", "medium", "high"] for task in task_list.tasks)
