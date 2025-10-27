# UI Generator - Implementation Roadmap

**For**: Junior developers with 1 year of Python experience
**Time**: 10-15 days for MVP (3-6 component types working)
**Goal**: Build a system where AI selects and configures interactive dashboard widgets

---

## 📚 What You Need to Know First

### Prerequisites
✅ **Python basics**: Classes, async/await, type hints
✅ **Pydantic**: Already used in `schemas.py`
✅ **LangChain**: Already used in `pattern_detector.py`, `content_writer.py`
✅ **HTTP requests**: Basic API calls with `httpx`
⚠️ **React/TypeScript**: For frontend (learn as you go)

### What You'll Learn
- Building LLM-powered component selectors
- Integrating multiple external APIs in parallel
- Component-based architecture
- Async Python patterns

### Important Context
**UI Generator is completely separate from ContentWriter**:
- ContentWriter = 4-8 blog-style text cards
- UI Generator = 3-6 interactive widgets with real data
- They don't overlap - they complement each other!

---

## 🗂️ Files You'll Work With

### New Files to Create
```
fabric_dashboard/
├── core/
│   ├── ui_generator.py          (LLM component selection)
│   └── api_enricher.py          (Fetch data from APIs)
├── clients/
│   ├── weather_client.py        (OpenWeatherMap)
│   ├── youtube_client.py        (YouTube API)
│   ├── eventbrite_client.py     (Eventbrite API)
│   └── mapbox_client.py         (Mapbox + geocoding)
└── tests/
    ├── test_ui_generator.py
    ├── test_api_enricher.py
    └── test_clients.py
```

### Files to Modify
```
fabric_dashboard/
├── models/schemas.py            (Add 6 component schemas)
└── core/dashboard_builder.py    (Wire in UI generator)
```

---

## 🗺️ Implementation Phases

| Phase | Days | What | Output |
|-------|------|------|--------|
| **1. Foundation** | 1-3 | Schemas + mock generator | Mock components work |
| **2. LLM Integration** | 4-5 | Hook up Claude | Real component selection |
| **3. API Clients** | 6-8 | Build 4 API clients | Real data fetching |
| **4. Integration** | 9 | Wire into dashboard | End-to-end flow |
| **5. Frontend** | 10-12 | React components | Widgets render |
| **6. Polish** | 13-15 | Errors, caching, docs | Production ready |

---

## 📋 Phase 1: Foundation (Days 1-3)

### Goal
Get basic structure working with mock data (no LLM, no APIs yet)

---

### Day 1 Morning: Add Component Schemas

**File**: `fabric_dashboard/models/schemas.py`

**What to do**: Add these at the end of the file (after Dashboard class)

```python
# ============================================================================
# UI COMPONENTS
# ============================================================================

class UIComponent(BaseModel):
    """Base class for UI components."""
    component_type: str
    title: str = Field(min_length=1, max_length=150)
    subtitle: Optional[str] = Field(None, max_length=200)
    pattern_source: str  # Which pattern generated this


# 1. Info Card (Weather, Stats)
class InfoCardItem(BaseModel):
    label: str = Field(min_length=1, max_length=50)
    value: str = Field(min_length=1, max_length=100)
    icon: str = Field(default="circle")  # lucide-react icon name


class InfoCard(UIComponent):
    component_type: Literal["info-card"] = "info-card"
    items: list[InfoCardItem] = Field(min_length=1, max_length=8)
    data_source: str = Field(default="manual")


# 2. Video Feed
class VideoItem(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    thumbnail_url: str
    video_url: str
    channel: str
    duration: str
    views: Optional[str] = None


class VideoFeed(UIComponent):
    component_type: Literal["video-feed"] = "video-feed"
    items: list[VideoItem] = Field(min_length=1, max_length=5)
    search_query: str


# 3. Event Calendar
class CalendarEvent(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    date: str  # ISO format YYYY-MM-DD
    location: str
    venue: Optional[str] = None
    url: str
    is_free: bool = True
    price: Optional[str] = None


class EventCalendar(UIComponent):
    component_type: Literal["event-calendar"] = "event-calendar"
    events: list[CalendarEvent] = Field(min_length=1, max_length=10)
    search_query: str


# 4. Task List
class TaskItem(BaseModel):
    id: str
    content: str = Field(min_length=1, max_length=300)
    checked: bool = False
    priority: Literal["low", "medium", "high"] = "medium"


class TaskList(UIComponent):
    component_type: Literal["task-list"] = "task-list"
    items: list[TaskItem] = Field(min_length=1, max_length=15)
    allow_editing: bool = True
    allow_reordering: bool = True


# 5. Content Card (Single Article)
class ContentCard(UIComponent):
    component_type: Literal["content-card"] = "content-card"
    article_title: str = Field(min_length=1, max_length=200)
    overview: str = Field(min_length=50, max_length=300)  # Brief summary
    url: str
    source_name: str
    published_date: Optional[str] = None
    search_query: str


# 6. Map Card
class MapMarker(BaseModel):
    lat: float = Field(ge=-90, le=90)
    lng: float = Field(ge=-180, le=180)
    label: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=200)
    icon: str = Field(default="location-dot")
    color: str = Field(default="#FF5533", pattern=r"^#[0-9a-fA-F]{6}$")


class MapCard(UIComponent):
    component_type: Literal["map-card"] = "map-card"
    center_lat: float = Field(ge=-90, le=90)
    center_lng: float = Field(ge=-180, le=180)
    zoom: int = Field(ge=1, le=20, default=10)
    style: Literal["streets", "satellite", "outdoors"] = "streets"
    markers: list[MapMarker] = Field(min_length=1, max_length=20)
    data_source: str = Field(default="manual")


# Union type for all components
UIComponentType = InfoCard | VideoFeed | EventCalendar | TaskList | ContentCard | MapCard
```

**Test it**:
```bash
python

# In Python REPL:
from fabric_dashboard.models.schemas import InfoCard, InfoCardItem

card = InfoCard(
    title="Test Weather",
    pattern_source="Test Pattern",
    items=[
        InfoCardItem(label="Temp", value="24°C", icon="thermometer")
    ],
    data_source="manual"
)

print(card.model_dump_json(indent=2))
# Should print valid JSON without errors ✅
```

---

### Day 1 Afternoon: Create UI Generator (Mock Mode)

**File**: `fabric_dashboard/core/ui_generator.py` (NEW)

**What to do**: Create a class similar to `content_writer.py`

```python
"""UI Generator module for creating interactive dashboard components."""

from typing import Optional

from langchain_anthropic import ChatAnthropic
from pydantic import BaseModel, Field

from fabric_dashboard.models.schemas import (
    Pattern,
    PersonaProfile,
    InfoCard,
    InfoCardItem,
    VideoFeed,
    VideoItem,
    TaskList,
    TaskItem,
    UIComponentType,
)
from fabric_dashboard.utils import logger


class UIGenerationResult(BaseModel):
    """Result from UI component generation."""

    components: list[UIComponentType] = Field(
        min_length=1,
        max_length=6,
        description="Generated UI components (1-6 components)",
    )
    reasoning: str = Field(
        description="Explanation of why these components were chosen"
    )


class UIGenerator:
    """Generates interactive UI components based on user patterns."""

    def __init__(self, mock_mode: bool = False):
        """
        Initialize UI generator.

        Args:
            mock_mode: If True, use mock generation instead of real LLM calls.
        """
        self.mock_mode = mock_mode
        self.llm: Optional[ChatAnthropic] = None

        if not mock_mode:
            # We'll add LLM initialization in Phase 2
            pass

    async def generate_components(
        self,
        patterns: list[Pattern],
        persona: PersonaProfile,
        max_components: int = 5,
    ) -> UIGenerationResult:
        """
        Generate UI components based on patterns and persona.

        Args:
            patterns: Detected user patterns
            persona: User persona profile
            max_components: Maximum number of components to generate

        Returns:
            UIGenerationResult with selected components
        """
        if self.mock_mode:
            return self._mock_generation(patterns, persona, max_components)
        else:
            # Phase 2: will implement LLM generation
            return self._mock_generation(patterns, persona, max_components)

    def _mock_generation(
        self,
        patterns: list[Pattern],
        persona: PersonaProfile,
        max_components: int,
    ) -> UIGenerationResult:
        """Generate mock components for testing."""
        logger.info(f"Generating mock UI components for {len(patterns)} patterns")

        components: list[UIComponentType] = []

        # For each pattern, generate 0-2 components
        for i, pattern in enumerate(patterns[:3]):  # Max 3 patterns
            # Pattern 1 → Info Card
            if i == 0 and len(components) < max_components:
                components.append(InfoCard(
                    title=f"{pattern.title} - Status",
                    subtitle="Current information",
                    pattern_source=pattern.title,
                    items=[
                        InfoCardItem(
                            label="Confidence",
                            value=f"{pattern.confidence:.0%}",
                            icon="trending-up"
                        ),
                        InfoCardItem(
                            label="Interactions",
                            value=str(pattern.interaction_count),
                            icon="activity"
                        ),
                    ],
                    data_source="mock"
                ))

            # Pattern 2 → Video Feed
            if i == 1 and len(components) < max_components:
                components.append(VideoFeed(
                    title=f"{pattern.title} - Videos",
                    subtitle="Learn more",
                    pattern_source=pattern.title,
                    items=[
                        VideoItem(
                            title=f"Guide to {pattern.title}",
                            thumbnail_url="https://via.placeholder.com/480x360",
                            video_url="https://youtube.com/watch?v=mock",
                            channel="Mock Channel",
                            duration="10:23",
                            views="1.2K"
                        )
                    ],
                    search_query=" ".join(pattern.keywords[:3])
                ))

            # Pattern 3 → Task List
            if i == 2 and len(components) < max_components:
                components.append(TaskList(
                    title=f"{pattern.title} - Tasks",
                    subtitle="Get started",
                    pattern_source=pattern.title,
                    items=[
                        TaskItem(
                            id=f"task-{j}",
                            content=f"Task {j+1} for {pattern.title}",
                            priority="medium"
                        )
                        for j in range(3)
                    ],
                ))

        # Ensure at least 1 component
        if not components:
            components.append(InfoCard(
                title="Dashboard Status",
                subtitle="Getting started",
                pattern_source="General",
                items=[InfoCardItem(label="Status", value="Ready", icon="check")],
                data_source="mock"
            ))

        logger.success(f"Generated {len(components)} mock components")

        return UIGenerationResult(
            components=components,
            reasoning="Mock generation for testing"
        )
```

**Test it**:
```python
# In Python REPL (use asyncio for async functions)
import asyncio
from fabric_dashboard.core.ui_generator import UIGenerator
from fabric_dashboard.models.schemas import Pattern, PersonaProfile

async def test():
    pattern = Pattern(
        title="Test Pattern",
        description="Test",
        confidence=0.8,
        keywords=["test"],
        interaction_count=10
    )

    persona = PersonaProfile(
        writing_style="casual",
        interests=["tech"],
        activity_level="moderate"
    )

    generator = UIGenerator(mock_mode=True)
    result = await generator.generate_components([pattern], persona)

    print(f"Generated {len(result.components)} components")
    for comp in result.components:
        print(f"- {comp.component_type}: {comp.title}")

asyncio.run(test())
# Should print components without errors ✅
```

---

### Day 2: Write Tests

**File**: `fabric_dashboard/tests/test_ui_generator.py` (NEW)

```python
"""Tests for UI Generator."""

import pytest

from fabric_dashboard.core.ui_generator import UIGenerator, UIGenerationResult
from fabric_dashboard.models.schemas import Pattern, PersonaProfile


@pytest.fixture
def mock_patterns():
    """Mock patterns for testing."""
    return [
        Pattern(
            title="Test Pattern 1",
            description="First test",
            confidence=0.9,
            keywords=["test", "demo"],
            interaction_count=20
        ),
        Pattern(
            title="Test Pattern 2",
            description="Second test",
            confidence=0.8,
            keywords=["test"],
            interaction_count=15
        ),
    ]


@pytest.fixture
def mock_persona():
    """Mock persona for testing."""
    return PersonaProfile(
        writing_style="casual",
        interests=["technology"],
        activity_level="high"
    )


@pytest.mark.asyncio
async def test_mock_generation(mock_patterns, mock_persona):
    """Test that mock mode generates valid components."""
    generator = UIGenerator(mock_mode=True)
    result = await generator.generate_components(mock_patterns, mock_persona)

    assert isinstance(result, UIGenerationResult)
    assert 1 <= len(result.components) <= 6
    assert len(result.reasoning) > 0

    for comp in result.components:
        assert hasattr(comp, "pattern_source")
        assert len(comp.title) > 0


@pytest.mark.asyncio
async def test_max_components_limit(mock_patterns, mock_persona):
    """Test max_components limit."""
    generator = UIGenerator(mock_mode=True)
    result = await generator.generate_components(
        mock_patterns,
        mock_persona,
        max_components=2
    )

    assert len(result.components) <= 2


def test_info_card_schema():
    """Test InfoCard validation."""
    from fabric_dashboard.models.schemas import InfoCard, InfoCardItem

    # Valid card
    card = InfoCard(
        title="Test",
        pattern_source="Pattern",
        items=[InfoCardItem(label="Label", value="Value", icon="check")],
        data_source="test"
    )
    assert card.component_type == "info-card"

    # Invalid card (empty items) should fail
    with pytest.raises(ValueError):
        InfoCard(
            title="Test",
            pattern_source="Pattern",
            items=[],
            data_source="test"
        )
```

**Run tests**:
```bash
python -m pytest fabric_dashboard/tests/test_ui_generator.py -v

# All tests should pass ✅
```

---

### Day 3: Review & Document

**What to do**:
1. Review all code written so far
2. Ensure tests pass
3. Commit to git (if using version control)
4. Take notes on any questions

**Checkpoint**: ✅ Mock UI Generator works, schemas validated, tests pass

---

## 📋 Phase 2: LLM Integration (Days 4-5)

### Goal
Hook up Claude to select components intelligently

---

### Day 4 Morning: Add LLM Initialization

**File**: `fabric_dashboard/core/ui_generator.py`

**Update the `__init__` method**:

```python
def __init__(self, mock_mode: bool = False):
    """Initialize UI generator."""
    self.mock_mode = mock_mode
    self.llm: Optional[ChatAnthropic] = None

    if not mock_mode:
        from fabric_dashboard.utils.config import get_config

        config = get_config()
        if not config:
            raise RuntimeError("Configuration not found")

        self.llm = ChatAnthropic(
            model_name="claude-sonnet-4-5",
            temperature=0.7,
            api_key=config.anthropic_api_key,
            timeout=60,
            max_tokens=4096,
        )
```

---

### Day 4 Afternoon: Create LLM Prompt

**File**: `fabric_dashboard/core/ui_generator.py`

**Add this method**:

```python
from langchain_core.prompts import ChatPromptTemplate

def _build_prompt(self) -> ChatPromptTemplate:
    """Build prompt for component selection."""

    system_message = """You are a UI component selector for generative interfaces.

Your task: Analyze user patterns and select 3-5 relevant UI components.

## Available Components:

1. **info-card**: Real-time data (weather, stats)
   - Use when: Location keywords (cities, countries)
   - Example: "Marrakech Right Now" with temperature

2. **video-feed**: YouTube videos for learning
   - Use when: "tutorial", "guide", "how to"
   - Example: "Morocco Travel Videos"

3. **event-calendar**: Upcoming events
   - Use when: "conference", "event", "meetup"
   - Example: "AI Conferences Near You"

4. **task-list**: Interactive checklists
   - Use when: Planning/organizing patterns
   - Example: "Trip Planning Checklist"

5. **content-card**: ONE recommended article/paper
   - Use when: Research/learning patterns
   - Example: ONE focused article for deep reading

6. **map-card**: Interactive location map
   - REQUIRED when: 2+ location keywords
   - Example: Map showing multiple cities

## Rules:
- Generate 3-5 components total
- Prioritize high-confidence patterns (>0.75)
- Location patterns → Map + Weather combo
- Each pattern generates 0-2 components
- Consider persona preferences

## Output:
For each component:
- component_type (exact name from list)
- title (engaging, specific)
- subtitle (optional context)
- pattern_source (pattern title)
- Minimal placeholder data (APIs will enrich later)

Provide reasoning for your choices."""

    human_message = """Analyze these patterns and select components:

## Patterns:
{patterns_context}

## Persona:
{persona_context}

Select 3-5 appropriate components and explain why."""

    return ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("human", human_message),
    ])
```

---

### Day 5: Implement LLM Generation

**File**: `fabric_dashboard/core/ui_generator.py`

**Add these methods**:

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    reraise=True,
)
async def _generate_with_claude(
    self,
    patterns: list[Pattern],
    persona: PersonaProfile,
    max_components: int,
) -> UIGenerationResult:
    """Generate components using Claude."""

    if not self.llm:
        raise RuntimeError("LLM not initialized")

    logger.info("Generating components with Claude")

    try:
        prompt = self._build_prompt()

        # Format context
        patterns_context = self._format_patterns(patterns)
        persona_context = self._format_persona(persona)

        # Create structured LLM
        structured_llm = self.llm.with_structured_output(UIGenerationResult)

        # Create chain
        chain = prompt | structured_llm

        # Execute
        result = await chain.ainvoke({
            "patterns_context": patterns_context,
            "persona_context": persona_context,
        })

        # Limit to max
        if len(result.components) > max_components:
            result.components = result.components[:max_components]

        logger.success(f"Generated {len(result.components)} components")
        return result

    except Exception as e:
        logger.error(f"Generation failed: {e}")
        logger.warning("Falling back to mock")
        return self._mock_generation(patterns, persona, max_components)


def _format_patterns(self, patterns: list[Pattern]) -> str:
    """Format patterns for prompt."""
    lines = []
    for i, pattern in enumerate(patterns, 1):
        lines.append(f"\n### Pattern {i}: {pattern.title}")
        lines.append(f"- Description: {pattern.description}")
        lines.append(f"- Keywords: {', '.join(pattern.keywords)}")
        lines.append(f"- Confidence: {pattern.confidence:.2f}")
        lines.append(f"- Interactions: {pattern.interaction_count}")
    return "\n".join(lines)


def _format_persona(self, persona: PersonaProfile) -> str:
    """Format persona for prompt."""
    return f"""
- Writing Style: {persona.writing_style}
- Interests: {', '.join(persona.interests)}
- Activity Level: {persona.activity_level}
- Content Depth: {persona.content_depth_preference}
"""
```

**Update `generate_components`**:
```python
async def generate_components(
    self,
    patterns: list[Pattern],
    persona: PersonaProfile,
    max_components: int = 5,
) -> UIGenerationResult:
    """Generate UI components."""
    if self.mock_mode:
        return self._mock_generation(patterns, persona, max_components)
    else:
        return await self._generate_with_claude(patterns, persona, max_components)
```

**Test with real LLM**:
```python
# Set mock_mode=False to use real Claude
generator = UIGenerator(mock_mode=False)
result = await generator.generate_components(patterns, persona)

print(result.reasoning)
for comp in result.components:
    print(f"{comp.component_type}: {comp.title}")

# Should see intelligent component selection ✅
```

---

## 📋 Phase 3: API Clients (Days 6-8)

### Goal
Build 4 API client classes to fetch real data

**Strategy**: Build one at a time, test each, then combine

---

### Day 6 Morning: Weather Client

**File**: `fabric_dashboard/clients/weather_client.py` (NEW)

```python
"""OpenWeatherMap API client."""

import httpx
from typing import Optional

from fabric_dashboard.utils import logger


class WeatherClient:
    """Client for OpenWeatherMap API."""

    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = httpx.AsyncClient(timeout=10.0)

    async def get_weather(
        self,
        city: str,
        country_code: Optional[str] = None
    ) -> dict:
        """Get current weather for a city."""
        try:
            query = f"{city},{country_code}" if country_code else city

            response = await self.client.get(
                self.BASE_URL,
                params={
                    "q": query,
                    "appid": self.api_key,
                    "units": "metric",
                }
            )
            response.raise_for_status()
            data = response.json()

            return {
                "city": data["name"],
                "country": data["sys"]["country"],
                "temp": f"{data['main']['temp']:.0f}°C",
                "feels_like": f"{data['main']['feels_like']:.0f}°C",
                "description": data["weather"][0]["description"].title(),
                "humidity": f"{data['main']['humidity']}%",
                "wind_speed": f"{data['wind']['speed']} m/s",
                "icon": data["weather"][0]["icon"],
            }

        except Exception as e:
            logger.error(f"Weather fetch failed: {e}")
            raise

    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()
```

**Get API key**: Sign up at https://openweathermap.org/api (free, 5 min)

**Test**:
```python
import asyncio

async def test():
    client = WeatherClient(api_key="YOUR_KEY")
    weather = await client.get_weather("London", "GB")
    print(weather)
    await client.close()

asyncio.run(test())
# Should print real weather data ✅
```

---

### Day 6 Afternoon: YouTube Client

**File**: `fabric_dashboard/clients/youtube_client.py` (NEW)

```python
"""YouTube Data API v3 client."""

import httpx

from fabric_dashboard.utils import logger


class YouTubeClient:
    """Client for YouTube Data API."""

    BASE_URL = "https://www.googleapis.com/youtube/v3/search"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = httpx.AsyncClient(timeout=10.0)

    async def search_videos(
        self,
        query: str,
        max_results: int = 5,
    ) -> list[dict]:
        """Search for videos."""
        try:
            response = await self.client.get(
                self.BASE_URL,
                params={
                    "part": "snippet",
                    "q": query,
                    "type": "video",
                    "maxResults": min(max_results, 50),
                    "key": self.api_key,
                }
            )
            response.raise_for_status()
            data = response.json()

            videos = []
            for item in data.get("items", []):
                video_id = item["id"]["videoId"]
                snippet = item["snippet"]

                videos.append({
                    "video_id": video_id,
                    "title": snippet["title"],
                    "description": snippet["description"][:200],
                    "channel": snippet["channelTitle"],
                    "thumbnail_url": snippet["thumbnails"]["high"]["url"],
                    "video_url": f"https://youtube.com/watch?v={video_id}",
                })

            logger.info(f"Found {len(videos)} videos for '{query}'")
            return videos

        except Exception as e:
            logger.error(f"YouTube search failed: {e}")
            raise

    async def close(self):
        await self.client.aclose()
```

**Get API key**: https://console.cloud.google.com/apis/library/youtube.googleapis.com

---

### Days 7-8: Eventbrite & Mapbox Clients

Similar structure - see spec for details. Key points:

**Eventbrite**: Search events by keyword + location
**Mapbox**: Geocode location names to lat/lng

---

### Day 8: API Enricher

**File**: `fabric_dashboard/core/api_enricher.py` (NEW)

This orchestrates all API calls in parallel:

```python
"""API enrichment layer."""

import asyncio
from typing import Optional

from fabric_dashboard.clients.weather_client import WeatherClient
from fabric_dashboard.clients.youtube_client import YouTubeClient
from fabric_dashboard.models.schemas import (
    UIComponentType,
    InfoCard,
    VideoFeed,
    InfoCardItem,
    VideoItem,
)
from fabric_dashboard.utils import logger


class APIEnricher:
    """Enriches UI components with real API data."""

    def __init__(
        self,
        weather_api_key: Optional[str] = None,
        youtube_api_key: Optional[str] = None,
    ):
        self.weather_client = (
            WeatherClient(weather_api_key) if weather_api_key else None
        )
        self.youtube_client = (
            YouTubeClient(youtube_api_key) if youtube_api_key else None
        )

    async def enrich_components(
        self,
        components: list[UIComponentType],
    ) -> list[UIComponentType]:
        """Enrich components with API data in parallel."""
        logger.info(f"Enriching {len(components)} components")

        tasks = []
        for comp in components:
            if comp.component_type == "info-card":
                tasks.append(self._enrich_info_card(comp))
            elif comp.component_type == "video-feed":
                tasks.append(self._enrich_video_feed(comp))
            else:
                # No enrichment needed
                tasks.append(asyncio.create_task(asyncio.sleep(0, result=comp)))

        enriched = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out exceptions
        result = []
        for item in enriched:
            if isinstance(item, Exception):
                logger.warning(f"Enrichment failed: {item}")
            else:
                result.append(item)

        logger.success(f"Enriched {len(result)}/{len(components)} components")
        return result

    async def _enrich_info_card(self, card: InfoCard) -> InfoCard:
        """Enrich info card with weather."""
        if not self.weather_client:
            return card

        try:
            # Extract city from title (simple approach)
            # TODO: Use NLP or LLM for better extraction
            city = card.title.split()[0]

            weather = await self.weather_client.get_weather(city)

            card.items = [
                InfoCardItem(label="Temperature", value=weather["temp"], icon="thermometer"),
                InfoCardItem(label="Conditions", value=weather["description"], icon="cloud"),
                InfoCardItem(label="Humidity", value=weather["humidity"], icon="droplets"),
            ]
            card.data_source = "weather_api"

            return card

        except Exception as e:
            logger.warning(f"Weather enrichment failed: {e}")
            return card

    async def _enrich_video_feed(self, feed: VideoFeed) -> VideoFeed:
        """Enrich video feed with YouTube."""
        if not self.youtube_client:
            return feed

        try:
            videos = await self.youtube_client.search_videos(
                feed.search_query,
                max_results=5
            )

            feed.items = [
                VideoItem(
                    title=v["title"],
                    thumbnail_url=v["thumbnail_url"],
                    video_url=v["video_url"],
                    channel=v["channel"],
                    duration="",
                    views=None,
                )
                for v in videos
            ]

            return feed

        except Exception as e:
            logger.warning(f"Video enrichment failed: {e}")
            return feed

    async def close(self):
        """Close all clients."""
        if self.weather_client:
            await self.weather_client.close()
        if self.youtube_client:
            await self.youtube_client.close()
```

---

## 📋 Phase 4: Integration (Day 9)

### Goal
Wire UI Generator into dashboard builder

**File**: `fabric_dashboard/core/dashboard_builder.py`

**Add imports**:
```python
from fabric_dashboard.core.ui_generator import UIGenerator
from fabric_dashboard.core.api_enricher import APIEnricher
```

**In `build_dashboard` function, after content generation**:

```python
# NEW: Generate UI components
ui_generator = UIGenerator(mock_mode=config.mock_mode)
component_result = await ui_generator.generate_components(
    patterns=pattern_result.patterns,
    persona=pattern_result.persona,
    max_components=5,
)

# NEW: Enrich with API data
api_enricher = APIEnricher(
    weather_api_key=getattr(config, 'weather_api_key', None),
    youtube_api_key=getattr(config, 'youtube_api_key', None),
)
enriched_components = await api_enricher.enrich_components(
    component_result.components
)
await api_enricher.close()

# Add to dashboard
return Dashboard(
    user_name=user_data.connection_id,
    cards=cards,
    components=enriched_components,  # NEW
    persona=pattern_result.persona,
    # ... rest of fields
)
```

**Update Dashboard schema** in `schemas.py`:
```python
class Dashboard(BaseModel):
    # ... existing fields ...
    components: list[UIComponentType] = Field(
        default_factory=list,
        description="Interactive UI components",
        max_length=6,
    )
```

**Test end-to-end**:
```bash
python -m fabric_dashboard generate --connection-id test_123

# Check output includes components
cat ~/.fabric-dashboard/dashboards/latest.json | jq '.components'
```

---

## ✅ Success Criteria

### MVP Complete When:
- [ ] UI Generator selects components intelligently
- [ ] At least 3 component types work end-to-end
- [ ] At least 2 APIs integrated (weather + YouTube)
- [ ] Components in dashboard JSON output
- [ ] Demo works: Morocco travel → Map + Weather + Videos

### Next Steps (Phase 5-6):
- Frontend rendering (React components)
- Error handling & caching
- Documentation

---

## 🆘 Common Issues & Solutions

### Issue: Pydantic ValidationError
```
Error: Field required
Solution: Check all required fields are present in model
Example: InfoCard needs title, pattern_source, items
```

### Issue: Async/Await Error
```
Error: Can't use 'await' with non-async function
Solution: Ensure function is 'async def' and you're using 'await'
```

### Issue: API Rate Limits
```
Error: 429 Too Many Requests
Solution: Add delays: await asyncio.sleep(1)
```

### Issue: LLM Schema Mismatch
```
Error: Invalid component_type returned
Solution: Check Literal types in schemas match exactly
```

---

## 🎯 Tips for Success

1. ✅ **Start with mock mode** - Get structure working first
2. ✅ **Test incrementally** - Test each piece individually
3. ✅ **Copy existing patterns** - Look at content_writer.py
4. ✅ **Read error messages** - Pydantic errors are helpful
5. ✅ **Use logger.info()** - Print debugging is your friend
6. ✅ **Ask for help** - Get code review before next phase

---

Good luck building! 🚀 Remember: Start simple, make it work, then make it better.
