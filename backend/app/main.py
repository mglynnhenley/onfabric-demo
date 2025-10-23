"""FastAPI backend for Fabric Dashboard demo."""

import asyncio
import json
from pathlib import Path
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Fabric Dashboard Demo API")

# CORS configuration
# This allows our React frontend (running on port 5173 or 3000) to talk to our backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint - use this to verify the server is running."""
    return {"status": "healthy", "service": "fabric-dashboard-demo"}


@app.websocket("/ws/generate/{persona}")
async def websocket_generate_dashboard(websocket: WebSocket, persona: str):
    """
    WebSocket endpoint for real-time dashboard generation.

    How it works:
    1. Frontend connects to this endpoint with a persona name
    2. We accept the connection
    3. We send progress updates as JSON messages
    4. We send the final HTML dashboard
    5. We close the connection

    Args:
        websocket: The WebSocket connection object
        persona: Which demo persona to generate (e.g., "fitness-enthusiast")
    """
    # Step 1: Accept the incoming WebSocket connection
    await websocket.accept()

    try:
        # For now, we'll simulate the generation process
        # Later, we'll replace this with real dashboard generation

        # Step 2: Send progress updates
        # Each update is a JSON object with a "type" field

        # 25% - Starting
        await websocket.send_text(json.dumps({
            "type": "progress",
            "percent": 25,
            "message": "Analyzing your digital patterns..."
        }))
        await asyncio.sleep(1)  # Simulate work taking time

        # 50% - Halfway
        await websocket.send_text(json.dumps({
            "type": "progress",
            "percent": 50,
            "message": "Generating personalized insights..."
        }))
        await asyncio.sleep(1)

        # 75% - Almost done
        await websocket.send_text(json.dumps({
            "type": "progress",
            "percent": 75,
            "message": "Creating your beautiful dashboard..."
        }))
        await asyncio.sleep(1)

        # Step 3: Load the pre-generated dashboard HTML file
        # The files are in backend/dashboards/{persona}.html
        # For example: backend/dashboards/fitness-enthusiast.html

        # Get the path to the dashboard file
        dashboards_dir = Path(__file__).parent.parent / "dashboards"
        dashboard_file = dashboards_dir / f"{persona}.html"

        # Check if the file exists
        if not dashboard_file.exists():
            # If the persona doesn't exist, send an error
            await websocket.send_text(json.dumps({
                "type": "error",
                "message": f"Dashboard for '{persona}' not found. Valid options: fitness-enthusiast, creative-professional, tech-learner"
            }))
            return

        # Read the HTML file
        # This loads the entire pre-generated dashboard
        dashboard_html = dashboard_file.read_text()

        # Send the real dashboard HTML to the frontend
        await websocket.send_text(json.dumps({
            "type": "complete",
            "html": dashboard_html
        }))

        print(f"✓ Sent {persona} dashboard ({len(dashboard_html):,} characters)")

    except WebSocketDisconnect:
        # This happens if the user closes their browser or navigates away
        # It's normal, not an error
        print(f"Client disconnected from {persona} generation")
    except Exception as e:
        # If something goes wrong, send an error message
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": f"Error generating dashboard: {str(e)}"
        }))
