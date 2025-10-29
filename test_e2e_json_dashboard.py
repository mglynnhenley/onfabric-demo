"""
End-to-end test for JSON dashboard generation with real LLM.

This test runs the complete pipeline:
1. DataFetcher (mock mode for user data)
2. PatternDetector (real LLM)
3. ThemeGenerator (real LLM)
4. ContentWriter (real LLM)
5. UIGenerator (real LLM)
6. DashboardBuilder (JSON generation)

Verifies the entire flow works with real Claude API calls.
"""

import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path

# Add fabric_dashboard to path
sys.path.insert(0, str(Path(__file__).parent))

from fabric_dashboard.core.data_fetcher import DataFetcher
from fabric_dashboard.core.pattern_detector import PatternDetector
from fabric_dashboard.core.theme_generator import ThemeGenerator
from fabric_dashboard.core.content_writer import ContentWriter
from fabric_dashboard.core.ui_generator import UIGenerator
from fabric_dashboard.core.dashboard_builder import DashboardBuilder
from fabric_dashboard.models.schemas import CardSize


async def test_e2e_json_dashboard():
    """Test complete pipeline with JSON output."""
    print("=" * 80)
    print("END-TO-END JSON DASHBOARD GENERATION TEST")
    print("=" * 80)
    print("\nThis test runs the ENTIRE pipeline with real LLM calls.")
    print("It may take 30-60 seconds to complete.\n")
    print("-" * 80)

    start_time = datetime.now()

    try:
        # Step 1: Initialize components (real AI, mock data)
        print("\n[1/7] Initializing pipeline components...")
        data_fetcher = DataFetcher(mock_mode=True)  # Mock user data
        pattern_detector = PatternDetector(mock_mode=False)  # Real AI
        theme_generator = ThemeGenerator(mock_mode=False)  # Real AI
        content_writer = ContentWriter(mock_mode=False)  # Real AI
        ui_generator = UIGenerator(mock_mode=False)  # Real AI
        dashboard_builder = DashboardBuilder()
        print("   ✓ All components initialized")

        # Step 2: Fetch data
        print("\n[2/7] Fetching user data...")
        user_data = data_fetcher.fetch_user_data(days_back=30)
        if not user_data:
            raise RuntimeError("Failed to load user data")

        interactions = user_data.summary.total_interactions
        platforms = user_data.summary.platforms
        print(f"   ✓ Loaded {interactions} interactions from {len(platforms)} platforms")

        # Step 3: Detect patterns
        print("\n[3/7] Detecting patterns with Claude API...")
        print("   (This may take 10-15 seconds...)")
        pattern_result = pattern_detector.detect_patterns(user_data)
        patterns = pattern_result.patterns
        persona = pattern_result.persona
        print(f"   ✓ Discovered {len(patterns)} patterns")
        print(f"   ✓ Persona: {persona.writing_style}")

        # Step 4: Generate theme
        print("\n[4/7] Generating color theme with Claude API...")
        print("   (This may take 5-10 seconds...)")
        color_scheme = theme_generator.generate_theme(persona, patterns)
        print(f"   ✓ Theme generated: {color_scheme.mood}")
        print(f"   ✓ Fonts: {color_scheme.fonts.heading} / {color_scheme.fonts.body}")
        print(f"   ✓ Background: {color_scheme.background_theme.type}")

        # Step 5: Generate content cards
        print("\n[5/7] Generating content cards with Claude API...")
        print("   (This may take 15-20 seconds...)")

        # Create enriched patterns (mock search)
        enriched_patterns = [
            type('EnrichedPattern', (), {'pattern': p, 'search_results': []})()
            for p in patterns[:6]  # Use 6 patterns
        ]

        # Generate cards with varied sizes
        card_sizes = [
            CardSize.LARGE,
            CardSize.MEDIUM,
            CardSize.MEDIUM,
            CardSize.SMALL,
            CardSize.SMALL,
            CardSize.COMPACT,
        ]

        cards = await content_writer.generate_cards(enriched_patterns, persona, card_sizes)
        print(f"   ✓ Generated {len(cards)} content cards")

        # Step 6: Generate UI components
        print("\n[6/7] Generating UI widgets with Claude API...")
        print("   (This may take 10-15 seconds...)")
        ui_result = await ui_generator.generate_components(patterns, persona)
        ui_components = ui_result.components
        print(f"   ✓ Selected {len(ui_components)} widgets")

        # Step 7: Build JSON dashboard
        print("\n[7/7] Building JSON dashboard...")
        dashboard_json = dashboard_builder.build_json(
            cards=cards,
            ui_components=ui_components,
            persona=persona,
            color_scheme=color_scheme,
        )

        # Validate JSON structure
        assert dashboard_json.id is not None
        assert dashboard_json.generated_at is not None
        assert len(dashboard_json.widgets) > 0
        assert dashboard_json.theme is not None
        assert dashboard_json.persona is not None

        print(f"   ✓ Dashboard JSON generated with {len(dashboard_json.widgets)} widgets")

        # Convert to dict and serialize
        dashboard_dict = dashboard_json.model_dump(mode='json')
        json_str = json.dumps(dashboard_dict, indent=2)
        json_size = len(json_str)

        print(f"   ✓ JSON serialization successful ({json_size:,} bytes)")

        # Print summary
        elapsed = (datetime.now() - start_time).total_seconds()
        print("\n" + "=" * 80)
        print("✅ END-TO-END TEST PASSED")
        print("=" * 80)
        print(f"\nGeneration time: {elapsed:.1f} seconds")
        print(f"\nDashboard Summary:")
        print(f"  - ID: {dashboard_json.id}")
        print(f"  - Widgets: {len(dashboard_json.widgets)}")
        print(f"  - Theme Mood: {dashboard_json.theme.mood}")
        print(f"  - Primary Color: {dashboard_json.theme.primary}")
        print(f"  - Fonts: {dashboard_json.theme.fonts.heading} / {dashboard_json.theme.fonts.body}")
        print(f"  - Background: {dashboard_json.theme.background_theme.type}")
        print(f"  - Persona: {dashboard_json.persona.writing_style}")
        print(f"  - JSON Size: {json_size:,} bytes")

        print("\nWidget Types:")
        widget_types = {}
        for widget in dashboard_json.widgets:
            widget_types[widget.type] = widget_types.get(widget.type, 0) + 1
        for widget_type, count in sorted(widget_types.items()):
            print(f"  - {widget_type}: {count}")

        print("\n" + "=" * 80)
        print("✅ Full pipeline working with real LLM!")
        print("=" * 80)

        return dashboard_json

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(test_e2e_json_dashboard())
