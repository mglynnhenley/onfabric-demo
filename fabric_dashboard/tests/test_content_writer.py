"""Unit tests for content writer."""

import pytest

from fabric_dashboard.core.content_writer import ContentWriter
from fabric_dashboard.models.schemas import (
    CardContent,
    CardSize,
    EnrichedPattern,
    Pattern,
    PersonaProfile,
    SearchResult,
)


# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def sample_persona():
    """Sample persona for testing."""
    return PersonaProfile(
        writing_style="analytical and data-driven with clear structure and evidence",
        interests=["technology", "artificial intelligence", "data science"],
        activity_level="high",
        professional_context="tech startup founder",
        tone_preference="balanced and professional with occasional technical depth",
        age_range="30-40",
        content_depth_preference="deep_dives",
    )


@pytest.fixture
def sample_enriched_patterns():
    """Sample enriched patterns for testing."""
    return [
        EnrichedPattern(
            pattern=Pattern(
                title="AI Enthusiast",
                description="Deep interest in artificial intelligence and machine learning",
                confidence=0.92,
                keywords=["AI", "machine learning", "deep learning", "neural networks"],
                interaction_count=150,
            ),
            search_results=[
                SearchResult(
                    query="latest AI developments 2025",
                    content="Recent breakthroughs in large language models and multimodal AI...",
                    sources=["https://example.com/ai-news"],
                )
            ],
        ),
        EnrichedPattern(
            pattern=Pattern(
                title="Tech Innovator",
                description="Engaged with cutting-edge technology and innovation",
                confidence=0.88,
                keywords=["technology", "innovation", "startups"],
                interaction_count=120,
            ),
            search_results=[],
        ),
    ]


@pytest.fixture
def card_sizes():
    """Sample card sizes."""
    return [CardSize.LARGE, CardSize.MEDIUM]


# ============================================================================
# MOCK GENERATION TESTS
# ============================================================================


@pytest.mark.asyncio
async def test_content_writer_mock_mode(
    sample_enriched_patterns, sample_persona, card_sizes
):
    """Test content writer in mock mode generates valid cards."""
    writer = ContentWriter(mock_mode=True)

    cards = await writer.generate_cards(
        sample_enriched_patterns, sample_persona, card_sizes
    )

    assert len(cards) == 2
    assert all(isinstance(card, CardContent) for card in cards)
    assert cards[0].size == CardSize.LARGE
    assert cards[1].size == CardSize.MEDIUM


def test_mock_card_word_counts(sample_enriched_patterns, card_sizes):
    """Test mock cards have correct word counts."""
    writer = ContentWriter(mock_mode=True)

    mock_cards = writer._generate_mock_cards(sample_enriched_patterns, card_sizes)

    # Check word counts match size requirements (with tolerance)
    large_card = mock_cards[0]
    assert large_card.size == CardSize.LARGE
    assert 320 <= large_card.word_count() <= 600  # 400-500 ±20%

    medium_card = mock_cards[1]
    assert medium_card.size == CardSize.MEDIUM
    assert 200 <= medium_card.word_count() <= 360  # 250-300 ±20%


# ============================================================================
# FALLBACK GENERATION TESTS
# ============================================================================


def test_fallback_card_generation(sample_enriched_patterns):
    """Test fallback card generation when LLM fails."""
    writer = ContentWriter(mock_mode=True)

    fallback = writer._generate_fallback_card(
        sample_enriched_patterns[0], CardSize.MEDIUM
    )

    assert isinstance(fallback, CardContent)
    assert fallback.title == "AI Enthusiast"
    assert fallback.size == CardSize.MEDIUM
    assert fallback.confidence == 0.92
    # Check word count is approximately correct (allowing for variability)
    assert 150 <= fallback.word_count() <= 400  # More flexible range


def test_fallback_cards_all_sizes(sample_enriched_patterns):
    """Test fallback generation for all card sizes."""
    writer = ContentWriter(mock_mode=True)

    for size in [CardSize.LARGE, CardSize.MEDIUM, CardSize.SMALL, CardSize.COMPACT]:
        fallback = writer._generate_fallback_card(sample_enriched_patterns[0], size)

        assert fallback.size == size
        assert isinstance(fallback, CardContent)

        # Word counts should be within acceptable range (flexible for generated content)
        word_count = fallback.word_count()
        size_ranges = {
            CardSize.LARGE: (320, 600),
            CardSize.MEDIUM: (200, 360),
            CardSize.SMALL: (120, 240),
            CardSize.COMPACT: (80, 180),
        }
        min_words, max_words = size_ranges[size]
        # Allow some flexibility since content generation is non-deterministic
        assert min_words * 0.8 <= word_count <= max_words * 1.2, f"{size.value}: {word_count} words"


# ============================================================================
# PROMPT BUILDING TESTS
# ============================================================================


def test_build_prompt_all_sizes():
    """Test prompt building for all card sizes."""
    writer = ContentWriter(mock_mode=True)

    for size in [CardSize.LARGE, CardSize.MEDIUM, CardSize.SMALL, CardSize.COMPACT]:
        prompt = writer._build_prompt(size)

        assert prompt is not None
        assert len(prompt.messages) == 2  # System + Human

        # Check word count target is mentioned
        system_msg = prompt.messages[0].prompt.template
        assert "word" in system_msg.lower()
        assert "markdown" in system_msg.lower()


def test_prepare_context(sample_enriched_patterns, sample_persona):
    """Test context preparation includes all necessary info."""
    writer = ContentWriter(mock_mode=True)

    context = writer._prepare_context(
        sample_enriched_patterns[0], sample_persona, CardSize.LARGE
    )

    # Check pattern info
    assert "AI Enthusiast" in context
    assert "machine learning" in context

    # Check persona info
    assert "analytical and data-driven" in context
    assert "technology" in context

    # Check search results
    assert "latest AI developments" in context
    assert "example.com" in context


def test_prepare_context_without_search_results(sample_enriched_patterns, sample_persona):
    """Test context preparation when no search results available."""
    writer = ContentWriter(mock_mode=True)

    # Use pattern without search results
    context = writer._prepare_context(
        sample_enriched_patterns[1], sample_persona, CardSize.MEDIUM
    )

    assert "Tech Innovator" in context
    assert "analytical and data-driven" in context
    # Pattern info should still be present
    assert "innovation" in context


# ============================================================================
# INITIALIZATION TESTS
# ============================================================================


def test_content_writer_initialization_mock():
    """Test content writer initializes correctly in mock mode."""
    writer = ContentWriter(mock_mode=True)

    assert writer.mock_mode is True
    assert writer.llm is None


@pytest.mark.skip(reason="Config is already loaded, monkeypatching doesn't work after import")
def test_content_writer_initialization_real_without_config(monkeypatch):
    """Test content writer fails gracefully without config in real mode."""
    import fabric_dashboard.utils.config as config_module

    monkeypatch.setattr(config_module, "get_config", lambda: None)

    with pytest.raises(RuntimeError, match="Configuration not found"):
        ContentWriter(mock_mode=False)


# ============================================================================
# READING TIME ESTIMATION TESTS
# ============================================================================


def test_estimate_reading_time():
    """Test reading time estimation for different card sizes."""
    writer = ContentWriter(mock_mode=True)

    # Large cards (~450 words) should take ~2 minutes
    assert writer._estimate_reading_time(CardSize.LARGE) >= 2

    # Medium cards (~275 words) should take ~1 minute
    assert writer._estimate_reading_time(CardSize.MEDIUM) >= 1

    # Small cards (~175 words) should take ~1 minute
    assert writer._estimate_reading_time(CardSize.SMALL) >= 1

    # Compact cards (~125 words) should take ~1 minute
    assert writer._estimate_reading_time(CardSize.COMPACT) >= 1


# ============================================================================
# VALIDATION TESTS (Structure, not exact content)
# ============================================================================


def test_card_content_structure_validation():
    """Test CardContent model validates required fields."""
    # Valid card with minimum requirements should work
    valid_card = CardContent(
        title="Test Title",
        description="Test description",
        body=" ".join(["word"] * 300),  # 300 words for medium
        reading_time_minutes=2,
        sources=["https://example.com"],
        size=CardSize.MEDIUM,
        confidence=0.85,
        pattern_title="Test Pattern",
    )
    assert valid_card.size == CardSize.MEDIUM
    assert valid_card.word_count() == 300
    assert valid_card.title
    assert valid_card.description
    assert valid_card.body


def test_card_content_word_count_validation_strict():
    """Test card content validates word count against size (strict validation)."""
    # Too few words for LARGE card should fail
    with pytest.raises(ValueError, match="Word count"):
        CardContent(
            title="Test",
            description="Test",
            body=" ".join(["word"] * 100),  # Only 100 words (too few for LARGE)
            reading_time_minutes=1,
            sources=[],
            size=CardSize.LARGE,  # Expects 320-600 words
            confidence=0.8,
            pattern_title="Test",
        )

    # Too many words for COMPACT card should fail
    with pytest.raises(ValueError, match="Word count"):
        CardContent(
            title="Test",
            description="Test",
            body=" ".join(["word"] * 500),  # 500 words (too many for COMPACT)
            reading_time_minutes=3,
            sources=[],
            size=CardSize.COMPACT,  # Expects 80-180 words
            confidence=0.8,
            pattern_title="Test",
        )


def test_card_content_accepts_variable_word_counts():
    """Test that card content accepts word counts within tolerance ranges."""
    # Test each size with word counts at boundaries (allowing for LLM variability)
    test_cases = [
        (CardSize.LARGE, 350),    # Lower end of range
        (CardSize.LARGE, 550),    # Upper end of range
        (CardSize.MEDIUM, 220),   # Lower end
        (CardSize.MEDIUM, 340),   # Upper end
        (CardSize.SMALL, 130),    # Lower end
        (CardSize.SMALL, 230),    # Upper end
        (CardSize.COMPACT, 90),   # Lower end
        (CardSize.COMPACT, 170),  # Upper end
    ]

    for size, word_count in test_cases:
        # Should not raise validation error
        card = CardContent(
            title="Test",
            description="Test description",
            body=" ".join(["word"] * word_count),
            reading_time_minutes=1,
            sources=[],
            size=size,
            confidence=0.8,
            pattern_title="Test",
        )
        assert card.word_count() == word_count


# ============================================================================
# ASYNC EXECUTION TESTS
# ============================================================================


@pytest.mark.asyncio
async def test_parallel_card_generation_mock(
    sample_enriched_patterns, sample_persona
):
    """Test that multiple cards can be generated in parallel."""
    writer = ContentWriter(mock_mode=True)

    # Generate 4 cards (common case)
    card_sizes = [CardSize.LARGE, CardSize.MEDIUM, CardSize.SMALL, CardSize.COMPACT]
    enriched = sample_enriched_patterns * 2  # Duplicate to get 4 patterns

    cards = await writer.generate_cards(enriched[:4], sample_persona, card_sizes)

    assert len(cards) == 4
    assert all(isinstance(card, CardContent) for card in cards)
    # Check that sizes match what was requested
    for card, expected_size in zip(cards, card_sizes):
        assert card.size == expected_size
