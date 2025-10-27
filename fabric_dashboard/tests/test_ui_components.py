"""Tests for UI component schemas and generation."""

import pytest
from datetime import datetime, timezone

from fabric_dashboard.models.ui_components import (
    InfoCard,
    MapCard,
    MapMarker,
    VideoFeed,
    EventCalendar,
    TaskList,
    TaskItem,
    ContentCard,
    UIGenerationResult,
)


class TestUIComponentSchemas:
    """Test UI component schema validation."""

    def test_info_card_valid(self):
        """Test valid InfoCard creation."""
        card = InfoCard(
            title="Local Weather",
            pattern_title="Weather Enthusiast",
            confidence=0.85,
            location="San Francisco, CA",
            info_type="weather",
            units="metric",
            show_forecast=True,
        )

        assert card.component_type == "info-card"
        assert card.title == "Local Weather"
        assert card.location == "San Francisco, CA"
        assert card.units == "metric"

    def test_info_card_invalid_units(self):
        """Test InfoCard with invalid units."""
        with pytest.raises(ValueError):
            InfoCard(
                title="Weather",
                pattern_title="Test",
                location="NYC",
                units="fahrenheit",  # Invalid - should be 'metric' or 'imperial'
            )

    def test_map_card_valid(self):
        """Test valid MapCard creation."""
        markers = [
            MapMarker(
                lat=37.7749,
                lng=-122.4194,
                title="San Francisco",
                description="City by the Bay",
            ),
            MapMarker(
                lat=37.8044, lng=-122.2712, title="Oakland", description="East Bay"
            ),
        ]

        card = MapCard(
            title="Bay Area Map",
            pattern_title="Location Explorer",
            confidence=0.80,
            center_lat=37.7749,
            center_lng=-122.4194,
            zoom=10,
            style="streets",
            markers=markers,
        )

        assert card.component_type == "map-card"
        assert len(card.markers) == 2
        assert card.zoom == 10
        assert card.style == "streets"

    def test_map_card_invalid_coordinates(self):
        """Test MapCard with invalid coordinates."""
        with pytest.raises(ValueError):
            MapCard(
                title="Map",
                pattern_title="Test",
                center_lat=95.0,  # Invalid - must be -90 to 90
                center_lng=0.0,
                markers=[
                    MapMarker(lat=0, lng=0, title="Origin"),
                ],
            )

    def test_video_feed_valid(self):
        """Test valid VideoFeed creation."""
        feed = VideoFeed(
            title="Tech Videos",
            pattern_title="Tech Enthusiast",
            confidence=0.90,
            search_query="machine learning tutorials",
            max_results=3,
            video_duration="medium",
            order_by="relevance",
        )

        assert feed.component_type == "video-feed"
        assert feed.search_query == "machine learning tutorials"
        assert feed.max_results == 3
        assert feed.video_duration == "medium"

    def test_video_feed_invalid_max_results(self):
        """Test VideoFeed with out-of-range max_results."""
        with pytest.raises(ValueError):
            VideoFeed(
                title="Videos",
                pattern_title="Test",
                search_query="tech",
                max_results=10,  # Invalid - must be 1-5
            )

    def test_event_calendar_valid(self):
        """Test valid EventCalendar creation."""
        calendar = EventCalendar(
            title="Tech Events",
            pattern_title="Event Goer",
            confidence=0.75,
            search_query="tech meetups",
            location="San Francisco, CA",
            date_range_days=30,
            max_events=5,
            include_online=True,
        )

        assert calendar.component_type == "event-calendar"
        assert calendar.search_query == "tech meetups"
        assert calendar.date_range_days == 30

    def test_task_list_valid(self):
        """Test valid TaskList creation."""
        tasks = [
            TaskItem(text="Learn Python", completed=False, priority="high"),
            TaskItem(text="Read article", completed=False, priority="medium"),
            TaskItem(text="Watch tutorial", completed=True, priority="low"),
        ]

        task_list = TaskList(
            title="Learning Goals",
            pattern_title="Learner",
            confidence=0.82,
            tasks=tasks,
            list_type="learning",
        )

        assert task_list.component_type == "task-list"
        assert len(task_list.tasks) == 3
        assert task_list.list_type == "learning"

    def test_task_list_invalid_length(self):
        """Test TaskList with invalid number of tasks."""
        with pytest.raises(ValueError):
            TaskList(
                title="Tasks",
                pattern_title="Test",
                tasks=[TaskItem(text="Only one task", priority="medium")],  # Too few
            )

    def test_content_card_valid(self):
        """Test valid ContentCard creation."""
        card = ContentCard(
            title="Deep Dive",
            pattern_title="Researcher",
            confidence=0.88,
            article_title="Understanding Machine Learning: A Comprehensive Guide",
            overview="An in-depth exploration of ML concepts covering neural networks, training strategies, and practical applications in modern software.",
            url="https://example.com/ml-guide",
            source_name="Tech Journal",
            published_date="2024-10-01",
            search_query="machine learning comprehensive guide",
        )

        assert card.component_type == "content-card"
        assert len(card.overview) >= 50
        assert card.url.startswith("http")

    def test_content_card_invalid_overview(self):
        """Test ContentCard with too-short overview."""
        with pytest.raises(ValueError):
            ContentCard(
                title="Article",
                pattern_title="Test",
                article_title="Test Article",
                overview="Too short",  # Invalid - must be at least 50 chars
                url="https://example.com",
                source_name="Source",
                search_query="test",
            )


class TestUIGenerationResult:
    """Test UIGenerationResult schema."""

    def test_valid_generation_result(self):
        """Test valid UIGenerationResult."""
        components = [
            InfoCard(
                title="Weather",
                pattern_title="Test Pattern 1",
                location="NYC",
                confidence=0.8,
            ),
            VideoFeed(
                title="Videos",
                pattern_title="Test Pattern 2",
                search_query="tech",
                confidence=0.75,
            ),
            TaskList(
                title="Tasks",
                pattern_title="Test Pattern 3",
                tasks=[
                    TaskItem(text="Task 1", priority="high"),
                    TaskItem(text="Task 2", priority="low"),
                ],
                confidence=0.7,
            ),
        ]

        result = UIGenerationResult(
            components=components, total_patterns_analyzed=5
        )

        assert len(result.components) == 3
        assert result.total_patterns_analyzed == 5
        assert isinstance(result.generated_at, datetime)

    def test_invalid_component_count_too_few(self):
        """Test UIGenerationResult with too few components."""
        with pytest.raises(ValueError):
            UIGenerationResult(
                components=[
                    InfoCard(
                        title="Weather",
                        pattern_title="Test",
                        location="NYC",
                        confidence=0.8,
                    ),
                ],  # Only 1 component - need 3-6
                total_patterns_analyzed=2,
            )

    def test_invalid_component_count_too_many(self):
        """Test UIGenerationResult with too many components."""
        components = [
            InfoCard(
                title=f"Card {i}",
                pattern_title=f"Pattern {i}",
                location="NYC",
                confidence=0.8,
            )
            for i in range(7)  # 7 components - max is 6
        ]

        with pytest.raises(ValueError):
            UIGenerationResult(
                components=components,
                total_patterns_analyzed=7,
            )


class TestMapMarker:
    """Test MapMarker schema."""

    def test_valid_marker(self):
        """Test valid marker creation."""
        marker = MapMarker(
            lat=37.7749,
            lng=-122.4194,
            title="San Francisco",
            description="Beautiful city",
        )

        assert marker.lat == 37.7749
        assert marker.lng == -122.4194
        assert marker.title == "San Francisco"

    def test_marker_without_description(self):
        """Test marker creation without optional description."""
        marker = MapMarker(lat=0.0, lng=0.0, title="Origin")

        assert marker.lat == 0.0
        assert marker.lng == 0.0
        assert marker.description is None


class TestTaskItem:
    """Test TaskItem schema."""

    def test_valid_task(self):
        """Test valid task creation."""
        task = TaskItem(text="Complete project", completed=False, priority="high")

        assert task.text == "Complete project"
        assert not task.completed
        assert task.priority == "high"

    def test_task_defaults(self):
        """Test task with default values."""
        task = TaskItem(text="Simple task")

        assert not task.completed
        assert task.priority == "medium"
