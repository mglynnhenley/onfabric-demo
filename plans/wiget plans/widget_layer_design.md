# Dynamic UI Widget Layer - Design Document

## Overview

This document outlines the design for a **pattern-aware widget generation system** that creates interactive, visually compelling UI components based on detected user patterns. This moves beyond static markdown cards to create truly personalized, generative interfaces.

## Goals

1. **Pattern-to-Widget Mapping**: Intelligently determine which interactive components best represent each pattern
2. **Visual Interest**: Create visually striking, demo-worthy components that showcase the platform's capabilities
3. **Personalization**: Generate widget content that's specific to the user's actual patterns and data
4. **Extensibility**: Design a system that can easily accommodate new widget types
5. **Integration**: Seamlessly integrate widgets into the existing card-based dashboard layout

## Architecture

### New Modules

```
fabric_dashboard/core/
  ├── widget_generator.py      # Main widget generation orchestrator
  ├── widgets/
  │   ├── __init__.py
  │   ├── base.py              # Abstract base widget class
  │   ├── map_widget.py        # Interactive maps for location patterns
  │   ├── timeline_widget.py   # Event timelines
  │   ├── gallery_widget.py    # Image galleries with API integration
  │   ├── clock_widget.py      # World clocks for timezone patterns
  │   ├── checklist_widget.py  # Interactive to-do/learning lists
  │   ├── chart_widget.py      # Data visualizations
  │   ├── quote_widget.py      # Featured quotes/highlights
  │   ├── weather_widget.py    # Weather displays for location patterns
  │   └── music_widget.py      # Music player/recommendations
```

### Data Models (additions to schemas.py)

```python
class WidgetType(str, Enum):
    """Available widget types."""
    MAP = "map"
    TIMELINE = "timeline"
    GALLERY = "gallery"
    CLOCK = "clock"
    CHECKLIST = "checklist"
    CHART = "chart"
    QUOTE = "quote"
    WEATHER = "weather"
    MUSIC = "music"
    FEED = "feed"

class WidgetData(BaseModel):
    """Base widget data structure."""
    widget_type: WidgetType
    title: str
    config: dict[str, Any]  # Widget-specific configuration
    data: dict[str, Any]    # Widget-specific data
    style_hints: dict[str, str] = Field(default_factory=dict)  # CSS hints from theme

class WidgetCard(CardContent):
    """Card that contains an interactive widget instead of markdown."""
    widget: WidgetData
    # Inherits: title, description, size, etc.
```

## Widget Type Specifications

### 1. Map Widget (`map_widget.py`)

**When to Use**: Travel patterns, location-based searches, geographic interests

**Pattern Signals**:
- Keywords: travel, visit, trip, city, country, beach, mountain, destination
- Multiple location mentions
- Geographic search queries

**Data Structure**:
```python
{
  "widget_type": "map",
  "title": "Your Travel Footprint",
  "config": {
    "center": {"lat": 37.9838, "lng": 23.7275},  # Athens
    "zoom": 4,
    "theme": "light",  # or "dark", "satellite"
  },
  "data": {
    "markers": [
      {
        "lat": 37.9838,
        "lng": 23.7275,
        "label": "Athens",
        "description": "Explored ancient history",
        "color": "#FF5733",
        "icon": "pin"
      },
      {
        "lat": 36.3932,
        "lng": 25.4615,
        "label": "Santorini",
        "description": "Sunset photography",
        "color": "#2E86AB"
      }
    ],
    "routes": [  # Optional connecting lines
      {"from": [37.9838, 23.7275], "to": [36.3932, 25.4615]}
    ]
  }
}
```

**Rendering**: Uses Leaflet.js or Mapbox GL for interactive maps

---

### 2. World Clock Widget (`clock_widget.py`)

**When to Use**: Multi-timezone patterns, global collaboration, international travel

**Pattern Signals**:
- Multiple time zones mentioned
- International locations
- Keywords: timezone, time difference, GMT, UTC
- Remote work patterns

**Data Structure**:
```python
{
  "widget_type": "clock",
  "title": "Your Time Zones",
  "config": {
    "display_mode": "analog",  # or "digital", "both"
    "show_seconds": true,
    "format_24h": false
  },
  "data": {
    "clocks": [
      {
        "timezone": "Europe/Athens",
        "label": "Athens",
        "primary": true,
        "color": "#2E86AB"
      },
      {
        "timezone": "America/New_York",
        "label": "New York",
        "color": "#F18F01"
      },
      {
        "timezone": "Asia/Tokyo",
        "label": "Tokyo",
        "color": "#C73E1D"
      }
    ]
  }
}
```

**Rendering**: CSS animations for analog clocks, real-time JS updates

---

### 3. Image Gallery Widget (`gallery_widget.py`)

**When to Use**: Fashion, design, art, photography, visual interests

**Pattern Signals**:
- Keywords: fashion, style, design, photography, art, aesthetic
- Visual platform activity (Pinterest, Instagram)
- Image search queries

**Data Structure**:
```python
{
  "widget_type": "gallery",
  "title": "Mediterranean Fashion Inspiration",
  "config": {
    "layout": "masonry",  # or "grid", "carousel"
    "columns": 3,
    "image_fit": "cover",
    "enable_lightbox": true
  },
  "data": {
    "images": [
      {
        "url": "https://images.unsplash.com/photo-...",
        "thumbnail": "https://images.unsplash.com/photo-...",
        "caption": "Linen summer styles",
        "credit": "Unsplash",
        "credit_url": "https://unsplash.com/...",
        "dominant_color": "#E8D5C4"
      }
    ],
    "image_source": "unsplash",  # or "google_images", "pinterest"
    "search_query": "mediterranean summer fashion linen"
  }
}
```

**Rendering**: Masonry grid with lazy loading, lightbox overlay

**API Integration**: 
- Unsplash API (free tier: 50 requests/hour)
- Google Custom Search API (for Google Images)
- Pexels API (free alternative)

---

### 4. Checklist Widget (`checklist_widget.py`)

**When to Use**: Learning patterns, goal-setting, skill development, task-oriented behavior

**Pattern Signals**:
- Keywords: learn, tutorial, how to, guide, steps, course
- Educational content
- Project/goal-oriented searches

**Data Structure**:
```python
{
  "widget_type": "checklist",
  "title": "Your Surfing Learning Path",
  "config": {
    "allow_editing": true,
    "show_progress": true,
    "enable_notes": true
  },
  "data": {
    "items": [
      {
        "id": "1",
        "text": "Master pop-up technique",
        "completed": false,
        "priority": "high",
        "notes": "Practice on land first",
        "resources": ["https://youtube.com/..."]
      },
      {
        "id": "2",
        "text": "Learn to read wave patterns",
        "completed": false,
        "priority": "medium"
      },
      {
        "id": "3",
        "text": "Book beginner lessons in Taghazout",
        "completed": true,
        "priority": "high"
      }
    ],
    "progress_percentage": 33,
    "category": "surfing"
  }
}
```

**Rendering**: Interactive checkboxes with local storage persistence, progress bars

---

### 5. Timeline Widget (`timeline_widget.py`)

**When to Use**: Event-based patterns, chronological activities, trip planning

**Pattern Signals**:
- Temporal keywords: schedule, itinerary, planning, dates
- Series of dated events
- Trip planning searches

**Data Structure**:
```python
{
  "widget_type": "timeline",
  "title": "Your Mediterranean Journey",
  "config": {
    "orientation": "vertical",  # or "horizontal"
    "show_dates": true,
    "interactive": true
  },
  "data": {
    "events": [
      {
        "date": "2025-09-15",
        "title": "Arrived in Santorini",
        "description": "First sunset at Oia",
        "icon": "✈️",
        "color": "#2E86AB",
        "image": "https://..."
      },
      {
        "date": "2025-09-18",
        "title": "Athens Exploration",
        "description": "Acropolis & local cuisine",
        "icon": "🏛️",
        "color": "#F18F01"
      }
    ]
  }
}
```

**Rendering**: Vertical timeline with scroll animations, expandable sections

---

### 6. Chart Widget (`chart_widget.py`)

**When to Use**: Data analysis patterns, metrics, quantitative interests

**Pattern Signals**:
- Keywords: data, statistics, metrics, trends, analysis
- Quantitative searches
- Technical/analytical persona

**Data Structure**:
```python
{
  "widget_type": "chart",
  "title": "Your Activity Trends",
  "config": {
    "chart_type": "line",  # or "bar", "pie", "radar"
    "height": 300,
    "interactive": true,
    "show_legend": true
  },
  "data": {
    "labels": ["Travel", "Food", "Photography", "Surfing", "Culture"],
    "datasets": [
      {
        "label": "Interest Level",
        "data": [95, 78, 82, 65, 88],
        "backgroundColor": "#2E86AB",
        "borderColor": "#1A5F7A"
      }
    ]
  }
}
```

**Rendering**: Chart.js or D3.js for interactive charts

---

### 7. Weather Widget (`weather_widget.py`)

**When to Use**: Outdoor activity patterns, travel destinations, location-specific interests

**Pattern Signals**:
- Outdoor activity keywords: surf, hike, beach, ski
- Specific destination searches
- Weather-dependent activities

**Data Structure**:
```python
{
  "widget_type": "weather",
  "title": "Surf Conditions",
  "config": {
    "display_mode": "detailed",  # or "compact"
    "show_forecast": true,
    "unit": "metric"
  },
  "data": {
    "locations": [
      {
        "name": "Taghazout, Morocco",
        "current": {
          "temp": 22,
          "condition": "Sunny",
          "wind_speed": 15,
          "wind_direction": "NW",
          "wave_height": 1.2,
          "icon": "☀️"
        },
        "forecast": [
          {"day": "Tomorrow", "temp": 23, "condition": "Clear", "wave_height": 1.5}
        ]
      }
    ]
  }
}
```

**Rendering**: Card with icons, animations, forecast slider

**API Integration**: OpenWeather API (free tier) or Weather.gov

---

### 8. Quote Widget (`quote_widget.py`)

**When to Use**: Philosophical patterns, literary interests, inspirational content

**Pattern Signals**:
- Keywords: quotes, philosophy, inspiration, wisdom
- Literary or reflective content
- Thoughtful persona

**Data Structure**:
```python
{
  "widget_type": "quote",
  "title": "Today's Inspiration",
  "config": {
    "style": "minimal",  # or "decorative", "card"
    "auto_rotate": false,
    "show_attribution": true
  },
  "data": {
    "quotes": [
      {
        "text": "The world is a book, and those who do not travel read only one page.",
        "author": "Saint Augustine",
        "context": "Travel philosophy",
        "background_image": "https://...",
        "text_position": "center"
      }
    ]
  }
}
```

**Rendering**: Large typography, optional background images, fade animations

---

### 9. Music Widget (`music_widget.py`)

**When to Use**: Music patterns, playlist creation, audio interests

**Pattern Signals**:
- Keywords: music, playlist, song, artist, genre
- Spotify/Apple Music activity
- Audio-related searches

**Data Structure**:
```python
{
  "widget_type": "music",
  "title": "Your Mediterranean Vibes",
  "config": {
    "auto_play": false,
    "show_controls": true,
    "enable_shuffle": true
  },
  "data": {
    "playlist": {
      "name": "Greek Summer",
      "description": "Inspired by your travels",
      "tracks": [
        {
          "title": "Island Vibes",
          "artist": "Sample Artist",
          "duration": "3:45",
          "preview_url": "https://...",
          "album_art": "https://..."
        }
      ],
      "embed_url": "https://open.spotify.com/embed/..."
    }
  }
}
```

**Rendering**: Spotify/Apple Music embeds or custom audio player

---

### 10. Feed Widget (`feed_widget.py`)

**When to Use**: Social patterns, community engagement, content aggregation

**Pattern Signals**:
- Social media activity
- Community participation keywords
- Following/engagement patterns

**Data Structure**:
```python
{
  "widget_type": "feed",
  "title": "Travel Community Highlights",
  "config": {
    "max_items": 5,
    "auto_refresh": false,
    "show_avatars": true
  },
  "data": {
    "items": [
      {
        "author": "Travel Enthusiast",
        "avatar": "https://...",
        "content": "Just discovered an amazing hidden beach in Crete!",
        "timestamp": "2 hours ago",
        "platform": "instagram",
        "engagement": {"likes": 245, "comments": 12}
      }
    ]
  }
}
```

**Rendering**: Social media-style feed cards with interactions

---

## Widget Generator Implementation

### Core Logic (`widget_generator.py`)

```python
class WidgetGenerator:
    """Generates interactive widgets based on patterns."""
    
    def __init__(self, mock_mode: bool = False):
        self.mock_mode = mock_mode
        self.widget_registry = self._initialize_widget_registry()
    
    def generate_widgets(
        self, 
        patterns: list[Pattern],
        persona: PersonaProfile,
        color_scheme: ColorScheme,
        max_widgets: int = 3
    ) -> list[WidgetCard]:
        """
        Generate 0-3 widget cards based on patterns.
        
        Strategy:
        1. Analyze patterns to determine best widget matches
        2. Score each pattern-widget pairing
        3. Select top N widget candidates
        4. Generate widget data using LLM + APIs
        5. Return WidgetCard objects
        """
        
    def _match_pattern_to_widget(self, pattern: Pattern) -> list[WidgetType]:
        """
        Determine which widget types best represent a pattern.
        Returns list of widget types sorted by relevance.
        """
        
    def _generate_widget_data(
        self,
        widget_type: WidgetType,
        pattern: Pattern,
        persona: PersonaProfile
    ) -> WidgetData:
        """Generate specific widget data using LLM and APIs."""
```

### Pattern-to-Widget Mapping Strategy

```python
PATTERN_WIDGET_MAPPING = {
    # Location-based patterns
    "travel": [WidgetType.MAP, WidgetType.TIMELINE, WidgetType.WEATHER],
    "location": [WidgetType.MAP, WidgetType.CLOCK, WidgetType.WEATHER],
    
    # Visual/Creative patterns
    "fashion": [WidgetType.GALLERY, WidgetType.QUOTE],
    "design": [WidgetType.GALLERY, WidgetType.CHART],
    "photography": [WidgetType.GALLERY, WidgetType.MAP],
    "art": [WidgetType.GALLERY, WidgetType.QUOTE],
    
    # Learning/Goal patterns
    "learning": [WidgetType.CHECKLIST, WidgetType.TIMELINE],
    "tutorial": [WidgetType.CHECKLIST, WidgetType.TIMELINE],
    "course": [WidgetType.CHECKLIST, WidgetType.CHART],
    
    # Social patterns
    "community": [WidgetType.FEED, WidgetType.QUOTE],
    "social": [WidgetType.FEED, WidgetType.TIMELINE],
    
    # Data/Analysis patterns
    "data": [WidgetType.CHART, WidgetType.TIMELINE],
    "metrics": [WidgetType.CHART],
    "analytics": [WidgetType.CHART],
    
    # Music/Audio patterns
    "music": [WidgetType.MUSIC, WidgetType.QUOTE],
    "playlist": [WidgetType.MUSIC],
    
    # Time/Schedule patterns
    "schedule": [WidgetType.TIMELINE, WidgetType.CHECKLIST],
    "planning": [WidgetType.TIMELINE, WidgetType.CHECKLIST, WidgetType.MAP],
}
```

## LLM Integration for Widget Generation

### Prompt Structure

```python
system_prompt = """You are a specialized UI component designer who generates data for interactive widgets.

Given a user pattern, you will generate realistic, personalized data for a specific widget type.

Rules:
1. All data must be relevant to the pattern and user persona
2. Use realistic values, locations, dates that align with the pattern
3. Be creative but grounded in the user's actual interests
4. For location data: use real coordinates
5. For images: provide search queries that will work with image APIs
6. For dates: use realistic timeframes
7. Ensure data is demo-worthy - visually interesting and compelling

Return valid JSON matching the widget data schema."""

human_prompt = """Generate widget data for:

Widget Type: {widget_type}
Pattern: {pattern_title}
Pattern Description: {pattern_description}
Keywords: {pattern_keywords}

User Persona:
- Interests: {persona_interests}
- Activity Level: {persona_activity_level}
- Writing Style: {persona_writing_style}

Generate complete widget data that would look impressive in a demo."""
```

## Dashboard Builder Integration

### Updated Card Generation

```python
class DashboardBuilder:
    
    def build(
        self,
        cards: list[CardContent],
        persona: PersonaProfile,
        color_scheme: ColorScheme,
        widgets: list[WidgetCard] = None,  # NEW
        ...
    ) -> Dashboard:
        """Build dashboard with both content cards and widget cards."""
        
        # Merge and sort cards
        all_cards = cards + (widgets or [])
        
        # Interleave widgets with content cards for visual variety
        final_cards = self._arrange_cards(all_cards)
        
        # Generate HTML with widget rendering
        html = self._generate_html(final_cards, ...)
```

### Widget Rendering in HTML

Each widget type will have a dedicated HTML/JS renderer:

```python
def _render_widget_card(self, widget_card: WidgetCard) -> str:
    """Render a widget card with interactive component."""
    
    widget_type = widget_card.widget.widget_type
    
    if widget_type == WidgetType.MAP:
        return self._render_map_widget(widget_card)
    elif widget_type == WidgetType.CLOCK:
        return self._render_clock_widget(widget_card)
    # ... etc
    
def _render_map_widget(self, widget_card: WidgetCard) -> str:
    """Render interactive map using Leaflet.js."""
    
    widget = widget_card.widget
    
    return f"""
    <div class="dashboard-card">
        <div id="map-{widget_card.id}" class="map-container"></div>
        <script>
            // Leaflet.js initialization
            const map = L.map('map-{widget_card.id}').setView(
                [{widget.config['center']['lat']}, {widget.config['center']['lng']}],
                {widget.config['zoom']}
            );
            
            // Add markers
            {self._generate_map_markers_js(widget.data['markers'])}
        </script>
    </div>
    """
```

## External Dependencies

### JavaScript Libraries (CDN)

```html
<!-- Maps -->
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<!-- Charts -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.js"></script>

<!-- Image Gallery -->
<script src="https://unpkg.com/masonry-layout@4.2.2/dist/masonry.pkgd.min.js"></script>

<!-- Animations -->
<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
```

### Python API Integrations

```python
# requirements.txt additions
unsplash-python==1.1.0  # Image gallery
openweather-python==0.2.1  # Weather data
spotipy==2.23.0  # Music data (optional)
```

## Demo Strategy

### Phase 1: Core Widgets (MVP for Demo)
1. **Map Widget** - Most visually impressive, works well with travel patterns
2. **Gallery Widget** - Shows image generation capability
3. **Checklist Widget** - Interactive, demonstrates personalization

### Phase 2: Enhanced Widgets
4. Clock Widget
5. Timeline Widget
6. Chart Widget

### Phase 3: Advanced Widgets
7. Weather Widget (API dependent)
8. Music Widget (API dependent)
9. Quote Widget
10. Feed Widget

## Implementation Phases

### Phase 1: Foundation (Days 1-2)
- [ ] Add widget data models to `schemas.py`
- [ ] Create `widget_generator.py` with pattern matching logic
- [ ] Create `widgets/base.py` with abstract Widget class
- [ ] Implement `WidgetType` enum and mapping dictionary

### Phase 2: Core Widgets (Days 3-4)
- [ ] Implement Map Widget (data generation + rendering)
- [ ] Implement Gallery Widget with Unsplash integration
- [ ] Implement Checklist Widget
- [ ] Add widget rendering to `dashboard_builder.py`

### Phase 3: Integration (Day 5)
- [ ] Update main orchestration to call widget generator
- [ ] Add widget cards to dashboard assembly
- [ ] Test with real user data
- [ ] Style polish and animations

### Phase 4: Additional Widgets (Days 6-7)
- [ ] Implement Clock Widget
- [ ] Implement Timeline Widget
- [ ] Implement Chart Widget
- [ ] Add more pattern-to-widget mappings

## Success Metrics

1. **Visual Impact**: Widgets significantly enhance dashboard aesthetics
2. **Relevance**: Generated widgets accurately reflect user patterns
3. **Interactivity**: Widgets are functional and engaging
4. **Performance**: Dashboard loads in < 3 seconds with widgets
5. **Demo Quality**: Dashboard impresses stakeholders and users

## Future Enhancements

1. **Widget Customization**: Allow users to configure widgets
2. **Widget Persistence**: Save widget states to local storage
3. **More Widget Types**: AR/VR previews, 3D visualizations, video widgets
4. **Real-time Data**: Live updating widgets (stock prices, social feeds)
5. **Widget Marketplace**: Community-contributed widget types
6. **AI-Generated Widget Types**: LLM proposes entirely new widget concepts

## Technical Considerations

### Performance
- Lazy load widget JavaScript
- Use intersection observer for off-screen widgets
- Optimize image loading with thumbnails
- Implement widget caching

### Accessibility
- Ensure keyboard navigation for all widgets
- Add ARIA labels
- Provide text alternatives for visual widgets
- Maintain color contrast ratios

### Error Handling
- Graceful fallback if widget fails to load
- Alternative static content if API calls fail
- Clear error messages in mock mode

### Testing
- Unit tests for each widget generator
- Integration tests for widget rendering
- Visual regression testing
- Performance benchmarks

---

## Conclusion

This widget layer transforms the dashboard from a static content display into a dynamic, personalized interface that adapts to user patterns. The system is designed to be extensible, visually impressive, and demo-ready while maintaining the existing architecture's elegance and simplicity.

The key innovation is using pattern analysis to intelligently select and populate widgets, creating a unique dashboard for each user that feels both personal and professionally designed.

