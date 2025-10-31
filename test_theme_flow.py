#!/usr/bin/env python3
"""
Test script to verify theme generation and serialization.
"""
import sys
import json
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from fabric_dashboard.core.theme_generator import ThemeGenerator
from fabric_dashboard.core.dashboard_builder import DashboardBuilder
from fabric_dashboard.models.schemas import PersonaProfile, Pattern

def test_theme_flow():
    """Test that theme is correctly generated and serialized."""
    print("=" * 80)
    print("TESTING THEME GENERATION AND SERIALIZATION")
    print("=" * 80)
    print()

    # Create minimal test data
    persona = PersonaProfile(
        writing_style="casual",
        interests=["fitness", "health"],
        activity_level="high",
        tone_preference="friendly",
        content_depth_preference="balanced"
    )

    patterns = [
        Pattern(
            title="Fitness Tracking",
            description="Regular workout logging",
            confidence=0.9,
            keywords=["workout", "fitness"],
            interaction_count=50
        )
    ]

    # Step 1: Generate theme
    print("1. Generating theme...")
    theme_gen = ThemeGenerator(mock_mode=True)
    color_scheme = theme_gen.generate_theme(persona, patterns)

    print(f"   ✓ Theme generated: {color_scheme.mood}")
    print(f"   ✓ Primary color: {color_scheme.primary}")
    print(f"   ✓ Background type: {color_scheme.background_theme.type}")
    print()

    # Step 2: Create DashboardJSON
    print("2. Building dashboard JSON...")
    builder = DashboardBuilder()

    # Create minimal dashboard with theme
    from fabric_dashboard.models.schemas import DashboardJSON, Widget
    from datetime import datetime, timezone

    dashboard_json = DashboardJSON(
        id="test-123",
        generated_at=datetime.now(timezone.utc),
        widgets=[
            Widget(
                id="test-1",
                type="stat-card",
                size="small",
                priority=1,
                data={"label": "Test", "value": "123", "trend": "+10%"}
            )
        ],
        theme=color_scheme,
        persona=persona
    )

    print(f"   ✓ Dashboard created with {len(dashboard_json.widgets)} widgets")
    print(f"   ✓ Theme attached: {hasattr(dashboard_json, 'theme')}")
    print()

    # Step 3: Serialize to dict (like WebSocket does)
    print("3. Serializing to JSON (WebSocket simulation)...")
    dashboard_dict = dashboard_json.model_dump(mode='json')

    print(f"   ✓ Serialized to dict")
    print(f"   ✓ Has 'theme' key: {'theme' in dashboard_dict}")
    print()

    # Step 4: Inspect theme in serialized dict
    print("4. Inspecting theme in serialized data...")
    if 'theme' in dashboard_dict:
        theme = dashboard_dict['theme']
        print(f"   ✓ Theme is present!")
        print(f"   ✓ Primary: {theme.get('primary')}")
        print(f"   ✓ Secondary: {theme.get('secondary')}")
        print(f"   ✓ Accent: {theme.get('accent')}")
        print(f"   ✓ Foreground: {theme.get('foreground')}")
        print(f"   ✓ Mood: {theme.get('mood')}")
        print()
        print(f"   ✓ Background theme:")
        bg = theme.get('background_theme', {})
        print(f"      - Type: {bg.get('type')}")
        print(f"      - Card BG: {bg.get('card_background')}")
        print(f"      - Backdrop blur: {bg.get('card_backdrop_blur')}")

        if bg.get('gradient'):
            grad = bg['gradient']
            print(f"      - Gradient type: {grad.get('type')}")
            print(f"      - Gradient colors: {grad.get('colors')}")
        elif bg.get('color'):
            print(f"      - Solid color: {bg.get('color')}")
        print()

        print(f"   ✓ Fonts:")
        fonts = theme.get('fonts', {})
        print(f"      - Heading: {fonts.get('heading')}")
        print(f"      - Body: {fonts.get('body')}")
        print(f"      - Mono: {fonts.get('mono')}")
        print()
    else:
        print("   ✗ ERROR: Theme key missing from serialized data!")
        print(f"   Available keys: {list(dashboard_dict.keys())}")
        return False

    # Step 5: Verify JSON serialization works
    print("5. Testing JSON string serialization...")
    try:
        json_str = json.dumps(dashboard_dict, indent=2)
        print(f"   ✓ Successfully serialized to JSON string ({len(json_str)} chars)")

        # Parse it back
        parsed = json.loads(json_str)
        print(f"   ✓ Successfully parsed back from JSON")
        print(f"   ✓ Theme still present: {'theme' in parsed}")
        print()
    except Exception as e:
        print(f"   ✗ JSON serialization failed: {e}")
        return False

    print("=" * 80)
    print("✅ ALL CHECKS PASSED - Theme flow is working correctly!")
    print("=" * 80)
    return True

if __name__ == "__main__":
    success = test_theme_flow()
    sys.exit(0 if success else 1)
