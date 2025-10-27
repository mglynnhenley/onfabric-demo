# Widget Data Schemas - JSON Interface Specification

## Overview

This document defines the **JSON data schemas** for all widget types. These schemas serve as:

1. **LLM Generation Contracts** - What data to generate for each widget
2. **Validation Schemas** - Pydantic models to validate data
3. **Rendering Props** - What the frontend expects
4. **Documentation** - Clear interface for each widget type

## Schema Structure

Each widget data schema follows this pattern:

```json
{
  "widget_type": "map|gallery|checklist|clock|timeline|chart|quote|weather|music|feed",
  "title": "Widget display title",
  "description": "Widget subtitle/description",
  "config": {
    // Widget-specific configuration (display preferences)
  },
  "data": {
    // Widget-specific data (actual content to display)
  }
}
```

---

## 1. Map Widget Schema

### Purpose
Display interactive maps with markers for location-based patterns (travel, geography).

### JSON Schema

```json
{
  "widget_type": "map",
  "title": "Your Travel Footprint",
  "description": "Mapping your recent Mediterranean adventures",
  "config": {
    "center": {
      "lat": 37.9838,
      "lng": 23.7275
    },
    "zoom": 6,
    "theme": "light",
    "enable_clustering": false,
    "show_routes": true
  },
  "data": {
    "markers": [
      {
        "lat": 37.9838,
        "lng": 23.7275,
        "label": "Athens",
        "description": "Explored ancient history & local cuisine",
        "color": "#2E86AB",
        "icon": "pin",
        "timestamp": "2025-09-18T14:20:00Z"
      },
      {
        "lat": 36.3932,
        "lng": 25.4615,
        "label": "Santorini",
        "description": "Sunset photography paradise",
        "color": "#F18F01",
        "icon": "pin",
        "timestamp": "2025-09-15T19:45:00Z"
      }
    ],
    "routes": [
      {
        "from": [37.9838, 23.7275],
        "to": [36.3932, 25.4615],
        "color": "#2E86AB",
        "style": "dashed"
      }
    ],
    "metadata": {
      "total_destinations": 2,
      "distance_km": 280,
      "date_range": "Sep 2025"
    }
  }
}
```

### TypeScript Interface (for reference)

```typescript
interface MapWidgetData {
  widget_type: "map";
  title: string;
  description: string;
  config: {
    center: { lat: number; lng: number };
    zoom: number;
    theme: "light" | "dark" | "satellite";
    enable_clustering?: boolean;
    show_routes?: boolean;
  };
  data: {
    markers: Array<{
      lat: number;
      lng: number;
      label: string;
      description: string;
      color?: string;
      icon?: "pin" | "star" | "circle";
      timestamp?: string;
    }>;
    routes?: Array<{
      from: [number, number];
      to: [number, number];
      color?: string;
      style?: "solid" | "dashed" | "dotted";
    }>;
    metadata?: {
      total_destinations?: number;
      distance_km?: number;
      date_range?: string;
    };
  };
}
```

### LLM Generation Prompt Template

```
Generate map widget data for a user with the following pattern:
Pattern: {pattern_title}
Keywords: {pattern_keywords}
Description: {pattern_description}

Extract or infer geographic locations mentioned in the pattern.
For each location:
- Find accurate lat/lng coordinates
- Create a descriptive label
- Write a brief description of what they did/plan there
- Assign a color from the user's theme

Return JSON matching this schema:
{schema}
```

---

## 2. Gallery Widget Schema

### Purpose
Display image galleries for visual interests (fashion, design, art, photography).

### JSON Schema

```json
{
  "widget_type": "gallery",
  "title": "Mediterranean Summer Style",
  "description": "Fashion inspiration from your interests",
  "config": {
    "layout": "masonry",
    "columns": 3,
    "image_fit": "cover",
    "enable_lightbox": true,
    "lazy_load": true
  },
  "data": {
    "images": [
      {
        "url": "https://images.unsplash.com/photo-...",
        "thumbnail": "https://images.unsplash.com/photo-...?w=400",
        "caption": "Linen summer dress styles",
        "alt_text": "Mediterranean summer fashion",
        "credit": "Photo by Jane Doe",
        "credit_url": "https://unsplash.com/@janedoe",
        "dominant_color": "#E8D5C4",
        "aspect_ratio": 1.0
      },
      {
        "url": "https://images.unsplash.com/photo-...",
        "thumbnail": "https://images.unsplash.com/photo-...?w=400",
        "caption": "Beach cover-ups and accessories",
        "alt_text": "Beach fashion accessories",
        "credit": "Photo by John Smith",
        "credit_url": "https://unsplash.com/@johnsmith",
        "dominant_color": "#C4D5E8",
        "aspect_ratio": 1.5
      }
    ],
    "metadata": {
      "total_images": 9,
      "source": "unsplash",
      "search_query": "mediterranean summer linen fashion"
    }
  }
}
```

### TypeScript Interface

```typescript
interface GalleryWidgetData {
  widget_type: "gallery";
  title: string;
  description: string;
  config: {
    layout: "masonry" | "grid" | "carousel";
    columns: number;
    image_fit: "cover" | "contain";
    enable_lightbox?: boolean;
    lazy_load?: boolean;
  };
  data: {
    images: Array<{
      url: string;
      thumbnail: string;
      caption: string;
      alt_text: string;
      credit?: string;
      credit_url?: string;
      dominant_color?: string;
      aspect_ratio?: number;
    }>;
    metadata?: {
      total_images?: number;
      source?: string;
      search_query?: string;
    };
  };
}
```

### LLM Generation Prompt Template

```
Generate gallery widget data for a user with this pattern:
Pattern: {pattern_title}
Keywords: {pattern_keywords}
Description: {pattern_description}

Create a search query that would find relevant images on Unsplash.
The query should combine:
- Main topic from pattern
- Visual style preferences
- Specific aesthetic details

For this demo, generate 9 image placeholders with:
- Descriptive captions
- Relevant alt text
- Appropriate aspect ratios

Return JSON matching this schema:
{schema}

Note: The actual URLs will be fetched from Unsplash API using your search_query.
```

---

## 3. Checklist Widget Schema

### Purpose
Interactive to-do lists for learning, goals, and task-oriented patterns.

### JSON Schema

```json
{
  "widget_type": "checklist",
  "title": "Your Surfing Journey",
  "description": "Track your progress as you learn",
  "config": {
    "allow_editing": true,
    "show_progress": true,
    "enable_notes": true,
    "enable_reordering": true,
    "persist_state": true
  },
  "data": {
    "items": [
      {
        "id": "1",
        "text": "Book beginner surf lessons in Taghazout",
        "completed": true,
        "priority": "high",
        "notes": "Found great camp with 5★ reviews",
        "resources": [
          {
            "title": "Taghazout Surf Camp Reviews",
            "url": "https://..."
          }
        ],
        "due_date": "2025-10-01",
        "category": "booking"
      },
      {
        "id": "2",
        "text": "Master the pop-up technique",
        "completed": false,
        "priority": "high",
        "notes": "Practice on land first, watch tutorial",
        "resources": [
          {
            "title": "Pop-up Tutorial Video",
            "url": "https://youtube.com/..."
          }
        ],
        "due_date": null,
        "category": "skill"
      },
      {
        "id": "3",
        "text": "Learn to read wave patterns",
        "completed": false,
        "priority": "medium",
        "notes": "Study swell direction and timing",
        "resources": [],
        "due_date": null,
        "category": "skill"
      }
    ],
    "metadata": {
      "total_tasks": 3,
      "completed_tasks": 1,
      "progress_percentage": 33,
      "category": "surfing",
      "estimated_completion": "2 weeks"
    }
  }
}
```

### TypeScript Interface

```typescript
interface ChecklistWidgetData {
  widget_type: "checklist";
  title: string;
  description: string;
  config: {
    allow_editing?: boolean;
    show_progress?: boolean;
    enable_notes?: boolean;
    enable_reordering?: boolean;
    persist_state?: boolean;
  };
  data: {
    items: Array<{
      id: string;
      text: string;
      completed: boolean;
      priority: "high" | "medium" | "low";
      notes?: string;
      resources?: Array<{
        title: string;
        url: string;
      }>;
      due_date?: string | null;
      category?: string;
    }>;
    metadata?: {
      total_tasks?: number;
      completed_tasks?: number;
      progress_percentage?: number;
      category?: string;
      estimated_completion?: string;
    };
  };
}
```

### LLM Generation Prompt Template

```
Generate checklist widget data for a learning/goal pattern:
Pattern: {pattern_title}
Keywords: {pattern_keywords}
Description: {pattern_description}

Create 4-6 actionable tasks that represent a logical learning path or goal progression.
Tasks should:
- Be specific and actionable
- Progress from basics to advanced
- Include realistic priorities
- Have helpful notes or tips
- Reference real resources when possible

Order tasks in a logical sequence (prerequisites first).
Mark 1-2 early tasks as completed to show progress.

Return JSON matching this schema:
{schema}
```

---

## 4. Clock Widget Schema

### Purpose
Display world clocks for multi-timezone patterns (global collaboration, travel).

### JSON Schema

```json
{
  "widget_type": "clock",
  "title": "Your Time Zones",
  "description": "Stay synchronized across continents",
  "config": {
    "display_mode": "analog",
    "show_seconds": true,
    "format_24h": false,
    "auto_update": true,
    "highlight_current": true
  },
  "data": {
    "clocks": [
      {
        "timezone": "Europe/Athens",
        "label": "Athens",
        "city": "Athens",
        "country": "Greece",
        "emoji": "🇬🇷",
        "primary": true,
        "color": "#2E86AB"
      },
      {
        "timezone": "America/New_York",
        "label": "New York",
        "city": "New York",
        "country": "USA",
        "emoji": "🇺🇸",
        "primary": false,
        "color": "#F18F01"
      },
      {
        "timezone": "Asia/Tokyo",
        "label": "Tokyo",
        "city": "Tokyo",
        "country": "Japan",
        "emoji": "🇯🇵",
        "primary": false,
        "color": "#C73E1D"
      }
    ],
    "metadata": {
      "total_zones": 3,
      "max_difference_hours": 16,
      "user_timezone": "Europe/Athens"
    }
  }
}
```

### TypeScript Interface

```typescript
interface ClockWidgetData {
  widget_type: "clock";
  title: string;
  description: string;
  config: {
    display_mode: "analog" | "digital" | "both";
    show_seconds?: boolean;
    format_24h?: boolean;
    auto_update?: boolean;
    highlight_current?: boolean;
  };
  data: {
    clocks: Array<{
      timezone: string;
      label: string;
      city: string;
      country: string;
      emoji?: string;
      primary?: boolean;
      color?: string;
    }>;
    metadata?: {
      total_zones?: number;
      max_difference_hours?: number;
      user_timezone?: string;
    };
  };
}
```

### LLM Generation Prompt Template

```
Generate clock widget data for a multi-timezone pattern:
Pattern: {pattern_title}
Keywords: {pattern_keywords}
Description: {pattern_description}

Identify 2-4 relevant timezones based on:
- Locations mentioned in the pattern
- International collaboration indicators
- Travel destinations

For each timezone:
- Use IANA timezone identifier (e.g., "America/New_York")
- Include city/country for display
- Assign colors from theme
- Mark the most relevant as primary

Return JSON matching this schema:
{schema}
```

---

## 5. Timeline Widget Schema

### Purpose
Display chronological events for trip planning, project milestones, historical patterns.

### JSON Schema

```json
{
  "widget_type": "timeline",
  "title": "Your Mediterranean Journey",
  "description": "A chronological view of your adventures",
  "config": {
    "orientation": "vertical",
    "show_dates": true,
    "interactive": true,
    "show_images": true,
    "animate_scroll": true
  },
  "data": {
    "events": [
      {
        "id": "1",
        "date": "2025-09-15",
        "title": "Arrived in Santorini",
        "description": "First sunset views from Oia, beginning of Mediterranean adventure",
        "icon": "✈️",
        "color": "#2E86AB",
        "image": "https://images.unsplash.com/photo-...",
        "category": "travel",
        "completed": true
      },
      {
        "id": "2",
        "date": "2025-09-18",
        "title": "Athens Exploration",
        "description": "Visited Acropolis, discovered local cuisine gems",
        "icon": "🏛️",
        "color": "#F18F01",
        "image": "https://images.unsplash.com/photo-...",
        "category": "travel",
        "completed": true
      },
      {
        "id": "3",
        "date": "2025-09-20",
        "title": "Research Phase",
        "description": "Planning Morocco surf trip, comparing Taghazout vs Essaouira",
        "icon": "🔍",
        "color": "#C73E1D",
        "image": null,
        "category": "planning",
        "completed": true
      },
      {
        "id": "4",
        "date": "2025-10-15",
        "title": "Surf Lessons Begin",
        "description": "Start beginner surf camp in Taghazout",
        "icon": "🏄",
        "color": "#2D9D78",
        "image": null,
        "category": "activity",
        "completed": false
      }
    ],
    "metadata": {
      "total_events": 4,
      "completed_events": 3,
      "date_range": "Sep 15 - Oct 15, 2025",
      "duration_days": 30
    }
  }
}
```

### TypeScript Interface

```typescript
interface TimelineWidgetData {
  widget_type: "timeline";
  title: string;
  description: string;
  config: {
    orientation: "vertical" | "horizontal";
    show_dates?: boolean;
    interactive?: boolean;
    show_images?: boolean;
    animate_scroll?: boolean;
  };
  data: {
    events: Array<{
      id: string;
      date: string;
      title: string;
      description: string;
      icon?: string;
      color?: string;
      image?: string | null;
      category?: string;
      completed?: boolean;
    }>;
    metadata?: {
      total_events?: number;
      completed_events?: number;
      date_range?: string;
      duration_days?: number;
    };
  };
}
```

### LLM Generation Prompt Template

```
Generate timeline widget data for a chronological pattern:
Pattern: {pattern_title}
Keywords: {pattern_keywords}
Description: {pattern_description}
User interactions: {recent_interactions}

Create 4-6 timeline events that represent:
- Past events (completed = true)
- Current activities (completed = true/false)
- Future plans (completed = false)

Events should:
- Be in chronological order
- Have realistic dates
- Include descriptive text
- Use appropriate emoji icons
- Distinguish past/future with completed flag

Return JSON matching this schema:
{schema}
```

---

## 6. Chart Widget Schema

### Purpose
Visualize data for analytical patterns (metrics, comparisons, distributions).

### JSON Schema

```json
{
  "widget_type": "chart",
  "title": "Your Interest Landscape",
  "description": "Visualizing your digital footprint",
  "config": {
    "chart_type": "radar",
    "height": 300,
    "interactive": true,
    "show_legend": true,
    "animate": true,
    "responsive": true
  },
  "data": {
    "labels": ["Travel", "Photography", "Culture", "Surfing", "Food"],
    "datasets": [
      {
        "label": "Interest Level",
        "data": [95, 82, 80, 65, 78],
        "backgroundColor": "rgba(46, 134, 171, 0.2)",
        "borderColor": "#2E86AB",
        "borderWidth": 2,
        "pointBackgroundColor": "#2E86AB",
        "pointBorderColor": "#fff",
        "pointHoverBackgroundColor": "#fff",
        "pointHoverBorderColor": "#2E86AB"
      }
    ],
    "metadata": {
      "chart_type": "radar",
      "max_value": 100,
      "unit": "percentage",
      "top_category": "Travel",
      "total_categories": 5
    }
  }
}
```

### Alternative Chart Types

#### Bar Chart
```json
{
  "config": {
    "chart_type": "bar",
    "orientation": "vertical"
  },
  "data": {
    "labels": ["Mon", "Tue", "Wed", "Thu", "Fri"],
    "datasets": [
      {
        "label": "Activity Level",
        "data": [12, 19, 15, 22, 18],
        "backgroundColor": "#2E86AB"
      }
    ]
  }
}
```

#### Line Chart
```json
{
  "config": {
    "chart_type": "line",
    "fill": true
  },
  "data": {
    "labels": ["Jan", "Feb", "Mar", "Apr", "May"],
    "datasets": [
      {
        "label": "Engagement Trend",
        "data": [65, 72, 68, 85, 92],
        "borderColor": "#2E86AB",
        "backgroundColor": "rgba(46, 134, 171, 0.1)",
        "tension": 0.4
      }
    ]
  }
}
```

### TypeScript Interface

```typescript
interface ChartWidgetData {
  widget_type: "chart";
  title: string;
  description: string;
  config: {
    chart_type: "radar" | "bar" | "line" | "pie" | "doughnut";
    height?: number;
    interactive?: boolean;
    show_legend?: boolean;
    animate?: boolean;
    responsive?: boolean;
    orientation?: "vertical" | "horizontal";
    fill?: boolean;
  };
  data: {
    labels: string[];
    datasets: Array<{
      label: string;
      data: number[];
      backgroundColor?: string | string[];
      borderColor?: string;
      borderWidth?: number;
      tension?: number;
      [key: string]: any; // Chart.js specific options
    }>;
    metadata?: {
      chart_type?: string;
      max_value?: number;
      unit?: string;
      top_category?: string;
      total_categories?: number;
    };
  };
}
```

### LLM Generation Prompt Template

```
Generate chart widget data for an analytical pattern:
Pattern: {pattern_title}
Keywords: {pattern_keywords}
Pattern confidence: {pattern_confidence}
Related patterns: {other_patterns}

Create a visualization that shows:
- Relative strength of different interests/topics
- Distribution or comparison
- Trend over time (if temporal data available)

Choose appropriate chart type:
- Radar: Multi-dimensional comparison
- Bar: Category comparison
- Line: Trends over time
- Pie: Distribution/composition

Return JSON matching this schema:
{schema}
```

---

## 7. Quote Widget Schema

### Purpose
Display inspirational quotes for philosophical, literary, or motivational patterns.

### JSON Schema

```json
{
  "widget_type": "quote",
  "title": "Travel Wisdom",
  "description": "Inspiration for your journey",
  "config": {
    "style": "minimal",
    "font_size": "large",
    "show_attribution": true,
    "background_style": "gradient",
    "text_position": "center",
    "auto_rotate": false
  },
  "data": {
    "quotes": [
      {
        "text": "The world is a book, and those who do not travel read only one page.",
        "author": "Saint Augustine",
        "source": "Confessions",
        "context": "Travel philosophy",
        "background_image": "https://images.unsplash.com/photo-...",
        "background_color": "#2E86AB",
        "text_color": "#FFFFFF",
        "relevance": "Aligns with user's travel exploration pattern"
      }
    ],
    "metadata": {
      "theme": "travel",
      "mood": "inspirational",
      "related_pattern": "Mediterranean Travel"
    }
  }
}
```

### TypeScript Interface

```typescript
interface QuoteWidgetData {
  widget_type: "quote";
  title: string;
  description: string;
  config: {
    style?: "minimal" | "decorative" | "card";
    font_size?: "small" | "medium" | "large";
    show_attribution?: boolean;
    background_style?: "gradient" | "image" | "solid";
    text_position?: "left" | "center" | "right";
    auto_rotate?: boolean;
  };
  data: {
    quotes: Array<{
      text: string;
      author: string;
      source?: string;
      context?: string;
      background_image?: string;
      background_color?: string;
      text_color?: string;
      relevance?: string;
    }>;
    metadata?: {
      theme?: string;
      mood?: string;
      related_pattern?: string;
    };
  };
}
```

### LLM Generation Prompt Template

```
Generate quote widget data for this pattern:
Pattern: {pattern_title}
Keywords: {pattern_keywords}
Description: {pattern_description}
Persona tone: {persona_tone}

Find or create a quote that:
- Resonates with the pattern theme
- Matches the user's persona tone
- Is genuine and well-attributed
- Provides inspiration or insight

Explain why this quote is relevant to the user.

Return JSON matching this schema:
{schema}
```

---

## 8. Weather Widget Schema

### Purpose
Display weather/conditions for outdoor activity patterns (surfing, hiking, travel).

### JSON Schema

```json
{
  "widget_type": "weather",
  "title": "Surf Conditions - Taghazout",
  "description": "Perfect waves await",
  "config": {
    "display_mode": "detailed",
    "show_forecast": true,
    "units": "metric",
    "show_surf_data": true,
    "auto_refresh_minutes": 15
  },
  "data": {
    "locations": [
      {
        "name": "Taghazout, Morocco",
        "lat": 30.5479,
        "lng": -9.7089,
        "current": {
          "timestamp": "2025-10-14T12:00:00Z",
          "temp": 22,
          "feels_like": 21,
          "condition": "Sunny",
          "condition_code": "clear",
          "icon": "☀️",
          "humidity": 65,
          "wind_speed": 15,
          "wind_direction": "NW",
          "wind_direction_degrees": 315,
          "uv_index": 7,
          "visibility_km": 10
        },
        "surf": {
          "wave_height_m": 1.2,
          "wave_period_s": 12,
          "swell_direction": "NW",
          "tide": "rising",
          "tide_time": "14:30",
          "surf_rating": 4,
          "surf_rating_text": "Good"
        },
        "forecast": [
          {
            "date": "2025-10-15",
            "day_name": "Tomorrow",
            "temp_high": 23,
            "temp_low": 18,
            "condition": "Clear",
            "icon": "☀️",
            "wave_height_m": 1.5,
            "wind_speed": 12
          },
          {
            "date": "2025-10-16",
            "day_name": "Wednesday",
            "temp_high": 21,
            "temp_low": 17,
            "condition": "Partly Cloudy",
            "icon": "⛅",
            "wave_height_m": 1.3,
            "wind_speed": 18
          }
        ]
      }
    ],
    "metadata": {
      "last_updated": "2025-10-14T12:00:00Z",
      "source": "OpenWeather",
      "activity_recommendation": "Excellent conditions for beginner surfing"
    }
  }
}
```

### TypeScript Interface

```typescript
interface WeatherWidgetData {
  widget_type: "weather";
  title: string;
  description: string;
  config: {
    display_mode: "compact" | "detailed";
    show_forecast?: boolean;
    units: "metric" | "imperial";
    show_surf_data?: boolean;
    auto_refresh_minutes?: number;
  };
  data: {
    locations: Array<{
      name: string;
      lat: number;
      lng: number;
      current: {
        timestamp: string;
        temp: number;
        feels_like?: number;
        condition: string;
        condition_code: string;
        icon: string;
        humidity?: number;
        wind_speed: number;
        wind_direction: string;
        wind_direction_degrees?: number;
        uv_index?: number;
        visibility_km?: number;
      };
      surf?: {
        wave_height_m: number;
        wave_period_s?: number;
        swell_direction?: string;
        tide?: string;
        tide_time?: string;
        surf_rating?: number;
        surf_rating_text?: string;
      };
      forecast?: Array<{
        date: string;
        day_name: string;
        temp_high: number;
        temp_low: number;
        condition: string;
        icon: string;
        wave_height_m?: number;
        wind_speed?: number;
      }>;
    }>;
    metadata?: {
      last_updated?: string;
      source?: string;
      activity_recommendation?: string;
    };
  };
}
```

### LLM Generation Prompt Template

```
Generate weather widget data for an outdoor activity pattern:
Pattern: {pattern_title}
Keywords: {pattern_keywords}
Description: {pattern_description}

Identify the most relevant location for weather data.
If the pattern involves:
- Surfing → Include surf conditions (wave height, swell, wind)
- Hiking → Include UV index, precipitation
- General travel → Standard weather

For DEMO purposes, generate realistic mock weather data.
For PRODUCTION, this will use OpenWeather API.

Return JSON matching this schema:
{schema}
```

---

## 9. Music Widget Schema

### Purpose
Display playlists or music recommendations for audio/music patterns.

### JSON Schema

```json
{
  "widget_type": "music",
  "title": "Your Mediterranean Vibes",
  "description": "Soundtrack inspired by your travels",
  "config": {
    "display_mode": "playlist",
    "auto_play": false,
    "show_controls": true,
    "enable_shuffle": true,
    "theme": "dark"
  },
  "data": {
    "playlist": {
      "name": "Greek Summer",
      "description": "Inspired by your Mediterranean adventures",
      "image": "https://i.scdn.co/image/...",
      "provider": "spotify",
      "embed_url": "https://open.spotify.com/embed/playlist/...",
      "tracks": [
        {
          "id": "1",
          "title": "Mediterranean Breeze",
          "artist": "Sample Artist",
          "album": "Summer Sounds",
          "duration_seconds": 225,
          "duration_display": "3:45",
          "preview_url": "https://p.scdn.co/mp3-preview/...",
          "album_art": "https://i.scdn.co/image/...",
          "spotify_url": "https://open.spotify.com/track/..."
        },
        {
          "id": "2",
          "title": "Sunset in Santorini",
          "artist": "Island Collective",
          "album": "Aegean Dreams",
          "duration_seconds": 198,
          "duration_display": "3:18",
          "preview_url": "https://p.scdn.co/mp3-preview/...",
          "album_art": "https://i.scdn.co/image/...",
          "spotify_url": "https://open.spotify.com/track/..."
        }
      ],
      "total_tracks": 2,
      "total_duration_minutes": 7
    },
    "metadata": {
      "genre": "Mediterranean, Chillout, World",
      "mood": "Relaxed, Sunny, Nostalgic",
      "related_pattern": "Mediterranean Travel"
    }
  }
}
```

### TypeScript Interface

```typescript
interface MusicWidgetData {
  widget_type: "music";
  title: string;
  description: string;
  config: {
    display_mode: "playlist" | "tracks" | "embed";
    auto_play?: boolean;
    show_controls?: boolean;
    enable_shuffle?: boolean;
    theme?: "light" | "dark";
  };
  data: {
    playlist: {
      name: string;
      description: string;
      image?: string;
      provider: "spotify" | "apple_music" | "youtube";
      embed_url?: string;
      tracks: Array<{
        id: string;
        title: string;
        artist: string;
        album: string;
        duration_seconds: number;
        duration_display: string;
        preview_url?: string;
        album_art?: string;
        spotify_url?: string;
      }>;
      total_tracks?: number;
      total_duration_minutes?: number;
    };
    metadata?: {
      genre?: string;
      mood?: string;
      related_pattern?: string;
    };
  };
}
```

### LLM Generation Prompt Template

```
Generate music widget data for an audio/music pattern:
Pattern: {pattern_title}
Keywords: {pattern_keywords}
Description: {pattern_description}
User interests: {persona_interests}

Create a thematic playlist that matches:
- The pattern's mood and theme
- User's interests and activities
- Time/place context if applicable

Generate 5-10 realistic track titles that would fit the theme.
Include genre/mood tags.

For PRODUCTION, this would use Spotify/Apple Music API.

Return JSON matching this schema:
{schema}
```

---

## 10. Feed Widget Schema

### Purpose
Display social-style feeds for community engagement patterns.

### JSON Schema

```json
{
  "widget_type": "feed",
  "title": "Travel Community Highlights",
  "description": "What fellow travelers are sharing",
  "config": {
    "max_items": 5,
    "auto_refresh": false,
    "show_avatars": true,
    "show_engagement": true,
    "compact_mode": false
  },
  "data": {
    "items": [
      {
        "id": "1",
        "author": "Travel Enthusiast",
        "author_handle": "@travelenthusiast",
        "avatar": "https://i.pravatar.cc/150?img=1",
        "content": "Just discovered an amazing hidden beach in Crete! Crystal clear water and barely anyone around. Best find of the trip 🏖️",
        "timestamp": "2025-10-14T10:30:00Z",
        "timestamp_display": "2 hours ago",
        "platform": "instagram",
        "platform_icon": "📷",
        "media": [
          {
            "type": "image",
            "url": "https://images.unsplash.com/photo-...",
            "thumbnail": "https://images.unsplash.com/photo-...?w=400",
            "alt": "Hidden beach in Crete"
          }
        ],
        "engagement": {
          "likes": 245,
          "comments": 12,
          "shares": 8
        },
        "tags": ["travel", "greece", "crete", "beach"]
      },
      {
        "id": "2",
        "author": "Mediterranean Foodie",
        "author_handle": "@medfoodie",
        "avatar": "https://i.pravatar.cc/150?img=2",
        "content": "The gyros from this tiny place near the Acropolis... life-changing! 🌯 Best street food in Athens hands down.",
        "timestamp": "2025-10-14T08:15:00Z",
        "timestamp_display": "4 hours ago",
        "platform": "instagram",
        "platform_icon": "📷",
        "media": [
          {
            "type": "image",
            "url": "https://images.unsplash.com/photo-...",
            "thumbnail": "https://images.unsplash.com/photo-...?w=400",
            "alt": "Greek gyros"
          }
        ],
        "engagement": {
          "likes": 189,
          "comments": 23,
          "shares": 5
        },
        "tags": ["food", "athens", "greece", "gyros"]
      }
    ],
    "metadata": {
      "total_items": 2,
      "source": "curated",
      "topic": "mediterranean_travel",
      "last_updated": "2025-10-14T12:00:00Z"
    }
  }
}
```

### TypeScript Interface

```typescript
interface FeedWidgetData {
  widget_type: "feed";
  title: string;
  description: string;
  config: {
    max_items?: number;
    auto_refresh?: boolean;
    show_avatars?: boolean;
    show_engagement?: boolean;
    compact_mode?: boolean;
  };
  data: {
    items: Array<{
      id: string;
      author: string;
      author_handle?: string;
      avatar?: string;
      content: string;
      timestamp: string;
      timestamp_display: string;
      platform: "instagram" | "twitter" | "reddit" | "linkedin";
      platform_icon?: string;
      media?: Array<{
        type: "image" | "video";
        url: string;
        thumbnail?: string;
        alt?: string;
      }>;
      engagement?: {
        likes?: number;
        comments?: number;
        shares?: number;
      };
      tags?: string[];
    }>;
    metadata?: {
      total_items?: number;
      source?: string;
      topic?: string;
      last_updated?: string;
    };
  };
}
```

### LLM Generation Prompt Template

```
Generate feed widget data for a community/social pattern:
Pattern: {pattern_title}
Keywords: {pattern_keywords}
Description: {pattern_description}

Create 3-5 realistic social media posts that:
- Relate to the pattern theme
- Feel authentic and engaging
- Include varied content (tips, discoveries, questions)
- Have realistic engagement metrics
- Match the platform style (Instagram, Reddit, etc.)

Return JSON matching this schema:
{schema}
```

---

## Pydantic Models for Validation

Here's how to implement these schemas as Pydantic models:

```python
# Add to fabric_dashboard/models/schemas.py

from typing import Literal, Optional, Any
from pydantic import BaseModel, Field, HttpUrl

class WidgetConfig(BaseModel):
    """Base widget configuration."""
    model_config = {"extra": "allow"}  # Allow widget-specific config

class WidgetDataBase(BaseModel):
    """Base widget data."""
    model_config = {"extra": "allow"}  # Allow widget-specific data

class WidgetData(BaseModel):
    """Complete widget specification."""
    widget_type: WidgetType
    title: str = Field(min_length=1, max_length=150)
    description: str = Field(min_length=1, max_length=300)
    config: dict[str, Any] = Field(default_factory=dict)
    data: dict[str, Any] = Field(default_factory=dict)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    def validate_schema(self) -> bool:
        """Validate widget data against type-specific schema."""
        # Add validation logic per widget type
        return True

# Specific models for each widget type
class MapMarker(BaseModel):
    lat: float = Field(ge=-90, le=90)
    lng: float = Field(ge=-180, le=180)
    label: str
    description: str
    color: Optional[str] = None
    icon: Optional[str] = "pin"
    timestamp: Optional[datetime] = None

class MapWidgetConfig(BaseModel):
    center: dict[str, float]  # {"lat": float, "lng": float}
    zoom: int = Field(ge=1, le=20, default=10)
    theme: Literal["light", "dark", "satellite"] = "light"
    enable_clustering: bool = False
    show_routes: bool = True

class MapWidgetData(BaseModel):
    markers: list[MapMarker]
    routes: Optional[list[dict[str, Any]]] = None
    metadata: Optional[dict[str, Any]] = None

# Similar models for other widget types...
```

---

## Usage in Widget Generation

### With Mock Data

```python
def generate_widget_data(pattern: Pattern) -> WidgetData:
    """Generate widget data matching schema."""
    
    if pattern matches travel:
        return WidgetData(
            widget_type=WidgetType.MAP,
            title=f"Your {pattern.title}",
            description=pattern.description[:100],
            config={
                "center": {"lat": 37.9838, "lng": 23.7275},
                "zoom": 6,
                "theme": "light"
            },
            data={
                "markers": [
                    {
                        "lat": 37.9838,
                        "lng": 23.7275,
                        "label": "Athens",
                        "description": "Ancient history exploration",
                        "color": "#2E86AB"
                    }
                ]
            }
        )
```

### With LLM Generation

```python
def generate_widget_data_with_llm(pattern: Pattern, widget_type: WidgetType) -> WidgetData:
    """Generate widget data using LLM."""
    
    # Get schema for this widget type
    schema_json = get_widget_schema(widget_type)
    
    # Build prompt
    prompt = f"""
    Generate {widget_type} widget data for this pattern:
    Pattern: {pattern.title}
    Keywords: {", ".join(pattern.keywords)}
    Description: {pattern.description}
    
    Return valid JSON matching this schema:
    {schema_json}
    """
    
    # Call LLM with structured output
    structured_llm = llm.with_structured_output(WidgetData)
    result = structured_llm.invoke(prompt)
    
    return result
```

---

## Testing with Schemas

```python
# test_widget_schemas.py

def test_map_widget_schema():
    """Test map widget data validation."""
    
    widget_data = WidgetData(
        widget_type=WidgetType.MAP,
        title="Test Map",
        description="Test description",
        config={
            "center": {"lat": 37.9838, "lng": 23.7275},
            "zoom": 6
        },
        data={
            "markers": [
                {
                    "lat": 37.9838,
                    "lng": 23.7275,
                    "label": "Athens",
                    "description": "Test location"
                }
            ]
        }
    )
    
    assert widget_data.widget_type == WidgetType.MAP
    assert len(widget_data.data["markers"]) == 1
    assert widget_data.config["zoom"] == 6
```

---

## Summary

These JSON schemas provide:

1. ✅ **Clear Contracts** - Exact data structure for each widget
2. ✅ **LLM-Friendly** - Easy to include in prompts
3. ✅ **Type-Safe** - Pydantic validation
4. ✅ **Documentation** - Self-documenting API
5. ✅ **Testable** - Easy to create mock data
6. ✅ **Extensible** - Easy to add new widget types

The schemas act as the interface between:
- **Pattern Detection** → Widget Selection → **Schema** → Data Generation → Rendering

This abstraction makes the system modular and maintainable.

