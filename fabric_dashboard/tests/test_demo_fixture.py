"""Test demo persona fixture schema validation."""

import json
from pathlib import Path

import pytest

from fabric_dashboard.models.schemas import (
    Pattern, PersonaProfile, ColorScheme, CardContent
)
from fabric_dashboard.models.ui_components import (
    MapCard, EventCalendar, VideoFeed, WeatherCard, TaskList, InfoCard
)


def test_demo_fixture_exists():
    """Demo fixture file exists."""
    fixture_path = Path(__file__).parent / "fixtures" / "personas" / "demo.json"
    assert fixture_path.exists(), f"Demo fixture not found at {fixture_path}"


def test_demo_fixture_valid_json():
    """Demo fixture is valid JSON."""
    fixture_path = Path(__file__).parent / "fixtures" / "personas" / "demo.json"

    with open(fixture_path) as f:
        data = json.load(f)

    assert "patterns" in data
    assert "persona" in data
    assert "theme" in data
    assert "ui_components" in data
    assert "content_cards" in data


def test_demo_patterns_valid():
    """Demo patterns match Pattern schema."""
    fixture_path = Path(__file__).parent / "fixtures" / "personas" / "demo.json"

    with open(fixture_path) as f:
        data = json.load(f)

    patterns = [Pattern(**p) for p in data["patterns"]]

    assert len(patterns) == 5
    assert all(p.confidence > 0.7 for p in patterns)
    assert all(len(p.keywords) > 0 for p in patterns)


def test_demo_persona_valid():
    """Demo persona matches PersonaProfile schema."""
    fixture_path = Path(__file__).parent / "fixtures" / "personas" / "demo.json"

    with open(fixture_path) as f:
        data = json.load(f)

    persona = PersonaProfile(**data["persona"])

    assert len(persona.interests) > 0
    assert persona.activity_level in ["low", "moderate", "high", "highly engaged"]


def test_demo_theme_valid():
    """Demo theme matches ColorScheme schema."""
    fixture_path = Path(__file__).parent / "fixtures" / "personas" / "demo.json"

    with open(fixture_path) as f:
        data = json.load(f)

    theme = ColorScheme(**data["theme"])

    assert theme.primary.startswith("#")
    assert len(theme.primary) == 7  # #RRGGBB
    assert theme.fonts.heading
    assert theme.fonts.body


def test_demo_ui_components_valid():
    """Demo UI components match their schemas."""
    fixture_path = Path(__file__).parent / "fixtures" / "personas" / "demo.json"

    with open(fixture_path) as f:
        data = json.load(f)

    component_classes = {
        "map-card": MapCard,
        "event-calendar": EventCalendar,
        "video-feed": VideoFeed,
        "weather-card": WeatherCard,
        "task-list": TaskList,
        "info-card": InfoCard,
    }

    components = []
    for comp_data in data["ui_components"]:
        comp_type = comp_data["component_type"]
        comp_class = component_classes[comp_type]
        components.append(comp_class(**comp_data))

    assert len(components) == 9

    # Verify specific components
    map_cards = [c for c in components if isinstance(c, MapCard)]
    assert len(map_cards) == 1
    assert len(map_cards[0].markers) == 5

    event_calendars = [c for c in components if isinstance(c, EventCalendar)]
    assert len(event_calendars) == 1
    assert len(event_calendars[0].events) == 10

    video_feeds = [c for c in components if isinstance(c, VideoFeed)]
    assert len(video_feeds) == 2

    weather_cards = [c for c in components if isinstance(c, WeatherCard)]
    assert len(weather_cards) == 3


def test_demo_content_cards_valid():
    """Demo content cards match CardContent schema."""
    fixture_path = Path(__file__).parent / "fixtures" / "personas" / "demo.json"

    with open(fixture_path) as f:
        data = json.load(f)

    cards = [CardContent(**c) for c in data["content_cards"]]

    assert len(cards) == 4
    assert all(card.reading_time_minutes > 0 for card in cards)
    assert all(len(card.body) > 100 for card in cards)
