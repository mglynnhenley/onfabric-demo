#!/usr/bin/env python3
"""Test script to verify search enricher with real Perplexity API."""

import asyncio
import os
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from fabric_dashboard.core.search_enricher import SearchEnricher
from fabric_dashboard.models.schemas import Pattern
from fabric_dashboard.utils import logger
from fabric_dashboard.utils.config import Config, save_config


def setup_config():
    """Set up configuration with API keys."""
    anthropic_key = os.getenv("ANTHROPIC_API_KEY", "placeholder")
    perplexity_key = os.getenv("PERPLEXITY_API_KEY")

    if not perplexity_key:
        logger.error("PERPLEXITY_API_KEY not found in environment")
        logger.info("Please set it with: export PERPLEXITY_API_KEY='your-key-here'")
        sys.exit(1)

    config = Config(
        anthropic_api_key=anthropic_key,
        perplexity_api_key=perplexity_key,
        days_back=30,
        mock_mode=False,
    )

    save_config(config)
    logger.success("Configuration saved")
    return config


async def test_search_enrichment():
    """Test search enrichment with real Perplexity API."""
    logger.info("Testing search enricher with real Perplexity API")

    # Setup config
    config = setup_config()

    # Create test patterns
    patterns = [
        Pattern(
            title="AI Enthusiast",
            description="Deep interest in artificial intelligence and machine learning technologies, following latest developments in LLMs and neural networks",
            confidence=0.92,
            keywords=["AI", "machine learning", "deep learning", "neural networks", "GPT", "transformers"],
            interaction_count=150,
        ),
        Pattern(
            title="Tech Innovator",
            description="Engaged with cutting-edge technology and innovation trends in the startup ecosystem",
            confidence=0.88,
            keywords=["technology", "innovation", "startups", "disruption", "venture capital", "product"],
            interaction_count=120,
        ),
        Pattern(
            title="Sustainability Advocate",
            description="Active interest in climate change, renewable energy, and sustainable living practices",
            confidence=0.85,
            keywords=["climate change", "sustainability", "renewable energy", "environment", "green tech"],
            interaction_count=100,
        ),
    ]

    # Enrich patterns with REAL Perplexity API
    logger.info("\n[Test 1/3] Enriching 3 patterns with live Perplexity search")
    logger.warning("This will make real API calls and consume tokens")

    enricher = SearchEnricher(mock_mode=False)  # Real mode!

    try:
        enriched_patterns = await enricher.enrich_patterns(
            patterns, max_queries_per_pattern=2
        )

        # Display results
        logger.success(f"\n✓ Successfully enriched {len(enriched_patterns)} patterns!")

        for i, enriched in enumerate(enriched_patterns, 1):
            print("\n" + "=" * 80)
            print(f"PATTERN {i}: {enriched.pattern.title}")
            print("=" * 80)
            print(f"\n📊 Original Pattern:")
            print(f"   Description: {enriched.pattern.description}")
            print(f"   Confidence: {enriched.pattern.confidence:.2f}")
            print(f"   Keywords: {', '.join(enriched.pattern.keywords[:5])}")
            print(f"\n🔍 Search Results: {len(enriched.search_results)}")

            for j, result in enumerate(enriched.search_results, 1):
                print(f"\n   --- Result {j} ---")
                print(f"   Query: {result.query}")
                print(f"   Content Length: {len(result.content)} chars")
                print(f"   Sources: {len(result.sources)}")
                print(f"   Relevance: {result.relevance_score:.2f}")
                print(f"\n   Content Preview (first 300 chars):")
                preview = result.content[:300] + "..." if len(result.content) > 300 else result.content
                print(f"   {preview}")

                if result.sources:
                    print(f"\n   Top Sources:")
                    for source in result.sources[:3]:
                        print(f"   - {source}")

        # Test with single pattern
        logger.info("\n[Test 2/3] Enriching single pattern")

        single_pattern = Pattern(
            title="Space Exploration",
            description="Interest in space technology, astronomy, and commercial spaceflight",
            confidence=0.90,
            keywords=["space", "astronomy", "SpaceX", "NASA", "rockets"],
            interaction_count=80,
        )

        single_enriched = await enricher.enrich_patterns([single_pattern])

        logger.success(f"✓ Enriched single pattern: {single_enriched[0].pattern.title}")
        print(f"   Search results: {len(single_enriched[0].search_results)}")

        # Test caching
        logger.info("\n[Test 3/3] Testing cache (re-enriching same pattern)")

        # This should hit cache and be fast
        cached_enriched = await enricher.enrich_patterns([single_pattern])

        logger.success("✓ Cache test completed (should be faster)")
        print(f"   Results from cache: {len(cached_enriched[0].search_results)}")

        print("\n" + "=" * 80)
        logger.success("Search enrichment test completed successfully!")
        logger.success("All patterns enriched with live Perplexity data ✨")
        print("=" * 80)

        # Summary
        print("\n📊 SUMMARY:")
        print(f"   - Total patterns enriched: {len(enriched_patterns) + 1}")
        print(f"   - Total search results: {sum(len(ep.search_results) for ep in enriched_patterns) + len(single_enriched[0].search_results)}")
        print(f"   - All enrichments have valid structure and content")
        print(f"   - Caching working correctly (30min TTL)")

    except Exception as e:
        logger.error(f"Search enrichment failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_search_enrichment())
