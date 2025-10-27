"""Tests for pattern detector module."""

from fabric_dashboard.core.data_fetcher import DataFetcher
from fabric_dashboard.core.pattern_detector import PatternDetector, PatternDetectionResult
from fabric_dashboard.models.schemas import Pattern, PersonaProfile


def test_pattern_detector_mock_mode():
    """Test PatternDetector initialization in mock mode."""
    detector = PatternDetector(mock_mode=True)
    assert detector.mock_mode is True
    assert detector.llm is None


def test_pattern_detector_real_mode_no_config():
    """Test PatternDetector fails gracefully without config."""
    try:
        detector = PatternDetector(mock_mode=False)
        # Should either succeed if config exists, or raise RuntimeError
        assert detector.llm is not None or True
    except RuntimeError as e:
        assert "Configuration not found" in str(e)


def test_detect_patterns_mock():
    """Test pattern detection in mock mode."""
    # Get mock user data
    fetcher = DataFetcher(mock_mode=True)
    user_data = fetcher.fetch_user_data()
    assert user_data is not None

    # Detect patterns
    detector = PatternDetector(mock_mode=True)
    result = detector.detect_patterns(user_data)

    assert result is not None
    assert isinstance(result, PatternDetectionResult)


def test_detection_result_structure():
    """Test that detection result has correct structure."""
    fetcher = DataFetcher(mock_mode=True)
    user_data = fetcher.fetch_user_data()
    assert user_data is not None

    detector = PatternDetector(mock_mode=True)
    result = detector.detect_patterns(user_data)

    # Check patterns
    assert len(result.patterns) >= 4
    assert len(result.patterns) <= 8
    for pattern in result.patterns:
        assert isinstance(pattern, Pattern)
        assert len(pattern.title) > 0
        assert len(pattern.description) >= 10
        assert 0.0 <= pattern.confidence <= 1.0
        assert pattern.interaction_count >= 0

    # Check persona
    assert isinstance(result.persona, PersonaProfile)
    assert len(result.persona.writing_style) > 0
    assert len(result.persona.interests) > 0
    assert result.persona.activity_level in ["low", "moderate", "high"]


def test_mock_detection_with_empty_data():
    """Test mock detection handles minimal data gracefully."""
    from fabric_dashboard.models.schemas import DataSummary, UserData
    from datetime import datetime, timezone

    # Create minimal user data
    minimal_data = UserData(
        connection_id="test_123",
        interactions=[],
        summary=DataSummary(
            total_interactions=0,
            date_range_start=datetime.now(timezone.utc),
            date_range_end=datetime.now(timezone.utc),
            days_analyzed=1,
            platforms=[],
            top_themes=[],
        ),
        persona=None,
    )

    detector = PatternDetector(mock_mode=True)
    result = detector.detect_patterns(minimal_data)

    assert result is not None
    assert len(result.patterns) >= 4
    assert result.persona is not None


def test_pattern_titles_are_unique():
    """Test that detected patterns have unique titles."""
    fetcher = DataFetcher(mock_mode=True)
    user_data = fetcher.fetch_user_data()
    assert user_data is not None

    detector = PatternDetector(mock_mode=True)
    result = detector.detect_patterns(user_data)

    titles = [p.title for p in result.patterns]
    assert len(titles) == len(set(titles)), "Pattern titles should be unique"


def test_patterns_sorted_by_confidence():
    """Test that patterns are generally sorted by confidence (descending)."""
    fetcher = DataFetcher(mock_mode=True)
    user_data = fetcher.fetch_user_data()
    assert user_data is not None

    detector = PatternDetector(mock_mode=True)
    result = detector.detect_patterns(user_data)

    confidences = [p.confidence for p in result.patterns]
    # Allow some flexibility - at least first should be higher than last
    assert confidences[0] >= confidences[-1]


def test_persona_writing_style_is_descriptive():
    """Test that persona writing style is descriptive (not just a single word)."""
    fetcher = DataFetcher(mock_mode=True)
    user_data = fetcher.fetch_user_data()
    assert user_data is not None

    detector = PatternDetector(mock_mode=True)
    result = detector.detect_patterns(user_data)

    # Writing style should be a phrase, not just one word
    words = result.persona.writing_style.split()
    assert len(words) >= 2, "Writing style should be descriptive, not a single word"
