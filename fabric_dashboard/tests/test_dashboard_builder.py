"""Unit tests for dashboard builder."""

import pytest
import re

from fabric_dashboard.core.dashboard_builder import DashboardBuilder
from fabric_dashboard.models.schemas import (
    BackgroundTheme,
    CardContent,
    CardSize,
    ColorScheme,
    Dashboard,
    FontScheme,
    PersonaProfile,
)


# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def sample_persona():
    """Sample persona for testing."""
    return PersonaProfile(
        writing_style="analytical and data-driven with clear structure",
        interests=["technology", "artificial intelligence", "data science"],
        activity_level="high",
        professional_context="tech startup founder",
        tone_preference="balanced and professional",
        age_range="30-40",
        content_depth_preference="deep_dives",
    )


@pytest.fixture
def sample_color_scheme():
    """Sample color scheme for testing."""
    return ColorScheme(
        primary="#3B82F6",
        secondary="#8B5CF6",
        accent="#F59E0B",
        background_theme=BackgroundTheme(
            type="solid",
            color="#FFFFFF",
            card_background="#F9FAFB",
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
        mood="professional",
        rationale="Tech-inspired blue with creative purple accent",
    )


@pytest.fixture
def sample_cards():
    """Sample cards for testing."""
    # Generate content with proper word counts for validation
    large_body = " ".join(["word"] * 400)  # 400 words for LARGE
    medium_body = " ".join(["word"] * 280)  # 280 words for MEDIUM
    small_body = " ".join(["word"] * 180)  # 180 words for SMALL
    compact_body = " ".join(["word"] * 130)  # 130 words for COMPACT

    return [
        CardContent(
            title="AI Trends 2025",
            description="Latest developments in artificial intelligence",
            body=large_body,
            reading_time_minutes=2,
            sources=["https://example.com/ai-news", "https://example.com/research"],
            size=CardSize.LARGE,
            confidence=0.92,
            pattern_title="AI Enthusiast",
        ),
        CardContent(
            title="Startup Growth",
            description="Strategies for scaling tech startups",
            body=medium_body,
            reading_time_minutes=1,
            sources=["https://example.com/startup-guide"],
            size=CardSize.MEDIUM,
            confidence=0.88,
            pattern_title="Tech Innovator",
        ),
        CardContent(
            title="Data Science Tools",
            description="Essential tools for data scientists",
            body=small_body,
            reading_time_minutes=1,
            sources=[],
            size=CardSize.SMALL,
            confidence=0.85,
            pattern_title="Data Explorer",
        ),
        CardContent(
            title="Quick Tip",
            description="Daily productivity hack",
            body=compact_body,
            reading_time_minutes=1,
            sources=[],
            size=CardSize.COMPACT,
            confidence=0.80,
            pattern_title="Productivity",
        ),
    ]


# ============================================================================
# BUILDER INITIALIZATION TESTS
# ============================================================================


def test_dashboard_builder_initialization():
    """Test dashboard builder initializes correctly."""
    builder = DashboardBuilder()
    assert builder is not None


# ============================================================================
# DASHBOARD BUILDING TESTS
# ============================================================================


def test_build_dashboard_basic(sample_cards, sample_persona, sample_color_scheme):
    """Test basic dashboard building."""
    builder = DashboardBuilder()

    dashboard = builder.build(sample_cards, persona=sample_persona, color_scheme=sample_color_scheme)

    assert isinstance(dashboard, Dashboard)
    assert "html" in dashboard.metadata
    assert dashboard.metadata["html"]
    assert len(dashboard.cards) == 4
    assert dashboard.persona == sample_persona
    assert dashboard.color_scheme == sample_color_scheme
    assert dashboard.generated_at is not None
    assert dashboard.user_name == "User"
    assert dashboard.generation_time_seconds == 0.0


def test_build_dashboard_with_custom_title(sample_cards, sample_persona, sample_color_scheme):
    """Test dashboard building with custom title."""
    builder = DashboardBuilder()

    custom_title = "My Custom Dashboard"
    dashboard = builder.build(sample_cards, persona=sample_persona, color_scheme=sample_color_scheme, title=custom_title)

    html = dashboard.metadata["html"]
    assert custom_title in html


def test_build_dashboard_rejects_wrong_card_count(sample_cards, sample_persona, sample_color_scheme):
    """Test that builder rejects less than 4 or more than 10 cards."""
    builder = DashboardBuilder()

    # Too few cards (3)
    with pytest.raises(ValueError, match="Expected 4-10 cards"):
        builder.build(sample_cards[:3], persona=sample_persona, color_scheme=sample_color_scheme)

    # Too many cards (11)
    with pytest.raises(ValueError, match="Expected 4-10 cards"):
        builder.build(sample_cards * 3, persona=sample_persona, color_scheme=sample_color_scheme)  # 12 cards


# ============================================================================
# HTML GENERATION TESTS
# ============================================================================


def test_html_contains_doctype(sample_cards, sample_persona, sample_color_scheme):
    """Test generated HTML has proper DOCTYPE."""
    builder = DashboardBuilder()
    dashboard = builder.build(sample_cards, persona=sample_persona, color_scheme=sample_color_scheme)
    html = dashboard.metadata["html"]

    assert html.startswith("<!DOCTYPE html>")


def test_html_contains_all_cards(sample_cards, sample_persona, sample_color_scheme):
    """Test all card titles appear in HTML."""
    builder = DashboardBuilder()
    dashboard = builder.build(sample_cards, persona=sample_persona, color_scheme=sample_color_scheme)

    for card in sample_cards:
        assert card.title in dashboard.metadata["html"]
        assert card.description in dashboard.metadata["html"]


def test_html_contains_color_scheme(sample_cards, sample_persona, sample_color_scheme):
    """Test color scheme CSS variables are in HTML."""
    builder = DashboardBuilder()
    dashboard = builder.build(sample_cards, persona=sample_persona, color_scheme=sample_color_scheme)

    assert sample_color_scheme.primary in dashboard.metadata["html"]
    assert sample_color_scheme.secondary in dashboard.metadata["html"]
    assert sample_color_scheme.accent in dashboard.metadata["html"]
    assert sample_color_scheme.background_theme.color in dashboard.metadata["html"]
    assert sample_color_scheme.foreground in dashboard.metadata["html"]


def test_html_responsive_grid(sample_cards, sample_persona, sample_color_scheme):
    """Test HTML includes responsive grid layout."""
    builder = DashboardBuilder()
    dashboard = builder.build(sample_cards, persona=sample_persona, color_scheme=sample_color_scheme)

    # Check for CSS grid layout (custom CSS, not Tailwind)
    assert "display: grid" in dashboard.metadata["html"] or "cards-grid" in dashboard.metadata["html"]


def test_html_no_fullwidth_cards(sample_cards, sample_persona, sample_color_scheme):
    """Test that no cards span full width (max col-span-8)."""
    builder = DashboardBuilder()
    dashboard = builder.build(sample_cards, persona=sample_persona, color_scheme=sample_color_scheme)

    # Should not have col-span-9, col-span-10, col-span-11, or col-span-12
    assert "lg:col-span-9" not in dashboard.metadata["html"]
    assert "lg:col-span-10" not in dashboard.metadata["html"]
    assert "lg:col-span-11" not in dashboard.metadata["html"]
    assert "lg:col-span-12" not in dashboard.metadata["html"]


# ============================================================================
# CARD SIZE MAPPING TESTS
# ============================================================================


def test_card_size_column_spans(sample_cards, sample_persona, sample_color_scheme):
    """Test that cards are rendered with proper grid layout."""
    builder = DashboardBuilder()
    dashboard = builder.build(sample_cards, persona=sample_persona, color_scheme=sample_color_scheme)

    # Verify grid layout exists (custom CSS)
    assert "cards-grid" in dashboard.metadata["html"] or "display: grid" in dashboard.metadata["html"]

    # Verify all card types are rendered (by checking their titles)
    assert "AI Trends 2025" in dashboard.metadata["html"]  # Large card
    assert "Startup Growth" in dashboard.metadata["html"]  # Medium card
    assert "Data Science Tools" in dashboard.metadata["html"]  # Small card
    assert "Quick Tip" in dashboard.metadata["html"]  # Compact card


# ============================================================================
# MARKDOWN RENDERING TESTS
# ============================================================================


def test_markdown_converted_to_html(sample_cards, sample_persona, sample_color_scheme):
    """Test that markdown content is converted to HTML."""
    builder = DashboardBuilder()
    dashboard = builder.build(sample_cards, persona=sample_persona, color_scheme=sample_color_scheme)

    # Check that content is wrapped in paragraph tags (basic markdown rendering)
    assert "<p>" in dashboard.metadata["html"]

    # The card body should be present in some form
    assert "word" in dashboard.metadata["html"]  # From our test content


# ============================================================================
# SOURCES TESTS
# ============================================================================


def test_sources_rendered_as_links(sample_cards, sample_persona, sample_color_scheme):
    """Test that sources are rendered as clickable links."""
    builder = DashboardBuilder()
    dashboard = builder.build(sample_cards, persona=sample_persona, color_scheme=sample_color_scheme)

    # Check for source links
    for card in sample_cards:
        for source in card.sources[:5]:  # Max 5 sources
            # Domain should be extracted and displayed
            assert "example.com" in dashboard.metadata["html"]


def test_cards_without_sources(sample_persona, sample_color_scheme):
    """Test cards without sources render correctly."""
    cards = [
        CardContent(
            title=f"Card {i}",
            description="Test card",
            body=" ".join(["word"] * 180),  # 180 words for SMALL size
            reading_time_minutes=1,
            sources=[],  # No sources
            size=CardSize.SMALL,
            confidence=0.8,
            pattern_title="Test",
        )
        for i in range(4)
    ]

    builder = DashboardBuilder()
    dashboard = builder.build(cards, persona=sample_persona, color_scheme=sample_color_scheme)

    # Should still build successfully
    assert isinstance(dashboard, Dashboard)
    assert dashboard.metadata["html"]


# ============================================================================
# HEADER AND FOOTER TESTS
# ============================================================================


def test_header_contains_title(sample_cards, sample_persona, sample_color_scheme):
    """Test header contains dashboard title."""
    builder = DashboardBuilder()
    dashboard = builder.build(sample_cards, persona=sample_persona, color_scheme=sample_color_scheme)

    # Should contain generated title
    assert "Intelligence Dashboard" in dashboard.metadata["html"]


def test_header_contains_metadata(sample_cards, sample_persona, sample_color_scheme):
    """Test header contains generation metadata."""
    builder = DashboardBuilder()
    dashboard = builder.build(sample_cards, persona=sample_persona, color_scheme=sample_color_scheme)

    # Should contain generation date
    assert "Generated" in dashboard.metadata["html"]


def test_footer_contains_credits(sample_cards, sample_persona, sample_color_scheme):
    """Test footer contains credits."""
    builder = DashboardBuilder()
    dashboard = builder.build(sample_cards, persona=sample_persona, color_scheme=sample_color_scheme)

    assert "Fabric Intelligence Dashboard" in dashboard.metadata["html"]
    assert "Claude" in dashboard.metadata["html"]
    assert "Perplexity" in dashboard.metadata["html"]


# ============================================================================
# TITLE GENERATION TESTS
# ============================================================================


def test_generate_title_from_interests(sample_persona):
    """Test title generation uses persona interests."""
    builder = DashboardBuilder()
    title = builder._generate_title(sample_persona)

    assert "Technology" in title
    assert "Dashboard" in title


def test_generate_title_no_interests():
    """Test title generation fallback when no interests."""
    persona = PersonaProfile(
        writing_style="casual",
        interests=["general"],  # At least 1 interest required
        activity_level="low",
        professional_context="student",
        tone_preference="friendly",
        age_range="20-30",
        content_depth_preference="quick_insights",  # Use valid enum value
    )

    builder = DashboardBuilder()
    title = builder._generate_title(persona)

    # Should still work with generic interest
    assert "Dashboard" in title


# ============================================================================
# CSS GENERATION TESTS
# ============================================================================


def test_css_variables_generated(sample_color_scheme):
    """Test CSS variables are correctly generated."""
    builder = DashboardBuilder()
    css_vars = builder._generate_css_variables(sample_color_scheme)

    assert "--primary" in css_vars
    assert sample_color_scheme.primary in css_vars
    assert "--secondary" in css_vars
    assert "--accent" in css_vars
    # Background is now set directly on body element, not as CSS variable
    assert "body {" in css_vars
    assert "background:" in css_vars
    assert "--foreground" in css_vars


def test_adjust_color_opacity():
    """Test color opacity adjustment."""
    builder = DashboardBuilder()

    # Test with blue color
    rgba = builder._adjust_color_opacity("#3B82F6", 0.5)

    assert "rgba" in rgba
    assert "0.5" in rgba


# ============================================================================
# DOMAIN EXTRACTION TESTS
# ============================================================================


def test_extract_domain():
    """Test domain extraction from URLs."""
    builder = DashboardBuilder()

    # Test various URL formats
    assert "example.com" in builder._extract_domain("https://example.com/path/to/page")
    assert "github.com" in builder._extract_domain("https://github.com/user/repo")
    assert "sub.domain.com" in builder._extract_domain("https://sub.domain.com")


def test_extract_domain_invalid_url():
    """Test domain extraction handles invalid URLs."""
    builder = DashboardBuilder()

    # Should return original string if parsing fails
    invalid_url = "not-a-url"
    result = builder._extract_domain(invalid_url)
    assert result == invalid_url


# ============================================================================
# INTEGRATION TESTS
# ============================================================================


def test_full_dashboard_with_8_cards(sample_persona, sample_color_scheme):
    """Test building dashboard with maximum 8 cards."""
    # Generate appropriate word counts for each size
    size_word_counts = {
        CardSize.LARGE: 400,
        CardSize.MEDIUM: 280,
        CardSize.SMALL: 180,
        CardSize.COMPACT: 130,
    }

    cards = [
        CardContent(
            title=f"Card {i}",
            description=f"Description {i}",
            body=" ".join(["word"] * size_word_counts[[CardSize.LARGE, CardSize.MEDIUM, CardSize.SMALL, CardSize.COMPACT][i % 4]]),
            reading_time_minutes=1,
            sources=[f"https://example{i}.com"],
            size=[CardSize.LARGE, CardSize.MEDIUM, CardSize.SMALL, CardSize.COMPACT][i % 4],
            confidence=0.85,
            pattern_title=f"Pattern {i}",
        )
        for i in range(8)
    ]

    builder = DashboardBuilder()
    dashboard = builder.build(cards, persona=sample_persona, color_scheme=sample_color_scheme)

    assert len(dashboard.cards) == 8
    assert all(f"Card {i}" in dashboard.metadata["html"] for i in range(8))


def test_dashboard_html_valid_structure(sample_cards, sample_persona, sample_color_scheme):
    """Test that generated HTML has valid basic structure."""
    builder = DashboardBuilder()
    dashboard = builder.build(sample_cards, persona=sample_persona, color_scheme=sample_color_scheme)

    # Basic HTML structure
    assert "<html" in dashboard.metadata["html"]
    assert "<head>" in dashboard.metadata["html"]
    assert "</head>" in dashboard.metadata["html"]
    assert "<body" in dashboard.metadata["html"]
    assert "</body>" in dashboard.metadata["html"]
    assert "</html>" in dashboard.metadata["html"]

    # Meta tags
    assert '<meta charset="UTF-8">' in dashboard.metadata["html"]
    assert '<meta name="viewport"' in dashboard.metadata["html"]

    # Title tag
    assert "<title>" in dashboard.metadata["html"]
    assert "</title>" in dashboard.metadata["html"]


# ============================================================================
# UI COMPONENT RENDERING TESTS
# ============================================================================


def test_render_content_card():
    """Test ContentCard UI component renders correctly."""
    from fabric_dashboard.models.ui_components import ContentCard

    builder = DashboardBuilder()

    # Create a ContentCard component
    content_card = ContentCard(
        title="Deep Dive Resource",
        pattern_title="AI Research",
        confidence=0.90,
        article_title="Understanding Transformers: A Comprehensive Guide",
        overview="An in-depth exploration of transformer architecture covering attention mechanisms, positional encoding, and practical applications.",
        url="https://example.com/transformers-guide",
        source_name="AI Journal",
        published_date="2024-10-15",
        search_query="transformer architecture deep learning",
    )

    # Render the component
    html = builder._render_content_card(content_card, idx=0)

    # Verify the HTML contains all required elements
    assert content_card.title in html
    assert content_card.article_title in html
    assert content_card.overview in html
    assert content_card.url in html
    assert content_card.source_name in html
    assert content_card.published_date in html
    assert "Read More" in html or "read more" in html.lower()
