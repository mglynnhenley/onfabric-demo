"""
Pipeline service - wraps the Fabric dashboard generation pipeline with progress streaming.

This service runs the actual Python pipeline (DataFetcher → PatternDetector → etc.)
and streams progress updates via callbacks for WebSocket communication.
"""

import asyncio
import sys
import logging
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)

# Add parent directory to path to import fabric_dashboard
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from fabric_dashboard.core.data_fetcher import DataFetcher
from fabric_dashboard.core.pattern_detector import PatternDetector
from fabric_dashboard.core.theme_generator import ThemeGenerator
from fabric_dashboard.core.content_writer import ContentWriter
from fabric_dashboard.core.ui_generator import UIGenerator
from fabric_dashboard.core.dashboard_builder import DashboardBuilder
from fabric_dashboard.core.search_enricher import SearchEnricher
from fabric_dashboard.models.schemas import (
    CardSize, Pattern, PersonaProfile, ColorScheme, CardContent
)


class PipelineService:
    """Service for running the dashboard generation pipeline with progress streaming."""

    def __init__(self):
        """Initialize pipeline service."""
        self.persona_fixtures_dir = Path(__file__).parent.parent.parent.parent / "fabric_dashboard" / "tests" / "fixtures" / "personas"

    def _load_demo_fixture(self) -> dict:
        """
        Load pre-crafted demo persona fixture.

        Returns:
            Dict with patterns, persona, theme, ui_components, content_cards.

        Raises:
            FileNotFoundError: If demo.json doesn't exist.
        """
        demo_fixture = self.persona_fixtures_dir / "demo.json"

        if not demo_fixture.exists():
            raise FileNotFoundError(
                f"Demo fixture not found at {demo_fixture}. "
                "Run fixture generation first."
            )

        import json
        with open(demo_fixture) as f:
            return json.load(f)

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
        logging.info("=" * 80)
        logging.info(f"🚀 STARTING DASHBOARD GENERATION FOR PERSONA: {persona}")
        logging.info("=" * 80)

        try:
            # Check if this is the demo persona
            if persona == "demo":
                logging.info("🎭 DEMO MODE: Loading pre-crafted demo persona")
                return await self._generate_demo_dashboard(progress_callback, start_time)

            # Send progress: Starting
            await self._send_progress(progress_callback, {
                "step": "initializing",
                "percent": 0,
                "message": "Initializing AI pipeline...",
            })

            # Step 1: Initialize components
            # DataFetcher stays in mock mode (use fixture data, not OnFabric)
            # AI components use real Claude API for generation
            logging.info("📦 STEP 1: Initializing pipeline components")
            logging.info("  • DataFetcher: MOCK mode (using fixture data)")
            logging.info("  • PatternDetector: REAL Claude AI")
            logging.info("  • SearchEnricher: REAL Perplexity API + Claude AI")
            logging.info("  • ThemeGenerator: REAL Claude AI")
            logging.info("  • ContentWriter: REAL Claude AI")
            logging.info("  • UIGenerator: REAL Claude AI")

            data_fetcher = DataFetcher(mock_mode=True)
            pattern_detector = PatternDetector(mock_mode=False)  # Real AI
            search_enricher = SearchEnricher(mock_mode=False)    # Real Perplexity + Claude
            theme_generator = ThemeGenerator(mock_mode=False)    # Real AI
            content_writer = ContentWriter(mock_mode=False)      # Real AI
            ui_generator = UIGenerator(mock_mode=False)          # Real AI
            dashboard_builder = DashboardBuilder()

            logging.info("✓ All components initialized")

            await asyncio.sleep(0.5)  # Brief pause for UX

            # Step 2: Fetch data (mock data for persona)
            logging.info("")
            logging.info("📊 STEP 2: Fetching user data")
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

            logging.info(f"✓ Loaded {interaction_count} interactions from {len(platforms)} platforms")
            logging.info(f"  Platforms: {', '.join(platforms)}")

            await asyncio.sleep(1)

            # Step 3: Detect patterns
            logging.info("")
            logging.info("🧠 STEP 3: Detecting patterns with Claude AI")
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

            logging.info(f"✓ Detected {len(patterns)} patterns")
            logging.info("")
            logging.info("PERSONA PROFILE:")
            logging.info(f"  Writing Style: {persona_profile.writing_style}")
            logging.info(f"  Interests: {', '.join(persona_profile.interests[:5])}")
            logging.info(f"  Activity Level: {persona_profile.activity_level}")
            logging.info(f"  Tone Preference: {persona_profile.tone_preference}")
            logging.info(f"  Content Depth: {persona_profile.content_depth_preference}")
            if persona_profile.professional_context:
                logging.info(f"  Professional Context: {persona_profile.professional_context}")
            if persona_profile.age_range:
                logging.info(f"  Age Range: {persona_profile.age_range}")
            logging.info("")
            logging.info("PATTERNS DETECTED:")
            for i, p in enumerate(patterns, 1):
                logging.info(f"  Pattern {i}: {p.title}")
                logging.info(f"    Confidence: {p.confidence:.0%}")
                logging.info(f"    Description: {p.description[:200]}...")
                logging.info(f"    Keywords: {', '.join(p.keywords[:5])}")
                logging.info(f"    Interactions: {p.interaction_count}")
                logging.info("")

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
            logging.info("")
            logging.info("🎨 STEP 4: Generating theme with Claude AI")
            await self._send_progress(progress_callback, {
                "step": "theme",
                "percent": 50,
                "message": "Creating personalized color scheme...",
            })

            color_scheme = theme_generator.generate_theme(persona_profile, patterns)

            logging.info(f"✓ Generated theme: {color_scheme.mood}")
            logging.info("")
            logging.info("COLOR SCHEME:")
            logging.info(f"  Mood: {color_scheme.mood}")
            logging.info(f"  Primary: {color_scheme.primary}")
            logging.info(f"  Secondary: {color_scheme.secondary}")
            logging.info(f"  Accent: {color_scheme.accent}")
            logging.info(f"  Foreground: {color_scheme.foreground}")
            logging.info(f"  Muted: {color_scheme.muted}")
            logging.info(f"  Success: {color_scheme.success}")
            logging.info(f"  Warning: {color_scheme.warning}")
            logging.info(f"  Destructive: {color_scheme.destructive}")
            logging.info(f"  Rationale: {color_scheme.rationale[:200]}...")
            logging.info("")
            logging.info("FONTS:")
            logging.info(f"  Heading: {color_scheme.fonts.heading}")
            logging.info(f"  Body: {color_scheme.fonts.body}")
            logging.info(f"  Mono: {color_scheme.fonts.mono}")
            logging.info("")
            logging.info("BACKGROUND:")
            logging.info(f"  Type: {color_scheme.background_theme.type}")
            if color_scheme.background_theme.gradient:
                logging.info(f"  Gradient: {color_scheme.background_theme.gradient.type}")
                logging.info(f"  Colors: {', '.join(color_scheme.background_theme.gradient.colors)}")
            logging.info("")

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

            # Step 5: Enrich patterns with search results
            logging.info("")
            logging.info("🔍 STEP 5: Enriching patterns with Perplexity search")
            await self._send_progress(progress_callback, {
                "step": "search",
                "percent": 60,
                "message": "Researching latest trends and insights...",
            })

            # Enrich patterns with real Perplexity searches
            enriched_patterns = await search_enricher.enrich_patterns(patterns, max_queries_per_pattern=2)

            logging.info(f"✓ Enriched {len(enriched_patterns)} patterns with search results")
            for i, ep in enumerate(enriched_patterns[:3], 1):
                logging.info(f"  Pattern {i}: {ep.pattern.title}")
                logging.info(f"    Search results: {len(ep.search_results)}")
                if ep.search_results:
                    for j, sr in enumerate(ep.search_results[:2], 1):
                        logging.info(f"      Query {j}: {sr.query}")
                        logging.info(f"      Sources: {len(sr.sources)}")
                logging.info("")

            await asyncio.sleep(1)

            # Step 6: Generate content cards
            logging.info("")
            logging.info("✍️  STEP 6: Writing content with Claude AI")
            await self._send_progress(progress_callback, {
                "step": "content",
                "percent": 70,
                "message": "Writing personalized insights...",
            })

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

            logging.info(f"  Generating {num_cards} cards in parallel...")
            cards = await content_writer.generate_cards(enriched_patterns, persona_profile, card_sizes)

            logging.info(f"✓ Generated {len(cards)} content cards")
            logging.info("")
            logging.info("CONTENT CARDS GENERATED:")
            for i, card in enumerate(cards, 1):
                logging.info(f"  Card {i}: {card.title}")
                logging.info(f"    Size: {card.size}")
                logging.info(f"    Description: {card.description}")
                logging.info(f"    Word count: {len(card.body.split())} words")
                logging.info(f"    Reading time: {card.reading_time_minutes} min")
                logging.info(f"    Preview: {card.body[:150]}...")
                logging.info("")

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

            # Step 7: Generate UI components
            logging.info("")
            logging.info("🧩 STEP 7: Generating UI components with Claude AI")
            await self._send_progress(progress_callback, {
                "step": "widgets",
                "percent": 85,
                "message": "Selecting live widgets...",
            })

            ui_result = await ui_generator.generate_components(patterns, persona_profile)
            ui_components = ui_result.components

            logging.info(f"✓ Generated {len(ui_components)} UI components")
            logging.info("")
            logging.info("UI COMPONENTS GENERATED:")
            for i, comp in enumerate(ui_components, 1):
                logging.info(f"  Component {i}: {comp.component_type}")
                logging.info(f"    Title: {comp.title}")
                logging.info(f"    Pattern: {comp.pattern_title}")
                logging.info(f"    Confidence: {comp.confidence:.0%}")

                # Log component-specific data
                if comp.component_type == "video-feed" and hasattr(comp, 'videos'):
                    logging.info(f"    Videos: {len(comp.videos)} videos")
                    if comp.videos:
                        logging.info(f"    Query: {comp.search_query}")
                elif comp.component_type == "event-calendar" and hasattr(comp, 'events'):
                    logging.info(f"    Events: {len(comp.events)} events")
                    if comp.events:
                        logging.info(f"    Query: {comp.search_query}")
                elif comp.component_type == "map-card" and hasattr(comp, 'markers'):
                    logging.info(f"    Markers: {len(comp.markers)} locations")
                    logging.info(f"    Center: ({comp.center_lat:.4f}, {comp.center_lng:.4f})")
                elif comp.component_type == "task-list" and hasattr(comp, 'tasks'):
                    logging.info(f"    Tasks: {len(comp.tasks)} items")
                elif comp.component_type == "info-card" and hasattr(comp, 'location'):
                    logging.info(f"    Location: {comp.location}")
                elif comp.component_type == "content-card" and hasattr(comp, 'overview'):
                    logging.info(f"    Overview: {comp.overview[:100]}...")

                logging.info("")

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

            # Step 8: Build dashboard (both HTML and JSON)
            logging.info("")
            logging.info("🏗️  STEP 8: Building dashboard")
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

            logging.info(f"✓ Dashboard assembled")
            logging.info(f"  - {len(cards)} content cards")
            logging.info(f"  - {len(ui_components)} widgets")
            logging.info(f"  - HTML size: {len(html):,} chars")

            await asyncio.sleep(0.5)

            # Step 9: Complete
            total_time = (datetime.now() - start_time).total_seconds()
            logging.info("")
            logging.info("=" * 80)
            logging.info(f"✅ DASHBOARD GENERATION COMPLETE ({total_time:.1f}s)")
            logging.info("=" * 80)

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

    async def _generate_demo_dashboard(
        self,
        progress_callback: Optional[Callable[[Dict[str, Any]], None]],
        start_time: datetime,
    ) -> tuple[str, Any]:
        """
        Generate dashboard from pre-crafted demo fixture (no LLM calls).

        Args:
            progress_callback: Async function to call with progress updates.
            start_time: When generation started (for timing).

        Returns:
            Tuple of (HTML string, DashboardJSON object).
        """
        from fabric_dashboard.models.ui_components import (
            MapCard, EventCalendar, VideoFeed, TaskList, InfoCard
        )
        from fabric_dashboard.core.dashboard_builder import DashboardBuilder

        # Load fixture
        await self._send_progress(progress_callback, {
            "step": "initializing",
            "percent": 0,
            "message": "Loading demo data...",
        })

        demo_data = self._load_demo_fixture()

        # Parse patterns
        await self._send_progress(progress_callback, {
            "step": "patterns",
            "percent": 30,
            "message": "Loading patterns...",
        })
        patterns = [Pattern(**p) for p in demo_data["patterns"]]

        logging.info(f"✓ Loaded {len(patterns)} patterns from demo fixture")

        # Parse persona
        persona_profile = PersonaProfile(**demo_data["persona"])

        # Parse theme
        await self._send_progress(progress_callback, {
            "step": "theme",
            "percent": 50,
            "message": "Loading theme...",
        })
        color_scheme = ColorScheme(**demo_data["theme"])

        logging.info(f"✓ Loaded theme: {color_scheme.mood}")

        # Parse UI components
        await self._send_progress(progress_callback, {
            "step": "widgets",
            "percent": 70,
            "message": "Loading widgets...",
        })

        ui_components = []
        for comp_data in demo_data["ui_components"]:
            comp_type = comp_data["component_type"]
            if comp_type == "map-card":
                ui_components.append(MapCard(**comp_data))
            elif comp_type == "event-calendar":
                ui_components.append(EventCalendar(**comp_data))
            elif comp_type == "video-feed":
                ui_components.append(VideoFeed(**comp_data))
            elif comp_type == "task-list":
                ui_components.append(TaskList(**comp_data))
            elif comp_type == "info-card":
                ui_components.append(InfoCard(**comp_data))
            else:
                logging.warning(f"Unknown component type: {comp_type}")

        logging.info(f"✓ Loaded {len(ui_components)} UI components")

        # Enrich UI components with real API data
        await self._send_progress(progress_callback, {
            "step": "enriching",
            "percent": 75,
            "message": "Enriching widgets with live data...",
        })

        ui_generator = UIGenerator(mock_mode=False)
        ui_components = await ui_generator._enrich_components(ui_components)

        logging.info(f"✓ Enriched UI components with live API data")

        # Parse content cards
        await self._send_progress(progress_callback, {
            "step": "content",
            "percent": 85,
            "message": "Loading content...",
        })
        cards = [CardContent(**c) for c in demo_data["content_cards"]]

        logging.info(f"✓ Loaded {len(cards)} content cards")

        # Build dashboard
        await self._send_progress(progress_callback, {
            "step": "building",
            "percent": 95,
            "message": "Assembling dashboard...",
        })

        dashboard_builder = DashboardBuilder()

        # Build HTML
        dashboard = dashboard_builder.build(
            cards=cards,
            ui_components=ui_components,
            persona=persona_profile,
            color_scheme=color_scheme,
            user_name="Demo User",
            generation_time_seconds=(datetime.now() - start_time).total_seconds(),
        )

        html = dashboard.metadata["html"]

        # Build JSON
        dashboard_json = dashboard_builder.build_json(
            cards=cards,
            ui_components=ui_components,
            persona=persona_profile,
            color_scheme=color_scheme,
        )

        total_time = (datetime.now() - start_time).total_seconds()
        logging.info(f"✅ DEMO DASHBOARD COMPLETE ({total_time:.1f}s)")

        await self._send_progress(progress_callback, {
            "step": "complete",
            "percent": 100,
            "message": "Demo ready!",
        })

        return html, dashboard_json

    async def _send_progress(
        self,
        callback: Optional[Callable[[Dict[str, Any]], None]],
        data: Dict[str, Any]
    ):
        """Send progress update via callback."""
        if callback:
            data["type"] = "progress"
            await callback(data)
