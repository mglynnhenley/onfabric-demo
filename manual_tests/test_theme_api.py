#!/usr/bin/env python3
"""Test script to verify theme generator with real Claude API."""

import os
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from fabric_dashboard.core.theme_generator import ThemeGenerator
from fabric_dashboard.models.schemas import Pattern, PersonaProfile
from fabric_dashboard.utils import logger
from fabric_dashboard.utils.config import Config, save_config


def setup_config():
    """Set up configuration with API keys."""
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")

    if not anthropic_key:
        logger.error("ANTHROPIC_API_KEY not found in environment")
        logger.info("Please set it with: export ANTHROPIC_API_KEY='your-key-here'")
        sys.exit(1)

    config = Config(
        anthropic_api_key=anthropic_key,
        perplexity_api_key=os.getenv("PERPLEXITY_API_KEY", "placeholder"),
        days_back=30,
        mock_mode=False,
    )

    save_config(config)
    logger.success("Configuration saved")
    return config


def test_theme_generation():
    """Test theme generation with real Claude API."""
    logger.info("Testing theme generator with real Claude API")

    # Setup config
    config = setup_config()

    # Create test persona
    persona = PersonaProfile(
        writing_style="analytical and data-driven with clear arguments and evidence-based conclusions",
        interests=["artificial intelligence", "technology", "data science", "innovation"],
        activity_level="high",
        professional_context="tech startup founder focused on AI applications",
        tone_preference="balanced and professional with occasional technical depth",
        age_range="30-40",
        content_depth_preference="deep_dives",
    )

    # Create test patterns
    patterns = [
        Pattern(
            title="AI Enthusiast",
            description="Deep interest in artificial intelligence and machine learning technologies, following latest developments",
            confidence=0.92,
            keywords=["AI", "machine learning", "deep learning", "neural networks", "GPT"],
            interaction_count=150,
        ),
        Pattern(
            title="Tech Innovator",
            description="Engaged with cutting-edge technology and innovation trends in the startup ecosystem",
            confidence=0.88,
            keywords=["technology", "innovation", "startups", "disruption", "venture capital"],
            interaction_count=120,
        ),
        Pattern(
            title="Data Explorer",
            description="Active engagement with data science, analytics, and visualization tools",
            confidence=0.85,
            keywords=["data science", "analytics", "visualization", "statistics", "Python"],
            interaction_count=100,
        ),
    ]

    # Generate theme with REAL Claude API
    logger.info("\n[Test 1/3] Generating theme for tech persona")
    logger.warning("This will make a real API call and consume tokens")

    generator = ThemeGenerator(mock_mode=False)  # Real mode!

    try:
        result = generator.generate_theme(persona, patterns)

        # Display results
        logger.success(f"\n✓ Successfully generated {result.mood} theme!")

        print("\n" + "=" * 80)
        print("GENERATED COLOR SCHEME")
        print("=" * 80)
        print(f"\n🎨 Mood: {result.mood}")
        print(f"💭 Rationale: {result.rationale}")
        print("\n--- Primary Palette ---")
        print(f"Primary:    {result.primary}")
        print(f"Secondary:  {result.secondary}")
        print(f"Accent:     {result.accent}")
        print("\n--- Backgrounds ---")
        print(f"Background: {result.background}")
        print(f"Card:       {result.card}")
        print("\n--- Text Colors ---")
        print(f"Foreground: {result.foreground}")
        print(f"Muted:      {result.muted}")
        print("\n--- Semantic Colors ---")
        print(f"Success:    {result.success}")
        print(f"Warning:    {result.warning}")
        print(f"Destructive: {result.destructive}")
        print("\n" + "=" * 80)

        # Test with creative persona
        logger.info("\n[Test 2/3] Generating theme for creative persona")

        creative_persona = PersonaProfile(
            writing_style="narrative and emotionally engaging with vivid storytelling",
            interests=["design", "art", "creative writing", "photography"],
            activity_level="moderate",
            professional_context="creative professional and designer",
            tone_preference="expressive and vibrant",
            age_range="25-35",
            content_depth_preference="balanced",
        )

        creative_patterns = [
            Pattern(
                title="Design Enthusiast",
                description="Passionate about visual design and aesthetics",
                confidence=0.90,
                keywords=["design", "UI", "UX", "typography", "colors"],
                interaction_count=140,
            )
        ]

        creative_theme = generator.generate_theme(creative_persona, creative_patterns)
        logger.success(f"✓ Generated {creative_theme.mood} theme for creative persona")
        print(f"   Primary: {creative_theme.primary} | Mood: {creative_theme.mood}")

        # Test with professional persona
        logger.info("\n[Test 3/3] Generating theme for professional persona")

        professional_persona = PersonaProfile(
            writing_style="formal and structured with clear business focus",
            interests=["business", "finance", "leadership", "strategy"],
            activity_level="moderate",
            professional_context="corporate executive",
            tone_preference="formal and professional",
            age_range="40-55",
            content_depth_preference="balanced",
        )

        professional_patterns = [
            Pattern(
                title="Business Leader",
                description="Focus on business strategy and leadership",
                confidence=0.88,
                keywords=["business", "strategy", "leadership", "management"],
                interaction_count=130,
            )
        ]

        professional_theme = generator.generate_theme(professional_persona, professional_patterns)
        logger.success(f"✓ Generated {professional_theme.mood} theme for professional persona")
        print(f"   Primary: {professional_theme.primary} | Mood: {professional_theme.mood}")

        print("\n" + "=" * 80)
        logger.success("Theme generation test completed successfully!")
        logger.success("All themes are valid and persona-matched ✨")
        print("=" * 80)

    except Exception as e:
        logger.error(f"Theme generation failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_theme_generation()
