"""FastAPI backend for Fabric Dashboard demo."""

import asyncio
import json
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

        # Step 3: Send the final HTML dashboard
        # For now, this is mock HTML
        # Later, we'll generate real dashboards here
        mock_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Dashboard for {persona}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    padding: 40px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                }}
                .container {{
                    max-width: 800px;
                    margin: 0 auto;
                    background: rgba(255,255,255,0.1);
                    padding: 40px;
                    border-radius: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Dashboard Generated!</h1>
                <p>Persona: <strong>{persona}</strong></p>
                <p>This is a mock dashboard. Soon we'll generate real personalized content here.</p>
            </div>
        </body>
        </html>
        """

        await websocket.send_text(json.dumps({
            "type": "complete",
            "html": mock_html
        }))

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
