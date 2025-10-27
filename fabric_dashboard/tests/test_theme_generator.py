"""Unit tests for theme generator."""

import pytest

from fabric_dashboard.core.theme_generator import ThemeGenerator
from fabric_dashboard.models.schemas import ColorScheme, Pattern, PersonaProfile


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
def creative_persona():
    """Creative persona for testing."""
    return PersonaProfile(
        writing_style="narrative and emotionally engaging",
        interests=["design", "art", "creative writing"],
        activity_level="moderate",
        professional_context="creative professional",
        tone_preference="expressive and vibrant",
        age_range="25-35",
        content_depth_preference="balanced",
    )


@pytest.fixture
def professional_persona():
    """Professional persona for testing."""
    return PersonaProfile(
        writing_style="formal and structured",
        interests=["business", "finance", "leadership"],
        activity_level="moderate",
        professional_context="corporate executive",
        tone_preference="formal and professional",
        age_range="40-55",
        content_depth_preference="balanced",
    )


@pytest.fixture
def sample_patterns():
    """Sample patterns for testing."""
    return [
        Pattern(
            title="AI Enthusiast",
            description="Deep interest in artificial intelligence and machine learning",
            confidence=0.92,
            keywords=["AI", "machine learning", "deep learning", "neural networks"],
            interaction_count=150,
        ),
        Pattern(
            title="Tech Innovator",
            description="Engaged with cutting-edge technology and innovation",
            confidence=0.88,
            keywords=["technology", "innovation", "startups", "disruption"],
            interaction_count=120,
        ),
        Pattern(
            title="Data Explorer",
            description="Active engagement with data science and analytics",
            confidence=0.85,
            keywords=["data science", "analytics", "visualization", "statistics"],
            interaction_count=100,
        ),
    ]


# ============================================================================
# DEFAULT THEME TESTS
# ============================================================================


def test_theme_generator_mock_mode(sample_persona, sample_patterns):
    """Test theme generator in mock mode returns default theme."""
    generator = ThemeGenerator(mock_mode=True)

    theme = generator.generate_theme(sample_persona, sample_patterns)

    assert isinstance(theme, ColorScheme)
    assert theme.mood == "professional and balanced"
    assert theme.primary == "#3b82f6"


def test_default_theme_structure():
    """Test default theme has all required fields."""
    generator = ThemeGenerator(mock_mode=True)

    theme = generator._default_theme()

    # Check all colors are present and valid hex codes
    assert theme.primary.startswith("#") and len(theme.primary) == 7
    assert theme.secondary.startswith("#") and len(theme.secondary) == 7
    assert theme.accent.startswith("#") and len(theme.accent) == 7
    assert theme.background.startswith("#") and len(theme.background) == 7
    assert theme.card.startswith("#") and len(theme.card) == 7
    assert theme.foreground.startswith("#") and len(theme.foreground) == 7
    assert theme.muted.startswith("#") and len(theme.muted) == 7
    assert theme.success.startswith("#") and len(theme.success) == 7
    assert theme.warning.startswith("#") and len(theme.warning) == 7
    assert theme.destructive.startswith("#") and len(theme.destructive) == 7

    # Check metadata
    assert theme.mood
    assert theme.rationale
    assert len(theme.mood) > 0
    assert len(theme.rationale) > 0


# ============================================================================
# VALIDATION TESTS
# ============================================================================


def test_color_scheme_validation_hex():
    """Test ColorScheme validates hex codes correctly."""
    # Valid hex codes should work
    valid_scheme = ColorScheme(
        primary="#3b82f6",
        secondary="#8b5cf6",
        accent="#06b6d4",
        background="#ffffff",
        card="#f8fafc",
        foreground="#0f172a",
        muted="#64748b",
        success="#22c55e",
        warning="#f59e0b",
        destructive="#ef4444",
        mood="professional",
        rationale="Test theme",
    )
    assert valid_scheme.primary == "#3b82f6"

    # Invalid hex codes should fail
    with pytest.raises(ValueError):
        ColorScheme(
            primary="3b82f6",  # Missing #
            secondary="#8b5cf6",
            accent="#06b6d4",
            background="#ffffff",
            card="#f8fafc",
            foreground="#0f172a",
            muted="#64748b",
            success="#22c55e",
            warning="#f59e0b",
            destructive="#ef4444",
            mood="professional",
            rationale="Test theme",
        )

    with pytest.raises(ValueError):
        ColorScheme(
            primary="#3b8",  # Too short
            secondary="#8b5cf6",
            accent="#06b6d4",
            background="#ffffff",
            card="#f8fafc",
            foreground="#0f172a",
            muted="#64748b",
            success="#22c55e",
            warning="#f59e0b",
            destructive="#ef4444",
            mood="professional",
            rationale="Test theme",
        )


def test_color_scheme_validation_mood():
    """Test ColorScheme validates mood field."""
    # Valid mood
    valid_scheme = ColorScheme(
        primary="#3b82f6",
        secondary="#8b5cf6",
        accent="#06b6d4",
        background="#ffffff",
        card="#f8fafc",
        foreground="#0f172a",
        muted="#64748b",
        success="#22c55e",
        warning="#f59e0b",
        destructive="#ef4444",
        mood="energetic and vibrant",
        rationale="Test theme",
    )
    assert valid_scheme.mood == "energetic and vibrant"

    # Empty mood should fail
    with pytest.raises(ValueError):
        ColorScheme(
            primary="#3b82f6",
            secondary="#8b5cf6",
            accent="#06b6d4",
            background="#ffffff",
            card="#f8fafc",
            foreground="#0f172a",
            muted="#64748b",
            success="#22c55e",
            warning="#f59e0b",
            destructive="#ef4444",
            mood="",  # Empty
            rationale="Test theme",
        )


# ============================================================================
# PROMPT BUILDING TESTS
# ============================================================================


def test_build_prompt():
    """Test prompt template is built correctly."""
    generator = ThemeGenerator(mock_mode=True)

    prompt = generator._build_prompt()

    assert prompt is not None
    assert len(prompt.messages) == 2  # System + Human
    assert "color" in prompt.messages[0].prompt.template.lower()
    assert "persona" in prompt.messages[1].prompt.template.lower()


def test_prepare_context(sample_persona, sample_patterns):
    """Test context preparation includes all relevant info."""
    generator = ThemeGenerator(mock_mode=True)

    context = generator._prepare_context(sample_persona, sample_patterns)

    assert "analytical and data-driven" in context
    assert "technology" in context
    assert "high" in context
    assert "AI Enthusiast" in context
    assert "Tech Innovator" in context


def test_prepare_context_minimal_persona():
    """Test context preparation with minimal persona."""
    minimal_persona = PersonaProfile(
        writing_style="simple",
        interests=["general"],
        activity_level="low",
    )
    patterns = []

    generator = ThemeGenerator(mock_mode=True)
    context = generator._prepare_context(minimal_persona, patterns)

    assert "simple" in context
    assert "general" in context
    assert "low" in context


# ============================================================================
# INTEGRATION TESTS (MOCK MODE)
# ============================================================================


def test_generate_theme_with_different_personas(
    sample_persona, creative_persona, professional_persona, sample_patterns
):
    """Test theme generation with different persona types."""
    generator = ThemeGenerator(mock_mode=True)

    # All should return valid themes
    tech_theme = generator.generate_theme(sample_persona, sample_patterns)
    creative_theme = generator.generate_theme(creative_persona, sample_patterns)
    professional_theme = generator.generate_theme(professional_persona, sample_patterns)

    assert isinstance(tech_theme, ColorScheme)
    assert isinstance(creative_theme, ColorScheme)
    assert isinstance(professional_theme, ColorScheme)


def test_theme_generator_initialization_mock():
    """Test theme generator initializes correctly in mock mode."""
    generator = ThemeGenerator(mock_mode=True)

    assert generator.mock_mode is True
    assert generator.llm is None


@pytest.mark.skip(reason="Config is already loaded, monkeypatching doesn't work after import")
def test_theme_generator_initialization_real_without_config(monkeypatch):
    """Test theme generator fails gracefully without config in real mode."""
    # Mock get_config to return None
    import fabric_dashboard.utils.config as config_module

    monkeypatch.setattr(config_module, "get_config", lambda: None)

    with pytest.raises(RuntimeError, match="Configuration not found"):
        ThemeGenerator(mock_mode=False)


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================


def test_generate_theme_fallback_on_error(sample_persona, sample_patterns, monkeypatch):
    """Test theme generator falls back to default on error."""
    generator = ThemeGenerator(mock_mode=False)

    # Mock LLM to raise error
    def mock_invoke(*args, **kwargs):
        raise Exception("API error")

    generator.llm = type("MockLLM", (), {"with_structured_output": lambda self, schema: type("MockStructured", (), {"__or__": lambda self, other: type("MockChain", (), {"invoke": mock_invoke})()})()})()

    # Should fall back to default theme
    theme = generator.generate_theme(sample_persona, sample_patterns)

    assert isinstance(theme, ColorScheme)
    assert theme.mood == "professional and balanced"  # Default theme
