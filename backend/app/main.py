"""
FastAPI backend for Fabric Dashboard demo.

This backend runs the ACTUAL Python pipeline with mock data
and streams real progress updates via WebSocket.
"""

import asyncio
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from app.services.pipeline_service import PipelineService

app = FastAPI(title="Fabric Dashboard Demo API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "fabric-dashboard-demo"}


@app.websocket("/ws/generate/{persona}")
async def websocket_generate_dashboard(websocket: WebSocket, persona: str):
    """
    WebSocket endpoint for real-time dashboard generation.

    This runs the ACTUAL Python pipeline (not pre-generated HTML).
    Progress updates are streamed as the AI works.

    Args:
        websocket: WebSocket connection
        persona: Persona identifier (e.g., 'fitness-enthusiast')
    """
    await websocket.accept()
    print(f"✓ WebSocket connected for {persona}")

    try:
        pipeline = PipelineService()

        # Define progress callback to send updates via WebSocket
        async def send_progress(data: dict):
            """Send progress update to frontend."""
            await websocket.send_text(json.dumps(data))
            print(f"  → {data.get('step')}: {data.get('percent')}% - {data.get('message')}")

        # Run the actual pipeline
        html = await pipeline.generate_dashboard(
            persona=persona,
            progress_callback=send_progress,
        )

        # Send complete message with final HTML
        await websocket.send_text(json.dumps({
            "type": "complete",
            "html": html,
            "persona": persona,
        }))

        print(f"✓ Dashboard generated for {persona} ({len(html):,} characters)")

    except WebSocketDisconnect:
        print(f"Client disconnected from {persona} generation")
    except FileNotFoundError as e:
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": f"Persona '{persona}' not found. Try: fitness-enthusiast, creative-professional, tech-learner, remote-worker"
        }))
    except Exception as e:
        print(f"✗ Error generating {persona}: {e}")
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": f"Generation failed: {str(e)}"
        }))
    finally:
        await websocket.close()
