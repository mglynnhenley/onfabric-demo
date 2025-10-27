# UI Generator - Technical Specification

## What Are We Building?

A **UI Generator** that creates interactive dashboard widgets based on user behavior patterns. This is an MVP proof-of-concept for **generative interfaces** - where AI intelligently chooses and configures UI components dynamically.

Think of it like this:
- **ContentWriter** (existing) → Generates text-based blog-style cards
- **UIGenerator** (new) → Generates interactive widgets with real data from APIs

---

## Why Is This Cool?

**Problem**: Every user has different interests, but dashboards are usually static and generic.

**Solution**: Generate personalized UI components on-the-fly:
- User interested in Morocco travel? → Weather widget + map + trip checklist + travel videos
- User researching AI? → Event calendar + research articles + video tutorials
- User into fitness? → Task tracker + weather for outdoor activities

**Demo Value**: Shows how AI can create entire interfaces with real data, not just text. Very impressive for investors/users.

---

## 🔄 Relationship to ContentWriter

**IMPORTANT**: UI Generator is completely separate from ContentWriter:

- **ContentWriter** (existing) → Generates 4-8 blog-style text cards (100-500 words each)
- **UI Generator** (new) → Generates 3-6 interactive widgets with real-time data

**No overlap**: ContentWriter handles narrative content, UI Generator handles actionable widgets. They work in parallel and complement each other.

---

## High-Level Architecture

```
┌─────────────────┐
│ Pattern Detector│  Analyzes user data
│  (existing)     │  Finds interests & persona
└────────┬────────┘
         │ patterns + persona
         ▼
┌─────────────────┐
│  UI Generator   │  LLM picks components
│     (NEW)       │  Matches patterns → components
└────────┬────────┘
         │ component configs
         ▼
┌─────────────────┐
│  API Enricher   │  Fetches real data
│     (NEW)       │  Weather, videos, events, maps
└────────┬────────┘
         │ enriched components
         ▼
┌─────────────────┐
│  Dashboard      │  Renders interactive widgets
│   (frontend)    │
└─────────────────┘
```

---

## Component Library: 6 Types

### 1. Info Card (Weather & Stats)
**What**: Real-time data display (weather, prices, metrics)
**Shadcn**: Custom Card with lucide-react icons
**APIs**: OpenWeatherMap
**Triggers**: Location keywords, trackable metrics

**Example**:
```json
{
  "component_type": "info-card",
  "title": "Marrakech Right Now",
  "subtitle": "Perfect travel weather",
  "items": [
    {"label": "Temperature", "value": "24°C", "icon": "thermometer"},
    {"label": "Conditions", "value": "Clear sky", "icon": "sun"},
    {"label": "Humidity", "value": "45%", "icon": "droplets"}
  ],
  "pattern_source": "Morocco Travel Planner",
  "data_source": "weather_api"
}
```

**When to use**:
- Pattern keywords contain cities/countries → Weather info
- Keywords like "price", "stock", "crypto" → Price tracking (future)

---

### 2. Video Feed
**What**: Curated YouTube videos for learning/entertainment
**Shadcn**: Grid of Cards with thumbnails
**APIs**: YouTube Data API v3
**Triggers**: Learning, entertainment, how-to patterns

**Example**:
```json
{
  "component_type": "video-feed",
  "title": "Morocco Travel Videos",
  "subtitle": "Visual inspiration for your trip",
  "items": [
    {
      "title": "10 Days in Morocco - Complete Guide",
      "thumbnail_url": "https://...",
      "video_url": "https://youtube.com/watch?v=...",
      "channel": "Travel With Me",
      "duration": "15:23",
      "views": "1.2M"
    }
  ],
  "pattern_source": "Morocco Travel Planner",
  "search_query": "morocco travel vlog 2025"
}
```

**When to use**:
- Keywords: "tutorial", "guide", "how to" → Video feed
- High engagement patterns with visual topics
- Persona `activity_level: "high"` → More video content

---

### 3. Event Calendar
**What**: Upcoming events from Eventbrite
**Shadcn**: `mini-calendar` or custom event list
**APIs**: Eventbrite API
**Triggers**: Event/conference keywords, time-sensitive patterns

**Example**:
```json
{
  "component_type": "event-calendar",
  "title": "Upcoming AI Events",
  "subtitle": "Conferences and meetups",
  "events": [
    {
      "name": "AI Summit 2025",
      "date": "2025-06-15",
      "location": "San Francisco, CA",
      "venue": "Moscone Center",
      "url": "https://eventbrite.com/e/...",
      "is_free": false,
      "price": "$299"
    }
  ],
  "pattern_source": "AI Research Enthusiast",
  "search_query": "artificial intelligence conference"
}
```

**When to use**:
- Keywords: "conference", "meetup", "event", "summit"
- Professional context in persona → Professional events
- Time-sensitive planning patterns

---

### 4. Task List (Interactive Checklist)
**What**: User-editable checklists with local storage
**Shadcn**: `list` component with checkboxes
**APIs**: None (local storage)
**Triggers**: Planning/organizing patterns, project keywords

**Example**:
```json
{
  "component_type": "task-list",
  "title": "Your Morocco Trip Checklist",
  "subtitle": "Stay organized",
  "items": [
    {"id": "1", "content": "Book flights to Marrakech", "checked": false, "priority": "high"},
    {"id": "2", "content": "Reserve riad accommodation", "checked": false, "priority": "high"},
    {"id": "3", "content": "Plan desert tour itinerary", "checked": false, "priority": "medium"}
  ],
  "pattern_source": "Morocco Travel Planner",
  "allow_editing": true,
  "allow_reordering": true
}
```

**When to use**:
- Keywords: "planning", "organize", "todo", "project"
- Travel patterns → Trip planning checklist
- Project/goal patterns → Project task list

---

### 5. Content Card (Single Article/Paper)
**What**: ONE recommended article or paper with brief overview from Perplexity
**Shadcn**: Single Card with link
**APIs**: Perplexity API (already integrated!)
**Triggers**: Research/learning patterns, news-related keywords

**Note**: This is separate from ContentWriter (which generates 4-8 blog-style text cards). Content Card provides ONE focused "deep dive" recommendation.

**Example**:
```json
{
  "component_type": "content-card",
  "title": "Recommended Deep Dive",
  "subtitle": "For your AI research interest",
  "article_title": "Attention Is All You Need Revisited",
  "overview": "A comprehensive analysis of transformer architectures five years after the original paper. Covers recent improvements in attention mechanisms, positional encoding advances, and practical implementation insights from real-world deployments.",
  "url": "https://arxiv.org/abs/2304.xxxxx",
  "source_name": "arXiv",
  "published_date": "2025-01-10",
  "pattern_source": "AI Research Enthusiast",
  "search_query": "latest transformer architecture improvements 2025"
}
```

**When to use**:
- Persona `content_depth_preference: "deep_dives"` → Content card
- Keywords: "research", "article", "news", "paper", "study"
- High confidence patterns (>0.8) → Priority for content card
- ONE focused resource for deep reading, not a list

---

### 6. Interactive Map
**What**: Visual map showing locations of interest
**Shadcn**: Custom component with Mapbox GL JS
**APIs**: Mapbox API + Geocoding
**Triggers**: 2+ location keywords, travel, events

**Example**:
```json
{
  "component_type": "map-card",
  "title": "Your Travel Destinations",
  "subtitle": "Places you've been exploring",
  "center_lat": 31.6295,
  "center_lng": -7.9811,
  "zoom": 6,
  "style": "streets",
  "markers": [
    {
      "lat": 31.6295,
      "lng": -7.9811,
      "label": "Marrakech",
      "description": "Explored 12 times",
      "icon": "location-dot",
      "color": "#FF5533"
    },
    {
      "lat": 34.0181,
      "lng": -5.0078,
      "label": "Fez",
      "description": "Historical city",
      "icon": "location-dot",
      "color": "#FF5533"
    }
  ],
  "pattern_source": "Morocco Travel Planner",
  "data_source": "geocoding_api"
}
```

**When to use**:
- Multiple location keywords (2+) → Map view
- Travel/trip patterns → Destination map
- Event patterns with locations → Event map
- Restaurant/venue searches → Local map

---

## API Integrations

| API | Purpose | Free Tier | Cost |
|-----|---------|-----------|------|
| **OpenWeatherMap** | Weather data | 60 calls/min, 1M/month | Free |
| **YouTube Data v3** | Video discovery | 10,000 units/day | Free |
| **Eventbrite** | Event search | Varies | Free |
| **Mapbox** | Maps + geocoding | 50k loads/month | Free |

All APIs have generous free tiers sufficient for MVP demos.

---

## Intelligence Layer: How the LLM Decides

### Input to UI Generator

```python
{
    "patterns": [
        {
            "title": "Morocco Travel Planner",
            "keywords": ["morocco", "travel", "marrakech", "fez", "desert"],
            "confidence": 0.87,
            "interaction_count": 45,
            "description": "Researching destinations, watching vlogs"
        }
    ],
    "persona": {
        "interests": ["travel", "photography", "culture"],
        "activity_level": "high",
        "content_depth_preference": "balanced",
        "tone_preference": "casual and conversational"
    }
}
```

### LLM Reasoning Process

The UI Generator LLM analyzes:
1. **Keywords** → Identify locations, topics, action verbs
2. **Confidence** → Prioritize high-confidence patterns (>0.75)
3. **Persona preferences** → Match component complexity to user
4. **Pattern type** → Map pattern intent to component type

**Example reasoning**:
> "Pattern 'Morocco Travel Planner' contains:
> - Locations: 'morocco', 'marrakech', 'fez' (3 cities) → **Map component** + **Weather**
> - Intent: 'travel', 'planning' → **Task list** for trip checklist
> - High engagement (45 interactions) → **Video feed** for vlogs
> - Confidence 0.87 (high) → **Content feed** for travel guides
>
> Selected: Map, Weather, Task List, Video Feed (4 components)"

### Component Selection Rules

```python
"""
For each pattern, choose 0-2 relevant components from:

1. **info-card**: Real-time data (weather, stats)
   - Required when: Keywords contain cities/countries
   - Optional when: Trackable metrics (stocks, crypto)

2. **video-feed**: YouTube videos
   - Use when: Keywords like "tutorial", "guide", "how to"
   - Use when: Visual/entertainment topics

3. **event-calendar**: Eventbrite events
   - Use when: Keywords "conference", "event", "meetup"
   - Use when: Professional patterns

4. **task-list**: Interactive checklists
   - Use when: Planning/organizing patterns
   - Use when: Keywords "todo", "checklist", "project"

5. **content-card**: ONE recommended article/paper
   - Use when: Research/news patterns
   - Use when: Deep-dive content preference
   - Provides single focused resource, not a list

6. **map-card**: Interactive map
   - Required when: 2+ location keywords
   - Use when: Travel, events, venues

## Global Rules:
- Generate 3-6 total components across all patterns
- Prioritize high-confidence patterns (>0.75)
- Consider persona preferences (activity_level, content_depth_preference)
- Each pattern can spawn 0-2 components
- Map + Weather = common combo for location patterns
- No duplicate component types unless intentional
"""
```

---

## Data Flow Architecture

```python
# 1. Pattern Detection (existing)
patterns = pattern_detector.detect_patterns(user_data)

# 2. Component Selection (LLM)
component_configs = ui_generator.select_components(
    patterns=patterns.patterns,
    persona=patterns.persona
)
# Returns: List of component configs (no API data yet)

# 3. API Enrichment (parallel API calls)
enriched_components = await api_enricher.enrich(component_configs)
# For each component:
#   - info-card → Fetch weather from OpenWeatherMap
#   - video-feed → Search YouTube API
#   - event-calendar → Search Eventbrite API
#   - map-card → Geocode locations via Mapbox
#   - content-card → Search Perplexity API (ONE article)
#   - task-list → No API (generate items from LLM)

# 4. Return to Dashboard
return Dashboard(
    cards=content_cards,
    components=enriched_components,
    ...
)
```

---

## File Structure

```
fabric_dashboard/
├── core/
│   ├── pattern_detector.py         (existing)
│   ├── content_writer.py            (existing)
│   ├── ui_generator.py              (NEW - LLM component selection)
│   ├── api_enricher.py              (NEW - API data fetching)
│   └── dashboard_builder.py         (update - wire in ui_generator)
├── models/
│   └── schemas.py                   (update - add 6 component schemas)
├── clients/
│   ├── weather_client.py            (NEW - OpenWeatherMap)
│   ├── youtube_client.py            (NEW - YouTube API)
│   ├── eventbrite_client.py         (NEW - Eventbrite API)
│   └── mapbox_client.py             (NEW - Mapbox + geocoding)
└── tests/
    ├── test_ui_generator.py         (NEW)
    ├── test_api_enricher.py         (NEW)
    └── test_clients.py              (NEW)
```

---

## Component Schemas (Pydantic)

```python
# In schemas.py

from typing import Literal, Optional
from pydantic import BaseModel, Field

# Base component
class UIComponent(BaseModel):
    component_type: str
    title: str = Field(min_length=1, max_length=150)
    subtitle: Optional[str] = Field(None, max_length=200)
    pattern_source: str  # Which pattern generated this

# 1. Info Card
class InfoCardItem(BaseModel):
    label: str
    value: str
    icon: str  # lucide-react icon name

class InfoCard(UIComponent):
    component_type: Literal["info-card"]
    items: list[InfoCardItem] = Field(min_length=1, max_length=8)
    data_source: str  # "weather_api", "stock_api", etc.

# 2. Video Feed
class VideoItem(BaseModel):
    title: str
    thumbnail_url: str
    video_url: str
    channel: str
    duration: str
    views: Optional[str]

class VideoFeed(UIComponent):
    component_type: Literal["video-feed"]
    items: list[VideoItem] = Field(min_length=1, max_length=5)
    search_query: str

# 3. Event Calendar
class CalendarEvent(BaseModel):
    name: str
    date: str  # ISO format
    location: str
    venue: Optional[str]
    url: str
    is_free: bool
    price: Optional[str]

class EventCalendar(UIComponent):
    component_type: Literal["event-calendar"]
    events: list[CalendarEvent] = Field(min_length=1, max_length=10)
    search_query: str

# 4. Task List
class TaskItem(BaseModel):
    id: str
    content: str
    checked: bool = False
    priority: Literal["low", "medium", "high"] = "medium"

class TaskList(UIComponent):
    component_type: Literal["task-list"]
    items: list[TaskItem] = Field(min_length=1, max_length=15)
    allow_editing: bool = True
    allow_reordering: bool = True

# 5. Content Card (Single Article)
class ContentCard(UIComponent):
    component_type: Literal["content-card"]
    article_title: str = Field(min_length=1, max_length=200)
    overview: str = Field(min_length=50, max_length=300)  # Brief 2-3 sentence summary
    url: str
    source_name: str
    published_date: Optional[str]
    search_query: str  # For Perplexity API

# 6. Map Card
class MapMarker(BaseModel):
    lat: float
    lng: float
    label: str
    description: Optional[str]
    icon: str = "location-dot"
    color: str = "#FF5533"

class MapCard(UIComponent):
    component_type: Literal["map-card"]
    center_lat: float
    center_lng: float
    zoom: int = Field(ge=1, le=20, default=10)
    style: Literal["streets", "satellite", "outdoors"] = "streets"
    markers: list[MapMarker] = Field(min_length=1, max_length=20)
    data_source: str = "geocoding_api"

# Union type for all components
UIComponentType = InfoCard | VideoFeed | EventCalendar | TaskList | ContentCard | MapCard
```

---

## Success Criteria

### MVP Complete When:
- ✅ UI Generator selects appropriate components for patterns
- ✅ All 6 component types can be generated
- ✅ API enrichment works for at least 3 component types
- ✅ Components included in dashboard JSON output
- ✅ Frontend renders at least 3 component types
- ✅ Demo flow works end-to-end with real data

### Stretch Goals:
- 🎯 All 6 component types render in frontend
- 🎯 All 4 APIs integrated and working
- 🎯 Interactive features (checkable tasks, draggable cards)
- 🎯 Error handling + graceful fallbacks
- 🎯 Component caching for API efficiency

---

## Common Pattern → Component Mappings

| Pattern Type | Likely Components |
|--------------|-------------------|
| **Travel** | Map, Weather, Task List, Video Feed |
| **Events/Conferences** | Event Calendar, Map, Content Card |
| **Learning/Tutorial** | Video Feed, Content Card, Task List |
| **Research** | Content Card, Video Feed |
| **Planning** | Task List, Event Calendar |
| **Local Discovery** | Map, Event Calendar, Content Card |
| **Fitness** | Weather (outdoor), Task List, Video Feed |

---

## Example: Morocco Travel Pattern

**Input Pattern**:
```python
Pattern(
    title="Morocco Travel Planner",
    keywords=["morocco", "marrakech", "fez", "sahara", "travel", "riad"],
    confidence=0.87,
    interaction_count=45
)
```

**LLM Selects**:
1. Map (3 cities → geographic visualization)
2. Weather (Marrakech → current conditions)
3. Video Feed (travel vlogs)
4. Task List (trip planning checklist)
5. Content Card (ONE travel guide article)

**API Enrichment**:
- Map: Geocode "Marrakech" → (31.63°N, 7.98°W)
- Weather: Fetch from OpenWeatherMap → 24°C, Clear
- Video: Search YouTube "morocco travel vlog" → 5 videos
- Task: Generate checklist items → "Book flights", "Reserve riad"
- Content: Search Perplexity → ONE comprehensive Morocco travel guide

**Result**: 5 fully populated, interactive components

---

## Resources

**APIs**:
- [OpenWeatherMap](https://openweathermap.org/api)
- [YouTube Data API v3](https://developers.google.com/youtube/v3)
- [Eventbrite API](https://www.eventbrite.com/platform/api)
- [Mapbox GL JS](https://docs.mapbox.com/mapbox-gl-js/api/)
- [Mapbox Geocoding](https://docs.mapbox.com/api/search/geocoding/)

**Frontend**:
- [shadcn/ui](https://ui.shadcn.com/)
- [Lucide React Icons](https://lucide.dev/)
- [Mapbox GL JS React](https://visgl.github.io/react-map-gl/)

**Backend**:
- [Pydantic V2](https://docs.pydantic.dev/latest/)
- [LangChain Structured Output](https://python.langchain.com/docs/how_to/structured_output/)

---

## Next Steps

See `ROADMAP.md` for step-by-step implementation guide for junior developers.
