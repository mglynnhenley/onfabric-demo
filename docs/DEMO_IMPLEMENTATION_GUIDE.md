# Interactive Demo - Step-by-Step Implementation Guide

**For**: Junior developers new to React/FastAPI
**Time**: 1 week, working part-time
**Goal**: Ship a working demo at demo.fabricdash.com

---

## 📋 Prerequisites

Before starting, make sure you have:

- [ ] Python 3.11+ installed (`python3 --version`)
- [ ] Node.js 18+ installed (`node --version`)
- [ ] Git configured (`git config --global user.name "Your Name"`)
- [ ] Text editor (VS Code recommended)
- [ ] Terminal access

**New to these tools?**
- Python: https://www.python.org/downloads/
- Node: https://nodejs.org/
- VS Code: https://code.visualstudio.com/

---

## 🗂️ Project Structure Overview

We're adding a `frontend/` folder alongside the existing Python code:

```
onfabric_mvp/
├── fabric_dashboard/      # ✅ Existing Python code (we keep this!)
│   ├── api/
│   ├── core/
│   ├── models/
│   └── ...
├── frontend/              # 🆕 NEW - We're building this
│   ├── src/
│   ├── package.json
│   └── ...
├── backend/               # 🆕 NEW - Thin FastAPI wrapper
│   ├── app/
│   └── requirements.txt
└── docs/
```

---

## Phase 1: Backend Setup (Days 1-2)

### Step 1.1: Create Backend Folder Structure

Open your terminal and navigate to the project root:

```bash
cd /Users/matildaglynn/Documents/projects/onfabric_mvp

# Create backend structure
mkdir -p backend/app
mkdir -p backend/dashboards

# Create __init__.py files
touch backend/app/__init__.py
```

**What we just did**: Created folders for our FastAPI backend.

---

### Step 1.2: Create Backend Requirements

Create a new file `backend/requirements.txt`:

```bash
cat > backend/requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn[standard]==0.24.0
websockets==12.0
python-multipart==0.0.6
pydantic==2.5.0

# Re-use existing project requirements
-e ../
EOF
```

**What this does**: Lists all Python packages our backend needs. The `-e ../` line means "also install the main fabric_dashboard package".

**Git checkpoint 1:**
```bash
git add backend/
git commit -m "chore: initialize backend structure"
```

---

### Step 1.3: Create FastAPI Main App

Create `backend/app/main.py`:

```python
"""
FastAPI backend for Fabric Dashboard Demo.

This is a thin wrapper around the existing Python pipeline.
It provides a WebSocket endpoint for real-time progress updates.
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
from datetime import datetime

app = FastAPI(
    title="Fabric Dashboard API",
    description="Backend for interactive dashboard demo",
    version="0.1.0"
)

# Allow requests from frontend (we'll update this with real domain later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "ok",
        "message": "Fabric Dashboard API",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/health")
async def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "backend": "running",
        "timestamp": datetime.utcnow().isoformat()
    }
```

**What this does**: Creates a basic FastAPI app with health check endpoints.

**Test it:**
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload

# In another terminal, test it:
curl http://localhost:8000/
```

You should see: `{"status":"ok","message":"Fabric Dashboard API",...}`

Press `Ctrl+C` to stop the server.

**Git checkpoint 2:**
```bash
git add backend/app/main.py
git commit -m "feat(backend): add FastAPI app with health check"
```

---

### Step 1.4: Add WebSocket Progress Endpoint

Update `backend/app/main.py` to add the WebSocket endpoint. Add this at the end of the file:

```python
# Add these imports at the top
import random
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.websocket("/ws/generate")
async def websocket_generate_dashboard(websocket: WebSocket):
    """
    WebSocket endpoint for real-time dashboard generation.

    Flow:
    1. Client connects
    2. We send progress updates every 2-3 seconds
    3. We generate the dashboard using existing pipeline
    4. We send the final HTML
    5. Connection closes
    """
    await websocket.accept()
    logger.info("WebSocket connection accepted")

    try:
        # Define generation steps (matches what UI expects)
        steps = [
            {"progress": 0, "step": "connecting", "message": "Connecting to data sources..."},
            {"progress": 10, "step": "fetching", "message": "Fetching your data from Fabric..."},
            {"progress": 25, "step": "analyzing", "message": "Analyzing patterns with Claude..."},
            {"progress": 45, "step": "theme", "message": "Creating personalized theme..."},
            {"progress": 60, "step": "components", "message": "Selecting UI components..."},
            {"progress": 75, "step": "enriching", "message": "Enriching with real-time data..."},
            {"progress": 90, "step": "building", "message": "Building dashboard HTML..."},
        ]

        # Send each step with a delay (simulate real work)
        for step in steps:
            await websocket.send_json(step)
            await asyncio.sleep(2)  # Wait 2 seconds between steps
            logger.info(f"Progress: {step['progress']}% - {step['message']}")

        # For now, send mock HTML
        # We'll replace this with real pipeline in Step 1.6
        mock_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Demo Dashboard</title>
            <style>
                body { font-family: sans-serif; padding: 40px; background: #f5f5f5; }
                .card { background: white; padding: 20px; border-radius: 8px; margin: 20px 0; }
                h1 { color: #4f46e5; }
            </style>
        </head>
        <body>
            <h1>Your Personalized Dashboard</h1>
            <div class="card">
                <h2>🌤️ Weather</h2>
                <p>San Francisco: 72°F, Sunny</p>
            </div>
            <div class="card">
                <h2>📺 Recommended Videos</h2>
                <p>Python Tutorial - Learn in 30 minutes</p>
            </div>
            <div class="card">
                <h2>📅 Upcoming Events</h2>
                <p>Tech Meetup - Tomorrow at 6pm</p>
            </div>
        </body>
        </html>
        """

        # Send completion message with HTML
        await websocket.send_json({
            "progress": 100,
            "step": "complete",
            "message": "Dashboard ready!",
            "html": mock_html
        })

        logger.info("Dashboard generation complete")

    except WebSocketDisconnect:
        logger.info("Client disconnected")
    except Exception as e:
        logger.error(f"Error during generation: {e}")
        await websocket.send_json({
            "error": str(e),
            "message": "Generation failed. Please try again."
        })
    finally:
        await websocket.close()
```

**What this does**:
- Accepts WebSocket connections from the frontend
- Sends progress updates every 2 seconds (simulating work)
- Sends a mock dashboard HTML at the end
- We'll replace the mock HTML with real generation later

**Test it manually** (optional - we'll test properly with frontend):
You can test WebSockets with a tool like `wscat`:
```bash
# Install wscat (optional)
npm install -g wscat

# Test the WebSocket
wscat -c ws://localhost:8000/ws/generate
```

**Git checkpoint 3:**
```bash
git add backend/app/main.py
git commit -m "feat(backend): add WebSocket endpoint for dashboard generation"
```

---

### Step 1.5: Generate Demo Dashboards

Create a script to generate 3 demo dashboards using our existing pipeline.

Create `backend/scripts/generate_demo_dashboards.py`:

```python
"""
Generate demo dashboards for different personas.

This script uses the existing fabric_dashboard pipeline to create
3 pre-generated dashboards that we can serve instantly.
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path so we can import fabric_dashboard
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from fabric_dashboard.core.ui_generator import UIGenerator
from fabric_dashboard.core.dashboard_builder import DashboardBuilder
from fabric_dashboard.core.theme_generator import ThemeGenerator
from fabric_dashboard.models.schemas import Pattern, PersonaProfile, CardSize


async def generate_demo_dashboard(persona_name: str, patterns_data: list):
    """Generate a single demo dashboard."""

    print(f"\n{'='*50}")
    print(f"Generating: {persona_name}")
    print(f"{'='*50}\n")

    # Create patterns from data
    patterns = [
        Pattern(
            pattern_title=p["title"],
            pattern_type=p["type"],
            confidence=p["confidence"],
            evidence=p["evidence"],
            interaction_count=p["interaction_count"]
        )
        for p in patterns_data
    ]

    print(f"✓ Created {len(patterns)} patterns")

    # Create persona profile
    persona = PersonaProfile(
        name=persona_name,
        primary_traits=patterns_data[0]["evidence"][:3],
        communication_style="professional",
        interests=[p["title"] for p in patterns_data[:3]]
    )

    print(f"✓ Created persona: {persona.name}")

    # Generate theme
    theme_gen = ThemeGenerator()
    theme = await theme_gen.generate_theme(patterns, persona)

    print(f"✓ Generated theme: {theme.primary_color}")

    # Generate UI components
    ui_gen = UIGenerator(mock_mode=True)
    components = await ui_gen.generate_components(patterns, persona)

    print(f"✓ Generated {len(components.components)} UI components")

    # Create mock cards (content cards - simplified for demo)
    from fabric_dashboard.models.schemas import Card
    cards = [
        Card(
            title="Welcome to Your Dashboard",
            content="This dashboard was generated based on your digital behavior patterns. It includes personalized widgets and insights tailored to your interests.",
            size=CardSize.MEDIUM,
            position=0
        )
    ]

    print(f"✓ Created {len(cards)} content cards")

    # Build dashboard HTML
    builder = DashboardBuilder()
    html = builder.build_dashboard(
        cards=cards,
        ui_components=components.components,
        theme=theme,
        persona=persona
    )

    print(f"✓ Built dashboard HTML ({len(html)} chars)")

    # Save to file
    output_dir = Path(__file__).parent.parent / "dashboards"
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / f"{persona_name}.html"
    output_file.write_text(html)

    print(f"✓ Saved to: {output_file}")
    print(f"✅ {persona_name} dashboard complete!\n")


async def main():
    """Generate all demo dashboards."""

    print("\n🚀 Generating Demo Dashboards")
    print("This will take about 2-3 minutes...\n")

    # Persona 1: Tech Entrepreneur
    tech_entrepreneur_patterns = [
        {
            "title": "Startup Founding Interest",
            "type": "interest",
            "confidence": 0.9,
            "evidence": ["entrepreneurship", "startups", "venture capital"],
            "interaction_count": 45
        },
        {
            "title": "AI/ML Enthusiasm",
            "type": "interest",
            "confidence": 0.85,
            "evidence": ["artificial intelligence", "machine learning", "LLMs"],
            "interaction_count": 38
        },
        {
            "title": "San Francisco Tech Scene",
            "type": "location",
            "confidence": 0.8,
            "evidence": ["SF", "Bay Area", "Silicon Valley"],
            "interaction_count": 32
        }
    ]

    # Persona 2: Digital Nomad
    digital_nomad_patterns = [
        {
            "title": "Remote Work Lifestyle",
            "type": "interest",
            "confidence": 0.88,
            "evidence": ["remote work", "digital nomad", "coworking"],
            "interaction_count": 41
        },
        {
            "title": "Travel & Exploration",
            "type": "interest",
            "confidence": 0.82,
            "evidence": ["travel", "backpacking", "world tour"],
            "interaction_count": 35
        },
        {
            "title": "Language Learning",
            "type": "skill",
            "confidence": 0.75,
            "evidence": ["Spanish", "French", "polyglot"],
            "interaction_count": 28
        }
    ]

    # Persona 3: Creative Professional
    creative_pro_patterns = [
        {
            "title": "Design & UX",
            "type": "skill",
            "confidence": 0.92,
            "evidence": ["UI design", "Figma", "user experience"],
            "interaction_count": 48
        },
        {
            "title": "Music Production",
            "type": "hobby",
            "confidence": 0.78,
            "evidence": ["Ableton", "synthesizers", "electronic music"],
            "interaction_count": 31
        },
        {
            "title": "Art & Culture",
            "type": "interest",
            "confidence": 0.81,
            "evidence": ["museums", "galleries", "contemporary art"],
            "interaction_count": 34
        }
    ]

    # Generate all three
    await generate_demo_dashboard("tech_entrepreneur", tech_entrepreneur_patterns)
    await generate_demo_dashboard("digital_nomad", digital_nomad_patterns)
    await generate_demo_dashboard("creative_pro", creative_pro_patterns)

    print("\n" + "="*50)
    print("✅ ALL DEMO DASHBOARDS GENERATED!")
    print("="*50)
    print("\nDashboards saved in: backend/dashboards/")
    print("- tech_entrepreneur.html")
    print("- digital_nomad.html")
    print("- creative_pro.html\n")


if __name__ == "__main__":
    asyncio.run(main())
```

**What this does**: Uses our existing pipeline to generate 3 demo dashboards and saves them as HTML files.

**Run it:**
```bash
cd backend

# Make scripts directory
mkdir -p scripts

# Create the file (paste the code above)
# Then run it:
python scripts/generate_demo_dashboards.py
```

**Expected output:**
```
🚀 Generating Demo Dashboards
This will take about 2-3 minutes...

==================================================
Generating: tech_entrepreneur
==================================================

✓ Created 3 patterns
✓ Created persona: tech_entrepreneur
✓ Generated theme: #6366f1
✓ Generated 5 UI components
✓ Created 1 content cards
✓ Built dashboard HTML (45231 chars)
✓ Saved to: backend/dashboards/tech_entrepreneur.html
✅ tech_entrepreneur dashboard complete!

[... similar for other personas ...]

==================================================
✅ ALL DEMO DASHBOARDS GENERATED!
==================================================
```

**Troubleshooting:**
- **Error: "No module named fabric_dashboard"**: Make sure you ran `pip install -e ../` from the backend folder
- **Error: "Config not found"**: That's okay for demo mode, the script will still work

**Git checkpoint 4:**
```bash
git add backend/scripts/generate_demo_dashboards.py
git add backend/dashboards/  # Add generated HTML files
git commit -m "feat(backend): add demo dashboard generator script"
```

---

### Step 1.6: Update WebSocket to Serve Real Dashboards

Now let's update the WebSocket endpoint to serve our pre-generated dashboards instead of mock HTML.

Update `backend/app/main.py` - replace the `mock_html` section with:

```python
# At the top, add this import
from pathlib import Path
import random

# ... existing code ...

@app.websocket("/ws/generate")
async def websocket_generate_dashboard(websocket: WebSocket):
    """WebSocket endpoint for real-time dashboard generation."""
    await websocket.accept()
    logger.info("WebSocket connection accepted")

    try:
        # ... existing steps code stays the same ...

        # Send each step with a delay (simulate real work)
        for step in steps:
            await websocket.send_json(step)
            await asyncio.sleep(2)
            logger.info(f"Progress: {step['progress']}% - {step['message']}")

        # NEW: Choose a random demo dashboard
        dashboards_dir = Path(__file__).parent.parent / "dashboards"
        available_dashboards = list(dashboards_dir.glob("*.html"))

        if not available_dashboards:
            raise FileNotFoundError(
                "No demo dashboards found. Run 'python scripts/generate_demo_dashboards.py' first."
            )

        # Pick random dashboard
        chosen_dashboard = random.choice(available_dashboards)
        logger.info(f"Serving dashboard: {chosen_dashboard.name}")

        # Read the HTML
        html = chosen_dashboard.read_text()

        # Send completion message with real HTML
        await websocket.send_json({
            "progress": 100,
            "step": "complete",
            "message": "Dashboard ready!",
            "html": html,
            "persona": chosen_dashboard.stem  # e.g., "tech_entrepreneur"
        })

        logger.info("Dashboard generation complete")

    except WebSocketDisconnect:
        logger.info("Client disconnected")
    except Exception as e:
        logger.error(f"Error during generation: {e}")
        await websocket.send_json({
            "error": str(e),
            "message": f"Generation failed: {str(e)}"
        })
    finally:
        await websocket.close()
```

**What changed**: Instead of sending mock HTML, we now pick a random pre-generated dashboard and send that.

**Git checkpoint 5:**
```bash
git add backend/app/main.py
git commit -m "feat(backend): serve pre-generated demo dashboards"
```

---

### Step 1.7: Test Backend End-to-End

Let's make sure everything works:

```bash
cd backend

# Start the server
uvicorn app.main:app --reload --port 8000

# Server should start and show:
# INFO:     Uvicorn running on http://127.0.0.1:8000
```

In another terminal:
```bash
# Test health check
curl http://localhost:8000/health

# Expected: {"status":"healthy","backend":"running",...}
```

**Manual WebSocket test** (optional):
```bash
# If you have wscat installed:
wscat -c ws://localhost:8000/ws/generate

# You should see progress messages every 2 seconds
# Then final HTML after ~14 seconds
```

Keep the backend running - we'll need it for the frontend!

---

## Phase 2: Frontend Setup (Days 3-4)

### Step 2.1: Create React App with Vite

Open a **new terminal** (keep backend running in the first one):

```bash
cd /Users/matildaglynn/Documents/projects/onfabric_mvp

# Create frontend with Vite
npm create vite@latest frontend -- --template react-ts

# Navigate into frontend
cd frontend

# Install dependencies
npm install

# Install additional packages we'll need
npm install @tanstack/react-query
```

**What this does**: Creates a new React + TypeScript project using Vite (fast build tool).

**Test it:**
```bash
npm run dev
```

You should see:
```
VITE v5.x.x  ready in 300 ms

➜  Local:   http://localhost:5173/
➜  press h + enter to show help
```

Open http://localhost:5173/ in your browser - you should see the Vite + React welcome page.

Press `Ctrl+C` to stop the dev server.

**Git checkpoint 6:**
```bash
git add frontend/
git commit -m "chore(frontend): initialize React app with Vite"
```

---

### Step 2.2: Install TailwindCSS

```bash
cd frontend

# Install Tailwind
npm install -D tailwindcss postcss autoprefixer

# Initialize Tailwind config
npx tailwindcss init -p
```

This creates `tailwind.config.js`. Update it to:

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

Update `src/index.css` to:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom animations */
@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

.animate-shimmer {
  animation: shimmer 2s infinite;
}

@keyframes gradient-shift {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

.animate-gradient {
  background-size: 200% 200%;
  animation: gradient-shift 15s ease infinite;
}
```

**Test it:**
```bash
npm run dev
```

Open http://localhost:5173/ - the page should still work (maybe different styling).

**Git checkpoint 7:**
```bash
git add frontend/
git commit -m "feat(frontend): add TailwindCSS"
```

---

### Step 2.3: Create App State Management

Create `frontend/src/types.ts`:

```typescript
/**
 * TypeScript types for the app.
 */

export type AppScreen = 'landing' | 'generating' | 'dashboard';

export interface ProgressStep {
  progress: number;
  step: string;
  message: string;
}

export interface GenerationComplete {
  progress: 100;
  step: 'complete';
  message: string;
  html: string;
  persona?: string;
}

export interface WebSocketMessage {
  progress: number;
  step: string;
  message: string;
  html?: string;
  persona?: string;
  error?: string;
}

export interface AppState {
  screen: AppScreen;
  progress: number;
  currentStep: string;
  currentMessage: string;
  dashboardHTML: string | null;
  persona: string | null;
  error: string | null;
}
```

**What this does**: Defines TypeScript types for our app's state. This helps catch bugs!

**Git checkpoint 8:**
```bash
git add frontend/src/types.ts
git commit -m "feat(frontend): add TypeScript types"
```

---

### Step 2.4: Create WebSocket Hook

Create `frontend/src/hooks/useWebSocket.ts`:

```typescript
/**
 * Custom hook for WebSocket connection to backend.
 */

import { useEffect, useRef, useState } from 'react';
import { WebSocketMessage } from '../types';

const WS_URL = 'ws://localhost:8000/ws/generate';

export function useWebSocket() {
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState<WebSocketMessage | null>(null);
  const [error, setError] = useState<string | null>(null);

  const wsRef = useRef<WebSocket | null>(null);

  const connect = () => {
    try {
      console.log('Connecting to WebSocket...', WS_URL);

      const ws = new WebSocket(WS_URL);
      wsRef.current = ws;

      ws.onopen = () => {
        console.log('WebSocket connected');
        setIsConnected(true);
        setError(null);
      };

      ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data) as WebSocketMessage;
          console.log('Received message:', message);
          setLastMessage(message);
        } catch (err) {
          console.error('Failed to parse message:', err);
        }
      };

      ws.onerror = (event) => {
        console.error('WebSocket error:', event);
        setError('Connection error. Is the backend running?');
      };

      ws.onclose = () => {
        console.log('WebSocket disconnected');
        setIsConnected(false);
      };

    } catch (err) {
      console.error('Failed to create WebSocket:', err);
      setError('Failed to connect to backend');
    }
  };

  const disconnect = () => {
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
      setIsConnected(false);
    }
  };

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      disconnect();
    };
  }, []);

  return {
    connect,
    disconnect,
    isConnected,
    lastMessage,
    error,
  };
}
```

**What this does**: Creates a React hook that manages the WebSocket connection. We'll use this to talk to our backend.

**Git checkpoint 9:**
```bash
git add frontend/src/hooks/
git commit -m "feat(frontend): add WebSocket hook"
```

---

### Step 2.5: Create Landing Screen Component

Create `frontend/src/components/Landing.tsx`:

```typescript
/**
 * Landing screen - the first thing users see.
 */

interface LandingProps {
  onGenerate: () => void;
}

export function Landing({ onGenerate }: LandingProps) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-500 animate-gradient flex items-center justify-center p-4">
      <div className="text-center text-white max-w-4xl">
        {/* Logo/Title */}
        <div className="mb-8">
          <h1 className="text-7xl font-bold mb-4 drop-shadow-lg">
            🎨 Fabric
          </h1>
          <h2 className="text-3xl font-semibold opacity-95">
            Your Personalized Dashboard
          </h2>
        </div>

        {/* Tagline */}
        <p className="text-xl mb-12 opacity-90 max-w-2xl mx-auto leading-relaxed">
          AI analyzes your digital behavior. Generates beautiful insights with live widgets. In 20 seconds.
        </p>

        {/* CTA Button */}
        <button
          onClick={onGenerate}
          className="bg-white text-indigo-600 px-12 py-5 rounded-xl text-2xl font-bold hover:scale-105 hover:shadow-2xl transition-all duration-200 active:scale-95"
        >
          Generate Demo Dashboard →
        </button>

        {/* Features */}
        <div className="mt-16 flex flex-wrap gap-8 justify-center">
          <Feature icon="⚡" label="AI-Powered Analysis" />
          <Feature icon="🎯" label="Personalized for You" />
          <Feature icon="📊" label="Live Real-Time Widgets" />
        </div>

        {/* Footer note */}
        <p className="mt-12 text-sm opacity-75">
          Demo mode • No signup required • Takes 20 seconds
        </p>
      </div>
    </div>
  );
}

function Feature({ icon, label }: { icon: string; label: string }) {
  return (
    <div className="flex items-center gap-3 bg-white/10 backdrop-blur-sm px-6 py-3 rounded-lg">
      <span className="text-3xl">{icon}</span>
      <span className="text-lg font-medium">{label}</span>
    </div>
  );
}
```

**What this does**: Creates the landing page UI.

**Git checkpoint 10:**
```bash
git add frontend/src/components/
git commit -m "feat(frontend): add Landing screen component"
```

---

### Step 2.6: Create Progress Screen Component

Create `frontend/src/components/Progress.tsx`:

```typescript
/**
 * Progress screen - shows generation progress.
 */

interface ProgressProps {
  progress: number;
  currentStep: string;
  currentMessage: string;
}

const steps = [
  { id: 'connecting', label: 'Connected to data sources', emoji: '🔌' },
  { id: 'fetching', label: 'Fetched your data', emoji: '📦' },
  { id: 'analyzing', label: 'Analyzed patterns with AI', emoji: '🤖' },
  { id: 'theme', label: 'Created personalized theme', emoji: '🎨' },
  { id: 'components', label: 'Selected UI components', emoji: '🧩' },
  { id: 'enriching', label: 'Enriched with real-time data', emoji: '🌐' },
  { id: 'building', label: 'Built dashboard HTML', emoji: '🏗️' },
];

const funFacts = [
  "Claude is analyzing your behavior patterns to find what matters most to you",
  "We're creating a unique color scheme based on your digital personality",
  "Real-time widgets will show weather, videos, and events personalized for you",
  "Your dashboard will be fully interactive and downloadable as HTML",
  "All processing happens in real-time—this isn't a pre-made template",
  "We use GPT-4 level AI to understand your interests and habits",
];

export function Progress({ progress, currentStep, currentMessage }: ProgressProps) {
  // Rotate fun facts every 5 seconds
  const [factIndex, setFactIndex] = React.useState(0);

  React.useEffect(() => {
    const interval = setInterval(() => {
      setFactIndex((prev) => (prev + 1) % funFacts.length);
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <div className="max-w-2xl w-full">
        {/* Header */}
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-900 mb-3">
            Creating Your Dashboard
          </h2>
          <p className="text-gray-600">
            This takes about 20 seconds...
          </p>
        </div>

        {/* Progress Bar */}
        <div className="mb-8">
          <div className="h-3 bg-gray-200 rounded-full overflow-hidden relative">
            <div
              className="h-full bg-gradient-to-r from-indigo-500 to-purple-500 transition-all duration-500 ease-out relative overflow-hidden"
              style={{ width: `${progress}%` }}
            >
              {/* Shimmer effect */}
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent animate-shimmer" />
            </div>
          </div>
          <p className="text-center text-sm text-gray-600 mt-3 font-medium">
            {progress}% complete
          </p>
        </div>

        {/* Current Step */}
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200 mb-6">
          <div className="flex items-center gap-4">
            <div className="text-4xl animate-pulse">
              {steps.find(s => s.id === currentStep)?.emoji || '⚙️'}
            </div>
            <div className="flex-1">
              <div className="text-lg font-semibold text-gray-900">
                {currentMessage}
              </div>
            </div>
          </div>
        </div>

        {/* Step List */}
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200 mb-6">
          <div className="space-y-3">
            {steps.map((step, index) => {
              const stepProgress = (index / steps.length) * 100;
              const isCompleted = progress > stepProgress;
              const isCurrent = step.id === currentStep;

              return (
                <div
                  key={step.id}
                  className={`flex items-center gap-3 transition-all duration-300 ${
                    isCompleted ? 'opacity-100' : 'opacity-40'
                  }`}
                >
                  <div className="flex-shrink-0 w-6 h-6 flex items-center justify-center">
                    {isCompleted ? (
                      <div className="w-5 h-5 bg-green-500 rounded-full flex items-center justify-center text-white text-xs">
                        ✓
                      </div>
                    ) : isCurrent ? (
                      <div className="w-4 h-4 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
                    ) : (
                      <div className="w-4 h-4 border-2 border-gray-300 rounded-full" />
                    )}
                  </div>
                  <span className={`text-sm ${isCompleted ? 'text-gray-900 font-medium' : 'text-gray-500'}`}>
                    {step.label}
                  </span>
                </div>
              );
            })}
          </div>
        </div>

        {/* Fun Fact */}
        <div className="bg-indigo-50 rounded-xl p-6 border border-indigo-100">
          <p className="text-sm text-indigo-900 leading-relaxed">
            <span className="text-xl mr-2">💡</span>
            {funFacts[factIndex]}
          </p>
        </div>
      </div>
    </div>
  );
}
```

**Add React import at the top:**
```typescript
import React from 'react';
```

**What this does**: Creates the progress screen with a nice progress bar, step indicators, and rotating fun facts.

**Git checkpoint 11:**
```bash
git add frontend/src/components/Progress.tsx
git commit -m "feat(frontend): add Progress screen component"
```

---

### Step 2.7: Create Dashboard Screen Component

Create `frontend/src/components/Dashboard.tsx`:

```typescript
/**
 * Dashboard screen - shows the generated dashboard.
 */

interface DashboardProps {
  html: string;
  onGenerateNew: () => void;
}

export function Dashboard({ html, onGenerateNew }: DashboardProps) {
  const handleDownload = () => {
    // Create a blob from the HTML
    const blob = new Blob([html], { type: 'text/html' });
    const url = URL.createObjectURL(blob);

    // Create download link
    const a = document.createElement('a');
    a.href = url;
    a.download = `fabric-dashboard-${Date.now()}.html`;
    document.body.appendChild(a);
    a.click();

    // Cleanup
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Action Bar */}
      <div className="bg-white border-b border-gray-200 sticky top-0 z-10 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">
              Your Dashboard
            </h2>
            <p className="text-sm text-gray-600">
              🎉 Generated successfully!
            </p>
          </div>

          <div className="flex gap-3">
            <button
              onClick={handleDownload}
              className="bg-indigo-600 text-white px-6 py-2.5 rounded-lg font-medium hover:bg-indigo-700 transition-colors flex items-center gap-2"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              Download HTML
            </button>

            <button
              onClick={onGenerateNew}
              className="border border-gray-300 text-gray-700 px-6 py-2.5 rounded-lg font-medium hover:bg-gray-50 transition-colors flex items-center gap-2"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Generate New
            </button>
          </div>
        </div>
      </div>

      {/* Dashboard Preview */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="bg-white rounded-xl shadow-lg overflow-hidden border border-gray-200">
          <iframe
            srcDoc={html}
            className="w-full h-[800px] border-0"
            title="Dashboard Preview"
            sandbox="allow-scripts allow-same-origin"
          />
        </div>

        {/* Footer */}
        <div className="mt-6 text-center text-sm text-gray-600">
          <p>
            💡 <strong>Tip:</strong> Download the HTML to view offline, or click "Generate New" for a different dashboard
          </p>
        </div>
      </div>
    </div>
  );
}
```

**What this does**: Creates the dashboard preview screen with download and regenerate buttons.

**Git checkpoint 12:**
```bash
git add frontend/src/components/Dashboard.tsx
git commit -m "feat(frontend): add Dashboard screen component"
```

---

### Step 2.8: Wire Everything Together in App.tsx

Replace `frontend/src/App.tsx` with:

```typescript
/**
 * Main App component - orchestrates all screens.
 */

import { useState, useEffect } from 'react';
import { Landing } from './components/Landing';
import { Progress } from './components/Progress';
import { Dashboard } from './components/Dashboard';
import { useWebSocket } from './hooks/useWebSocket';
import type { AppState } from './types';

function App() {
  const { connect, disconnect, lastMessage, error: wsError } = useWebSocket();

  const [state, setState] = useState<AppState>({
    screen: 'landing',
    progress: 0,
    currentStep: 'connecting',
    currentMessage: 'Starting...',
    dashboardHTML: null,
    persona: null,
    error: null,
  });

  // Handle WebSocket messages
  useEffect(() => {
    if (!lastMessage) return;

    if (lastMessage.error) {
      // Error occurred
      setState(prev => ({
        ...prev,
        error: lastMessage.error!,
      }));
      alert(`Error: ${lastMessage.error}`);
      // Go back to landing
      setState(prev => ({ ...prev, screen: 'landing' }));
      return;
    }

    if (lastMessage.step === 'complete' && lastMessage.html) {
      // Generation complete!
      setState(prev => ({
        ...prev,
        screen: 'dashboard',
        progress: 100,
        dashboardHTML: lastMessage.html!,
        persona: lastMessage.persona || null,
      }));
      disconnect();
    } else {
      // Progress update
      setState(prev => ({
        ...prev,
        progress: lastMessage.progress,
        currentStep: lastMessage.step,
        currentMessage: lastMessage.message,
      }));
    }
  }, [lastMessage, disconnect]);

  const handleGenerate = () => {
    setState({
      screen: 'generating',
      progress: 0,
      currentStep: 'connecting',
      currentMessage: 'Connecting to server...',
      dashboardHTML: null,
      persona: null,
      error: null,
    });

    // Connect to WebSocket
    connect();
  };

  const handleGenerateNew = () => {
    setState({
      screen: 'landing',
      progress: 0,
      currentStep: 'connecting',
      currentMessage: 'Starting...',
      dashboardHTML: null,
      persona: null,
      error: null,
    });
  };

  // Show error if WebSocket connection fails
  useEffect(() => {
    if (wsError && state.screen === 'generating') {
      alert(`Connection Error: ${wsError}\n\nMake sure the backend is running:\ncd backend && uvicorn app.main:app --reload`);
      setState(prev => ({ ...prev, screen: 'landing' }));
    }
  }, [wsError, state.screen]);

  // Render current screen
  switch (state.screen) {
    case 'landing':
      return <Landing onGenerate={handleGenerate} />;

    case 'generating':
      return (
        <Progress
          progress={state.progress}
          currentStep={state.currentStep}
          currentMessage={state.currentMessage}
        />
      );

    case 'dashboard':
      return (
        <Dashboard
          html={state.dashboardHTML!}
          onGenerateNew={handleGenerateNew}
        />
      );

    default:
      return <div>Unknown screen</div>;
  }
}

export default App;
```

**What this does**: This is the main app that:
1. Shows landing screen
2. Connects to WebSocket when user clicks "Generate"
3. Shows progress screen with real-time updates
4. Shows dashboard when complete
5. Handles errors

**Clean up unused files:**
```bash
cd frontend/src

# Remove default Vite files we don't need
rm App.css
```

**Update `frontend/src/main.tsx`** (should already be mostly correct, but let's make sure):

```typescript
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
```

**Git checkpoint 13:**
```bash
git add frontend/src/
git commit -m "feat(frontend): wire all components together in App"
```

---

### Step 2.9: Test End-to-End

Now let's test the complete flow!

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Browser:**
1. Open http://localhost:5173/
2. You should see the landing page with gradient background
3. Click "Generate Demo Dashboard"
4. You should see:
   - Progress bar animating
   - Steps being checked off
   - Fun facts rotating
   - After ~14 seconds, dashboard appears
5. Click "Download HTML" - should download a file
6. Click "Generate New" - should go back to landing

**Troubleshooting:**

**Problem**: "Connection Error" alert
- **Solution**: Make sure backend is running on port 8000

**Problem**: "No demo dashboards found"
- **Solution**: Run `python backend/scripts/generate_demo_dashboards.py`

**Problem**: Blank dashboard preview
- **Solution**: Check browser console for errors

**Problem**: Progress stuck at 0%
- **Solution**: Check backend terminal for errors

**If everything works:** 🎉 Success! You have a working demo!

**Git checkpoint 14:**
```bash
git add -A
git commit -m "feat: complete interactive demo MVP (local)"
```

---

## Phase 3: Deployment (Days 5-6)

### Step 3.1: Prepare Backend for Railway

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements first (for layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY app/ /app/app/
COPY dashboards/ /app/dashboards/

# Expose port (Railway sets this via $PORT)
EXPOSE 8000

# Start server
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
```

Create `backend/.dockerignore`:
```
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
.git/
.gitignore
*.md
scripts/
```

**Git checkpoint 15:**
```bash
git add backend/Dockerfile backend/.dockerignore
git commit -m "chore(backend): add Docker configuration for deployment"
```

---

### Step 3.2: Update Backend for Production

Update `backend/app/main.py` - change CORS settings for production:

```python
# Update CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Local development
        "https://demo.fabricdash.com",  # Production (update with your domain)
        "https://*.vercel.app",  # Vercel preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Git checkpoint 16:**
```bash
git add backend/app/main.py
git commit -m "chore(backend): configure CORS for production"
```

---

### Step 3.3: Deploy Backend to Railway

**Install Railway CLI:**
```bash
npm install -g @railway/cli
```

**Deploy:**
```bash
cd backend

# Login to Railway
railway login

# Create new project
railway init

# Deploy
railway up
```

Railway will:
1. Build your Docker container
2. Deploy it
3. Give you a URL like `https://your-app.up.railway.app`

**Note your backend URL** - we'll need it for the frontend!

---

### Step 3.4: Update Frontend for Production

Update `frontend/src/hooks/useWebSocket.ts`:

```typescript
// At the top, detect environment
const WS_URL = import.meta.env.PROD
  ? 'wss://your-app.up.railway.app/ws/generate'  // UPDATE THIS with your Railway URL
  : 'ws://localhost:8000/ws/generate';
```

**Replace `your-app.up.railway.app` with your actual Railway URL!**

**Git checkpoint 17:**
```bash
git add frontend/src/hooks/useWebSocket.ts
git commit -m "chore(frontend): configure WebSocket URL for production"
```

---

### Step 3.5: Deploy Frontend to Vercel

**Install Vercel CLI:**
```bash
npm install -g vercel
```

**Deploy:**
```bash
cd frontend

# Login to Vercel
vercel login

# Deploy to production
vercel --prod
```

Vercel will:
1. Build your React app
2. Deploy to CDN
3. Give you a URL like `https://your-app.vercel.app`

**Add custom domain** (optional):
```bash
vercel domains add demo.fabricdash.com
```

---

### Step 3.6: Test Production

Visit your Vercel URL and test:
1. Landing page loads
2. Can generate dashboard
3. Progress updates work
4. Dashboard displays
5. Download works

**If WebSocket fails:**
- Check Railway logs: `railway logs`
- Make sure Railway URL is correct in frontend
- Check CORS settings in backend

---

## Phase 4: Polish & Launch (Day 7)

### Step 4.1: Add Error Boundaries

Create `frontend/src/components/ErrorBoundary.tsx`:

```typescript
import React, { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Uncaught error:', error, errorInfo);
  }

  public render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
          <div className="max-w-md w-full bg-white rounded-xl shadow-lg p-8 text-center">
            <div className="text-6xl mb-4">😞</div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              Oops! Something went wrong
            </h2>
            <p className="text-gray-600 mb-6">
              {this.state.error?.message || 'An unexpected error occurred'}
            </p>
            <button
              onClick={() => window.location.reload()}
              className="bg-indigo-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-indigo-700 transition-colors"
            >
              Reload Page
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
```

Wrap your app in `frontend/src/main.tsx`:

```typescript
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import { ErrorBoundary } from './components/ErrorBoundary.tsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  </React.StrictMode>,
)
```

**Git checkpoint 18:**
```bash
git add frontend/src/
git commit -m "feat(frontend): add error boundary for crash recovery"
```

---

### Step 4.2: Add Analytics (PostHog)

Sign up at https://posthog.com (free tier)

Install PostHog:
```bash
cd frontend
npm install posthog-js
```

Create `frontend/src/lib/analytics.ts`:

```typescript
import posthog from 'posthog-js';

const POSTHOG_KEY = 'YOUR_POSTHOG_KEY';  // Get from PostHog dashboard
const POSTHOG_HOST = 'https://app.posthog.com';

// Initialize only in production
if (import.meta.env.PROD && POSTHOG_KEY !== 'YOUR_POSTHOG_KEY') {
  posthog.init(POSTHOG_KEY, {
    api_host: POSTHOG_HOST,
    autocapture: false,  // Manual tracking only
  });
}

export const analytics = {
  track: (event: string, properties?: Record<string, any>) => {
    if (import.meta.env.PROD) {
      posthog.capture(event, properties);
    } else {
      console.log('Analytics (dev):', event, properties);
    }
  },
};
```

Add tracking to `frontend/src/App.tsx`:

```typescript
import { analytics } from './lib/analytics';

// In handleGenerate:
const handleGenerate = () => {
  analytics.track('demo_generation_started');
  // ... rest of code
};

// When generation completes (in useEffect):
if (lastMessage.step === 'complete') {
  analytics.track('demo_generation_completed', {
    duration_seconds: Math.round(lastMessage.progress / 100 * 20),
  });
  // ... rest of code
}

// In handleDownload (Dashboard component):
const handleDownload = () => {
  analytics.track('dashboard_downloaded');
  // ... rest of code
};
```

**Git checkpoint 19:**
```bash
git add frontend/
git commit -m "feat(frontend): add analytics tracking with PostHog"
```

---

### Step 4.3: Create README

Create `README.md` in project root:

```markdown
# Fabric Intelligence Dashboard - Interactive Demo

Generate personalized, AI-powered dashboards from your digital behavior.

🌐 **Live Demo**: https://demo.fabricdash.com

## Features

- ⚡ **AI-Powered**: Claude analyzes your patterns
- 🎯 **Personalized**: Unique dashboards for each user
- 📊 **Live Widgets**: Real-time weather, videos, events
- 🎨 **Beautiful Design**: Tailwind CSS responsive UI
- 📥 **Downloadable**: Get your dashboard as HTML

## Tech Stack

### Frontend
- React 18 + TypeScript
- Vite
- TailwindCSS
- WebSockets

### Backend
- FastAPI (Python 3.11)
- WebSocket support
- Existing Fabric Dashboard pipeline

## Local Development

### Prerequisites
- Python 3.11+
- Node.js 18+

### Backend Setup

\`\`\`bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Generate demo dashboards
python scripts/generate_demo_dashboards.py

# Run server
uvicorn app.main:app --reload --port 8000
\`\`\`

### Frontend Setup

\`\`\`bash
cd frontend

# Install dependencies
npm install

# Run dev server
npm run dev
\`\`\`

Visit http://localhost:5173/

## Deployment

- **Frontend**: Vercel (automatic from main branch)
- **Backend**: Railway (Docker deployment)

## Project Structure

\`\`\`
├── backend/           # FastAPI WebSocket server
│   ├── app/
│   ├── dashboards/    # Pre-generated demo dashboards
│   └── scripts/
├── frontend/          # React + TypeScript UI
│   └── src/
└── fabric_dashboard/  # Core Python pipeline
\`\`\`

## License

MIT
```

**Git checkpoint 20:**
```bash
git add README.md
git commit -m "docs: add comprehensive README"
```

---

### Step 4.4: Final Deploy

```bash
# Deploy backend
cd backend
railway up

# Deploy frontend
cd frontend
vercel --prod

# Push to GitHub
git push origin main
```

---

## 🎉 You're Done!

You now have:
- ✅ Working local development environment
- ✅ Backend deployed on Railway
- ✅ Frontend deployed on Vercel
- ✅ Analytics tracking
- ✅ Error handling
- ✅ Beautiful UI

**Share your demo:**
- Tweet: "Just built an AI-powered dashboard generator in 1 week! 🚀 [link]"
- LinkedIn: Post with demo video
- Show HN: "Show HN: AI-generated personalized dashboards"

---

## Troubleshooting Common Issues

### Issue: "Module not found" errors
**Solution:** Make sure you ran `npm install` in frontend folder

### Issue: WebSocket connection fails
**Solution:**
1. Check backend is running: `curl http://localhost:8000/health`
2. Check WebSocket URL in `useWebSocket.ts`
3. Check CORS settings in backend

### Issue: Dashboard doesn't show
**Solution:**
1. Check browser console for errors
2. Make sure dashboards were generated: `ls backend/dashboards/`
3. Check backend logs for errors

### Issue: "No demo dashboards found"
**Solution:** Run `python backend/scripts/generate_demo_dashboards.py`

### Issue: Blank screen after generation
**Solution:**
1. Check if HTML is valid: open downloaded file in browser
2. Check iframe sandbox settings
3. Check browser console

---

## Next Steps

**Want to add real API key input?**
1. Add form to Landing screen
2. Pass keys to backend in WebSocket message
3. Update backend to use real API keys instead of mock mode

**Want to add user accounts?**
1. Add Clerk or Auth0 for authentication
2. Store dashboards in database (PostgreSQL)
3. Add dashboard history page

**Want better performance?**
1. Add Redis caching for API responses
2. Pre-generate more dashboards
3. Use Celery for background tasks

---

## Getting Help

**Stuck?** Check:
1. Browser console (F12)
2. Backend logs (`railway logs` or terminal output)
3. GitHub Issues

**Need changes?**
- Frontend code: `frontend/src/`
- Backend code: `backend/app/`
- Dashboard generation: `fabric_dashboard/`

---

*This guide was created for junior developers. If something is unclear, please open an issue!*
