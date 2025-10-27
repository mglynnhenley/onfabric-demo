# Widget Layer Implementation Roadmap

## Executive Summary

This roadmap prioritizes implementing 3 high-impact widgets for an impressive demo, followed by a clear path to expand the system. The focus is on widgets that:
1. Look visually stunning
2. Demonstrate pattern-awareness
3. Require minimal external dependencies
4. Work well with existing data

**Timeline**: 5-7 days for MVP demo-ready implementation

---

## Phase 1: Foundation (Day 1) 🏗️

### Goals
- Set up core infrastructure for widget system
- Establish patterns for widget generation
- No actual widgets yet, just the framework

### Tasks

#### 1.1 Update Data Models (`schemas.py`)

```python
# Add to schemas.py

class WidgetType(str, Enum):
    """Available widget types."""
    MAP = "map"
    GALLERY = "gallery"
    CHECKLIST = "checklist"
    CLOCK = "clock"
    TIMELINE = "timeline"
    CHART = "chart"
    QUOTE = "quote"
    WEATHER = "weather"
    MUSIC = "music"
    FEED = "feed"

class WidgetConfig(BaseModel):
    """Base configuration for widgets."""
    display_mode: str = "default"
    interactive: bool = True
    auto_refresh: bool = False
    theme_override: Optional[dict[str, str]] = None

class WidgetData(BaseModel):
    """Complete widget specification."""
    widget_type: WidgetType
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=300)
    config: dict[str, Any] = Field(default_factory=dict)
    data: dict[str, Any] = Field(default_factory=dict)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class WidgetCard(BaseModel):
    """Card containing a widget instead of markdown content."""
    title: str = Field(min_length=1, max_length=150)
    description: str = Field(min_length=1, max_length=300)
    widget: WidgetData
    size: CardSize = CardSize.MEDIUM  # Default to medium
    pattern_title: str
    confidence: float = Field(ge=0.0, le=1.0, default=1.0)
```

#### 1.2 Create Widget Generator Module

```bash
mkdir -p fabric_dashboard/core/widgets
touch fabric_dashboard/core/widgets/__init__.py
touch fabric_dashboard/core/widgets/base.py
touch fabric_dashboard/core/widget_generator.py
```

**File**: `fabric_dashboard/core/widgets/base.py`

```python
"""Base widget class for all widget types."""

from abc import ABC, abstractmethod
from typing import Any, Optional

from fabric_dashboard.models.schemas import Pattern, PersonaProfile, WidgetData, WidgetType


class BaseWidget(ABC):
    """Abstract base class for all widgets."""
    
    widget_type: WidgetType
    
    @abstractmethod
    def can_generate(self, pattern: Pattern, persona: PersonaProfile) -> float:
        """
        Determine if this widget is appropriate for the pattern.
        
        Returns:
            Relevance score 0.0-1.0, where 0.0 = not relevant, 1.0 = perfect match
        """
        pass
    
    @abstractmethod
    def generate_widget_data(
        self, 
        pattern: Pattern, 
        persona: PersonaProfile,
        mock_mode: bool = False
    ) -> WidgetData:
        """
        Generate widget data for the given pattern.
        
        Args:
            pattern: The pattern to generate a widget for
            persona: User's persona profile
            mock_mode: If True, generate mock data instead of API calls
            
        Returns:
            Complete WidgetData specification
        """
        pass
    
    def _calculate_relevance(self, pattern: Pattern, keywords: list[str]) -> float:
        """
        Helper to calculate pattern relevance based on keyword matches.
        
        Args:
            pattern: Pattern to check
            keywords: List of relevant keywords for this widget type
            
        Returns:
            Relevance score 0.0-1.0
        """
        # Check pattern keywords
        pattern_keywords = [k.lower() for k in pattern.keywords]
        matches = sum(1 for k in keywords if k.lower() in pattern_keywords)
        
        # Check pattern title
        title_matches = sum(1 for k in keywords if k.lower() in pattern.title.lower())
        
        # Check pattern description
        desc_matches = sum(1 for k in keywords if k.lower() in pattern.description.lower())
        
        # Weight and normalize
        total_score = (matches * 1.0) + (title_matches * 0.5) + (desc_matches * 0.3)
        max_possible = len(keywords) * 1.8
        
        return min(total_score / max_possible, 1.0) if max_possible > 0 else 0.0
```

**File**: `fabric_dashboard/core/widget_generator.py`

```python
"""Widget generator that creates interactive UI components from patterns."""

from typing import Optional

from fabric_dashboard.models.schemas import (
    Pattern,
    PersonaProfile,
    WidgetCard,
    CardSize,
)
from fabric_dashboard.core.widgets.base import BaseWidget
from fabric_dashboard.utils import logger


class WidgetGenerator:
    """Generates pattern-aware interactive widgets."""
    
    def __init__(self, mock_mode: bool = False):
        """
        Initialize widget generator.
        
        Args:
            mock_mode: If True, generate mock widgets instead of using APIs
        """
        self.mock_mode = mock_mode
        self.widget_types: list[BaseWidget] = []
        self._register_widgets()
    
    def _register_widgets(self):
        """Register all available widget types."""
        # Will populate as we implement widgets
        # from fabric_dashboard.core.widgets.map_widget import MapWidget
        # self.widget_types.append(MapWidget())
        pass
    
    def generate_widgets(
        self,
        patterns: list[Pattern],
        persona: PersonaProfile,
        max_widgets: int = 2
    ) -> list[WidgetCard]:
        """
        Generate widget cards from patterns.
        
        Strategy:
        1. For each pattern, score relevance with each widget type
        2. Select top pattern-widget pairings
        3. Generate widget data
        4. Return as WidgetCard objects
        
        Args:
            patterns: List of detected patterns
            persona: User persona
            max_widgets: Maximum number of widgets to generate (0-3)
            
        Returns:
            List of WidgetCard objects (0-max_widgets)
        """
        if not self.widget_types:
            logger.warning("No widget types registered yet")
            return []
        
        if max_widgets == 0:
            return []
        
        logger.info(f"Generating up to {max_widgets} widgets from {len(patterns)} patterns")
        
        # Score all pattern-widget combinations
        candidates = []
        for pattern in patterns:
            for widget_type in self.widget_types:
                relevance = widget_type.can_generate(pattern, persona)
                if relevance > 0.3:  # Threshold for consideration
                    candidates.append({
                        'pattern': pattern,
                        'widget_type': widget_type,
                        'relevance': relevance,
                        'combined_score': relevance * pattern.confidence
                    })
        
        # Sort by combined score (relevance × pattern confidence)
        candidates.sort(key=lambda x: x['combined_score'], reverse=True)
        
        # Generate top N widgets
        widget_cards = []
        for candidate in candidates[:max_widgets]:
            try:
                widget_data = candidate['widget_type'].generate_widget_data(
                    candidate['pattern'],
                    persona,
                    self.mock_mode
                )
                
                # Determine card size based on widget type
                size = self._determine_card_size(candidate['widget_type'])
                
                widget_card = WidgetCard(
                    title=widget_data.title,
                    description=widget_data.description,
                    widget=widget_data,
                    size=size,
                    pattern_title=candidate['pattern'].title,
                    confidence=candidate['pattern'].confidence
                )
                
                widget_cards.append(widget_card)
                logger.success(f"Generated {widget_data.widget_type.value} widget for pattern: {candidate['pattern'].title}")
                
            except Exception as e:
                logger.error(f"Failed to generate widget: {e}")
                continue
        
        return widget_cards
    
    def _determine_card_size(self, widget_type: BaseWidget) -> CardSize:
        """Determine appropriate card size for widget type."""
        # Most widgets look good in MEDIUM, but maps and galleries benefit from LARGE
        large_widgets = ['map', 'gallery', 'timeline']
        
        if widget_type.widget_type.value in large_widgets:
            return CardSize.LARGE
        else:
            return CardSize.MEDIUM
```

**Estimated Time**: 3-4 hours

---

## Phase 2: First Widget - Interactive Map (Day 2) 🗺️

### Why Map First?
- Most visually impressive
- Works great with travel patterns (common in user data)
- Uses free, stable Leaflet.js library (no API keys needed)
- Immediate "wow" factor

### Tasks

#### 2.1 Implement Map Widget Logic

**File**: `fabric_dashboard/core/widgets/map_widget.py`

```python
"""Interactive map widget for location-based patterns."""

from typing import Optional
import re

from fabric_dashboard.models.schemas import Pattern, PersonaProfile, WidgetData, WidgetType
from fabric_dashboard.core.widgets.base import BaseWidget
from fabric_dashboard.utils import logger


class MapWidget(BaseWidget):
    """Generates interactive maps for travel/location patterns."""
    
    widget_type = WidgetType.MAP
    
    # Common location keywords
    LOCATION_KEYWORDS = [
        'travel', 'trip', 'visit', 'destination', 'city', 'country',
        'beach', 'mountain', 'island', 'tour', 'explore', 'journey',
        'vacation', 'holiday', 'adventure', 'flight', 'hotel'
    ]
    
    def can_generate(self, pattern: Pattern, persona: PersonaProfile) -> float:
        """Check if pattern is suitable for a map widget."""
        return self._calculate_relevance(pattern, self.LOCATION_KEYWORDS)
    
    def generate_widget_data(
        self,
        pattern: Pattern,
        persona: PersonaProfile,
        mock_mode: bool = False
    ) -> WidgetData:
        """Generate map widget data."""
        
        if mock_mode:
            return self._generate_mock_map(pattern)
        else:
            # TODO: Use LLM to extract locations and coordinates
            return self._generate_mock_map(pattern)
    
    def _generate_mock_map(self, pattern: Pattern) -> WidgetData:
        """Generate mock map data for testing."""
        
        # Default Mediterranean travel example
        markers = [
            {
                'lat': 37.9838,
                'lng': 23.7275,
                'label': 'Athens',
                'description': 'Explored ancient history & local cuisine',
                'color': '#2E86AB',
                'icon': 'pin'
            },
            {
                'lat': 36.3932,
                'lng': 25.4615,
                'label': 'Santorini',
                'description': 'Sunset photography paradise',
                'color': '#F18F01',
                'icon': 'pin'
            },
            {
                'lat': 35.3387,
                'lng': 25.1442,
                'label': 'Crete',
                'description': 'Next destination on your list',
                'color': '#C73E1D',
                'icon': 'pin'
            }
        ]
        
        # Calculate center point
        avg_lat = sum(m['lat'] for m in markers) / len(markers)
        avg_lng = sum(m['lng'] for m in markers) / len(markers)
        
        return WidgetData(
            widget_type=WidgetType.MAP,
            title=f"Your {pattern.title} Journey",
            description=f"Mapping your adventures from {pattern.description[:50]}...",
            config={
                'center': {'lat': avg_lat, 'lng': avg_lng},
                'zoom': 6,
                'theme': 'light'
            },
            data={
                'markers': markers,
                'show_routes': True
            }
        )
```

#### 2.2 Add Map Rendering to Dashboard Builder

**File**: `fabric_dashboard/core/dashboard_builder.py` (additions)

```python
# Add to _build_cards_grid method

def _build_card(self, card: Union[CardContent, WidgetCard], idx: int) -> str:
    """Build card HTML (either content or widget)."""
    
    # Check if this is a widget card
    if isinstance(card, WidgetCard):
        return self._build_widget_card(card, idx)
    else:
        return self._build_content_card(card, idx)

def _build_widget_card(self, widget_card: WidgetCard, idx: int) -> str:
    """Build HTML for a widget card."""
    
    widget_type = widget_card.widget.widget_type
    
    if widget_type == WidgetType.MAP:
        return self._render_map_widget(widget_card, idx)
    else:
        # Fallback to placeholder
        return self._render_widget_placeholder(widget_card, idx)

def _render_map_widget(self, widget_card: WidgetCard, idx: int) -> str:
    """Render interactive map widget."""
    
    widget = widget_card.widget
    map_id = f"map-{idx}"
    
    # Extract markers for JavaScript
    markers_js = self._generate_map_markers_js(widget.data.get('markers', []))
    center = widget.config.get('center', {'lat': 0, 'lng': 0})
    zoom = widget.config.get('zoom', 4)
    
    return f"""<div class="dashboard-card widget-card map-card" data-card-index="{idx}">
        <div class="p-6">
            <div class="widget-header mb-4">
                <h2 class="text-xl font-semibold text-[var(--foreground)]">{widget.title}</h2>
                <p class="text-sm text-[var(--foreground)] opacity-70 mt-1">{widget.description}</p>
            </div>
            
            <div id="{map_id}" class="map-container" style="height: 400px; border-radius: 8px; overflow: hidden;"></div>
            
            <div class="widget-footer mt-4">
                <p class="text-xs text-[var(--foreground)] opacity-60">
                    📍 {len(widget.data.get('markers', []))} destinations • Based on "{widget_card.pattern_title}"
                </p>
            </div>
        </div>
        
        <script>
            // Initialize map after Leaflet loads
            if (typeof L !== 'undefined') {{
                const map_{idx} = L.map('{map_id}').setView([{center['lat']}, {center['lng']}], {zoom});
                
                // Add tile layer
                L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                    attribution: '© OpenStreetMap contributors',
                    maxZoom: 18,
                }}).addTo(map_{idx});
                
                // Add markers
                {markers_js}
            }}
        </script>
    </div>"""

def _generate_map_markers_js(self, markers: list[dict]) -> str:
    """Generate JavaScript code for map markers."""
    
    js_lines = []
    for i, marker in enumerate(markers):
        js_lines.append(f"""
        L.marker([{marker['lat']}, {marker['lng']}])
            .addTo(map_{i})
            .bindPopup('<b>{marker['label']}</b><br>{marker['description']}');
        """)
    
    return "\n".join(js_lines)

# Add Leaflet CSS/JS to _build_head method
def _build_head(self, title: str, color_scheme: ColorScheme) -> str:
    """Build HTML head with Leaflet for maps."""
    
    # ... existing head content ...
    
    # Add before closing </head>:
    leaflet_includes = """
    <!-- Leaflet.js for maps -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    """
```

#### 2.3 Register Map Widget

Update `widget_generator.py`:

```python
def _register_widgets(self):
    """Register all available widget types."""
    from fabric_dashboard.core.widgets.map_widget import MapWidget
    self.widget_types.append(MapWidget())
```

**Estimated Time**: 4-5 hours

---

## Phase 3: Second Widget - Image Gallery (Day 3) 🎨

### Why Gallery Second?
- High visual impact
- Works with fashion, design, art patterns
- Can use free Unsplash API (50 requests/hour)
- Demonstrates API integration

### Tasks

#### 3.1 Add Unsplash Integration

```bash
pip install requests
```

**File**: `fabric_dashboard/utils/image_api.py`

```python
"""Image API integration for gallery widgets."""

import requests
from typing import Optional
from fabric_dashboard.utils.config import get_config
from fabric_dashboard.utils import logger


class UnsplashClient:
    """Client for Unsplash API."""
    
    BASE_URL = "https://api.unsplash.com"
    
    def __init__(self, access_key: Optional[str] = None):
        self.access_key = access_key or self._get_api_key()
    
    def _get_api_key(self) -> str:
        """Get API key from config."""
        config = get_config()
        return getattr(config, 'unsplash_api_key', None) or 'DEMO_KEY'
    
    def search_photos(self, query: str, per_page: int = 9) -> list[dict]:
        """
        Search for photos on Unsplash.
        
        Args:
            query: Search query
            per_page: Number of results (max 30)
            
        Returns:
            List of photo data dicts
        """
        try:
            response = requests.get(
                f"{self.BASE_URL}/search/photos",
                params={
                    'query': query,
                    'per_page': per_page,
                    'orientation': 'squarish'
                },
                headers={'Authorization': f'Client-ID {self.access_key}'},
                timeout=10
            )
            
            if response.status_code == 200:
                results = response.json().get('results', [])
                return [self._format_photo(photo) for photo in results]
            else:
                logger.warning(f"Unsplash API error: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Failed to fetch Unsplash photos: {e}")
            return []
    
    def _format_photo(self, photo: dict) -> dict:
        """Format Unsplash photo data."""
        return {
            'url': photo['urls']['regular'],
            'thumbnail': photo['urls']['small'],
            'caption': photo.get('description') or photo.get('alt_description', ''),
            'credit': f"Photo by {photo['user']['name']}",
            'credit_url': photo['user']['links']['html'],
            'dominant_color': photo.get('color', '#cccccc')
        }
```

#### 3.2 Implement Gallery Widget

**File**: `fabric_dashboard/core/widgets/gallery_widget.py`

```python
"""Image gallery widget for visual interests."""

from fabric_dashboard.models.schemas import Pattern, PersonaProfile, WidgetData, WidgetType
from fabric_dashboard.core.widgets.base import BaseWidget
from fabric_dashboard.utils.image_api import UnsplashClient
from fabric_dashboard.utils import logger


class GalleryWidget(BaseWidget):
    """Generates image galleries for visual patterns."""
    
    widget_type = WidgetType.GALLERY
    
    VISUAL_KEYWORDS = [
        'fashion', 'style', 'design', 'art', 'photography',
        'aesthetic', 'visual', 'outfit', 'interior', 'architecture',
        'decor', 'beauty', 'makeup', 'hair', 'accessories'
    ]
    
    def __init__(self):
        self.unsplash = UnsplashClient()
    
    def can_generate(self, pattern: Pattern, persona: PersonaProfile) -> float:
        """Check if pattern is suitable for gallery widget."""
        return self._calculate_relevance(pattern, self.VISUAL_KEYWORDS)
    
    def generate_widget_data(
        self,
        pattern: Pattern,
        persona: PersonaProfile,
        mock_mode: bool = False
    ) -> WidgetData:
        """Generate gallery widget data."""
        
        if mock_mode:
            return self._generate_mock_gallery(pattern)
        
        # Generate search query from pattern
        search_query = self._generate_search_query(pattern, persona)
        
        # Fetch images from Unsplash
        images = self.unsplash.search_photos(search_query, per_page=9)
        
        if not images:
            logger.warning(f"No images found for query: {search_query}")
            return self._generate_mock_gallery(pattern)
        
        return WidgetData(
            widget_type=WidgetType.GALLERY,
            title=f"{pattern.title} Inspiration",
            description=f"Visual exploration of {pattern.description[:60]}...",
            config={
                'layout': 'masonry',
                'columns': 3,
                'enable_lightbox': True
            },
            data={
                'images': images,
                'search_query': search_query
            }
        )
    
    def _generate_search_query(self, pattern: Pattern, persona: PersonaProfile) -> str:
        """Generate Unsplash search query from pattern."""
        # Use pattern keywords and interests
        keywords = pattern.keywords[:3]  # Top 3 keywords
        return ' '.join(keywords)
    
    def _generate_mock_gallery(self, pattern: Pattern) -> WidgetData:
        """Generate mock gallery with placeholder images."""
        
        # Use placeholders for demo
        mock_images = [
            {
                'url': f'https://picsum.photos/400/400?random={i}',
                'thumbnail': f'https://picsum.photos/200/200?random={i}',
                'caption': f'Inspiration {i+1}',
                'credit': 'Lorem Picsum',
                'credit_url': 'https://picsum.photos',
                'dominant_color': '#e8d5c4'
            }
            for i in range(9)
        ]
        
        return WidgetData(
            widget_type=WidgetType.GALLERY,
            title=f"{pattern.title} Gallery",
            description=pattern.description[:100],
            config={'layout': 'grid', 'columns': 3},
            data={'images': mock_images}
        )
```

#### 3.3 Add Gallery Rendering

Add to `dashboard_builder.py`:

```python
def _build_widget_card(self, widget_card: WidgetCard, idx: int) -> str:
    """Build HTML for widget card."""
    
    widget_type = widget_card.widget.widget_type
    
    if widget_type == WidgetType.MAP:
        return self._render_map_widget(widget_card, idx)
    elif widget_type == WidgetType.GALLERY:
        return self._render_gallery_widget(widget_card, idx)
    else:
        return self._render_widget_placeholder(widget_card, idx)

def _render_gallery_widget(self, widget_card: WidgetCard, idx: int) -> str:
    """Render image gallery widget."""
    
    widget = widget_card.widget
    images = widget.data.get('images', [])
    
    # Build image grid HTML
    images_html = []
    for i, img in enumerate(images[:9]):  # Max 9 images
        images_html.append(f"""
        <div class="gallery-item" data-index="{i}">
            <img src="{img['thumbnail']}" alt="{img['caption']}" 
                 class="gallery-image" loading="lazy"
                 data-full-url="{img['url']}">
            <div class="gallery-caption">
                <p class="text-xs">{img['caption'][:50]}</p>
            </div>
        </div>
        """)
    
    return f"""<div class="dashboard-card widget-card gallery-card" data-card-index="{idx}">
        <div class="p-6">
            <div class="widget-header mb-4">
                <h2 class="text-xl font-semibold text-[var(--foreground)]">{widget.title}</h2>
                <p class="text-sm text-[var(--foreground)] opacity-70 mt-1">{widget.description}</p>
            </div>
            
            <div class="gallery-grid">
                {''.join(images_html)}
            </div>
            
            <div class="widget-footer mt-4">
                <p class="text-xs text-[var(--foreground)] opacity-60">
                    📸 {len(images)} images • Based on "{widget_card.pattern_title}"
                </p>
            </div>
        </div>
    </div>
    
    <style>
        .gallery-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0.5rem;
        }}
        
        .gallery-item {{
            position: relative;
            aspect-ratio: 1;
            overflow: hidden;
            border-radius: 8px;
            cursor: pointer;
            transition: transform 0.2s;
        }}
        
        .gallery-item:hover {{
            transform: scale(1.05);
        }}
        
        .gallery-image {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}
        
        .gallery-caption {{
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: linear-gradient(to top, rgba(0,0,0,0.7), transparent);
            color: white;
            padding: 0.5rem;
            opacity: 0;
            transition: opacity 0.2s;
        }}
        
        .gallery-item:hover .gallery-caption {{
            opacity: 1;
        }}
    </style>
    """
```

**Estimated Time**: 4-5 hours

---

## Phase 4: Third Widget - Interactive Checklist (Day 4) ✅

### Why Checklist Third?
- Demonstrates interactivity and state management
- Works well with learning/goal patterns
- No external APIs needed
- Users can actually interact with it

### Tasks

#### 4.1 Implement Checklist Widget

**File**: `fabric_dashboard/core/widgets/checklist_widget.py`

```python
"""Interactive checklist widget for learning/goal patterns."""

from fabric_dashboard.models.schemas import Pattern, PersonaProfile, WidgetData, WidgetType
from fabric_dashboard.core.widgets.base import BaseWidget


class ChecklistWidget(BaseWidget):
    """Generates interactive checklists for learning patterns."""
    
    widget_type = WidgetType.CHECKLIST
    
    LEARNING_KEYWORDS = [
        'learn', 'learning', 'tutorial', 'guide', 'how to',
        'course', 'lesson', 'practice', 'skill', 'goal',
        'training', 'study', 'master', 'improve', 'develop'
    ]
    
    def can_generate(self, pattern: Pattern, persona: PersonaProfile) -> float:
        """Check if pattern is suitable for checklist widget."""
        return self._calculate_relevance(pattern, self.LEARNING_KEYWORDS)
    
    def generate_widget_data(
        self,
        pattern: Pattern,
        persona: PersonaProfile,
        mock_mode: bool = False
    ) -> WidgetData:
        """Generate checklist widget data."""
        
        # For MVP, always use mock data (could use LLM later)
        return self._generate_mock_checklist(pattern)
    
    def _generate_mock_checklist(self, pattern: Pattern) -> WidgetData:
        """Generate mock checklist based on pattern."""
        
        # Extract topic from pattern title
        topic = pattern.title.replace("Learning", "").replace("Journey", "").strip()
        
        # Generate relevant tasks
        tasks = [
            {
                'id': '1',
                'text': f'Research {topic} fundamentals',
                'completed': True,
                'priority': 'high',
                'notes': 'Found great resources online'
            },
            {
                'id': '2',
                'text': f'Practice {topic.lower()} basics',
                'completed': False,
                'priority': 'high',
                'notes': 'Start with beginner tutorials'
            },
            {
                'id': '3',
                'text': f'Join {topic.lower()} community',
                'completed': False,
                'priority': 'medium',
                'notes': ''
            },
            {
                'id': '4',
                'text': f'Complete first {topic.lower()} project',
                'completed': False,
                'priority': 'medium',
                'notes': ''
            }
        ]
        
        completed_count = sum(1 for t in tasks if t['completed'])
        progress = int((completed_count / len(tasks)) * 100)
        
        return WidgetData(
            widget_type=WidgetType.CHECKLIST,
            title=f"Your {topic} Journey",
            description=f"Track your progress as you {pattern.description[:50].lower()}...",
            config={
                'allow_editing': True,
                'show_progress': True
            },
            data={
                'items': tasks,
                'progress_percentage': progress,
                'category': topic.lower()
            }
        )
```

#### 4.2 Add Checklist Rendering

Add to `dashboard_builder.py`:

```python
def _render_checklist_widget(self, widget_card: WidgetCard, idx: int) -> str:
    """Render interactive checklist widget."""
    
    widget = widget_card.widget
    items = widget.data.get('items', [])
    progress = widget.data.get('progress_percentage', 0)
    checklist_id = f"checklist-{idx}"
    
    # Build checklist items HTML
    items_html = []
    for item in items:
        checked = 'checked' if item['completed'] else ''
        priority_color = {
            'high': 'text-red-600',
            'medium': 'text-yellow-600',
            'low': 'text-green-600'
        }.get(item['priority'], 'text-gray-600')
        
        items_html.append(f"""
        <div class="checklist-item p-3 border-b border-[var(--border)] hover:bg-[var(--card)] transition">
            <div class="flex items-start gap-3">
                <input type="checkbox" {checked} 
                       class="checklist-checkbox mt-1" 
                       data-item-id="{item['id']}"
                       onchange="updateChecklistProgress('{checklist_id}')">
                <div class="flex-1">
                    <p class="text-sm font-medium {'line-through opacity-50' if item['completed'] else ''}">{item['text']}</p>
                    {f'<p class="text-xs text-[var(--muted)] mt-1">💬 {item["notes"]}</p>' if item['notes'] else ''}
                </div>
                <span class="text-xs {priority_color} font-semibold">{item['priority'].upper()}</span>
            </div>
        </div>
        """)
    
    return f"""<div class="dashboard-card widget-card checklist-card" data-card-index="{idx}">
        <div class="p-6">
            <div class="widget-header mb-4">
                <h2 class="text-xl font-semibold text-[var(--foreground)]">{widget.title}</h2>
                <p class="text-sm text-[var(--foreground)] opacity-70 mt-1">{widget.description}</p>
            </div>
            
            <div class="progress-bar mb-4">
                <div class="flex justify-between items-center mb-2">
                    <span class="text-sm font-medium">Progress</span>
                    <span class="text-sm font-bold" id="{checklist_id}-progress">{progress}%</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-[var(--primary)] h-2 rounded-full transition-all duration-300" 
                         id="{checklist_id}-bar"
                         style="width: {progress}%"></div>
                </div>
            </div>
            
            <div id="{checklist_id}" class="checklist-items border border-[var(--border)] rounded-lg overflow-hidden">
                {''.join(items_html)}
            </div>
        </div>
        
        <script>
            function updateChecklistProgress(checklistId) {{
                const container = document.getElementById(checklistId);
                const checkboxes = container.querySelectorAll('.checklist-checkbox');
                const total = checkboxes.length;
                const checked = Array.from(checkboxes).filter(cb => cb.checked).length;
                const progress = Math.round((checked / total) * 100);
                
                document.getElementById(checklistId + '-progress').textContent = progress + '%';
                document.getElementById(checklistId + '-bar').style.width = progress + '%';
                
                // Save to localStorage
                const state = Array.from(checkboxes).map(cb => ({{
                    id: cb.dataset.itemId,
                    checked: cb.checked
                }}));
                localStorage.setItem(checklistId, JSON.stringify(state));
            }}
            
            // Restore from localStorage on load
            (function() {{
                const checklistId = '{checklist_id}';
                const saved = localStorage.getItem(checklistId);
                if (saved) {{
                    const state = JSON.parse(saved);
                    state.forEach(item => {{
                        const checkbox = document.querySelector(`[data-item-id="${{item.id}}"]`);
                        if (checkbox) checkbox.checked = item.checked;
                    }});
                    updateChecklistProgress(checklistId);
                }}
            }})();
        </script>
    </div>"""
```

**Estimated Time**: 3-4 hours

---

## Phase 5: Integration & Polish (Day 5) 🎨

### Tasks

#### 5.1 Update Main Orchestration

**File**: `fabric_dashboard/commands/generate.py` (or main orchestration file)

```python
# Add widget generation to main flow

from fabric_dashboard.core.widget_generator import WidgetGenerator

# In generate_dashboard function:

# After pattern detection and content generation:
widget_generator = WidgetGenerator(mock_mode=mock_mode)
widget_cards = widget_generator.generate_widgets(
    patterns=patterns,
    persona=persona,
    max_widgets=2  # Generate 2 widgets for demo
)

# Combine content cards and widget cards
all_cards = content_cards + widget_cards

# Pass to dashboard builder
dashboard = dashboard_builder.build(
    cards=all_cards,
    persona=persona,
    color_scheme=color_scheme,
    ...
)
```

#### 5.2 Add Styling Polish

Update CSS in `dashboard_builder.py`:

```css
/* Widget-specific styles */
.widget-card {
    position: relative;
}

.widget-header {
    border-bottom: 1px solid var(--border);
    padding-bottom: 1rem;
}

.map-container {
    border: 1px solid var(--border);
}

.gallery-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: 0.5rem;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .map-container {
        height: 300px !important;
    }
    
    .gallery-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}
```

#### 5.3 Testing

- Test with real user data
- Test with multiple patterns
- Test responsive behavior
- Test widget interactivity

**Estimated Time**: 4-5 hours

---

## Phase 6: Additional Widgets (Days 6-7) - Post-MVP

After the core 3 widgets are working, prioritize:

1. **Clock Widget** - Quick to implement, good for global patterns
2. **Timeline Widget** - Great for trip planning patterns
3. **Chart Widget** - Use Chart.js for data visualization

---

## Success Metrics

### MVP Demo Success Criteria

1. ✅ At least 2 widgets generated per dashboard
2. ✅ Widgets match pattern relevance (no random generation)
3. ✅ Interactive elements work (map pan/zoom, gallery lightbox, checklist state)
4. ✅ Responsive on mobile/tablet
5. ✅ Visually impressive and cohesive with existing design
6. ✅ No console errors or broken functionality

### Technical Success Criteria

1. ✅ Widget system is extensible (easy to add new widget types)
2. ✅ Fallback behavior works (if widget fails, show content card)
3. ✅ Performance impact minimal (< 500ms additional load time)
4. ✅ Code is testable and maintainable

---

## Risk Mitigation

### Risk: External APIs Fail
**Mitigation**: Always provide mock fallback data

### Risk: Widgets Don't Match Patterns Well
**Mitigation**: Conservative relevance thresholds (0.3+)

### Risk: Performance Issues
**Mitigation**: Lazy load widget JS, limit to 2-3 widgets max

### Risk: Design Inconsistency
**Mitigation**: Use existing color scheme variables, consistent spacing

---

## Future Enhancements (Post-Demo)

1. **LLM-Generated Widget Data**: Use Claude to extract locations, generate tasks, etc.
2. **User Customization**: Allow users to configure widgets
3. **Widget Persistence**: Save user interactions across sessions
4. **More Widget Types**: Weather, music, quotes, etc.
5. **Widget Marketplace**: Community-contributed widgets
6. **Real-time Widgets**: Live data updates

---

## Resource Requirements

### External Libraries (Free Tier)
- Leaflet.js (CDN, free)
- Unsplash API (50 requests/hour free)
- Chart.js (CDN, free)

### Python Packages
```
# Add to requirements.txt
requests>=2.31.0  # For API calls
```

### Configuration
```python
# Add to Config model in schemas.py
unsplash_api_key: Optional[str] = Field(None, description="Unsplash API key for galleries")
```

---

## Next Steps

1. **Day 1**: Implement foundation (schemas, base classes)
2. **Day 2**: Build and test Map Widget
3. **Day 3**: Build and test Gallery Widget
4. **Day 4**: Build and test Checklist Widget
5. **Day 5**: Integration, testing, polish
6. **Day 6-7**: Additional widgets if time permits

**Start with**: Creating the schema updates in `schemas.py`

Ready to begin implementation? 🚀

