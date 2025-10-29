"""
Test real LLM theme generation to verify everything works before updating WebSocket.
"""

import sys
from pathlib import Path

# Add fabric_dashboard to path
sys.path.insert(0, str(Path(__file__).parent))

from fabric_dashboard.core.theme_generator import ThemeGenerator
from fabric_dashboard.models.schemas import PersonaProfile, Pattern


def test_real_theme_generation():
    """Test theme generation with real Claude API."""
    print("Testing real LLM theme generation...")
    print("-" * 60)

    # Create test persona
    persona = PersonaProfile(
        writing_style="analytical and data-driven",
        interests=["technology", "productivity", "startups"],
        activity_level="high",
        professional_context="startup founder",
        tone_preference="professional but approachable",
        content_depth_preference="deep_dives",
    )

    # Create test patterns
    patterns = [
        Pattern(
            title="Early Morning Productivity",
            description="User is most active between 6-9am, often engaging with productivity content",
            confidence=0.92,
            keywords=["morning", "productivity", "focus", "routine"],
            interaction_count=45,
        ),
        Pattern(
            title="Tech Startup Interest",
            description="Frequent engagement with startup ecosystem content and founder stories",
            confidence=0.88,
            keywords=["startup", "founder", "funding", "growth"],
            interaction_count=38,
        ),
    ]

    # Initialize with real LLM (mock_mode=False)
    print("\n1. Initializing ThemeGenerator with mock_mode=False...")
    theme_gen = ThemeGenerator(mock_mode=False)

    # Generate theme
    print("2. Generating theme with Claude API...")
    print("   This may take 5-10 seconds...\n")

    color_scheme = theme_gen.generate_theme(persona, patterns)

    # Print results
    print("✅ Theme generated successfully!")
    print("-" * 60)
    print(f"Mood: {color_scheme.mood}")
    print(f"Rationale: {color_scheme.rationale}")
    print(f"\nColors:")
    print(f"  Primary: {color_scheme.primary}")
    print(f"  Secondary: {color_scheme.secondary}")
    print(f"  Accent: {color_scheme.accent}")
    print(f"  Foreground: {color_scheme.foreground}")
    print(f"\nFonts:")
    print(f"  Heading: {color_scheme.fonts.heading}")
    print(f"  Body: {color_scheme.fonts.body}")
    print(f"  Mono: {color_scheme.fonts.mono}")
    print(f"\nBackground:")
    print(f"  Type: {color_scheme.background_theme.type}")
    if color_scheme.background_theme.type == "solid":
        print(f"  Color: {color_scheme.background_theme.color}")
    elif color_scheme.background_theme.type == "gradient":
        print(f"  Gradient Type: {color_scheme.background_theme.gradient.type}")
        print(f"  Colors: {', '.join(color_scheme.background_theme.gradient.colors)}")
    print(f"  Card Background: {color_scheme.background_theme.card_background}")
    print(f"  Backdrop Blur: {color_scheme.background_theme.card_backdrop_blur}")
    print("-" * 60)
    print("\n✅ Real LLM theme generation is working!")

    return color_scheme


if __name__ == "__main__":
    try:
        test_real_theme_generation()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
