#!/usr/bin/env python3
"""Test script to verify pattern detector with real Claude API."""

import os
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from fabric_dashboard.core.data_fetcher import DataFetcher
from fabric_dashboard.core.pattern_detector import PatternDetector
from fabric_dashboard.utils import logger
from fabric_dashboard.utils.config import Config, save_config


def setup_config():
    """Set up configuration with API keys."""
    # Check if API key is in environment
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")

    if not anthropic_key:
        logger.error("ANTHROPIC_API_KEY not found in environment")
        logger.info("Please set it with: export ANTHROPIC_API_KEY='your-key-here'")
        sys.exit(1)

    # Create config (perplexity key is optional for this test)
    config = Config(
        anthropic_api_key=anthropic_key,
        perplexity_api_key=os.getenv("PERPLEXITY_API_KEY", "placeholder"),
        days_back=30,
        mock_mode=False,
    )

    # Save config
    save_config(config)
    logger.success("Configuration saved")
    return config


def test_pattern_detection():
    """Test pattern detection with real Claude API."""
    logger.info("Testing pattern detector with real Claude API")

    # Setup config
    config = setup_config()

    # Step 1: Fetch mock user data
    logger.info("\n[Step 1/2] Fetching user data (using mock data)")
    fetcher = DataFetcher(mock_mode=True)
    user_data = fetcher.fetch_user_data()

    if not user_data:
        logger.error("Failed to fetch user data")
        return

    logger.success(f"Fetched {len(user_data.interactions)} interactions")

    # Step 2: Detect patterns with REAL Claude API
    logger.info("\n[Step 2/2] Detecting patterns with REAL Claude API")
    logger.warning("This will make a real API call and consume tokens")

    detector = PatternDetector(mock_mode=False)  # Real mode!

    try:
        result = detector.detect_patterns(user_data)

        # Display results
        logger.success(f"\n✓ Successfully detected {len(result.patterns)} patterns!")

        print("\n" + "="*80)
        print("DETECTED PATTERNS")
        print("="*80)

        for i, pattern in enumerate(result.patterns, 1):
            print(f"\n{i}. {pattern.title}")
            print(f"   Confidence: {pattern.confidence:.2f}")
            print(f"   Description: {pattern.description}")
            print(f"   Keywords: {', '.join(pattern.keywords)}")
            print(f"   Interaction Count: {pattern.interaction_count}")

        print("\n" + "="*80)
        print("PERSONA PROFILE")
        print("="*80)
        print(f"\nWriting Style: {result.persona.writing_style}")
        print(f"Tone Preference: {result.persona.tone_preference}")
        print(f"Activity Level: {result.persona.activity_level}")
        print(f"Professional Context: {result.persona.professional_context}")
        print(f"Age Range: {result.persona.age_range}")
        print(f"Content Depth: {result.persona.content_depth_preference}")
        print(f"\nInterests:")
        for interest in result.persona.interests:
            print(f"  • {interest}")

        print("\n" + "="*80)
        logger.success("Pattern detection test completed successfully!")

    except Exception as e:
        logger.error(f"Pattern detection failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_pattern_detection()
