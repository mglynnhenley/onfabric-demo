"""Unit tests for Pydantic data models."""

from datetime import datetime, timedelta

import pytest
from pydantic import ValidationError

from fabric_dashboard.models.schemas import (
    BackgroundTheme,
    CardContent,
    CardSize,
    ColorScheme,
    Config,
    Dashboard,
    DataSummary,
    EnrichedPattern,
    FontScheme,
    Pattern,
    PersonaProfile,
    SearchResult,
    UserData,
)


# ============================================================================
# PERSONA & USER DATA TESTS
# ============================================================================


def test_persona_profile_valid():
    """Test valid PersonaProfile creation."""
    persona = PersonaProfile(
        writing_style="analytical and data-driven with clear structure",
        interests=["AI", "technology", "startups"],
        activity_level="high",
        professional_context="startup founder",
        tone_preference="formal and professional with occasional wit",
        age_range="25-34",
        content_depth_preference="deep_dives",
    )
    assert persona.writing_style == "analytical and data-driven with clear structure"
    assert len(persona.interests) == 3
    assert persona.activity_level == "high"
    assert persona.tone_preference == "formal and professional with occasional wit"


def test_persona_profile_minimal():
    """Test PersonaProfile with minimal required fields."""
    persona = PersonaProfile(
        writing_style="narrative and emotionally engaging", interests=["photography"]
    )
    assert persona.writing_style == "narrative and emotionally engaging"
    assert persona.activity_level == "moderate"  # default
    assert persona.tone_preference == "balanced and approachable"  # default


def test_persona_profile_invalid_interests():
    """Test PersonaProfile rejects empty interests list."""
    with pytest.raises(ValidationError):
        PersonaProfile(
            writing_style="analytical and structured", interests=[]
        )


def test_data_summary_valid():
    """Test valid DataSummary creation."""
    now = datetime.now()
    summary = DataSummary(
        total_interactions=1500,
        date_range_start=now - timedelta(days=30),
        date_range_end=now,
        days_analyzed=30,
        platforms=["instagram", "google"],
        top_themes=["AI", "design", "travel"],
    )
    assert summary.total_interactions == 1500
    assert summary.days_analyzed == 30


def test_user_data_valid():
    """Test valid UserData creation."""
    now = datetime.now()
    summary = DataSummary(
        total_interactions=100,
        date_range_start=now - timedelta(days=7),
        date_range_end=now,
        days_analyzed=7,
        platforms=["instagram"],
    )
    user_data = UserData(
        connection_id="test-123",
        interactions=[{"type": "post", "content": "test"}],
        summary=summary,
    )
    assert user_data.connection_id == "test-123"
    assert len(user_data.interactions) == 1


# ============================================================================
# COLOR SCHEME TESTS
# ============================================================================


def test_color_scheme_valid():
    """Test valid ColorScheme creation."""
    colors = ColorScheme(
        primary="#3B82F6",
        secondary="#1E40AF",
        accent="#10B981",
        background_theme=BackgroundTheme(
            type="solid",
            color="#F9FAFB",
            card_background="#FFFFFF",
            card_backdrop_blur=False,
        ),
        fonts=FontScheme(
            heading="Inter",
            body="Inter",
            mono="Fira Code",
            heading_url="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap",
            body_url="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap",
            mono_url="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500&display=swap",
        ),
        foreground="#111827",
        muted="#6B7280",
        success="#10B981",
        warning="#F59E0B",
        destructive="#EF4444",
        mood="energetic",
        rationale="Vibrant blues for tech-focused professional",
    )
    assert colors.primary == "#3B82F6"
    assert colors.mood == "energetic"


def test_color_scheme_invalid_hex():
    """Test ColorScheme rejects invalid hex codes."""
    with pytest.raises(ValidationError):
        ColorScheme(
            primary="blue",  # Not a hex code
            secondary="#1E40AF",
            accent="#10B981",
            background_theme=BackgroundTheme(
                type="solid",
                color="#F9FAFB",
                card_background="#FFFFFF",
                card_backdrop_blur=False,
            ),
            fonts=FontScheme(
                heading="Inter",
                body="Inter",
                mono="Fira Code",
                heading_url="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap",
                body_url="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap",
                mono_url="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500&display=swap",
            ),
            foreground="#111827",
            muted="#6B7280",
            success="#10B981",
            warning="#F59E0B",
            destructive="#EF4444",
            mood="calm",
            rationale="Test",
        )


def test_color_scheme_empty_mood():
    """Test ColorScheme rejects empty mood."""
    with pytest.raises(ValidationError):
        ColorScheme(
            primary="#3B82F6",
            secondary="#1E40AF",
            accent="#10B981",
            background_theme=BackgroundTheme(
                type="solid",
                color="#F9FAFB",
                card_background="#FFFFFF",
                card_backdrop_blur=False,
            ),
            fonts=FontScheme(
                heading="Inter",
                body="Inter",
                mono="Fira Code",
                heading_url="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap",
                body_url="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap",
                mono_url="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500&display=swap",
            ),
            foreground="#111827",
            muted="#6B7280",
            success="#10B981",
            warning="#F59E0B",
            destructive="#EF4444",
            mood="",  # Empty mood
            rationale="Test",
        )


# ============================================================================
# PATTERN & SEARCH TESTS
# ============================================================================


def test_pattern_valid():
    """Test valid Pattern creation."""
    pattern = Pattern(
        title="AI Safety Research",
        description="User shows strong interest in AI safety and alignment research",
        confidence=0.85,
        keywords=["AI", "safety", "alignment", "AGI"],
        interaction_count=42,
    )
    assert pattern.confidence == 0.85
    assert len(pattern.keywords) == 4


def test_pattern_invalid_confidence():
    """Test Pattern rejects invalid confidence scores."""
    with pytest.raises(ValidationError):
        Pattern(
            title="Test",
            description="Test pattern",
            confidence=1.5,  # > 1.0
            keywords=[],
            interaction_count=10,
        )


def test_search_result_valid():
    """Test valid SearchResult creation."""
    result = SearchResult(
        query="latest AI safety research 2025",
        content="Recent developments in AI safety include...",
        sources=["https://example.com/article1"],
        relevance_score=0.9,
    )
    assert result.query == "latest AI safety research 2025"
    assert result.relevance_score == 0.9
    assert isinstance(result.fetched_at, datetime)


def test_enriched_pattern_valid():
    """Test valid EnrichedPattern creation."""
    pattern = Pattern(
        title="Test Pattern",
        description="Test description",
        confidence=0.8,
        keywords=["test"],
        interaction_count=5,
    )
    search = SearchResult(
        query="test query",
        content="test content",
        sources=["https://example.com"],
    )
    enriched = EnrichedPattern(pattern=pattern, search_results=[search])
    assert enriched.pattern.title == "Test Pattern"
    assert len(enriched.search_results) == 1


# ============================================================================
# CARD CONTENT TESTS
# ============================================================================


def test_card_content_large_valid():
    """Test valid large CardContent."""
    # Generate content with ~450 words (within 320-600 range for LARGE)
    body = " ".join(["word"] * 450)

    card = CardContent(
        title="Deep Dive into AI Safety",
        description="A comprehensive analysis of current approaches",
        body=body,
        reading_time_minutes=8,
        sources=["https://example.com"],
        size=CardSize.LARGE,
        confidence=0.9,
        pattern_title="AI Safety Research",
    )
    assert card.size == CardSize.LARGE
    assert card.reading_time_minutes == 8


def test_card_content_medium_valid():
    """Test valid medium CardContent."""
    # Generate content with ~280 words (within 200-360 range for MEDIUM)
    body = " ".join(["word"] * 280)

    card = CardContent(
        title="ESG Trends 2025",
        description="Key developments in sustainable investing",
        body=body,
        reading_time_minutes=4,
        sources=["https://example.com"],
        size=CardSize.MEDIUM,
        confidence=0.85,
        pattern_title="ESG Investing",
    )
    assert card.size == CardSize.MEDIUM


def test_card_content_small_valid():
    """Test valid small CardContent."""
    # Generate content with ~175 words (within 120-240 range for SMALL)
    body = " ".join(["word"] * 175)

    card = CardContent(
        title="Space Update",
        description="Latest from SpaceX",
        body=body,
        reading_time_minutes=2,
        sources=["https://example.com"],
        size=CardSize.SMALL,
        confidence=0.8,
        pattern_title="Space Exploration",
    )
    assert card.size == CardSize.SMALL


def test_card_content_compact_valid():
    """Test valid compact CardContent."""
    # Generate content with ~125 words (within 80-180 range for COMPACT)
    body = " ".join(["word"] * 125)

    card = CardContent(
        title="Quick Insight",
        description="Fast facts",
        body=body,
        reading_time_minutes=1,
        sources=["https://example.com"],
        size=CardSize.COMPACT,
        confidence=0.75,
        pattern_title="Tech News",
    )
    assert card.size == CardSize.COMPACT


def test_card_content_invalid_word_count():
    """Test CardContent rejects content with wrong word count for size."""
    # 50 words is too short for LARGE (needs 320-600)
    body = " ".join(["word"] * 50)

    with pytest.raises(ValidationError) as exc_info:
        CardContent(
            title="Test",
            description="Test",
            body=body,
            reading_time_minutes=1,
            sources=[],
            size=CardSize.LARGE,
            confidence=0.8,
            pattern_title="Test",
        )
    assert "Word count" in str(exc_info.value)


# ============================================================================
# DASHBOARD TESTS
# ============================================================================


def test_dashboard_valid_minimum():
    """Test valid Dashboard with minimum 4 cards."""
    now = datetime.now()

    persona = PersonaProfile(
        writing_style="analytical and data-driven", interests=["technology"]
    )

    summary = DataSummary(
        total_interactions=100,
        date_range_start=now - timedelta(days=7),
        date_range_end=now,
        days_analyzed=7,
        platforms=["instagram"],
    )

    colors = ColorScheme(
        primary="#3B82F6",
        secondary="#1E40AF",
        accent="#10B981",
        background_theme=BackgroundTheme(
            type="solid",
            color="#F9FAFB",
            card_background="#FFFFFF",
            card_backdrop_blur=False,
        ),
        fonts=FontScheme(
            heading="Inter",
            body="Inter",
            mono="Fira Code",
            heading_url="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap",
            body_url="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap",
            mono_url="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500&display=swap",
        ),
        foreground="#111827",
        muted="#6B7280",
        success="#10B981",
        warning="#F59E0B",
        destructive="#EF4444",
        mood="professional",
        rationale="Clean, professional palette",
    )

    # Create 4 cards with appropriate word counts
    cards = [
        CardContent(
            title=f"Card {i}",
            description="Description",
            body=" ".join(["word"] * 450),  # LARGE size
            reading_time_minutes=8,
            sources=[],
            size=CardSize.LARGE,
            confidence=0.9,
            pattern_title=f"Pattern {i}",
        )
        for i in range(4)
    ]

    dashboard = Dashboard(
        user_name="Test User",
        color_scheme=colors,
        cards=cards,
        persona=persona,
        data_summary=summary,
        generation_time_seconds=12.5,
    )

    assert dashboard.user_name == "Test User"
    assert len(dashboard.cards) == 4
    assert dashboard.generation_time_seconds == 12.5


def test_dashboard_valid_maximum():
    """Test valid Dashboard with maximum 8 cards."""
    now = datetime.now()

    persona = PersonaProfile(
        writing_style="narrative and story-driven", interests=["travel"]
    )

    summary = DataSummary(
        total_interactions=200,
        date_range_start=now - timedelta(days=30),
        date_range_end=now,
        days_analyzed=30,
        platforms=["instagram", "google"],
    )

    colors = ColorScheme(
        primary="#8B5CF6",
        secondary="#7C3AED",
        accent="#EC4899",
        background_theme=BackgroundTheme(
            type="solid",
            color="#FAF5FF",
            card_background="#FFFFFF",
            card_backdrop_blur=False,
        ),
        fonts=FontScheme(
            heading="Inter",
            body="Inter",
            mono="Fira Code",
            heading_url="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap",
            body_url="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap",
            mono_url="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500&display=swap",
        ),
        foreground="#1F2937",
        muted="#6B7280",
        success="#10B981",
        warning="#F59E0B",
        destructive="#EF4444",
        mood="creative",
        rationale="Vibrant creative palette",
    )

    # Create 8 cards with appropriate word counts
    cards = [
        CardContent(
            title=f"Card {i}",
            description="Description",
            body=" ".join(["word"] * 280),  # MEDIUM size
            reading_time_minutes=4,
            sources=[],
            size=CardSize.MEDIUM,
            confidence=0.85,
            pattern_title=f"Pattern {i}",
        )
        for i in range(8)
    ]

    dashboard = Dashboard(
        user_name="Creative User",
        color_scheme=colors,
        cards=cards,
        persona=persona,
        data_summary=summary,
        generation_time_seconds=15.2,
    )

    assert len(dashboard.cards) == 8


def test_dashboard_invalid_too_few_cards():
    """Test Dashboard rejects fewer than 4 cards."""
    now = datetime.now()

    persona = PersonaProfile(
        writing_style="concise and technical", interests=["tech"]
    )

    summary = DataSummary(
        total_interactions=50,
        date_range_start=now - timedelta(days=7),
        date_range_end=now,
        days_analyzed=7,
        platforms=["instagram"],
    )

    colors = ColorScheme(
        primary="#3B82F6",
        secondary="#1E40AF",
        accent="#10B981",
        background_theme=BackgroundTheme(
            type="solid",
            color="#F9FAFB",
            card_background="#FFFFFF",
            card_backdrop_blur=False,
        ),
        fonts=FontScheme(
            heading="Inter",
            body="Inter",
            mono="Fira Code",
            heading_url="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap",
            body_url="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap",
            mono_url="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500&display=swap",
        ),
        foreground="#111827",
        muted="#6B7280",
        success="#10B981",
        warning="#F59E0B",
        destructive="#EF4444",
        mood="calm",
        rationale="Test",
    )

    # Only 3 cards (too few)
    cards = [
        CardContent(
            title=f"Card {i}",
            description="Description",
            body=" ".join(["word"] * 450),
            reading_time_minutes=8,
            sources=[],
            size=CardSize.LARGE,
            confidence=0.9,
            pattern_title=f"Pattern {i}",
        )
        for i in range(3)
    ]

    with pytest.raises(ValidationError) as exc_info:
        Dashboard(
            user_name="Test",
            color_scheme=colors,
            cards=cards,
            persona=persona,
            data_summary=summary,
            generation_time_seconds=10.0,
        )
    # Pydantic's validation error message will mention "at least 4 items"
    assert "at least 4" in str(exc_info.value) or "min_length=4" in str(exc_info.value)


def test_dashboard_invalid_too_many_cards():
    """Test Dashboard rejects more than 8 cards."""
    now = datetime.now()

    persona = PersonaProfile(
        writing_style="curatorial and aesthetic", interests=["art"]
    )

    summary = DataSummary(
        total_interactions=300,
        date_range_start=now - timedelta(days=30),
        date_range_end=now,
        days_analyzed=30,
        platforms=["instagram", "pinterest"],
    )

    colors = ColorScheme(
        primary="#EC4899",
        secondary="#DB2777",
        accent="#F59E0B",
        background_theme=BackgroundTheme(
            type="solid",
            color="#FFF1F2",
            card_background="#FFFFFF",
            card_backdrop_blur=False,
        ),
        fonts=FontScheme(
            heading="Inter",
            body="Inter",
            mono="Fira Code",
            heading_url="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap",
            body_url="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap",
            mono_url="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500&display=swap",
        ),
        foreground="#1F2937",
        muted="#6B7280",
        success="#10B981",
        warning="#F59E0B",
        destructive="#EF4444",
        mood="vibrant",
        rationale="Test",
    )

    # 9 cards (too many)
    cards = [
        CardContent(
            title=f"Card {i}",
            description="Description",
            body=" ".join(["word"] * 125),
            reading_time_minutes=2,
            sources=[],
            size=CardSize.COMPACT,
            confidence=0.8,
            pattern_title=f"Pattern {i}",
        )
        for i in range(9)
    ]

    with pytest.raises(ValidationError) as exc_info:
        Dashboard(
            user_name="Test",
            color_scheme=colors,
            cards=cards,
            persona=persona,
            data_summary=summary,
            generation_time_seconds=18.0,
        )
    # Pydantic's validation error message will mention "at most 8 items"
    assert "at most 8" in str(exc_info.value) or "max_length=8" in str(exc_info.value)


# ============================================================================
# CONFIG TESTS
# ============================================================================


def test_config_valid():
    """Test valid Config creation."""
    config = Config(
        anthropic_api_key="sk-test-123",
        perplexity_api_key="pplx-test-456",
        days_back=30,
        max_patterns=6,
    )
    assert config.days_back == 30
    assert config.enable_search is True  # default


def test_config_defaults():
    """Test Config uses sensible defaults."""
    config = Config(
        anthropic_api_key="sk-test-123", perplexity_api_key="pplx-test-456"
    )
    assert config.days_back == 30
    assert config.max_patterns == 8
    assert config.enable_search is True
    assert config.debug is False
    assert config.mock_mode is False


def test_config_invalid_days_back():
    """Test Config rejects invalid days_back values."""
    with pytest.raises(ValidationError):
        Config(
            anthropic_api_key="sk-test-123",
            perplexity_api_key="pplx-test-456",
            days_back=400,  # > 365
        )
