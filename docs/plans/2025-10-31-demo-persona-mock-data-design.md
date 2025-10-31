# Demo Persona Mock Data Design

**Date**: 2025-10-31
**Purpose**: General showcase demo with broad appeal and wow factor
**Approach**: Widget-driven design - mock complete pipeline outputs for "demo" persona

## Overview

Create a pre-crafted "demo" persona that bypasses all LLM calls and returns rich, handcrafted dashboard data. This provides a reliable, impressive demo experience without API costs or latency.

**Key Decision**: Mock pipeline outputs (patterns, widgets, theme, content), not OnFabric input data.

## Integration Architecture

### Pipeline Service Modification

Enhance `backend/app/services/pipeline_service.py` to detect `persona == "demo"` and load pre-crafted outputs:

```python
if persona == "demo":
    # Load pre-crafted demo data
    demo_data = load_demo_fixture()

    # Stream fake progress updates for UX
    await send_progress("patterns", 30, demo_data.patterns)
    await send_progress("theme", 50, demo_data.theme)
    # ... etc

    # Return pre-built dashboard
    return build_dashboard(demo_data)
```

### Fixture File Location

```
fabric_dashboard/tests/fixtures/personas/demo.json
```

### JSON Structure

```json
{
  "patterns": [...],           // 5 PatternDetectionResult patterns
  "persona": {...},            // PersonaProfile
  "theme": {...},              // ColorScheme
  "ui_components": [...],      // 9 pre-configured widgets
  "content_cards": [...]       // 2 written content cards
}
```

## Patterns (5 Distinct)

1. **"Surf & Travel Enthusiast"**
   - Confidence: 0.89
   - Keywords: surf, Morocco, Tagazhout, travel, Atlantic
   - Description: "Deep engagement with surf culture and Atlantic coast travel, particularly Morocco's legendary point breaks"
   - Triggers: Map widget

2. **"Tech Startup Navigator"**
   - Confidence: 0.85
   - Keywords: startups, London, tech events, founders, pitching
   - Description: "Active participant in London's startup ecosystem, attending demo days and founder events"
   - Triggers: Event calendar widget

3. **"AI Safety Researcher"**
   - Confidence: 0.92
   - Keywords: AI safety, alignment, ethics, research, existential risk
   - Description: "Seriously engaged with AI safety and alignment research, exploring both technical and philosophical dimensions"
   - Triggers: Info card, task list

4. **"AI Alignment Deep Diver"**
   - Confidence: 0.87
   - Keywords: Robert Miles, mesa-optimization, scalable oversight, instrumental convergence
   - Description: "Systematic consumption of AI alignment educational content, particularly technical explainers"
   - Triggers: Video feed (AI alignment)

5. **"Celebrity Cooking Entertainment"**
   - Confidence: 0.78
   - Keywords: Gordon Ramsay, cooking techniques, chef tutorials, recipes
   - Description: "Enjoys watching professional chefs demonstrate cooking techniques and personalities"
   - Triggers: Video feed (cooking)

## UI Components (9 Widgets)

### 1. Map Card - Tagazhout Surf Spots

```javascript
{
  component_type: "map-card",
  title: "Tagazhout Surf Spots",
  pattern_title: "Surf & Travel Enthusiast",
  center_lat: 30.5447,
  center_lng: -9.7143,
  zoom_level: 13,
  markers: [
    {
      name: "Anchor Point",
      lat: 30.5380,
      lng: -9.7215,
      description: "Right point break, works best on big NW swells"
    },
    {
      name: "Hash Point",
      lat: 30.5420,
      lng: -9.7190,
      description: "Powerful right-hander, intermediate to advanced"
    },
    {
      name: "Killer Point",
      lat: 30.5445,
      lng: -9.7165,
      description: "Long right point, multiple sections"
    },
    {
      name: "La Source",
      lat: 30.5520,
      lng: -9.7100,
      description: "Beach break, good for beginners"
    },
    {
      name: "Boilers",
      lat: 30.5350,
      lng: -9.7250,
      description: "Heavy reef break, experts only"
    }
  ]
}
```

### 2. Event Calendar - London Startup & Club Events

```javascript
{
  component_type: "event-calendar",
  title: "London Events",
  pattern_title: "Tech Startup Navigator",
  search_query: "London tech startup and club events 2025",
  events: [
    {
      title: "TechCrunch Disrupt London",
      date: "2025-11-15",
      location: "ExCeL London",
      url: "https://techcrunch.com/events",
      type: "startup"
    },
    {
      title: "Fabric: Four Tet All Night",
      date: "2025-11-16",
      location: "Fabric, Farringdon",
      url: "https://fabriclondon.com",
      type: "club"
    },
    {
      title: "Seedcamp Demo Day",
      date: "2025-11-08",
      location: "Barbican Centre",
      url: "https://seedcamp.com",
      type: "startup"
    },
    {
      title: "Printworks: Adam Beyer",
      date: "2025-11-10",
      location: "Printworks London",
      url: "https://printworkslondon.co.uk",
      type: "club"
    },
    {
      title: "Founders Forum",
      date: "2025-11-22",
      location: "The Shard",
      url: "https://foundersforum.com",
      type: "startup"
    },
    {
      title: "Ministry of Sound: Carl Cox",
      date: "2025-11-23",
      location: "Ministry of Sound, Elephant & Castle",
      url: "https://ministryofsound.com",
      type: "club"
    },
    {
      title: "AI Safety Summit",
      date: "2025-11-29",
      location: "King's College",
      url: "https://aisafetysummit.com",
      type: "startup"
    },
    {
      title: "Corsica Studios: Boiler Room",
      date: "2025-12-01",
      location: "Corsica Studios, Elephant & Castle",
      url: "https://corsicastudios.com",
      type: "club"
    },
    {
      title: "Pitch@Palace",
      date: "2025-12-06",
      location: "St James's Palace",
      url: "https://pitchatpalace.com",
      type: "startup"
    },
    {
      title: "Village Underground: Jamie xx",
      date: "2025-12-07",
      location: "Shoreditch",
      url: "https://villageunderground.co.uk",
      type: "club"
    }
  ]
}
```

### 3. Video Feed #1 - AI Alignment (Real YouTube Links)

```javascript
{
  component_type: "video-feed",
  title: "AI Alignment Fundamentals",
  pattern_title: "AI Alignment Deep Diver",
  search_query: "AI alignment safety research",
  videos: [
    {
      title: "The AI Alignment Problem",
      channel: "Robert Miles",
      thumbnail_url: "https://i.ytimg.com/vi/EUjc1WuyPT8/maxresdefault.jpg",
      url: "https://www.youtube.com/watch?v=EUjc1WuyPT8",
      duration: "8:42"
    },
    {
      title: "Mesa-Optimization: What It Is & Why We Should Care",
      channel: "Robert Miles",
      thumbnail_url: "https://i.ytimg.com/vi/bJLcIBixGj8/maxresdefault.jpg",
      url: "https://www.youtube.com/watch?v=bJLcIBixGj8",
      duration: "11:33"
    },
    {
      title: "Scalable Oversight - AI Alignment",
      channel: "Robert Miles",
      thumbnail_url: "https://i.ytimg.com/vi/VJ3bJRhIf9Y/maxresdefault.jpg",
      url: "https://www.youtube.com/watch?v=VJ3bJRhIf9Y",
      duration: "9:15"
    },
    {
      title: "Instrumental Convergence",
      channel: "Robert Miles",
      thumbnail_url: "https://i.ytimg.com/vi/ZeecOKBus3Q/maxresdefault.jpg",
      url: "https://www.youtube.com/watch?v=ZeecOKBus3Q",
      duration: "10:28"
    }
  ]
}
```

### 4. Video Feed #2 - Celebrity Cooking (Real YouTube Links)

```javascript
{
  component_type: "video-feed",
  title: "Cooking with the Pros",
  pattern_title: "Celebrity Cooking Entertainment",
  search_query: "celebrity chef cooking videos",
  videos: [
    {
      title: "Gordon Ramsay's ULTIMATE COOKERY COURSE: How to Cook the Perfect Steak",
      channel: "Gordon Ramsay",
      thumbnail_url: "https://i.ytimg.com/vi/AmC9SmCBUj4/maxresdefault.jpg",
      url: "https://www.youtube.com/watch?v=AmC9SmCBUj4",
      duration: "4:47"
    },
    {
      title: "Matty Matheson Makes His Legendary Burger | The Burger Show",
      channel: "First We Feast",
      thumbnail_url: "https://i.ytimg.com/vi/nbCFRAjTRlA/maxresdefault.jpg",
      url: "https://www.youtube.com/watch?v=nbCFRAjTRlA",
      duration: "13:45"
    },
    {
      title: "Jacques Pépin Demonstrates Knife Skills",
      channel: "KQED",
      thumbnail_url: "https://i.ytimg.com/vi/nffGuGwCE3E/maxresdefault.jpg",
      url: "https://www.youtube.com/watch?v=nffGuGwCE3E",
      duration: "7:52"
    },
    {
      title: "Perfect Pasta Aglio e Olio | Basics with Babish",
      channel: "Babish Culinary Universe",
      thumbnail_url: "https://i.ytimg.com/vi/bJUiWdM__Qw/maxresdefault.jpg",
      url: "https://www.youtube.com/watch?v=bJUiWdM__Qw",
      duration: "5:24"
    }
  ]
}
```

### 5. Weather Card - Tagazhout

```javascript
{
  component_type: "weather-card",
  title: "Tagazhout Weather",
  pattern_title: "Surf & Travel Enthusiast",
  location: "Tagazhout, Morocco",
  lat: 30.5447,
  lng: -9.7143,
  current_temp: 22,
  feels_like: 21,
  condition: "Partly Cloudy",
  wind_speed: 15,
  wind_direction: "NW",
  humidity: 68,
  forecast: [
    {day: "Today", high: 24, low: 18, condition: "Sunny"},
    {day: "Tomorrow", high: 23, low: 17, condition: "Clear"},
    {day: "Saturday", high: 25, low: 19, condition: "Sunny"}
  ]
}
```

### 6. Weather Card - London

```javascript
{
  component_type: "weather-card",
  title: "London Weather",
  pattern_title: "Tech Startup Navigator",
  location: "London, UK",
  lat: 51.5074,
  lng: -0.1278,
  current_temp: 12,
  feels_like: 9,
  condition: "Overcast",
  wind_speed: 18,
  wind_direction: "SW",
  humidity: 78,
  forecast: [
    {day: "Today", high: 14, low: 9, condition: "Cloudy"},
    {day: "Tomorrow", high: 13, low: 8, condition: "Light Rain"},
    {day: "Saturday", high: 15, low: 10, condition: "Partly Cloudy"}
  ]
}
```

### 7. Weather Card - Berlin

```javascript
{
  component_type: "weather-card",
  title: "Berlin Weather",
  pattern_title: "AI Safety Researcher",
  location: "Berlin, Germany",
  lat: 52.5200,
  lng: 13.4050,
  current_temp: 8,
  feels_like: 5,
  condition: "Clear",
  wind_speed: 12,
  wind_direction: "E",
  humidity: 72,
  forecast: [
    {day: "Today", high: 11, low: 5, condition: "Sunny"},
    {day: "Tomorrow", high: 10, low: 4, condition: "Clear"},
    {day: "Saturday", high: 12, low: 6, condition: "Partly Cloudy"}
  ]
}
```

### 8. Task List - Dual Focus

```javascript
{
  component_type: "task-list",
  title: "Current Explorations",
  pattern_title: "AI Safety Researcher",
  tasks: [
    {
      text: "Read Superintelligence by Nick Bostrom",
      completed: false,
      category: "AI Safety"
    },
    {
      text: "Watch Robert Miles alignment playlist",
      completed: true,
      category: "AI Safety"
    },
    {
      text: "Review Anthropic's Constitutional AI paper",
      completed: false,
      category: "AI Safety"
    },
    {
      text: "Try rock climbing at Castle Climbing",
      completed: false,
      category: "Fitness"
    },
    {
      text: "Join local bouldering group",
      completed: false,
      category: "Fitness"
    },
    {
      text: "Test out yoga classes in Shoreditch",
      completed: true,
      category: "Fitness"
    }
  ]
}
```

### 9. Info Card - AI Safety Overview

```javascript
{
  component_type: "info-card",
  title: "AI Safety Fundamentals",
  pattern_title: "AI Safety Researcher",
  location: "London AI Safety Hub",
  overview: "Exploring the critical challenges in ensuring advanced AI systems remain beneficial and aligned with human values. Focus areas include alignment problem, scalable oversight, interpretability, and value learning.",
  key_topics: [
    "Alignment Problem",
    "Scalable Oversight",
    "Interpretability",
    "Value Learning"
  ],
  confidence: 0.88
}
```

## Content Cards (2 Cards)

### Card #1 - Surf & Travel

```javascript
{
  title: "The Magic Hour at Anchor Point",
  description: "Why Morocco's legendary right-hander deserves a spot on every surfer's bucket list",
  body: `There's a moment just after dawn at Anchor Point when the offshore wind picks up and the first set of the day peels down the point in perfect, glassy sections. You're not just riding a wave here—you're riding geography itself, a rocky finger jutting into the Atlantic that's been sculpting perfect rights for millennia.

The locals will tell you that Anchor Point isn't Morocco's best wave. Hash Point is more powerful, Killer Point is longer, Boilers is more challenging. But what makes Anchor so special is its consistency. While other spots need that perfect combination of swell, wind, and tide, Anchor works 200+ days a year. It's the wave that turned Tagazhout from a sleepy fishing village into one of Africa's premier surf destinations.

What surprised me most wasn't the waves—I'd seen the videos, read the guides. It was the community. Dawn patrol sessions with Moroccan rippers who grew up on these breaks. Sunset tagines at local cafes where everyone dissects the day's conditions. The Dutch couple who'd been "visiting for two weeks" three years ago and never left.

If you're planning a trip: November through March for the biggest swells, but September-October offers warmer water and smaller crowds. Book accommodation in Tagazhout village, not Agadir—you want to be able to check the surf from your window. And bring a 5/3mm wetsuit; the Atlantic here is colder than you think.`,
  reading_time_minutes: 3,
  size: "MEDIUM",
  pattern_title: "Surf & Travel Enthusiast"
}
```

### Card #2 - Tech Startup

```javascript
{
  title: "London's Quiet AI Revolution",
  description: "How the city became Europe's unexpected AI safety capital",
  body: `Walk down Tottenham Court Road on a Wednesday evening and you'll stumble upon something remarkable: 200+ people crammed into a basement discussing mesa-optimization and reward hacking. This is the London AI Safety Hub's weekly meetup, and it's just one node in an ecosystem that's quietly making London the center of European AI safety research.

The math is compelling. DeepMind's headquarters in King's Cross. Anthropic's expanding London office. The UK AI Safety Institute at the Frontier AI Taskforce. Oxford and Cambridge churning out technical safety researchers. Government taking AI risk seriously after the 2023 Bletchley Summit. Add a timezone that bridges US West Coast and Asia, and you have a perfect storm.

But what makes London special isn't the institutions—it's the culture. Unlike SF's "move fast and break things," London's AI scene carries a distinctly cautious flavor. Maybe it's the proximity to government. Maybe it's European sensibility about existential risk. Whatever it is, you can feel it in the conversations at Founders Forum, in the pitch decks at Seedcamp, in the due diligence questions from VCs on Sand Hill Row.

The next wave is already forming. Every week brings new safety-focused startups: companies building interpretability tools, alignment testing frameworks, governance infrastructure. They're not asking "can we build AGI?"—they're asking "when we do, how do we make sure it goes well?"

The revolution won't be televised. But it might be livestreamed from a King's Cross conference room.`,
  reading_time_minutes: 3,
  size: "LARGE",
  pattern_title: "Tech Startup Navigator"
}
```

## Theme - "Electric Midnight"

**Design Philosophy**: Avoid generic purple gradients and Inter/Roboto fonts (per CLAUDE.md). Create distinctive, energetic aesthetic combining startup energy with contemplative depth.

```javascript
{
  mood: "energetic and curious",
  primary: "#00D9FF",        // Electric cyan
  secondary: "#FF006E",      // Hot magenta
  accent: "#FFBE0B",         // Vibrant amber
  background: "#0A0E27",     // Deep midnight blue
  foreground: "#E8F1F5",     // Crisp off-white
  muted: "#64748B",          // Slate gray
  success: "#00F5A0",        // Neon mint
  warning: "#FF8E3C",        // Warm orange
  destructive: "#FF006E",    // Hot magenta

  rationale: "Combines the energy of a startup scene with the contemplative depth of AI research. Electric cyan and magenta create visual impact while midnight blue background provides sophistication. Avoids generic purple gradients.",

  fonts: {
    heading: "Archivo Black",      // Bold, geometric, distinctive
    body: "Work Sans",             // Clean but not generic
    mono: "JetBrains Mono"         // Modern code font
  },

  background_theme: {
    type: "gradient-mesh",
    gradient: {
      type: "radial-mesh",
      colors: ["#0A0E27", "#1A1F3A", "#00D9FF15"],  // Subtle cyan glow
      angle: 135,
      stops: [0, 50, 100]
    }
  }
}
```

## Persona Profile

```javascript
{
  writing_style: "intellectually curious yet accessible, blends technical precision with narrative storytelling",
  interests: [
    "AI safety and alignment research",
    "Surf culture and travel",
    "London startup ecosystem",
    "Fitness exploration and movement",
    "Celebrity chef cooking techniques"
  ],
  activity_level: "highly engaged",
  professional_context: "Tech founder or researcher in AI safety space, likely early 30s, values both work and lifestyle balance",
  tone_preference: "thoughtful and observational with occasional playfulness",
  age_range: "28-35",
  content_depth_preference: "substantive with personal narrative - prefers 'why it matters' over surface-level facts"
}
```

## Implementation Notes

1. **No LLM Calls**: When `persona == "demo"`, bypass all AI services (PatternDetector, ThemeGenerator, SearchEnricher, ContentWriter, UIGenerator)

2. **Progress Streaming**: Maintain realistic progress updates for UX even though data is pre-loaded

3. **File Structure**: Use existing persona fixture pattern in `fabric_dashboard/tests/fixtures/personas/`

4. **Schema Compliance**: All mock data must match existing Pydantic models (Pattern, ColorScheme, UIComponent, ContentCard)

5. **Frontend Compatibility**: Ensure all widget types are currently supported by frontend components

6. **Real Links**: Use actual YouTube URLs and event links for authentic demo experience

7. **Diverse Widget Types**: 9 total widgets showcasing map, calendar, video feeds (2), weather (3), task list, info card

8. **Content Quality**: Two substantive content cards with engaging narrative writing, avoiding generic AI patterns
