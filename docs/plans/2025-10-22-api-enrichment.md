# API Enrichment Implementation Plan

> **For Claude:** Use `${SUPERPOWERS_SKILLS_ROOT}/skills/collaboration/executing-plans/SKILL.md` to implement this plan task-by-task.

**Goal:** Implement real-time API data enrichment for UI components, replacing LLM placeholder data with actual weather, videos, events, and map data.

**Architecture:** Add enrichment methods to UIGenerator that call existing API clients (WeatherAPIClient, YouTubeAPIClient, EventbriteAPIClient, MapboxGeocodingClient) to populate components with real-time data. Use async parallel calls for performance, with graceful fallback to placeholder data on failures.

**Tech Stack:** Python async/await, httpx for HTTP clients, existing API client classes, Pydantic for validation

---

## Current State

**Working:**
- ✅ All 6 UI component types defined in `models/ui_components.py`
- ✅ All 4 API clients implemented in `core/api_clients.py` with mock mode
- ✅ UIGenerator selects components intelligently using Claude
- ✅ Dashboard renders all component types with placeholder data

**Missing:**
- ❌ `_enrich_components()` method just returns components as-is (line 441-460 in `core/ui_generator.py`)
- ❌ No integration between API clients and component enrichment
- ❌ Components show LLM-generated placeholders instead of real data

---

## Task 1: Add Enrichment Tests

**Files:**
- Modify: `fabric_dashboard/tests/test_ui_generator.py`

**Step 1: Add test for weather enrichment**

Add at end of file (before last line):

```python
class TestAPIEnrichment:
    """Tests for real API data enrichment."""

    @pytest.mark.asyncio
    async def test_enrich_weather_component(self):
        """Test that weather component gets enriched with real data."""
        # Create mock weather component
        weather_component = InfoCard(
            title="Local Weather",
            pattern_title="Travel Pattern",
            confidence=0.85,
            location="San Francisco, CA",
            info_type="weather",
            units="metric",
            show_forecast=True,
        )

        # Initialize generator with mock mode
        generator = UIGenerator(mock_mode=True)

        # Enrich component
        enriched = await generator._enrich_weather(weather_component)

        # Verify it's still a valid InfoCard
        assert isinstance(enriched, InfoCard)
        assert enriched.title == "Local Weather"
        assert enriched.location == "San Francisco, CA"

    @pytest.mark.asyncio
    async def test_enrich_video_component(self):
        """Test that video component gets enriched with real data."""
        video_component = VideoFeed(
            title="Learning Videos",
            pattern_title="AI Research",
            confidence=0.9,
            search_query="machine learning tutorial",
            max_results=3,
            video_duration="any",
            order_by="relevance",
        )

        generator = UIGenerator(mock_mode=True)
        enriched = await generator._enrich_videos(video_component)

        assert isinstance(enriched, VideoFeed)
        assert enriched.search_query == "machine learning tutorial"

    @pytest.mark.asyncio
    async def test_enrich_events_component(self):
        """Test that events component gets enriched with real data."""
        events_component = EventCalendar(
            title="Upcoming Events",
            pattern_title="Tech Meetups",
            confidence=0.8,
            search_query="tech meetup",
            location="San Francisco, CA",
            date_range_days=30,
            max_events=5,
            include_online=True,
        )

        generator = UIGenerator(mock_mode=True)
        enriched = await generator._enrich_events(events_component)

        assert isinstance(enriched, EventCalendar)
        assert enriched.search_query == "tech meetup"

    @pytest.mark.asyncio
    async def test_enrich_map_component(self):
        """Test that map component gets enriched with geocoded data."""
        map_component = MapCard(
            title="Travel Destinations",
            pattern_title="Travel Pattern",
            confidence=0.85,
            center_lat=37.7749,
            center_lng=-122.4194,
            zoom=10,
            style="streets",
            markers=[
                MapMarker(
                    lat=37.7749,
                    lng=-122.4194,
                    title="San Francisco",
                    description="Starting point",
                )
            ],
        )

        generator = UIGenerator(mock_mode=True)
        enriched = await generator._enrich_map(map_component)

        assert isinstance(enriched, MapCard)
        assert len(enriched.markers) > 0

    @pytest.mark.asyncio
    async def test_enrich_components_dispatch(self):
        """Test that _enrich_components dispatches to correct enrichers."""
        generator = UIGenerator(mock_mode=True)

        # Create mix of components
        components = [
            InfoCard(
                title="Weather",
                pattern_title="Pattern",
                confidence=0.8,
                location="San Francisco",
                info_type="weather",
                units="metric",
            ),
            VideoFeed(
                title="Videos",
                pattern_title="Pattern",
                confidence=0.8,
                search_query="test",
                max_results=3,
            ),
        ]

        # Enrich all
        enriched = await generator._enrich_components(components)

        # Should return same number of components
        assert len(enriched) == 2
        assert isinstance(enriched[0], InfoCard)
        assert isinstance(enriched[1], VideoFeed)

    @pytest.mark.asyncio
    async def test_enrichment_handles_errors_gracefully(self):
        """Test that enrichment errors don't crash, just log warnings."""
        generator = UIGenerator(mock_mode=True)

        # Create component with invalid data to trigger error
        weather_component = InfoCard(
            title="Weather",
            pattern_title="Pattern",
            confidence=0.8,
            location="InvalidCityName12345",
            info_type="weather",
            units="metric",
        )

        # Should not raise exception, just return original component
        enriched = await generator._enrich_weather(weather_component)
        assert isinstance(enriched, InfoCard)
```

**Step 2: Run tests to verify they fail**

```bash
python -m pytest fabric_dashboard/tests/test_ui_generator.py::TestAPIEnrichment -v
```

Expected: FAIL - Methods `_enrich_weather`, `_enrich_videos`, `_enrich_events`, `_enrich_map` not found

**Step 3: Commit test structure**

```bash
git add fabric_dashboard/tests/test_ui_generator.py
git commit -m "test: add API enrichment test cases"
```

---

## Task 2: Implement Weather Enrichment

**Files:**
- Modify: `fabric_dashboard/core/ui_generator.py:441-460` (replace existing `_enrich_components`)
- Modify: `fabric_dashboard/models/ui_components.py` (add data field to InfoCard)

**Step 1: Update InfoCard schema to hold enriched weather data**

In `fabric_dashboard/models/ui_components.py`, find the `InfoCard` class (line 41) and add optional data field:

```python
class InfoCard(UIComponent):
    """Weather or location-based information card.

    Uses OpenWeatherMap API to show current weather and forecast.
    """

    component_type: Literal["info-card"] = "info-card"
    location: str = Field(
        min_length=1,
        max_length=100,
        description="City name or location (e.g., 'San Francisco, CA')",
    )
    info_type: Literal["weather"] = Field(
        default="weather", description="Type of info (currently only weather)"
    )
    units: Literal["metric", "imperial"] = Field(
        default="metric", description="Temperature units"
    )
    show_forecast: bool = Field(
        default=True, description="Whether to show 3-day forecast"
    )
    # NEW: Field to hold enriched API data
    enriched_data: Optional[dict] = Field(
        default=None, description="Enriched data from API (weather, forecast, etc.)"
    )
```

**Step 2: Implement _enrich_weather method**

In `fabric_dashboard/core/ui_generator.py`, after line 460, add:

```python
async def _enrich_weather(self, component: InfoCard) -> InfoCard:
    """
    Enrich weather info card with real OpenWeatherMap data.

    Args:
        component: InfoCard to enrich.

    Returns:
        InfoCard with enriched_data populated or original on error.
    """
    try:
        logger.info(f"Enriching weather for {component.location}")

        # Fetch current weather
        weather_data = await self.weather_client.get_current_weather(
            location=component.location,
            units=component.units,
        )

        # Fetch forecast if requested
        forecast_data = []
        if component.show_forecast:
            forecast_data = await self.weather_client.get_forecast(
                location=component.location,
                days=3,
                units=component.units,
            )

        # Create enriched data structure
        enriched_data = {
            "current": weather_data,
            "forecast": forecast_data,
        }

        # Return new instance with enriched data
        # (Pydantic models are immutable, so use model_copy with update)
        return component.model_copy(update={"enriched_data": enriched_data})

    except Exception as e:
        logger.warning(f"Weather enrichment failed for {component.location}: {e}")
        # Return original component with placeholder data
        return component
```

**Step 3: Run weather enrichment test**

```bash
python -m pytest fabric_dashboard/tests/test_ui_generator.py::TestAPIEnrichment::test_enrich_weather_component -v
```

Expected: PASS

**Step 4: Commit weather enrichment**

```bash
git add fabric_dashboard/core/ui_generator.py fabric_dashboard/models/ui_components.py
git commit -m "feat: add weather API enrichment"
```

---

## Task 3: Implement Video Enrichment

**Files:**
- Modify: `fabric_dashboard/core/ui_generator.py` (add after `_enrich_weather`)
- Modify: `fabric_dashboard/models/ui_components.py` (add data field to VideoFeed)

**Step 1: Update VideoFeed schema**

In `fabric_dashboard/models/ui_components.py`, find the `VideoFeed` class (line 93) and add:

```python
class VideoFeed(UIComponent):
    """YouTube video recommendations feed.

    Uses YouTube Data API v3 to fetch recent videos matching user interests.
    """

    component_type: Literal["video-feed"] = "video-feed"
    search_query: str = Field(
        min_length=1, max_length=200, description="YouTube search query"
    )
    max_results: int = Field(
        ge=1, le=5, default=3, description="Number of videos to show (1-5)"
    )
    video_duration: Literal["any", "short", "medium", "long"] = Field(
        default="any", description="Video length preference"
    )
    order_by: Literal["relevance", "date", "viewCount"] = Field(
        default="relevance", description="Sort order for results"
    )
    # NEW: Field to hold enriched video data
    enriched_videos: Optional[list[dict]] = Field(
        default=None, description="Enriched video data from YouTube API"
    )
```

**Step 2: Implement _enrich_videos method**

In `fabric_dashboard/core/ui_generator.py`, after `_enrich_weather`, add:

```python
async def _enrich_videos(self, component: VideoFeed) -> VideoFeed:
    """
    Enrich video feed with real YouTube search results.

    Args:
        component: VideoFeed to enrich.

    Returns:
        VideoFeed with enriched_videos populated or original on error.
    """
    try:
        logger.info(f"Enriching videos for query: {component.search_query}")

        # Search YouTube API
        videos = await self.youtube_client.search_videos(
            query=component.search_query,
            max_results=component.max_results,
            duration=component.video_duration,
            order_by=component.order_by,
        )

        # Return new instance with enriched videos
        return component.model_copy(update={"enriched_videos": videos})

    except Exception as e:
        logger.warning(f"Video enrichment failed for '{component.search_query}': {e}")
        return component
```

**Step 3: Run video enrichment test**

```bash
python -m pytest fabric_dashboard/tests/test_ui_generator.py::TestAPIEnrichment::test_enrich_video_component -v
```

Expected: PASS

**Step 4: Commit video enrichment**

```bash
git add fabric_dashboard/core/ui_generator.py fabric_dashboard/models/ui_components.py
git commit -m "feat: add YouTube video API enrichment"
```

---

## Task 4: Implement Events Enrichment

**Files:**
- Modify: `fabric_dashboard/core/ui_generator.py` (add after `_enrich_videos`)
- Modify: `fabric_dashboard/models/ui_components.py` (add data field to EventCalendar)

**Step 1: Update EventCalendar schema**

In `fabric_dashboard/models/ui_components.py`, find the `EventCalendar` class (line 128) and add:

```python
class EventCalendar(UIComponent):
    """Upcoming events calendar.

    Uses Eventbrite API to fetch relevant local/online events.
    """

    component_type: Literal["event-calendar"] = "event-calendar"
    search_query: str = Field(
        min_length=1,
        max_length=200,
        description="Event search query (e.g., 'tech meetups')",
    )
    location: Optional[str] = Field(
        None, max_length=100, description="Location for local events (optional)"
    )
    date_range_days: int = Field(
        ge=1, le=90, default=30, description="Number of days to look ahead"
    )
    max_events: int = Field(
        ge=1, le=10, default=5, description="Maximum number of events to show"
    )
    include_online: bool = Field(
        default=True, description="Include online/virtual events"
    )
    # NEW: Field to hold enriched event data
    enriched_events: Optional[list[dict]] = Field(
        default=None, description="Enriched event data from Eventbrite API"
    )
```

**Step 2: Implement _enrich_events method**

In `fabric_dashboard/core/ui_generator.py`, after `_enrich_videos`, add:

```python
async def _enrich_events(self, component: EventCalendar) -> EventCalendar:
    """
    Enrich event calendar with real Eventbrite results.

    Args:
        component: EventCalendar to enrich.

    Returns:
        EventCalendar with enriched_events populated or original on error.
    """
    try:
        logger.info(f"Enriching events for query: {component.search_query}")

        # Search Eventbrite API
        events = await self.eventbrite_client.search_events(
            query=component.search_query,
            location=component.location,
            date_range_days=component.date_range_days,
            max_events=component.max_events,
            include_online=component.include_online,
        )

        # Return new instance with enriched events
        return component.model_copy(update={"enriched_events": events})

    except Exception as e:
        logger.warning(f"Event enrichment failed for '{component.search_query}': {e}")
        return component
```

**Step 3: Run events enrichment test**

```bash
python -m pytest fabric_dashboard/tests/test_ui_generator.py::TestAPIEnrichment::test_enrich_events_component -v
```

Expected: PASS

**Step 4: Commit events enrichment**

```bash
git add fabric_dashboard/core/ui_generator.py fabric_dashboard/models/ui_components.py
git commit -m "feat: add Eventbrite events API enrichment"
```

---

## Task 5: Implement Map Enrichment

**Files:**
- Modify: `fabric_dashboard/core/ui_generator.py` (add after `_enrich_events`)

**Step 1: Implement _enrich_map method**

In `fabric_dashboard/core/ui_generator.py`, after `_enrich_events`, add:

```python
async def _enrich_map(self, component: MapCard) -> MapCard:
    """
    Enrich map card by geocoding marker locations.

    Note: This is mostly pre-populated by LLM, but we could enhance
    by geocoding location names to precise coordinates.

    Args:
        component: MapCard to enrich.

    Returns:
        MapCard with refined coordinates or original on error.
    """
    try:
        logger.info(f"Enriching map with {len(component.markers)} markers")

        # For now, maps are already well-formed from LLM
        # In future, could geocode marker titles to refine coordinates
        # or add additional nearby points of interest

        # Example: Geocode first marker to refine center point
        if component.markers:
            first_marker = component.markers[0]
            geocoded = await self.mapbox_client.geocode(first_marker.title)

            # Update center coordinates with geocoded data
            return component.model_copy(update={
                "center_lat": geocoded["lat"],
                "center_lng": geocoded["lng"],
            })

        return component

    except Exception as e:
        logger.warning(f"Map enrichment failed: {e}")
        return component
```

**Step 2: Run map enrichment test**

```bash
python -m pytest fabric_dashboard/tests/test_ui_generator.py::TestAPIEnrichment::test_enrich_map_component -v
```

Expected: PASS

**Step 3: Commit map enrichment**

```bash
git add fabric_dashboard/core/ui_generator.py
git commit -m "feat: add Mapbox geocoding enrichment for maps"
```

---

## Task 6: Implement Enrichment Dispatcher

**Files:**
- Modify: `fabric_dashboard/core/ui_generator.py:441-460` (replace existing `_enrich_components`)

**Step 1: Replace _enrich_components with dispatch logic**

In `fabric_dashboard/core/ui_generator.py`, replace lines 441-460 with:

```python
async def _enrich_components(
    self, components: list[UIComponentType]
) -> list[UIComponentType]:
    """
    Enrich components with real data from APIs.

    Dispatches each component to its specific enrichment method,
    running all enrichments in parallel for performance.

    Args:
        components: Components from LLM selection.

    Returns:
        Components enriched with API data (or original on errors).
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
            # No enrichment needed for task-list, content-card
            # Just return as-is by creating a dummy coroutine
            async def return_component():
                return comp
            tasks.append(return_component())

    # Execute all enrichments in parallel
    try:
        enriched = await asyncio.gather(*tasks, return_exceptions=False)
        logger.success(f"Successfully enriched {len(enriched)} components")
        return enriched

    except Exception as e:
        logger.error(f"Enrichment failed: {e}")
        # Return original components if parallel execution fails
        return components
```

**Step 2: Add asyncio import at top of file**

At line 7 in `fabric_dashboard/core/ui_generator.py`, verify `asyncio` is imported:

```python
import asyncio
from typing import Optional
```

**Step 3: Run full enrichment dispatch test**

```bash
python -m pytest fabric_dashboard/tests/test_ui_generator.py::TestAPIEnrichment::test_enrich_components_dispatch -v
```

Expected: PASS

**Step 4: Run all enrichment tests**

```bash
python -m pytest fabric_dashboard/tests/test_ui_generator.py::TestAPIEnrichment -v
```

Expected: All 6 tests PASS

**Step 5: Commit enrichment dispatcher**

```bash
git add fabric_dashboard/core/ui_generator.py
git commit -m "feat: implement parallel API enrichment dispatcher"
```

---

## Task 7: Update Dashboard Rendering to Use Enriched Data

**Files:**
- Modify: `fabric_dashboard/core/dashboard_builder.py` (update component renderers)

**Step 1: Update weather widget to use enriched_data**

In `fabric_dashboard/core/dashboard_builder.py`, find `_render_info_card` method (line 540) and update to use enriched_data:

```python
def _render_info_card(self, component, idx: int) -> str:
    """
    Render weather information card.

    Args:
        component: InfoCard component.
        idx: Component index.

    Returns:
        HTML for weather widget.
    """
    component_id = f"weather-{idx}"

    # Check if we have enriched data
    current_weather = None
    forecast_data = None
    if component.enriched_data:
        current_weather = component.enriched_data.get("current")
        forecast_data = component.enriched_data.get("forecast", [])

    # Initial display values (will be replaced by JavaScript if using mock data)
    temp_display = "--°"
    condition_display = "Loading..."
    feels_like_display = "--°"
    humidity_display = "---%"
    wind_display = "-- km/h"

    if current_weather:
        # Use real enriched data
        temp_display = current_weather.get("temperature", "--")
        temp_unit = current_weather.get("temp_unit", "°")
        temp_display = f"{temp_display}{temp_unit}"
        condition_display = current_weather.get("condition", "Unknown")
        feels_like_display = current_weather.get("feels_like", "--°")
        humidity_display = current_weather.get("humidity", "---%")
        wind_display = current_weather.get("wind_speed", "-- km/h")

    return f'''<div class="ui-component weather-widget rounded-lg border border-[var(--border)] bg-white shadow-sm overflow-hidden p-6" id="{component_id}">
        <h3 class="text-lg font-semibold text-[var(--foreground)] mb-4">{component.title}</h3>

        <!-- Current Weather -->
        <div class="flex items-center justify-between mb-6">
            <div>
                <div class="text-4xl font-bold text-[var(--foreground)]" id="{component_id}-temp">{temp_display}</div>
                <div class="text-sm text-[var(--foreground)] opacity-70" id="{component_id}-location">{component.location}</div>
            </div>
            <div class="text-right">
                <div class="text-xl text-[var(--foreground)]" id="{component_id}-condition">{condition_display}</div>
                <div class="text-sm text-[var(--foreground)] opacity-70">
                    <span id="{component_id}-feels">Feels like {feels_like_display}</span>
                </div>
            </div>
        </div>

        <!-- Weather Details -->
        <div class="grid grid-cols-2 gap-4 mb-4">
            <div class="text-sm">
                <span class="text-[var(--foreground)] opacity-60">Humidity</span>
                <div class="font-semibold" id="{component_id}-humidity">{humidity_display}</div>
            </div>
            <div class="text-sm">
                <span class="text-[var(--foreground)] opacity-60">Wind</span>
                <div class="font-semibold" id="{component_id}-wind">{wind_display}</div>
            </div>
        </div>

        <!-- 3-Day Forecast (if enabled and data available) -->
        {self._render_weather_forecast_with_data(component_id, forecast_data) if component.show_forecast and forecast_data else ''}

        <!-- Hidden data for JavaScript (for mock mode fallback) -->
        <script type="application/json" id="{component_id}-data">
            {self._component_to_json(component)}
        </script>
    </div>'''
```

**Step 2: Add helper method for forecast with real data**

In `fabric_dashboard/core/dashboard_builder.py`, after `_render_weather_forecast` (line 927), add:

```python
def _render_weather_forecast_with_data(self, component_id: str, forecast_data: list) -> str:
    """Render 3-day forecast with real API data."""
    if not forecast_data:
        return self._render_weather_forecast(component_id)

    forecast_html = []
    for day_data in forecast_data[:3]:
        day_name = day_data.get("day_name", "")[:3]  # Mon, Tue, Wed
        high = day_data.get("temperature_high", "--")
        low = day_data.get("temperature_low", "--")

        forecast_html.append(f'''
            <div class="text-center">
                <div class="text-xs font-medium">{day_name}</div>
                <div class="text-lg font-semibold">{high}°</div>
                <div class="text-xs opacity-70">{low}°</div>
            </div>
        ''')

    return f'''<div class="border-t border-[var(--border)] pt-4 mt-4">
        <div class="text-xs font-semibold text-[var(--foreground)] opacity-60 uppercase tracking-wide mb-3">3-Day Forecast</div>
        <div class="grid grid-cols-3 gap-3">
            {''.join(forecast_html)}
        </div>
    </div>'''
```

**Step 3: Update video feed to use enriched_videos**

In `fabric_dashboard/core/dashboard_builder.py`, find `_render_video_feed` method (line 621) and update:

```python
def _render_video_feed(self, component, idx: int) -> str:
    """
    Render YouTube video feed.

    Args:
        component: VideoFeed component.
        idx: Component index.

    Returns:
        HTML for video grid.
    """
    component_id = f"videos-{idx}"

    # Use enriched videos if available, otherwise mock data
    if component.enriched_videos:
        videos = component.enriched_videos[:component.max_results]
        videos_html = '\n'.join([
            f'''<div class="aspect-video">
            <iframe
                width="100%"
                height="100%"
                src="https://www.youtube.com/embed/{video['video_id']}"
                title="{video['title']}"
                frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen
                class="rounded-lg"
            ></iframe>
        </div>'''
            for video in videos
        ])
    else:
        # Fallback to mock videos
        mock_videos = [
            {'id': 'dQw4w9WgXcQ', 'title': 'Video 1'},
            {'id': 'jNQXAC9IVRw', 'title': 'Video 2'},
            {'id': 'y6120QOlsfU', 'title': 'Video 3'},
        ][:component.max_results]

        videos_html = '\n'.join([
            f'''<div class="aspect-video">
            <iframe
                width="100%"
                height="100%"
                src="https://www.youtube.com/embed/{video['id']}"
                title="{video['title']}"
                frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen
                class="rounded-lg"
            ></iframe>
        </div>'''
            for video in mock_videos
        ])

    return f'''<div class="ui-component rounded-lg border border-[var(--border)] bg-white shadow-sm overflow-hidden p-6" id="{component_id}">
        <h3 class="text-lg font-semibold text-[var(--foreground)] mb-4">{component.title}</h3>
        <div class="video-grid">
            {videos_html}
        </div>
        <div class="mt-4 text-xs text-[var(--foreground)] opacity-60">
            Searching: "{component.search_query}"
        </div>
    </div>'''
```

**Step 4: Update event calendar to use enriched_events**

In `fabric_dashboard/core/dashboard_builder.py`, find `_render_event_calendar` method (line 667) and update to use `component.enriched_events` if available (similar pattern to videos - use enriched data if present, otherwise mock data).

**Step 5: Test dashboard rendering with enriched data**

```bash
python -m pytest fabric_dashboard/tests/test_dashboard_builder.py -v
```

Expected: PASS (existing tests should still work)

**Step 6: Commit dashboard rendering updates**

```bash
git add fabric_dashboard/core/dashboard_builder.py
git commit -m "feat: update dashboard to render enriched API data"
```

---

## Task 8: Add API Configuration

**Files:**
- Modify: `fabric_dashboard/utils/config.py`
- Create: `.env.example`
- Modify: `README.md` (add API setup section)

**Step 1: Add API key fields to Config model**

In `fabric_dashboard/utils/config.py`, find the `Config` class and add API key fields:

```python
class Config(BaseModel):
    """Configuration for fabric_dashboard."""

    # Existing fields
    anthropic_api_key: str = Field(...)
    perplexity_api_key: Optional[str] = Field(None)

    # NEW: External API keys for UI components
    openweathermap_api_key: Optional[str] = Field(
        None, description="OpenWeatherMap API key for weather widgets"
    )
    youtube_api_key: Optional[str] = Field(
        None, description="YouTube Data API v3 key for video feeds"
    )
    eventbrite_api_key: Optional[str] = Field(
        None, description="Eventbrite API token for event calendars"
    )
    mapbox_api_key: Optional[str] = Field(
        None, description="Mapbox API token for interactive maps"
    )

    # Rest of existing fields...
```

**Step 2: Create .env.example file**

Create new file at project root:

```bash
# API Keys for Fabric Dashboard

# Required: Anthropic Claude API key
ANTHROPIC_API_KEY=sk-ant-...

# Optional: Perplexity API key for search enrichment
PERPLEXITY_API_KEY=pplx-...

# Optional: External API keys for UI components
# Get these from:
# - OpenWeatherMap: https://home.openweathermap.org/api_keys
# - YouTube: https://console.cloud.google.com/apis/credentials
# - Eventbrite: https://www.eventbrite.com/account-settings/apps
# - Mapbox: https://account.mapbox.com/access-tokens/

OPENWEATHERMAP_API_KEY=
YOUTUBE_API_KEY=
EVENTBRITE_API_KEY=
MAPBOX_API_KEY=
```

**Step 3: Update init command to prompt for API keys**

In `fabric_dashboard/commands/init.py`, add prompts for optional API keys (after Perplexity prompt).

**Step 4: Test configuration loading**

```bash
python -c "from fabric_dashboard.utils.config import get_config; c = get_config(); print(c.openweathermap_api_key)"
```

Expected: Prints key or None (no errors)

**Step 5: Commit configuration changes**

```bash
git add fabric_dashboard/utils/config.py .env.example fabric_dashboard/commands/init.py
git commit -m "feat: add external API key configuration"
```

---

## Task 9: End-to-End Testing

**Files:**
- Manual testing with real dashboard generation

**Step 1: Run dashboard generation with mock mode**

```bash
python -m fabric_dashboard generate --mock
```

Expected:
- Dashboard generates successfully
- Components show mock data
- HTML file opens in browser

**Step 2: Verify mock enrichment works**

Check generated dashboard:
- Weather widget shows mock temperature/conditions
- Video feed shows mock videos
- Events calendar shows mock events
- All components render without errors

**Step 3: Test with real API keys (if available)**

```bash
# First, ensure API keys are configured
python -m fabric_dashboard generate --no-mock
```

Expected:
- Weather widget shows REAL temperature for location
- Video feed shows REAL YouTube search results
- Events calendar shows REAL upcoming events
- No crashes or errors

**Step 4: Test error handling**

Remove one API key from config and run again:

```bash
python -m fabric_dashboard generate --no-mock
```

Expected:
- Dashboard still generates
- Component with missing API key shows placeholder/mock data
- Warning logged but no crash

**Step 5: Run full test suite**

```bash
python -m pytest fabric_dashboard/tests/ -v
```

Expected: All tests PASS (including new enrichment tests)

**Step 6: Document testing results**

Create `docs/api-enrichment-test-results.md` with:
- Test date
- Which APIs were tested
- Sample output (screenshots or JSON)
- Any issues encountered

---

## Task 10: Documentation Update

**Files:**
- Modify: `UI_GENERATOR_STATUS.md`
- Modify: `README.md`

**Step 1: Update UI_GENERATOR_STATUS.md**

Mark Phase 3 as complete:

```markdown
### Phase 3: API Enrichment ✅ **COMPLETE**

**Implemented:**
- [x] Enrichment dispatcher with parallel async calls
- [x] Weather enrichment using OpenWeatherMap
- [x] Video enrichment using YouTube Data API
- [x] Events enrichment using Eventbrite API
- [x] Map enrichment using Mapbox Geocoding
- [x] Graceful error handling with fallback to placeholders
- [x] Dashboard rendering updated to use enriched data
- [x] Configuration support for API keys
- [x] Tests for all enrichment methods
```

**Step 2: Update MVP completion status**

```markdown
## 🎯 MVP Success Criteria

| Criterion | Status |
|-----------|--------|
| UI Generator selects appropriate components | ✅ **DONE** |
| All 6 component types can be generated | ✅ **DONE** |
| API enrichment works for ≥3 types | ✅ **DONE** (all 4) |
| Components in dashboard JSON output | ✅ **DONE** |
| Frontend renders ≥3 component types | ✅ **DONE** (all 6) |
| Demo flow works with real data | ✅ **DONE** |

**MVP Completion**: **6/6 criteria met** (100%)
```

**Step 3: Add API setup guide to README.md**

Add new section to README:

```markdown
## External API Setup (Optional)

The dashboard can enrich UI components with real-time data from external APIs:

### Weather Widgets (OpenWeatherMap)

1. Sign up: https://openweathermap.org/api
2. Get free API key: https://home.openweathermap.org/api_keys
3. Add to `.env`: `OPENWEATHERMAP_API_KEY=your_key`

### Video Feeds (YouTube Data API v3)

1. Enable API: https://console.cloud.google.com/apis/library/youtube.googleapis.com
2. Create credentials: https://console.cloud.google.com/apis/credentials
3. Add to `.env`: `YOUTUBE_API_KEY=your_key`

### Event Calendars (Eventbrite)

1. Sign up: https://www.eventbrite.com/platform/api
2. Get token: https://www.eventbrite.com/account-settings/apps
3. Add to `.env`: `EVENTBRITE_API_KEY=your_token`

### Interactive Maps (Mapbox)

1. Sign up: https://account.mapbox.com/
2. Get token: https://account.mapbox.com/access-tokens/
3. Add to `.env`: `MAPBOX_API_KEY=your_token`

**Note**: All APIs have generous free tiers. Components work without API keys (showing placeholder data).
```

**Step 4: Commit documentation updates**

```bash
git add UI_GENERATOR_STATUS.md README.md docs/api-enrichment-test-results.md
git commit -m "docs: update status and add API setup guide"
```

---

## Success Criteria

✅ **Phase 3 complete when:**
- [ ] All 6 enrichment tests pass
- [ ] Weather widget shows real temperature from OpenWeatherMap
- [ ] Video feed shows real YouTube search results
- [ ] Event calendar shows real Eventbrite events
- [ ] Map component uses real geocoded coordinates
- [ ] Dashboard generates without errors when API keys missing (fallback works)
- [ ] End-to-end test with real API keys succeeds
- [ ] Documentation updated with API setup instructions

---

## Estimated Time

- **Task 1** (Tests): 15 minutes
- **Task 2** (Weather): 20 minutes
- **Task 3** (Videos): 15 minutes
- **Task 4** (Events): 15 minutes
- **Task 5** (Map): 10 minutes
- **Task 6** (Dispatcher): 15 minutes
- **Task 7** (Dashboard Rendering): 30 minutes
- **Task 8** (Configuration): 20 minutes
- **Task 9** (Testing): 30 minutes
- **Task 10** (Documentation): 15 minutes

**Total: ~3 hours**

---

## Notes

- All API clients already exist and work in mock mode
- Schema updates add optional fields (backward compatible)
- Error handling ensures components always render (graceful degradation)
- Parallel enrichment (asyncio.gather) improves performance
- Mock mode still works for development without API keys
