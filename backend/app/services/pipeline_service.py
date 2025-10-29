"""
Pipeline service - wraps the Fabric dashboard generation pipeline with progress streaming.

This service runs the actual Python pipeline (DataFetcher → PatternDetector → etc.)
and streams progress updates via callbacks for WebSocket communication.
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional, Dict, Any

# Add parent directory to path to import fabric_dashboard
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from fabric_dashboard.core.data_fetcher import DataFetcher
from fabric_dashboard.core.pattern_detector import PatternDetector
from fabric_dashboard.core.theme_generator import ThemeGenerator
from fabric_dashboard.core.content_writer import ContentWriter
from fabric_dashboard.core.ui_generator import UIGenerator
from fabric_dashboard.core.dashboard_builder import DashboardBuilder
from fabric_dashboard.models.schemas import CardSize


class PipelineService:
    """Service for running the dashboard generation pipeline with progress streaming."""

    def __init__(self):
        """Initialize pipeline service."""
        self.persona_fixtures_dir = Path(__file__).parent.parent.parent.parent / "fabric_dashboard" / "tests" / "fixtures" / "personas"

    async def generate_dashboard(
        self,
        persona: str,
        progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None,
    ) -> tuple[str, Any]:
        """
        Generate a dashboard for the given persona using the real pipeline.

        Args:
            persona: Persona identifier (e.g., 'fitness-enthusiast')
            progress_callback: Async function to call with progress updates

        Returns:
            Tuple of (HTML string, DashboardJSON object)

        Raises:
            FileNotFoundError: If persona fixture doesn't exist
            RuntimeError: If generation fails
        """
        start_time = datetime.now()

        try:
            # Send progress: Starting
            await self._send_progress(progress_callback, {
                "step": "initializing",
                "percent": 0,
                "message": "Initializing AI pipeline...",
            })

            # Step 1: Initialize components
            # DataFetcher stays in mock mode (use fixture data, not OnFabric)
            # AI components use real Claude API for generation
            data_fetcher = DataFetcher(mock_mode=True)
            pattern_detector = PatternDetector(mock_mode=False)  # Real AI
            theme_generator = ThemeGenerator(mock_mode=False)    # Real AI
            content_writer = ContentWriter(mock_mode=False)      # Real AI
            ui_generator = UIGenerator(mock_mode=False)          # Real AI
            dashboard_builder = DashboardBuilder()

            await asyncio.sleep(0.5)  # Brief pause for UX

            # Step 2: Fetch data (mock data for persona)
            await self._send_progress(progress_callback, {
                "step": "data",
                "percent": 10,
                "message": f"Loading {persona.replace('-', ' ')} behavior data...",
            })

            # Load persona-specific fixture if available, else use default
            persona_fixture = self.persona_fixtures_dir / f"{persona}.json"
            if not persona_fixture.exists():
                # Fallback to default mock data
                user_data = data_fetcher.fetch_user_data(days_back=30)
            else:
                # TODO: Load persona-specific data
                # For now, use default
                user_data = data_fetcher.fetch_user_data(days_back=30)

            if not user_data:
                raise RuntimeError("Failed to load user data")

            interaction_count = user_data.summary.total_interactions
            platforms = user_data.summary.platforms

            await asyncio.sleep(1)

            # Step 3: Detect patterns
            await self._send_progress(progress_callback, {
                "step": "patterns",
                "percent": 30,
                "message": "Analyzing patterns with Claude AI...",
                "data": {
                    "interactions": interaction_count,
                    "platforms": platforms,
                }
            })

            pattern_result = pattern_detector.detect_patterns(user_data)
            patterns = pattern_result.patterns
            persona_profile = pattern_result.persona

            # Send discovered patterns
            await self._send_progress(progress_callback, {
                "step": "patterns_complete",
                "percent": 35,
                "message": f"Discovered {len(patterns)} patterns",
                "data": {
                    "patterns": [
                        {
                            "title": p.title,
                            "confidence": p.confidence,
                            "description": p.description[:100],  # Truncate for preview
                        } for p in patterns[:4]  # Send top 4
                    ]
                }
            })

            await asyncio.sleep(1.5)

            # Step 4: Generate theme
            await self._send_progress(progress_callback, {
                "step": "theme",
                "percent": 50,
                "message": "Creating personalized color scheme...",
            })

            color_scheme = theme_generator.generate_theme(persona_profile, patterns)

            # Send theme info
            await self._send_progress(progress_callback, {
                "step": "theme_complete",
                "percent": 55,
                "message": "Theme generated",
                "data": {
                    "mood": color_scheme.mood,
                    "primary": color_scheme.primary,
                    "rationale": color_scheme.rationale[:150] if color_scheme.rationale else "",
                }
            })

            await asyncio.sleep(1)

            # Step 5: Generate content cards
            await self._send_progress(progress_callback, {
                "step": "content",
                "percent": 70,
                "message": "Writing personalized insights...",
            })

            # Create enriched patterns (mock - no actual search in demo)
            enriched_patterns = [
                type('EnrichedPattern', (), {'pattern': p, 'search_results': []})()
                for p in patterns
            ]

            # Generate more cards for generative feel (8-10 cards)
            import random
            num_cards = min(len(enriched_patterns), random.choice([8, 9, 10]))
            enriched_patterns = enriched_patterns[:num_cards]

            # More varied card sizes - mostly COMPACT and SMALL for dense, generative feel
            # Weights: 40% COMPACT, 35% SMALL, 15% MEDIUM, 10% LARGE
            size_pool = (
                [CardSize.COMPACT] * 4 +
                [CardSize.SMALL] * 3 +
                [CardSize.MEDIUM] * 2 +
                [CardSize.LARGE] * 1
            )
            card_sizes = [random.choice(size_pool) for _ in range(num_cards)]

            cards = await content_writer.generate_cards(enriched_patterns, persona_profile, card_sizes)

            # Send card titles
            await self._send_progress(progress_callback, {
                "step": "content_complete",
                "percent": 75,
                "message": f"Generated {len(cards)} insight cards",
                "data": {
                    "cards": [{"title": card.title} for card in cards[:3]]
                }
            })

            await asyncio.sleep(1)

            # Step 6: Generate UI components
            await self._send_progress(progress_callback, {
                "step": "widgets",
                "percent": 85,
                "message": "Selecting live widgets...",
            })

            ui_result = await ui_generator.generate_components(patterns, persona_profile)
            ui_components = ui_result.components

            # Send widget info
            await self._send_progress(progress_callback, {
                "step": "widgets_complete",
                "percent": 90,
                "message": f"Selected {len(ui_components)} widgets",
                "data": {
                    "widgets": [c.component_type for c in ui_components]
                }
            })

            await asyncio.sleep(0.5)

            # Step 7: Build dashboard (both HTML and JSON)
            await self._send_progress(progress_callback, {
                "step": "building",
                "percent": 95,
                "message": "Assembling final dashboard...",
            })

            # Build HTML (for backward compatibility)
            dashboard = dashboard_builder.build(
                cards=cards,
                ui_components=ui_components,
                persona=persona_profile,
                color_scheme=color_scheme,
                user_name="Demo User",
                generation_time_seconds=(datetime.now() - start_time).total_seconds(),
            )

            html = dashboard.metadata["html"]

            # Build JSON (for new pin board frontend)
            dashboard_json = dashboard_builder.build_json(
                cards=cards,
                ui_components=ui_components,
                persona=persona_profile,
                color_scheme=color_scheme,
            )

            await asyncio.sleep(0.5)

            # Step 8: Complete
            await self._send_progress(progress_callback, {
                "step": "complete",
                "percent": 100,
                "message": "Dashboard ready!",
            })

            return html, dashboard_json

        except Exception as e:
            # Send error
            if progress_callback:
                await progress_callback({
                    "type": "error",
                    "message": f"Generation failed: {str(e)}"
                })
            raise RuntimeError(f"Pipeline failed: {e}")

    async def _send_progress(
        self,
        callback: Optional[Callable[[Dict[str, Any]], None]],
        data: Dict[str, Any]
    ):
        """Send progress update via callback."""
        if callback:
            data["type"] = "progress"
            await callback(data)
