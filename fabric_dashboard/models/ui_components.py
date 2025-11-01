"""UI Component schemas for generative UI generation.

This module defines the data models for interactive dashboard widgets that are
dynamically selected and configured by the UI Generator based on user patterns.

These components are SEPARATE from ContentWriter's blog-style text cards.
"""

from datetime import datetime, timezone
from typing import Literal, Optional, Union

from pydantic import BaseModel, Field


# ============================================================================
# BASE COMPONENT
# ============================================================================


class UIComponent(BaseModel):
    """Base class for all UI components."""

    component_type: str = Field(description="Type of UI component")
    title: str = Field(min_length=1, max_length=100, description="Component title")
    pattern_title: str = Field(
        description="Title of the pattern this component is based on"
    )
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        default=1.0,
        description="Pattern confidence (affects component positioning)",
    )


# ============================================================================
# COMPONENT TYPES
# ============================================================================


class InfoCard(UIComponent):
    """Weather or location-based information card.

    Uses OpenWeatherMap API to show current weather and forecast.
    """

    component_type: Literal["info-card"] = "info-card"
    location: str = Field(
        min_length=1,
        max_length=100,
        description="City name or location (e.g., 'San Francisco, CA')",
    )
    info_type: Literal["weather"] = Field(
        default="weather", description="Type of info (currently only weather)"
    )
    units: Literal["metric", "imperial"] = Field(
        default="metric", description="Temperature units"
    )
    show_forecast: bool = Field(
        default=True, description="Whether to show 3-day forecast"
    )
    enriched_data: Optional[dict] = Field(
        default=None, description="Enriched weather data from API"
    )


class MapMarker(BaseModel):
    """Marker for map component."""

    lat: float = Field(ge=-90, le=90, description="Latitude")
    lng: float = Field(ge=-180, le=180, description="Longitude")
    title: str = Field(min_length=1, max_length=100, description="Marker title")
    description: Optional[str] = Field(
        None, max_length=300, description="Optional marker description"
    )


class MapCard(UIComponent):
    """Interactive map with location markers.

    Uses Mapbox GL JS for rendering and Geocoding API for address resolution.
    """

    component_type: Literal["map-card"] = "map-card"
    center_lat: float = Field(ge=-90, le=90, description="Map center latitude")
    center_lng: float = Field(ge=-180, le=180, description="Map center longitude")
    zoom: int = Field(ge=1, le=20, default=10, description="Initial zoom level")
    style: Literal["streets", "satellite", "outdoors"] = Field(
        default="streets", description="Map style"
    )
    markers: list[MapMarker] = Field(
        min_length=1, max_length=20, description="Location markers"
    )


class VideoFeed(UIComponent):
    """YouTube video recommendations feed.

    Uses YouTube Data API v3 to fetch recent videos matching user interests.
    """

    component_type: Literal["video-feed"] = "video-feed"
    search_query: str = Field(
        min_length=1, max_length=200, description="YouTube search query"
    )
    max_results: int = Field(
        ge=1, le=5, default=3, description="Number of videos to show (1-5)"
    )
    video_duration: Literal["any", "short", "medium", "long"] = Field(
        default="any", description="Video length preference"
    )
    order_by: Literal["relevance", "date", "viewCount"] = Field(
        default="relevance", description="Sort order for results"
    )
    enriched_videos: Optional[list[dict]] = Field(
        default=None, description="Enriched video data from YouTube API"
    )


class Event(BaseModel):
    """Event details for calendar component."""

    name: str = Field(min_length=1, max_length=200, description="Event name")
    date: str = Field(
        description="Event date/time (ISO 8601 format or relative like '2024-10-20T19:00:00Z')"
    )
    location: Optional[str] = Field(
        None, max_length=200, description="Event location"
    )
    url: Optional[str] = Field(None, description="Event URL for more info")
    is_virtual: bool = Field(default=False, description="Whether event is online")


class EventCalendar(UIComponent):
    """Upcoming events calendar.

    Uses Eventbrite API to fetch relevant local/online events.
    """

    component_type: Literal["event-calendar", "calendar-card"] = "event-calendar"
    search_query: str = Field(
        min_length=1,
        max_length=200,
        description="Event search query (e.g., 'tech meetups')",
    )
    location: Optional[str] = Field(
        None, max_length=100, description="Location for local events (optional)"
    )
    date_range_days: int = Field(
        ge=1, le=90, default=30, description="Number of days to look ahead"
    )
    max_events: int = Field(
        ge=1, le=10, default=5, description="Maximum number of events to show"
    )
    include_online: bool = Field(
        default=True, description="Include online/virtual events"
    )
    enriched_events: Optional[list[dict]] = Field(
        default=None, description="Enriched event data from Ticketmaster API"
    )


class TaskItem(BaseModel):
    """Task item for task list component."""

    text: str = Field(min_length=1, max_length=200, description="Task text")
    completed: bool = Field(default=False, description="Task completion status")
    priority: Literal["low", "medium", "high"] = Field(
        default="medium", description="Task priority"
    )


class TaskList(UIComponent):
    """Suggested action items and tasks.

    Generated by LLM based on user patterns (no external API).
    """

    component_type: Literal["task-list"] = "task-list"
    tasks: list[TaskItem] = Field(
        min_length=2, max_length=8, description="List of suggested tasks"
    )
    list_type: Literal["goals", "recommendations", "learning"] = Field(
        default="recommendations",
        description="Type of task list (affects styling and framing)",
    )


class ContentCard(UIComponent):
    """Single article/paper recommendation with brief overview.

    Uses Perplexity API to find ONE relevant deep-dive resource.
    This is DIFFERENT from ContentWriter's blog cards.
    """

    component_type: Literal["content-card"] = "content-card"
    article_title: str = Field(
        min_length=1, max_length=200, description="Article/paper title"
    )
    overview: str = Field(
        min_length=50,
        max_length=300,
        description="Brief 2-3 sentence summary of the content",
    )
    url: str = Field(description="Link to the full article/paper")
    source_name: str = Field(
        min_length=1, max_length=100, description="Source/publication name"
    )
    published_date: Optional[str] = Field(
        None, description="Publication date if available"
    )
    search_query: str = Field(
        min_length=1,
        max_length=200,
        description="Search query used to find this content",
    )


# ============================================================================
# UNION TYPE
# ============================================================================

UIComponentType = Union[
    InfoCard,
    MapCard,
    VideoFeed,
    EventCalendar,
    TaskList,
    ContentCard,
]

# ============================================================================
# GENERATION RESULT
# ============================================================================


class UIGenerationResult(BaseModel):
    """Result from UI generation containing 3-6 interactive components."""

    components: list[UIComponentType] = Field(
        min_length=3,
        max_length=6,
        description="3-6 interactive UI components selected based on user patterns",
    )
    generated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="When components were generated",
    )
    total_patterns_analyzed: int = Field(
        ge=0, description="Number of patterns analyzed"
    )
