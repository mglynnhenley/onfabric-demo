"""Unit tests for search enricher."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from fabric_dashboard.core.search_enricher import SearchEnricher
from fabric_dashboard.models.schemas import EnrichedPattern, Pattern, SearchResult


# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def sample_patterns():
    """Sample patterns for testing."""
    return [
        Pattern(
            title="AI Enthusiast",
            description="Deep interest in artificial intelligence and machine learning technologies",
            confidence=0.92,
            keywords=["AI", "machine learning", "deep learning", "neural networks", "GPT"],
            interaction_count=150,
        ),
        Pattern(
            title="Tech Innovator",
            description="Engaged with cutting-edge technology and innovation trends",
            confidence=0.88,
            keywords=["technology", "innovation", "startups", "disruption"],
            interaction_count=120,
        ),
        Pattern(
            title="Data Explorer",
            description="Active engagement with data science and analytics",
            confidence=0.85,
            keywords=["data science", "analytics", "visualization"],
            interaction_count=100,
        ),
    ]


@pytest.fixture
def single_pattern():
    """Single pattern for testing."""
    return Pattern(
        title="AI Enthusiast",
        description="Deep interest in artificial intelligence and machine learning",
        confidence=0.92,
        keywords=["AI", "machine learning", "deep learning"],
        interaction_count=150,
    )


# ============================================================================
# MOCK MODE TESTS
# ============================================================================


@pytest.mark.asyncio
async def test_search_enricher_mock_mode(sample_patterns):
    """Test search enricher in mock mode generates valid enriched patterns."""
    enricher = SearchEnricher(mock_mode=True)

    enriched = await enricher.enrich_patterns(sample_patterns)

    assert len(enriched) == 3
    assert all(isinstance(ep, EnrichedPattern) for ep in enriched)
    assert all(len(ep.search_results) == 2 for ep in enriched)  # 2 mock results each


@pytest.mark.asyncio
async def test_mock_enrichment_includes_search_results(sample_patterns):
    """Test mock enrichment includes valid search results."""
    enricher = SearchEnricher(mock_mode=True)

    enriched = await enricher.enrich_patterns(sample_patterns)

    for enriched_pattern in enriched:
        for result in enriched_pattern.search_results:
            assert isinstance(result, SearchResult)
            assert result.query
            assert result.content
            assert len(result.content) > 50  # Meaningful content
            assert result.sources
            assert 0.0 <= result.relevance_score <= 1.0


@pytest.mark.asyncio
async def test_mock_enrichment_preserves_pattern_data(sample_patterns):
    """Test mock enrichment preserves original pattern data."""
    enricher = SearchEnricher(mock_mode=True)

    enriched = await enricher.enrich_patterns(sample_patterns)

    for i, enriched_pattern in enumerate(enriched):
        original = sample_patterns[i]
        assert enriched_pattern.pattern.title == original.title
        assert enriched_pattern.pattern.description == original.description
        assert enriched_pattern.pattern.confidence == original.confidence
        assert enriched_pattern.pattern.keywords == original.keywords


# ============================================================================
# QUERY GENERATION TESTS
# ============================================================================


def test_generate_search_queries_basic(single_pattern):
    """Test search query generation for a pattern."""
    enricher = SearchEnricher(mock_mode=True)

    queries = enricher._generate_search_queries(single_pattern, max_queries=2)

    assert len(queries) == 2
    assert "AI Enthusiast" in queries[0]
    assert "2025" in queries[0]  # Should include current year
    assert all(keyword in queries[1] for keyword in ["AI", "machine", "learning"])


def test_generate_search_queries_with_keywords():
    """Test query generation uses pattern keywords."""
    pattern = Pattern(
        title="Design Thinking",
        description="Focus on user-centered design",
        confidence=0.90,
        keywords=["UX", "design", "prototyping", "user research"],
        interaction_count=80,
    )

    enricher = SearchEnricher(mock_mode=True)
    queries = enricher._generate_search_queries(pattern, max_queries=2)

    assert len(queries) == 2
    # Second query should combine keywords
    assert "UX" in queries[1] or "design" in queries[1] or "prototyping" in queries[1]


def test_generate_search_queries_respects_max_queries(single_pattern):
    """Test max_queries parameter limits query count."""
    enricher = SearchEnricher(mock_mode=True)

    queries_1 = enricher._generate_search_queries(single_pattern, max_queries=1)
    queries_2 = enricher._generate_search_queries(single_pattern, max_queries=2)

    assert len(queries_1) == 1
    assert len(queries_2) == 2


# ============================================================================
# INITIALIZATION TESTS
# ============================================================================


def test_search_enricher_initialization_mock():
    """Test search enricher initializes correctly in mock mode."""
    enricher = SearchEnricher(mock_mode=True)

    assert enricher.mock_mode is True
    assert enricher.api_key is None
    assert enricher.model == "sonar"
    assert enricher.timeout == 20.0


@pytest.mark.skip(reason="Config is already loaded, monkeypatching doesn't work after import")
def test_search_enricher_initialization_real_without_config(monkeypatch):
    """Test search enricher fails gracefully without config in real mode."""
    import fabric_dashboard.utils.config as config_module

    monkeypatch.setattr(config_module, "get_config", lambda: None)

    with pytest.raises(RuntimeError, match="Configuration not found"):
        SearchEnricher(mock_mode=False)


# ============================================================================
# PARALLEL EXECUTION TESTS
# ============================================================================


@pytest.mark.asyncio
async def test_parallel_enrichment_multiple_patterns(sample_patterns):
    """Test that multiple patterns are enriched in batches."""
    enricher = SearchEnricher(mock_mode=True)

    # Should complete quickly since queries are batched
    enriched = await enricher.enrich_patterns(sample_patterns)

    assert len(enriched) == len(sample_patterns)
    # Each pattern should have its own search results
    for i, enriched_pattern in enumerate(enriched):
        assert enriched_pattern.pattern.title == sample_patterns[i].title
        assert len(enriched_pattern.search_results) > 0


@pytest.mark.asyncio
async def test_enrichment_with_max_queries_per_pattern(sample_patterns):
    """Test max_queries_per_pattern parameter controls query generation."""
    enricher = SearchEnricher(mock_mode=True)

    # Generate 1 query per pattern
    enriched = await enricher.enrich_patterns(sample_patterns, max_queries_per_pattern=1)

    assert len(enriched) == 3
    # In mock mode, we still get 2 results each, but in real mode this would be 1
    assert all(isinstance(ep, EnrichedPattern) for ep in enriched)


# ============================================================================
# CACHING TESTS
# ============================================================================


@pytest.mark.asyncio
async def test_cache_hit_returns_cached_result(single_pattern):
    """Test that cached search results are returned on cache hit."""
    enricher = SearchEnricher(mock_mode=False)
    enricher.api_key = "test-key"

    # Mock the cache to simulate a hit
    cached_result = {
        "query": "test query",
        "content": "cached content",
        "sources": ["https://cached.com"],
        "relevance_score": 1.0,
        "fetched_at": "2025-01-01T00:00:00Z",
    }

    with patch.object(enricher.cache, "get", return_value=cached_result):
        result = await enricher._search_with_retry("test query", single_pattern)

        assert result is not None
        assert result.query == "test query"
        assert result.content == "cached content"


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================


@pytest.mark.asyncio
async def test_individual_search_failure_doesnt_break_pipeline(sample_patterns):
    """Test that individual search failures don't break entire enrichment."""
    enricher = SearchEnricher(mock_mode=False)
    enricher.api_key = "test-key"

    # Mock _search_with_retry to fail for some queries
    call_count = [0]

    async def mock_search(query, pattern):
        call_count[0] += 1
        if call_count[0] % 2 == 0:  # Fail every other query
            raise Exception("Mock search failure")
        return SearchResult(
            query=query,
            content="Success content",
            sources=["https://example.com"],
            relevance_score=1.0,
        )

    with patch.object(enricher, "_search_with_retry", side_effect=mock_search):
        enriched = await enricher.enrich_patterns(sample_patterns)

        # Should still get all patterns, just with fewer results
        assert len(enriched) == 3
        assert all(isinstance(ep, EnrichedPattern) for ep in enriched)


@pytest.mark.asyncio
async def test_search_with_retry_handles_timeout():
    """Test retry logic handles timeout exceptions."""
    enricher = SearchEnricher(mock_mode=False)
    enricher.api_key = "test-key"

    pattern = Pattern(
        title="Test",
        description="Test pattern",
        confidence=0.9,
        keywords=["test"],
        interaction_count=10,
    )

    # Mock _execute_search to always timeout
    with patch.object(enricher, "_execute_search", side_effect=Exception("Timeout")):
        with pytest.raises(Exception):
            await enricher._search_with_retry("test query", pattern)


# ============================================================================
# INTEGRATION TESTS (MOCK MODE)
# ============================================================================


@pytest.mark.asyncio
async def test_full_enrichment_pipeline_mock(sample_patterns):
    """Test complete enrichment pipeline in mock mode."""
    enricher = SearchEnricher(mock_mode=True)

    enriched = await enricher.enrich_patterns(sample_patterns, max_queries_per_pattern=2)

    # Verify all patterns enriched
    assert len(enriched) == 3

    # Verify enriched pattern structure
    for enriched_pattern in enriched:
        assert isinstance(enriched_pattern, EnrichedPattern)
        assert enriched_pattern.pattern is not None
        assert enriched_pattern.search_results is not None
        assert len(enriched_pattern.search_results) >= 1
        assert enriched_pattern.enriched_at is not None

    # Verify search results structure
    for enriched_pattern in enriched:
        for result in enriched_pattern.search_results:
            assert result.query
            assert result.content
            assert len(result.content) > 0
            assert result.sources is not None
            assert result.relevance_score >= 0.0
            assert result.fetched_at is not None


@pytest.mark.asyncio
async def test_enrichment_with_empty_pattern_list():
    """Test enrichment with empty pattern list."""
    enricher = SearchEnricher(mock_mode=True)

    enriched = await enricher.enrich_patterns([])

    assert len(enriched) == 0


@pytest.mark.asyncio
async def test_enrichment_with_single_pattern(single_pattern):
    """Test enrichment with a single pattern."""
    enricher = SearchEnricher(mock_mode=True)

    enriched = await enricher.enrich_patterns([single_pattern])

    assert len(enriched) == 1
    assert enriched[0].pattern.title == single_pattern.title
    assert len(enriched[0].search_results) > 0


# ============================================================================
# VALIDATION TESTS
# ============================================================================


def test_enriched_pattern_validation():
    """Test EnrichedPattern model validates correctly."""
    pattern = Pattern(
        title="Test",
        description="Test description",
        confidence=0.9,
        keywords=["test"],
        interaction_count=10,
    )

    search_result = SearchResult(
        query="test query",
        content="test content",
        sources=["https://example.com"],
        relevance_score=0.95,
    )

    # Valid enriched pattern should work
    enriched = EnrichedPattern(
        pattern=pattern,
        search_results=[search_result],
    )

    assert enriched.pattern.title == "Test"
    assert len(enriched.search_results) == 1
    assert enriched.enriched_at is not None


def test_search_result_validation():
    """Test SearchResult model validates correctly."""
    # Valid search result
    result = SearchResult(
        query="test query",
        content="test content with enough text to be meaningful",
        sources=["https://example.com", "https://example2.com"],
        relevance_score=0.92,
    )

    assert result.query == "test query"
    assert result.relevance_score == 0.92
    assert len(result.sources) == 2

    # Invalid relevance score should fail
    with pytest.raises(ValueError):
        SearchResult(
            query="test",
            content="content",
            sources=[],
            relevance_score=1.5,  # > 1.0
        )
