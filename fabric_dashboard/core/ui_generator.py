"""UI Generator module using Claude for component selection and configuration.

This module generates 3-6 interactive UI components based on user patterns.
It is SEPARATE from ContentWriter, which generates blog-style text cards.
"""

import asyncio
from typing import Optional

from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from tenacity import retry, stop_after_attempt, wait_exponential

# API clients are now injected via constructor for better testability
from fabric_dashboard.models.schemas import Pattern, PersonaProfile
from fabric_dashboard.models.ui_components import (
    ContentCard,
    EventCalendar,
    InfoCard,
    MapCard,
    MapMarker,
    TaskItem,
    TaskList,
    UIComponentType,
    UIGenerationResult,
    VideoFeed,
)
from fabric_dashboard.utils import logger
from fabric_dashboard.utils.config import get_config


class ComponentSelectionResult(BaseModel):
    """Result from LLM component selection.

    This model is used with LangChain's with_structured_output() to ensure
    the LLM returns validated component configurations.
    """

    components: list[UIComponentType] = Field(
        min_length=3,
        max_length=6,
        description="3-6 selected UI components with complete configuration",
    )


class UIGenerator:
    """Generates interactive UI components based on user patterns."""

    def __init__(
        self,
        weather_api=None,
        videos_api=None,
        events_api=None,
        geocoding_api=None,
        mock_mode: bool = False,
    ):
        """
        Initialize UI Generator with API dependencies.

        Args:
            weather_api: Weather API implementation.
            videos_api: Video API implementation.
            events_api: Events API implementation.
            geocoding_api: Geocoding API implementation.
            mock_mode: Use mock data for testing.
        """
        self.mock_mode = mock_mode
        self.llm: Optional[ChatAnthropic] = None

        # Initialize APIs (create defaults if not provided)
        if weather_api is None:
            from fabric_dashboard.api import OpenWeatherAPI

            config = get_config() if not mock_mode else None
            weather_api = OpenWeatherAPI(
                api_key=getattr(config, "openweathermap_api_key", None) if config else None,
                mock_mode=mock_mode,
            )

        if videos_api is None:
            from fabric_dashboard.api import YouTubeAPI

            config = get_config() if not mock_mode else None
            videos_api = YouTubeAPI(
                api_key=getattr(config, "youtube_api_key", None) if config else None,
                mock_mode=mock_mode,
            )

        if events_api is None:
            from fabric_dashboard.api import TicketmasterAPI

            config = get_config() if not mock_mode else None
            events_api = TicketmasterAPI(
                api_key=getattr(config, "ticketmaster_api_key", None) if config else None,
                mock_mode=mock_mode,
            )

        if geocoding_api is None:
            from fabric_dashboard.api import MapboxAPI

            config = get_config() if not mock_mode else None
            geocoding_api = MapboxAPI(
                api_key=getattr(config, "mapbox_api_key", None) if config else None,
                mock_mode=mock_mode,
            )

        self.weather = weather_api
        self.videos = videos_api
        self.events = events_api
        self.geocoding = geocoding_api

        if not mock_mode:
            config = get_config()
            if not config:
                raise RuntimeError(
                    "Configuration not found. Run 'fabric-dashboard init' first."
                )

            self.llm = ChatAnthropic(
                model_name="claude-sonnet-4-5",
                temperature=0.8,  # Balanced creativity for component selection
                api_key=config.anthropic_api_key,
                timeout=60,
                max_tokens=4096,
                stop=None,
            )

    async def generate_components(
        self,
        patterns: list[Pattern],
        persona: PersonaProfile,
    ) -> UIGenerationResult:
        """
        Generate UI components based on patterns.

        Args:
            patterns: Detected patterns from PatternDetector.
            persona: User's persona profile.

        Returns:
            UIGenerationResult with 3-6 configured components.
        """
        if self.mock_mode:
            return await self._generate_mock_components(patterns, persona)

        return await self._generate_with_claude(patterns, persona)

    async def _generate_mock_components(
        self,
        patterns: list[Pattern],
        persona: PersonaProfile,
    ) -> UIGenerationResult:
        """
        Generate mock UI components for testing.

        Args:
            patterns: Detected patterns.
            persona: User's persona profile.

        Returns:
            UIGenerationResult with mock components.
        """
        logger.info("Using mock UI component generation")

        components: list[UIComponentType] = []

        # Generate diverse mock components
        if len(patterns) >= 1:
            # Weather info card
            components.append(
                InfoCard(
                    title="Local Weather",
                    pattern_title=patterns[0].title,
                    confidence=patterns[0].confidence,
                    location="San Francisco, CA",
                    info_type="weather",
                    units="metric",
                    show_forecast=True,
                )
            )

        if len(patterns) >= 2:
            # Video feed
            components.append(
                VideoFeed(
                    title=f"{patterns[1].title} Videos",
                    pattern_title=patterns[1].title,
                    confidence=patterns[1].confidence,
                    search_query=" ".join(patterns[1].keywords[:2]),
                    max_results=3,
                    video_duration="any",
                    order_by="relevance",
                )
            )

        if len(patterns) >= 3:
            # Event calendar
            components.append(
                EventCalendar(
                    title=f"{patterns[2].title} Events",
                    pattern_title=patterns[2].title,
                    confidence=patterns[2].confidence,
                    search_query=" ".join(patterns[2].keywords[:2]),
                    location="San Francisco, CA",
                    date_range_days=30,
                    max_events=5,
                    include_online=True,
                )
            )

        if len(patterns) >= 4:
            # Task list
            mock_tasks = [
                TaskItem(
                    text=f"Explore more about {patterns[3].keywords[0]}", priority="high"
                ),
                TaskItem(
                    text=f"Research {patterns[3].keywords[1] if len(patterns[3].keywords) > 1 else 'related topics'}",
                    priority="medium",
                ),
                TaskItem(text="Review saved content", priority="low"),
            ]
            components.append(
                TaskList(
                    title="Recommended Actions",
                    pattern_title=patterns[3].title,
                    confidence=patterns[3].confidence,
                    tasks=mock_tasks,
                    list_type="recommendations",
                )
            )

        # Always add a map card (full width, visually prominent)
        if patterns and len(components) < 6:
            components.append(
                MapCard(
                    title="Places of Interest",
                    pattern_title=patterns[0].title,
                    confidence=patterns[0].confidence,
                    center_lat=37.7749,
                    center_lng=-122.4194,
                    zoom=12,
                    style="streets",
                    markers=[
                        MapMarker(
                            lat=37.7749,
                            lng=-122.4194,
                            title="San Francisco",
                            description="City by the Bay",
                        ),
                        MapMarker(
                            lat=37.8024,
                            lng=-122.4058,
                            title="Alcatraz Island",
                            description="Historic landmark",
                        ),
                        MapMarker(
                            lat=37.7694,
                            lng=-122.4862,
                            title="Golden Gate Park",
                            description="Urban park and recreation",
                        ),
                    ],
                )
            )

        # Always add a content card
        if patterns:
            components.append(
                ContentCard(
                    title="Deep Dive Resource",
                    pattern_title=patterns[0].title,
                    confidence=patterns[0].confidence,
                    article_title=f"Understanding {patterns[0].title}: A Comprehensive Guide",
                    overview=f"An in-depth exploration of {patterns[0].title} covering key concepts, "
                    f"practical applications, and recent developments in the field.",
                    url="https://example.com/article",
                    source_name="Tech Insights",
                    published_date="2024-10-15",
                    search_query=" ".join(patterns[0].keywords[:3]),
                )
            )

        logger.success(f"Generated {len(components)} mock UI components")
        return UIGenerationResult(
            components=components[:6],  # Max 6 components
            total_patterns_analyzed=len(patterns),
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True,
    )
    async def _generate_with_claude(
        self,
        patterns: list[Pattern],
        persona: PersonaProfile,
    ) -> UIGenerationResult:
        """
        Generate components using Claude API with retry logic.

        Args:
            patterns: Detected patterns.
            persona: User's persona profile.

        Returns:
            UIGenerationResult with selected components.

        Raises:
            RuntimeError: If generation fails after retries.
        """
        if not self.llm:
            raise RuntimeError("LLM not initialized")

        logger.info("Generating UI components with Claude")

        try:
            # Build prompt template
            prompt = self._build_prompt()

            # Prepare context
            context = self._prepare_context(patterns, persona)

            # Create structured LLM
            structured_llm = self.llm.with_structured_output(ComponentSelectionResult)

            # Create chain
            chain = prompt | structured_llm

            # Execute
            result = await chain.ainvoke({"context": context})

            # Deduplicate components before enrichment (saves API calls)
            unique_components = self._deduplicate_components(result.components)

            # Enrich components with real data from APIs
            enriched_components = await self._enrich_components(unique_components)

            logger.success(f"Generated {len(enriched_components)} UI components")
            return UIGenerationResult(
                components=enriched_components,
                total_patterns_analyzed=len(patterns),
            )

        except Exception as e:
            logger.error(f"UI generation failed: {e}")
            # Fallback to mock generation
            logger.warning("Falling back to mock UI generation")
            return await self._generate_mock_components(patterns, persona)

    def _build_prompt(self) -> ChatPromptTemplate:
        """
        Build prompt template for component selection.

        Returns:
            ChatPromptTemplate for UI generation.
        """
        system_message = """You are an expert UI designer specializing in personalized dashboard interfaces.

Your task is to select and configure 3-6 interactive UI components based on user patterns and interests.

## Available Component Types:

1. **info-card** (Weather Widget)
   - Use when: User shows interest in specific locations, travel, outdoor activities
   - Provides: Current weather + 3-day forecast
   - Required: location (city name), units (metric/imperial)

2. **map-card** (Interactive Map)
   - Use when: User has location-based interests, travel patterns, geographic focus
   - Provides: Interactive map with custom markers
   - Required: center coordinates, markers (1-20 locations)

3. **video-feed** (YouTube Recommendations)
   - Use when: User engages with video content or specific topics
   - Provides: 3-5 relevant YouTube videos
   - Required: search_query, max_results (1-5), video_duration

4. **event-calendar** (Upcoming Events)
   - Use when: User shows interest in events, networking, learning opportunities
   - Provides: 5-10 relevant local/online events
   - Required: search_query, location (optional), date_range_days

5. **task-list** (Action Items)
   - Use when: User would benefit from guided next steps or learning goals
   - Provides: 2-8 suggested tasks/recommendations
   - Required: tasks array, list_type (goals/recommendations/learning)

6. **content-card** (Deep Dive Article)
   - Use when: User needs ONE focused resource for deep learning
   - Provides: Single article/paper with brief overview and link
   - Required: search_query, overview (2-3 sentences)

## Selection Strategy:

1. **Analyze patterns** for dominant themes and interests
2. **Match components** to user behavior and needs
3. **Diversify selection** - choose 3-6 different component types
4. **Prioritize high-confidence patterns** (confidence > 0.75)
5. **Consider combinations**:
   - Location interest → weather + map
   - Learning focus → videos + events + tasks
   - Research interest → content card + videos

## Configuration Guidelines:

- **Titles**: Clear, specific (max 100 chars)
- **Search queries**: Use actual pattern keywords (not generic terms)
- **Locations**: Be specific (e.g., "San Francisco, CA" not just "California")
- **Task items**: Actionable, relevant to patterns
- **Map markers**: Real places related to user interests

## Quality Criteria:

✓ Each component clearly ties to a specific pattern
✓ Configuration is complete and realistic
✓ Variety in component types (not all videos or all events)
✓ Search queries use actual keywords from patterns
✓ Total: 3-6 components (not more, not less)

## CRITICAL: NO DUPLICATE COMPONENTS

**IMPORTANT**: You MUST generate diverse, non-duplicate components:
- Each component must have a UNIQUE title
- Do NOT create multiple components for the same pattern/topic
- If a pattern deserves multiple widgets, make them meaningfully different
  (e.g., "AI Research Papers" vs "AI Safety Events", NOT two identical "AI Events")
- Aim for 3-6 varied widgets covering different aspects of the persona

**Examples of what NOT to do:**
❌ "AI Safety Events" + "AI Safety Events" (exact duplicate)
❌ "AI Events" + "AI Tech Events" (essentially the same)

**Examples of good diversity:**
✅ "AI Research Papers" + "Tech Industry Events" + "Philosophy Lectures"
✅ "Machine Learning Videos" + "AI Safety Conferences" + "Tech News Map"

Your response will be automatically validated against a Pydantic schema."""

        human_message = """Select and configure UI components for this user:

{context}

Choose 3-6 diverse, relevant components with complete configuration."""

        return ChatPromptTemplate.from_messages([
            ("system", system_message),
            ("human", human_message),
        ])

    def _deduplicate_components(
        self, components: list[UIComponentType]
    ) -> list[UIComponentType]:
        """
        Remove duplicate components by type+title.

        Args:
            components: List of generated components (may contain duplicates)

        Returns:
            List of unique components (first occurrence kept)
        """
        seen = set()
        unique = []

        for comp in components:
            # Create deduplication key from component type and normalized title
            key = (comp.__class__.__name__, comp.title.lower().strip())

            if key not in seen:
                seen.add(key)
                unique.append(comp)
            else:
                logger.warning(
                    f"⚠ Removed duplicate: {comp.__class__.__name__} - {comp.title}"
                )

        if len(unique) < len(components):
            logger.info(
                f"Deduplicated {len(components)} → {len(unique)} components"
            )

        return unique

    def _prepare_context(
        self, patterns: list[Pattern], persona: PersonaProfile
    ) -> str:
        """
        Prepare context for component selection.

        Args:
            patterns: Detected patterns.
            persona: User persona.

        Returns:
            Formatted context string.
        """
        context_parts = [
            "## User Persona",
            f"**Writing Style**: {persona.writing_style}",
            f"**Interests**: {', '.join(persona.interests[:5])}",
            f"**Activity Level**: {persona.activity_level}",
            f"**Content Depth**: {persona.content_depth_preference}",
        ]

        if persona.professional_context:
            context_parts.append(
                f"**Professional Context**: {persona.professional_context}"
            )

        context_parts.append("\n## Detected Patterns")

        for i, pattern in enumerate(patterns[:8], 1):
            context_parts.append(f"\n### Pattern {i}: {pattern.title}")
            context_parts.append(f"**Description**: {pattern.description[:200]}...")
            context_parts.append(f"**Confidence**: {pattern.confidence:.2f}")
            context_parts.append(f"**Keywords**: {', '.join(pattern.keywords[:8])}")
            context_parts.append(f"**Interactions**: {pattern.interaction_count}")

        return "\n".join(context_parts)

    async def _enrich_components(
        self, components: list[UIComponentType]
    ) -> list[UIComponentType]:
        """
        Enrich components with real API data.

        Dispatches each component to appropriate enrichment method,
        running all in parallel for performance.

        Args:
            components: Components from LLM selection.

        Returns:
            Components with enriched data.
        """
        logger.info(f"Enriching {len(components)} components with API data")

        # Create enrichment tasks for parallel execution
        tasks = []
        for comp in components:
            if comp.component_type == "info-card":
                tasks.append(self._enrich_weather(comp))
            elif comp.component_type == "video-feed":
                tasks.append(self._enrich_videos(comp))
            elif comp.component_type == "event-calendar":
                tasks.append(self._enrich_events(comp))
            elif comp.component_type == "map-card":
                tasks.append(self._enrich_map(comp))
            else:
                # No enrichment needed (task-list, content-card)
                async def return_as_is():
                    return comp
                tasks.append(return_as_is())

        # Execute all enrichments in parallel
        try:
            enriched = await asyncio.gather(*tasks, return_exceptions=False)
            logger.success(f"Successfully enriched {len(enriched)} components")
            return enriched
        except Exception as e:
            logger.error(f"Enrichment failed: {e}")
            # Return original components on failure
            return components

    async def _enrich_weather(self, component: InfoCard) -> InfoCard:
        """
        Enrich weather component with real API data.

        Strategy: Geocode location first, then fetch weather.

        Args:
            component: InfoCard to enrich.

        Returns:
            InfoCard with enriched_data populated.
        """
        try:
            logger.info(f"Enriching weather for {component.location}")

            # Step 1: Geocode location to coordinates
            coords = await self.geocoding.geocode(component.location)

            # Step 2: Fetch current weather
            current = await self.weather.get_current_weather(
                lat=coords["lat"],
                lon=coords["lon"],
                units=component.units,
            )

            # Step 3: Fetch forecast if requested
            forecast = []
            if component.show_forecast:
                forecast = await self.weather.get_forecast(
                    lat=coords["lat"],
                    lon=coords["lon"],
                    days=3,
                    units=component.units,
                )

            # Step 4: Return enriched component
            enriched_data = {
                "current": current,
                "forecast": forecast,
                "location": coords["formatted_address"],
            }

            return component.model_copy(update={"enriched_data": enriched_data})

        except Exception as e:
            logger.warning(f"Weather enrichment failed for {component.location}: {e}")
            return component

    async def _enrich_videos(self, component: VideoFeed) -> VideoFeed:
        """
        Enrich video component with YouTube search results.

        Args:
            component: VideoFeed to enrich.

        Returns:
            VideoFeed with enriched_videos populated.
        """
        try:
            logger.info(f"Enriching videos for query: {component.search_query}")

            videos = await self.videos.search_videos(
                query=component.search_query,
                max_results=component.max_results,
                duration=component.video_duration,
                order_by=component.order_by,
            )

            return component.model_copy(update={"enriched_videos": videos})

        except Exception as e:
            logger.warning(f"Video enrichment failed for '{component.search_query}': {e}")
            return component

    async def _enrich_events(self, component: EventCalendar) -> EventCalendar:
        """
        Enrich event calendar with Ticketmaster results.

        Args:
            component: EventCalendar to enrich.

        Returns:
            EventCalendar with enriched_events populated.
        """
        try:
            logger.info(f"Enriching events for query: {component.search_query}")

            # Geocode location if provided
            lat, lon = None, None
            if component.location:
                coords = await self.geocoding.geocode(component.location)
                lat, lon = coords["lat"], coords["lon"]

            # Search for events
            events = await self.events.search_events(
                query=component.search_query,
                lat=lat,
                lon=lon,
                radius_miles=25,
                max_results=component.max_events,
            )

            return component.model_copy(update={"enriched_events": events})

        except Exception as e:
            logger.warning(f"Event enrichment failed for '{component.search_query}': {e}")
            return component

    async def _enrich_map(self, component: MapCard) -> MapCard:
        """
        Enrich map component (currently minimal - coordinates already from LLM).

        Args:
            component: MapCard to enrich.

        Returns:
            MapCard (unchanged for now).
        """
        try:
            logger.info(f"Map component already has {len(component.markers)} markers")
            # Map coordinates already populated by LLM
            # Could add POI enrichment in future
            return component

        except Exception as e:
            logger.warning(f"Map enrichment failed: {e}")
            return component
