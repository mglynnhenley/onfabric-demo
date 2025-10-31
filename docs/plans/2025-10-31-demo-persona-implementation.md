# Demo Persona Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create a pre-crafted "demo" persona that bypasses all LLM calls and returns rich, handcrafted dashboard data for reliable demo experience.

**Architecture:** Create demo.json fixture with complete pipeline outputs (patterns, theme, UI components, content cards). Modify pipeline_service.py to detect persona == "demo" and load fixture instead of calling AI services.

**Tech Stack:** Python, Pydantic schemas, JSON fixtures, FastAPI WebSocket streaming

---

## Task 1: Create Demo Fixture File

**Files:**
- Create: `fabric_dashboard/tests/fixtures/personas/demo.json`

**Step 1: Create personas directory**

```bash
mkdir -p fabric_dashboard/tests/fixtures/personas
```

**Step 2: Create demo.json fixture**

Create `fabric_dashboard/tests/fixtures/personas/demo.json` with this complete content:

```json
{
  "patterns": [
    {
      "title": "Surf & Travel Enthusiast",
      "description": "Deep engagement with surf culture and Atlantic coast travel, particularly Morocco's legendary point breaks. Follows surf forecasts, saves travel guides, and researches optimal surf seasons.",
      "confidence": 0.89,
      "keywords": ["surf", "Morocco", "Tagazhout", "travel", "Atlantic", "waves", "point breaks"],
      "interaction_count": 45,
      "time_range": {
        "start": "2025-09-01T00:00:00Z",
        "end": "2025-10-31T00:00:00Z"
      },
      "top_interactions": []
    },
    {
      "title": "Tech Startup Navigator",
      "description": "Active participant in London's startup ecosystem, attending demo days, founder events, and nightlife. Balances professional networking with cultural experiences in the city's electronic music scene.",
      "confidence": 0.85,
      "keywords": ["startups", "London", "tech events", "founders", "pitching", "clubs", "nightlife"],
      "interaction_count": 38,
      "time_range": {
        "start": "2025-09-01T00:00:00Z",
        "end": "2025-10-31T00:00:00Z"
      },
      "top_interactions": []
    },
    {
      "title": "AI Safety Researcher",
      "description": "Seriously engaged with AI safety and alignment research, exploring both technical and philosophical dimensions. Reads academic papers, follows key researchers, and participates in safety-focused communities.",
      "confidence": 0.92,
      "keywords": ["AI safety", "alignment", "ethics", "research", "existential risk", "governance"],
      "interaction_count": 52,
      "time_range": {
        "start": "2025-09-01T00:00:00Z",
        "end": "2025-10-31T00:00:00Z"
      },
      "top_interactions": []
    },
    {
      "title": "AI Alignment Deep Diver",
      "description": "Systematic consumption of AI alignment educational content, particularly technical explainers. Watches Robert Miles videos, reads Anthropic papers, and explores mesa-optimization and scalable oversight concepts.",
      "confidence": 0.87,
      "keywords": ["Robert Miles", "mesa-optimization", "scalable oversight", "instrumental convergence", "AI alignment"],
      "interaction_count": 31,
      "time_range": {
        "start": "2025-09-01T00:00:00Z",
        "end": "2025-10-31T00:00:00Z"
      },
      "top_interactions": []
    },
    {
      "title": "Celebrity Cooking Entertainment",
      "description": "Enjoys watching professional chefs demonstrate cooking techniques and personalities. Follows Gordon Ramsay, Matty Matheson, and other celebrity chefs for both entertainment and skill development.",
      "confidence": 0.78,
      "keywords": ["Gordon Ramsay", "cooking techniques", "chef tutorials", "recipes", "culinary"],
      "interaction_count": 24,
      "time_range": {
        "start": "2025-09-01T00:00:00Z",
        "end": "2025-10-31T00:00:00Z"
      },
      "top_interactions": []
    }
  ],
  "persona": {
    "writing_style": "intellectually curious yet accessible, blends technical precision with narrative storytelling",
    "interests": [
      "AI safety and alignment research",
      "Surf culture and travel",
      "London startup ecosystem",
      "Fitness exploration and movement",
      "Celebrity chef cooking techniques",
      "Electronic music and nightlife"
    ],
    "activity_level": "highly engaged",
    "professional_context": "Tech founder or researcher in AI safety space, likely early 30s, values both work and lifestyle balance",
    "tone_preference": "thoughtful and observational with occasional playfulness",
    "age_range": "28-35",
    "content_depth_preference": "substantive with personal narrative - prefers 'why it matters' over surface-level facts"
  },
  "theme": {
    "mood": "energetic and curious",
    "primary": "#00D9FF",
    "secondary": "#FF006E",
    "accent": "#FFBE0B",
    "background": "#0A0E27",
    "foreground": "#E8F1F5",
    "muted": "#64748B",
    "success": "#00F5A0",
    "warning": "#FF8E3C",
    "destructive": "#FF006E",
    "rationale": "Combines the energy of a startup scene with the contemplative depth of AI research. Electric cyan and magenta create visual impact while midnight blue background provides sophistication. Avoids generic purple gradients.",
    "fonts": {
      "heading": "Archivo Black",
      "body": "Work Sans",
      "mono": "JetBrains Mono"
    },
    "background_theme": {
      "type": "gradient-mesh",
      "gradient": {
        "type": "radial-mesh",
        "colors": ["#0A0E27", "#1A1F3A", "#00D9FF15"],
        "angle": 135,
        "stops": [0, 50, 100]
      }
    }
  },
  "ui_components": [
    {
      "component_type": "map-card",
      "title": "Tagazhout Surf Spots",
      "pattern_title": "Surf & Travel Enthusiast",
      "confidence": 0.89,
      "center_lat": 30.5447,
      "center_lng": -9.7143,
      "zoom_level": 13,
      "markers": [
        {
          "name": "Anchor Point",
          "lat": 30.5380,
          "lng": -9.7215,
          "description": "Right point break, works best on big NW swells"
        },
        {
          "name": "Hash Point",
          "lat": 30.5420,
          "lng": -9.7190,
          "description": "Powerful right-hander, intermediate to advanced"
        },
        {
          "name": "Killer Point",
          "lat": 30.5445,
          "lng": -9.7165,
          "description": "Long right point, multiple sections"
        },
        {
          "name": "La Source",
          "lat": 30.5520,
          "lng": -9.7100,
          "description": "Beach break, good for beginners"
        },
        {
          "name": "Boilers",
          "lat": 30.5350,
          "lng": -9.7250,
          "description": "Heavy reef break, experts only"
        }
      ]
    },
    {
      "component_type": "event-calendar",
      "title": "London Events",
      "pattern_title": "Tech Startup Navigator",
      "confidence": 0.85,
      "search_query": "London tech startup and club events 2025",
      "events": [
        {
          "title": "TechCrunch Disrupt London",
          "date": "2025-11-15",
          "location": "ExCeL London",
          "url": "https://techcrunch.com/events",
          "type": "startup"
        },
        {
          "title": "Fabric: Four Tet All Night",
          "date": "2025-11-16",
          "location": "Fabric, Farringdon",
          "url": "https://fabriclondon.com",
          "type": "club"
        },
        {
          "title": "Seedcamp Demo Day",
          "date": "2025-11-08",
          "location": "Barbican Centre",
          "url": "https://seedcamp.com",
          "type": "startup"
        },
        {
          "title": "Printworks: Adam Beyer",
          "date": "2025-11-10",
          "location": "Printworks London",
          "url": "https://printworkslondon.co.uk",
          "type": "club"
        },
        {
          "title": "Founders Forum",
          "date": "2025-11-22",
          "location": "The Shard",
          "url": "https://foundersforum.com",
          "type": "startup"
        },
        {
          "title": "Ministry of Sound: Carl Cox",
          "date": "2025-11-23",
          "location": "Ministry of Sound, Elephant & Castle",
          "url": "https://ministryofsound.com",
          "type": "club"
        },
        {
          "title": "AI Safety Summit",
          "date": "2025-11-29",
          "location": "King's College",
          "url": "https://aisafetysummit.com",
          "type": "startup"
        },
        {
          "title": "Corsica Studios: Boiler Room",
          "date": "2025-12-01",
          "location": "Corsica Studios, Elephant & Castle",
          "url": "https://corsicastudios.com",
          "type": "club"
        },
        {
          "title": "Pitch@Palace",
          "date": "2025-12-06",
          "location": "St James's Palace",
          "url": "https://pitchatpalace.com",
          "type": "startup"
        },
        {
          "title": "Village Underground: Jamie xx",
          "date": "2025-12-07",
          "location": "Shoreditch",
          "url": "https://villageunderground.co.uk",
          "type": "club"
        }
      ]
    },
    {
      "component_type": "video-feed",
      "title": "AI Alignment Fundamentals",
      "pattern_title": "AI Alignment Deep Diver",
      "confidence": 0.87,
      "search_query": "AI alignment safety research",
      "videos": [
        {
          "title": "The AI Alignment Problem",
          "channel": "Robert Miles",
          "thumbnail_url": "https://i.ytimg.com/vi/EUjc1WuyPT8/maxresdefault.jpg",
          "url": "https://www.youtube.com/watch?v=EUjc1WuyPT8",
          "duration": "8:42"
        },
        {
          "title": "Mesa-Optimization: What It Is & Why We Should Care",
          "channel": "Robert Miles",
          "thumbnail_url": "https://i.ytimg.com/vi/bJLcIBixGj8/maxresdefault.jpg",
          "url": "https://www.youtube.com/watch?v=bJLcIBixGj8",
          "duration": "11:33"
        },
        {
          "title": "Scalable Oversight - AI Alignment",
          "channel": "Robert Miles",
          "thumbnail_url": "https://i.ytimg.com/vi/VJ3bJRhIf9Y/maxresdefault.jpg",
          "url": "https://www.youtube.com/watch?v=VJ3bJRhIf9Y",
          "duration": "9:15"
        },
        {
          "title": "Instrumental Convergence",
          "channel": "Robert Miles",
          "thumbnail_url": "https://i.ytimg.com/vi/ZeecOKBus3Q/maxresdefault.jpg",
          "url": "https://www.youtube.com/watch?v=ZeecOKBus3Q",
          "duration": "10:28"
        }
      ]
    },
    {
      "component_type": "video-feed",
      "title": "Cooking with the Pros",
      "pattern_title": "Celebrity Cooking Entertainment",
      "confidence": 0.78,
      "search_query": "celebrity chef cooking videos",
      "videos": [
        {
          "title": "Gordon Ramsay's ULTIMATE COOKERY COURSE: How to Cook the Perfect Steak",
          "channel": "Gordon Ramsay",
          "thumbnail_url": "https://i.ytimg.com/vi/AmC9SmCBUj4/maxresdefault.jpg",
          "url": "https://www.youtube.com/watch?v=AmC9SmCBUj4",
          "duration": "4:47"
        },
        {
          "title": "Matty Matheson Makes His Legendary Burger | The Burger Show",
          "channel": "First We Feast",
          "thumbnail_url": "https://i.ytimg.com/vi/nbCFRAjTRlA/maxresdefault.jpg",
          "url": "https://www.youtube.com/watch?v=nbCFRAjTRlA",
          "duration": "13:45"
        },
        {
          "title": "Jacques Pépin Demonstrates Knife Skills",
          "channel": "KQED",
          "thumbnail_url": "https://i.ytimg.com/vi/nffGuGwCE3E/maxresdefault.jpg",
          "url": "https://www.youtube.com/watch?v=nffGuGwCE3E",
          "duration": "7:52"
        },
        {
          "title": "Perfect Pasta Aglio e Olio | Basics with Babish",
          "channel": "Babish Culinary Universe",
          "thumbnail_url": "https://i.ytimg.com/vi/bJUiWdM__Qw/maxresdefault.jpg",
          "url": "https://www.youtube.com/watch?v=bJUiWdM__Qw",
          "duration": "5:24"
        }
      ]
    },
    {
      "component_type": "weather-card",
      "title": "Tagazhout Weather",
      "pattern_title": "Surf & Travel Enthusiast",
      "confidence": 0.89,
      "location": "Tagazhout, Morocco",
      "lat": 30.5447,
      "lng": -9.7143,
      "current_temp": 22,
      "feels_like": 21,
      "condition": "Partly Cloudy",
      "wind_speed": 15,
      "wind_direction": "NW",
      "humidity": 68,
      "forecast": [
        {"day": "Today", "high": 24, "low": 18, "condition": "Sunny"},
        {"day": "Tomorrow", "high": 23, "low": 17, "condition": "Clear"},
        {"day": "Saturday", "high": 25, "low": 19, "condition": "Sunny"}
      ]
    },
    {
      "component_type": "weather-card",
      "title": "London Weather",
      "pattern_title": "Tech Startup Navigator",
      "confidence": 0.85,
      "location": "London, UK",
      "lat": 51.5074,
      "lng": -0.1278,
      "current_temp": 12,
      "feels_like": 9,
      "condition": "Overcast",
      "wind_speed": 18,
      "wind_direction": "SW",
      "humidity": 78,
      "forecast": [
        {"day": "Today", "high": 14, "low": 9, "condition": "Cloudy"},
        {"day": "Tomorrow", "high": 13, "low": 8, "condition": "Light Rain"},
        {"day": "Saturday", "high": 15, "low": 10, "condition": "Partly Cloudy"}
      ]
    },
    {
      "component_type": "weather-card",
      "title": "Berlin Weather",
      "pattern_title": "AI Safety Researcher",
      "confidence": 0.92,
      "location": "Berlin, Germany",
      "lat": 52.5200,
      "lng": 13.4050,
      "current_temp": 8,
      "feels_like": 5,
      "condition": "Clear",
      "wind_speed": 12,
      "wind_direction": "E",
      "humidity": 72,
      "forecast": [
        {"day": "Today", "high": 11, "low": 5, "condition": "Sunny"},
        {"day": "Tomorrow", "high": 10, "low": 4, "condition": "Clear"},
        {"day": "Saturday", "high": 12, "low": 6, "condition": "Partly Cloudy"}
      ]
    },
    {
      "component_type": "task-list",
      "title": "Current Explorations",
      "pattern_title": "AI Safety Researcher",
      "confidence": 0.92,
      "tasks": [
        {
          "text": "Read Superintelligence by Nick Bostrom",
          "completed": false,
          "category": "AI Safety"
        },
        {
          "text": "Watch Robert Miles alignment playlist",
          "completed": true,
          "category": "AI Safety"
        },
        {
          "text": "Review Anthropic's Constitutional AI paper",
          "completed": false,
          "category": "AI Safety"
        },
        {
          "text": "Try rock climbing at Castle Climbing",
          "completed": false,
          "category": "Fitness"
        },
        {
          "text": "Join local bouldering group",
          "completed": false,
          "category": "Fitness"
        },
        {
          "text": "Test out yoga classes in Shoreditch",
          "completed": true,
          "category": "Fitness"
        }
      ]
    },
    {
      "component_type": "info-card",
      "title": "AI Safety Fundamentals",
      "pattern_title": "AI Safety Researcher",
      "confidence": 0.92,
      "location": "London AI Safety Hub",
      "overview": "Exploring the critical challenges in ensuring advanced AI systems remain beneficial and aligned with human values. Focus areas include alignment problem, scalable oversight, interpretability, and value learning.",
      "key_topics": [
        "Alignment Problem",
        "Scalable Oversight",
        "Interpretability",
        "Value Learning"
      ]
    }
  ],
  "content_cards": [
    {
      "title": "The Magic Hour at Anchor Point",
      "description": "Why Morocco's legendary right-hander deserves a spot on every surfer's bucket list",
      "body": "There's a moment just after dawn at Anchor Point when the offshore wind picks up and the first set of the day peels down the point in perfect, glassy sections. You're not just riding a wave here—you're riding geography itself, a rocky finger jutting into the Atlantic that's been sculpting perfect rights for millennia.\n\nThe locals will tell you that Anchor Point isn't Morocco's best wave. Hash Point is more powerful, Killer Point is longer, Boilers is more challenging. But what makes Anchor so special is its consistency. While other spots need that perfect combination of swell, wind, and tide, Anchor works 200+ days a year. It's the wave that turned Tagazhout from a sleepy fishing village into one of Africa's premier surf destinations.\n\nWhat surprised me most wasn't the waves—I'd seen the videos, read the guides. It was the community. Dawn patrol sessions with Moroccan rippers who grew up on these breaks. Sunset tagines at local cafes where everyone dissects the day's conditions. The Dutch couple who'd been \"visiting for two weeks\" three years ago and never left.\n\nIf you're planning a trip: November through March for the biggest swells, but September-October offers warmer water and smaller crowds. Book accommodation in Tagazhout village, not Agadir—you want to be able to check the surf from your window. And bring a 5/3mm wetsuit; the Atlantic here is colder than you think.",
      "reading_time_minutes": 3,
      "size": "MEDIUM",
      "pattern_title": "Surf & Travel Enthusiast"
    },
    {
      "title": "London's Quiet AI Revolution",
      "description": "How the city became Europe's unexpected AI safety capital",
      "body": "Walk down Tottenham Court Road on a Wednesday evening and you'll stumble upon something remarkable: 200+ people crammed into a basement discussing mesa-optimization and reward hacking. This is the London AI Safety Hub's weekly meetup, and it's just one node in an ecosystem that's quietly making London the center of European AI safety research.\n\nThe math is compelling. DeepMind's headquarters in King's Cross. Anthropic's expanding London office. The UK AI Safety Institute at the Frontier AI Taskforce. Oxford and Cambridge churning out technical safety researchers. Government taking AI risk seriously after the 2023 Bletchley Summit. Add a timezone that bridges US West Coast and Asia, and you have a perfect storm.\n\nBut what makes London special isn't the institutions—it's the culture. Unlike SF's \"move fast and break things,\" London's AI scene carries a distinctly cautious flavor. Maybe it's the proximity to government. Maybe it's European sensibility about existential risk. Whatever it is, you can feel it in the conversations at Founders Forum, in the pitch decks at Seedcamp, in the due diligence questions from VCs on Sand Hill Row.\n\nThe next wave is already forming. Every week brings new safety-focused startups: companies building interpretability tools, alignment testing frameworks, governance infrastructure. They're not asking \"can we build AGI?\"—they're asking \"when we do, how do we make sure it goes well?\"\n\nThe revolution won't be televised. But it might be livestreamed from a King's Cross conference room.",
      "reading_time_minutes": 3,
      "size": "LARGE",
      "pattern_title": "Tech Startup Navigator"
    }
  ]
}
```

**Step 3: Commit fixture file**

```bash
git add fabric_dashboard/tests/fixtures/personas/demo.json
git commit -m "feat: add demo persona fixture with complete mock data

- 5 patterns (surf, startup, AI safety, alignment, cooking)
- 9 UI components (map, calendar, 2x video, 3x weather, task, info)
- 2 content cards with engaging narratives
- Electric Midnight theme (Archivo Black + Work Sans)
- Real YouTube links and London events"
```

---

## Task 2: Add Demo Fixture Loader Function

**Files:**
- Modify: `backend/app/services/pipeline_service.py:35-433`

**Step 1: Add fixture loader method**

Add this method to the `PipelineService` class after `__init__` (around line 40):

```python
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
```

**Step 2: Import required schemas at top of file**

Add these imports after the existing imports (around line 32):

```python
from fabric_dashboard.models.schemas import (
    CardSize, Pattern, PersonaProfile, ColorScheme, ContentCard
)
```

**Step 3: Commit loader function**

```bash
git add backend/app/services/pipeline_service.py
git commit -m "feat: add demo fixture loader to pipeline service"
```

---

## Task 3: Add Demo Path to generate_dashboard

**Files:**
- Modify: `backend/app/services/pipeline_service.py:42-413`

**Step 1: Add demo detection at start of generate_dashboard**

Add this code right after the logging setup (after line 64, before Step 1 comment):

```python
        # Check if this is the demo persona
        if persona == "demo":
            logger.info("🎭 DEMO MODE: Loading pre-crafted demo persona")
            return await self._generate_demo_dashboard(progress_callback, start_time)
```

**Step 2: Add _generate_demo_dashboard method**

Add this method to PipelineService class (after generate_dashboard method, around line 433):

```python
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
    from fabric_dashboard.models.schemas import (
        Pattern, PersonaProfile, ColorScheme, ContentCard
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

    logger.info(f"✓ Loaded {len(patterns)} patterns from demo fixture")

    # Parse persona
    persona_profile = PersonaProfile(**demo_data["persona"])

    # Parse theme
    await self._send_progress(progress_callback, {
        "step": "theme",
        "percent": 50,
        "message": "Loading theme...",
    })
    color_scheme = ColorScheme(**demo_data["theme"])

    logger.info(f"✓ Loaded theme: {color_scheme.mood}")

    # Parse UI components
    await self._send_progress(progress_callback, {
        "step": "widgets",
        "percent": 70,
        "message": "Loading widgets...",
    })

    # Import UI component schemas dynamically
    from fabric_dashboard.models.schemas import (
        MapCard, EventCalendar, VideoFeed, WeatherCard, TaskList, InfoCard
    )

    ui_components = []
    for comp_data in demo_data["ui_components"]:
        comp_type = comp_data["component_type"]
        if comp_type == "map-card":
            ui_components.append(MapCard(**comp_data))
        elif comp_type == "event-calendar":
            ui_components.append(EventCalendar(**comp_data))
        elif comp_type == "video-feed":
            ui_components.append(VideoFeed(**comp_data))
        elif comp_type == "weather-card":
            ui_components.append(WeatherCard(**comp_data))
        elif comp_type == "task-list":
            ui_components.append(TaskList(**comp_data))
        elif comp_type == "info-card":
            ui_components.append(InfoCard(**comp_data))
        else:
            logger.warning(f"Unknown component type: {comp_type}")

    logger.info(f"✓ Loaded {len(ui_components)} UI components")

    # Parse content cards
    await self._send_progress(progress_callback, {
        "step": "content",
        "percent": 85,
        "message": "Loading content...",
    })
    cards = [ContentCard(**c) for c in demo_data["content_cards"]]

    logger.info(f"✓ Loaded {len(cards)} content cards")

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
    logger.info(f"✅ DEMO DASHBOARD COMPLETE ({total_time:.1f}s)")

    await self._send_progress(progress_callback, {
        "step": "complete",
        "percent": 100,
        "message": "Demo ready!",
    })

    return html, dashboard_json
```

**Step 3: Commit demo path implementation**

```bash
git add backend/app/services/pipeline_service.py
git commit -m "feat: implement demo persona generation path

- Detect persona == 'demo' in generate_dashboard
- Add _generate_demo_dashboard method
- Parse fixture data into Pydantic models
- Stream progress updates for UX
- Build dashboard without LLM calls"
```

---

## Task 4: Manual End-to-End Test

**Step 1: Start backend server**

```bash
cd backend
source .venv/bin/activate
python -m uvicorn app.main:app --reload --port 8000
```

Expected: Server starts on http://localhost:8000

**Step 2: Test WebSocket endpoint**

In a new terminal, create test script `test_demo.py`:

```python
#!/usr/bin/env python3
import asyncio
import websockets
import json

async def test_demo():
    uri = "ws://localhost:8000/ws/generate/demo"
    async with websockets.connect(uri) as websocket:
        print("Connected to WebSocket")

        async for message in websocket:
            data = json.loads(message)
            print(f"[{data.get('step', 'unknown')}] {data.get('percent', 0)}% - {data.get('message', '')}")

            if data.get("step") == "complete":
                print("✅ Demo generation complete!")
                break

asyncio.run(test_demo())
```

Run test:

```bash
python test_demo.py
```

Expected output:
```
Connected to WebSocket
[initializing] 0% - Loading demo data...
[patterns] 30% - Loading patterns...
[theme] 50% - Loading theme...
[widgets] 70% - Loading widgets...
[content] 85% - Loading content...
[building] 95% - Assembling dashboard...
[complete] 100% - Demo ready!
✅ Demo generation complete!
```

**Step 3: Verify backend logs**

Check backend terminal for:
```
🎭 DEMO MODE: Loading pre-crafted demo persona
✓ Loaded 5 patterns from demo fixture
✓ Loaded theme: energetic and curious
✓ Loaded 9 UI components
✓ Loaded 2 content cards
✅ DEMO DASHBOARD COMPLETE (0.X s)
```

**Step 4: Test with frontend**

```bash
cd frontend
npm run dev
```

Navigate to: `http://localhost:5173/?persona=demo`

Verify:
- Map shows Tagazhout surf spots
- Calendar shows London startup + club events
- Video feeds show real YouTube thumbnails
- Weather cards show Tagazhout, London, Berlin
- Task list shows AI safety + fitness tasks
- Info card shows AI safety overview
- Content cards render with narratives
- Theme uses Electric Midnight colors (cyan #00D9FF, magenta #FF006E)

**Step 5: Commit test script**

```bash
git add test_demo.py
git commit -m "test: add demo persona WebSocket test script"
```

---

## Task 5: Add Schema Validation Test

**Files:**
- Create: `fabric_dashboard/tests/test_demo_fixture.py`

**Step 1: Write fixture validation test**

Create `fabric_dashboard/tests/test_demo_fixture.py`:

```python
"""Test demo persona fixture schema validation."""

import json
from pathlib import Path

import pytest

from fabric_dashboard.models.schemas import (
    Pattern, PersonaProfile, ColorScheme, ContentCard,
    MapCard, EventCalendar, VideoFeed, WeatherCard, TaskList, InfoCard
)


def test_demo_fixture_exists():
    """Demo fixture file exists."""
    fixture_path = Path(__file__).parent / "fixtures" / "personas" / "demo.json"
    assert fixture_path.exists(), f"Demo fixture not found at {fixture_path}"


def test_demo_fixture_valid_json():
    """Demo fixture is valid JSON."""
    fixture_path = Path(__file__).parent / "fixtures" / "personas" / "demo.json"

    with open(fixture_path) as f:
        data = json.load(f)

    assert "patterns" in data
    assert "persona" in data
    assert "theme" in data
    assert "ui_components" in data
    assert "content_cards" in data


def test_demo_patterns_valid():
    """Demo patterns match Pattern schema."""
    fixture_path = Path(__file__).parent / "fixtures" / "personas" / "demo.json"

    with open(fixture_path) as f:
        data = json.load(f)

    patterns = [Pattern(**p) for p in data["patterns"]]

    assert len(patterns) == 5
    assert all(p.confidence > 0.7 for p in patterns)
    assert all(len(p.keywords) > 0 for p in patterns)


def test_demo_persona_valid():
    """Demo persona matches PersonaProfile schema."""
    fixture_path = Path(__file__).parent / "fixtures" / "personas" / "demo.json"

    with open(fixture_path) as f:
        data = json.load(f)

    persona = PersonaProfile(**data["persona"])

    assert len(persona.interests) > 0
    assert persona.activity_level in ["low", "moderate", "high", "highly engaged"]


def test_demo_theme_valid():
    """Demo theme matches ColorScheme schema."""
    fixture_path = Path(__file__).parent / "fixtures" / "personas" / "demo.json"

    with open(fixture_path) as f:
        data = json.load(f)

    theme = ColorScheme(**data["theme"])

    assert theme.primary.startswith("#")
    assert len(theme.primary) == 7  # #RRGGBB
    assert theme.fonts.heading
    assert theme.fonts.body


def test_demo_ui_components_valid():
    """Demo UI components match their schemas."""
    fixture_path = Path(__file__).parent / "fixtures" / "personas" / "demo.json"

    with open(fixture_path) as f:
        data = json.load(f)

    component_classes = {
        "map-card": MapCard,
        "event-calendar": EventCalendar,
        "video-feed": VideoFeed,
        "weather-card": WeatherCard,
        "task-list": TaskList,
        "info-card": InfoCard,
    }

    components = []
    for comp_data in data["ui_components"]:
        comp_type = comp_data["component_type"]
        comp_class = component_classes[comp_type]
        components.append(comp_class(**comp_data))

    assert len(components) == 9

    # Verify specific components
    map_cards = [c for c in components if isinstance(c, MapCard)]
    assert len(map_cards) == 1
    assert len(map_cards[0].markers) == 5

    event_calendars = [c for c in components if isinstance(c, EventCalendar)]
    assert len(event_calendars) == 1
    assert len(event_calendars[0].events) == 10

    video_feeds = [c for c in components if isinstance(c, VideoFeed)]
    assert len(video_feeds) == 2

    weather_cards = [c for c in components if isinstance(c, WeatherCard)]
    assert len(weather_cards) == 3


def test_demo_content_cards_valid():
    """Demo content cards match ContentCard schema."""
    fixture_path = Path(__file__).parent / "fixtures" / "personas" / "demo.json"

    with open(fixture_path) as f:
        data = json.load(f)

    cards = [ContentCard(**c) for c in data["content_cards"]]

    assert len(cards) == 2
    assert all(card.reading_time_minutes > 0 for card in cards)
    assert all(len(card.body) > 100 for card in cards)
```

**Step 2: Run test**

```bash
cd /Users/matildaglynn/Documents/projects/onfabric_mvp/.worktrees/demo-persona/backend
source .venv/bin/activate
python -m pytest fabric_dashboard/tests/test_demo_fixture.py -v
```

Expected: All tests pass

**Step 3: Commit test**

```bash
git add fabric_dashboard/tests/test_demo_fixture.py
git commit -m "test: add schema validation for demo fixture"
```

---

## Task 6: Final Verification & Cleanup

**Step 1: Run full test suite**

```bash
python -m pytest fabric_dashboard/tests/ -v
```

Expected: All tests pass

**Step 2: Verify no regressions on real personas**

Start backend and test with a different persona:

```bash
# In one terminal
cd backend && source .venv/bin/activate
python -m uvicorn app.main:app --reload --port 8000

# In another terminal - test with real persona
curl -X GET "http://localhost:8000/ws/generate/fitness-enthusiast"
```

Expected: Real persona still works (calls LLMs)

**Step 3: Clean up test script**

```bash
rm test_demo.py  # Optional - keep if useful for future testing
```

**Step 4: Final commit**

```bash
git add -A
git commit -m "feat: complete demo persona implementation

✅ Pre-crafted fixture with 5 patterns, 9 widgets, 2 content cards
✅ Pipeline service detects persona == 'demo'
✅ No LLM calls for demo persona
✅ Schema validation tests
✅ Manual testing verified
✅ No regressions on real personas"
```

---

## Success Criteria

- [ ] `demo.json` fixture created with complete data
- [ ] Pipeline detects `persona == "demo"` and loads fixture
- [ ] All fixture data validates against Pydantic schemas
- [ ] WebSocket streams progress updates during demo generation
- [ ] Dashboard generates in <1 second (no LLM calls)
- [ ] All 9 widgets render correctly in frontend
- [ ] Theme applies Electric Midnight colors
- [ ] Real personas still work (no regressions)
- [ ] All tests pass

## Implementation Notes

- **No LLM calls**: Demo persona bypasses PatternDetector, ThemeGenerator, SearchEnricher, ContentWriter, UIGenerator
- **Progress streaming**: Maintains UX by sending fake progress updates
- **Schema compliance**: All fixture data must validate against existing Pydantic models
- **Real links**: YouTube URLs and event links are real for authentic demo
- **Diverse widgets**: 9 widgets showcase map, calendar, videos, weather, tasks, info card types
