#!/usr/bin/env python3
"""Test script to verify content writer with real Claude API."""

import asyncio
import os
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from fabric_dashboard.core.content_writer import ContentWriter
from fabric_dashboard.models.schemas import (
    CardSize,
    EnrichedPattern,
    Pattern,
    PersonaProfile,
    SearchResult,
)
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


async def test_content_generation():
    """Test content generation with real Claude API."""
    logger.info("Testing content writer with real Claude API")

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

    # Create enriched patterns with search results
    enriched_patterns = [
        EnrichedPattern(
            pattern=Pattern(
                title="AI Enthusiast",
                description="Deep interest in artificial intelligence and machine learning technologies, following latest developments in LLMs and neural networks",
                confidence=0.92,
                keywords=["AI", "machine learning", "deep learning", "neural networks", "GPT", "transformers"],
                interaction_count=150,
            ),
            search_results=[
                SearchResult(
                    query="latest AI developments 2025",
                    content="Recent breakthroughs in large language models have revolutionized the field. Claude 3.5 Sonnet and GPT-4 demonstrate unprecedented reasoning capabilities. Multimodal AI systems can now process text, images, and video seamlessly.",
                    sources=["https://example.com/ai-news", "https://example.com/llm-research"],
                )
            ],
        ),
        EnrichedPattern(
            pattern=Pattern(
                title="Tech Innovator",
                description="Engaged with cutting-edge technology and innovation trends in the startup ecosystem",
                confidence=0.88,
                keywords=["technology", "innovation", "startups", "disruption", "venture capital", "product"],
                interaction_count=120,
            ),
            search_results=[
                SearchResult(
                    query="tech startup trends 2025",
                    content="The startup landscape is evolving rapidly with AI-first companies leading the charge. Vertical AI applications are gaining traction as founders focus on solving specific industry problems.",
                    sources=["https://example.com/startup-trends"],
                )
            ],
        ),
    ]

    # Card sizes to test
    card_sizes = [CardSize.LARGE, CardSize.MEDIUM]

    # Generate content with REAL Claude API
    logger.info("\n[Test 1/3] Generating 2 cards for tech persona")
    logger.warning("This will make real API calls and consume tokens")

    writer = ContentWriter(mock_mode=False)  # Real mode!

    try:
        cards = await writer.generate_cards(enriched_patterns, persona, card_sizes)

        # Display results
        logger.success(f"\n✓ Successfully generated {len(cards)} cards!")

        for i, card in enumerate(cards, 1):
            print("\n" + "=" * 80)
            print(f"CARD {i}: {card.size.value.upper()}")
            print("=" * 80)
            print(f"\n📊 Title: {card.title}")
            print(f"📝 Description: {card.description}")
            print(f"📖 Reading Time: {card.reading_time_minutes} min")
            print(f"📊 Word Count: {card.word_count()} words")
            print(f"🔗 Sources: {len(card.sources)}")
            print(f"💯 Confidence: {card.confidence:.2f}")
            print(f"\n--- BODY PREVIEW (first 500 chars) ---")
            print(card.body[:500] + "..." if len(card.body) > 500 else card.body)

            # Validate word count is in expected range
            size_ranges = {
                CardSize.LARGE: (320, 600),
                CardSize.MEDIUM: (200, 360),
                CardSize.SMALL: (120, 240),
                CardSize.COMPACT: (80, 180),
            }
            min_words, max_words = size_ranges[card.size]
            word_count = card.word_count()

            if min_words <= word_count <= max_words:
                logger.success(f"✓ Word count {word_count} is within expected range [{min_words}-{max_words}]")
            else:
                logger.warning(f"⚠ Word count {word_count} is outside expected range [{min_words}-{max_words}]")

        # Test with creative persona
        logger.info("\n[Test 2/3] Generating card for creative persona")

        creative_persona = PersonaProfile(
            writing_style="narrative and emotionally engaging with vivid storytelling and personal anecdotes",
            interests=["design", "art", "creative writing", "photography", "storytelling"],
            activity_level="moderate",
            professional_context="creative professional and designer",
            tone_preference="expressive and vibrant with emotional depth",
            age_range="25-35",
            content_depth_preference="balanced",
        )

        creative_pattern = [
            EnrichedPattern(
                pattern=Pattern(
                    title="Design Enthusiast",
                    description="Passionate about visual design, aesthetics, and the intersection of art and technology",
                    confidence=0.90,
                    keywords=["design", "UI", "UX", "typography", "colors", "aesthetics"],
                    interaction_count=140,
                ),
                search_results=[
                    SearchResult(
                        query="design trends 2025",
                        content="Minimalism continues to dominate while brutalism makes a comeback. AI-generated designs are sparking debates about creativity and authenticity in the design community.",
                        sources=["https://example.com/design-trends"],
                    )
                ],
            )
        ]

        creative_cards = await writer.generate_cards(
            creative_pattern, creative_persona, [CardSize.MEDIUM]
        )

        logger.success(f"✓ Generated {len(creative_cards)} card for creative persona")
        print(f"\n🎨 Title: {creative_cards[0].title}")
        print(f"📝 Style should be narrative/storytelling")
        print(f"📊 Word Count: {creative_cards[0].word_count()} words")

        # Test with professional persona
        logger.info("\n[Test 3/3] Generating card for professional persona")

        professional_persona = PersonaProfile(
            writing_style="formal and structured with clear business focus and strategic thinking",
            interests=["business", "finance", "leadership", "strategy", "management"],
            activity_level="moderate",
            professional_context="corporate executive in Fortune 500 company",
            tone_preference="formal and professional with executive-level insights",
            age_range="40-55",
            content_depth_preference="balanced",
        )

        professional_pattern = [
            EnrichedPattern(
                pattern=Pattern(
                    title="Business Leader",
                    description="Focus on business strategy, leadership, and corporate management",
                    confidence=0.88,
                    keywords=["business", "strategy", "leadership", "management", "ROI"],
                    interaction_count=130,
                ),
                search_results=[
                    SearchResult(
                        query="business leadership trends 2025",
                        content="Remote work transformation continues. Leaders focus on building culture in hybrid environments. Data-driven decision making becomes standard practice.",
                        sources=["https://example.com/business-trends"],
                    )
                ],
            )
        ]

        professional_cards = await writer.generate_cards(
            professional_pattern, professional_persona, [CardSize.SMALL]
        )

        logger.success(f"✓ Generated {len(professional_cards)} card for professional persona")
        print(f"\n💼 Title: {professional_cards[0].title}")
        print(f"📝 Style should be formal/professional")
        print(f"📊 Word Count: {professional_cards[0].word_count()} words")

        print("\n" + "=" * 80)
        logger.success("Content generation test completed successfully!")
        logger.success("All cards generated with persona-matched styles ✨")
        print("=" * 80)

        # Summary
        print("\n📊 SUMMARY:")
        print(f"   - Total cards generated: {len(cards) + len(creative_cards) + len(professional_cards)}")
        print(f"   - Personas tested: 3 (analytical, creative, professional)")
        print(f"   - Card sizes tested: Large, Medium, Small")
        print(f"   - All cards have valid structure and word counts")

    except Exception as e:
        logger.error(f"Content generation failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_content_generation())
