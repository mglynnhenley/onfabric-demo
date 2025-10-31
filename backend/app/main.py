"""
FastAPI backend for Fabric Dashboard demo.

This backend runs the ACTUAL Python pipeline with mock data
and streams real progress updates via WebSocket.
"""

import asyncio
import json
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Load environment variables from .env file in project root
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)

from app.services.pipeline_service import PipelineService
from app.test_data import get_mock_ui_components, get_mock_persona, get_mock_color_scheme

app = FastAPI(title="Fabric Dashboard Demo API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "fabric-dashboard-demo"}


@app.get("/test/widgets")
async def test_widgets():
    """
    Test endpoint that returns mock dashboard data with all 7 widget types.

    This bypasses the AI pipeline and returns pre-built mock data to test
    that the frontend can render all widget types correctly.

    Returns:
        JSONResponse with complete dashboard data including all widget types
    """
    import sys
    from pathlib import Path

    # Add parent directory to path to import fabric_dashboard
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))

    from fabric_dashboard.core.dashboard_builder import DashboardBuilder
    from fabric_dashboard.core.theme_generator import ThemeGenerator
    from fabric_dashboard.models.schemas import PersonaProfile, ColorScheme

    try:
        # Get mock data
        mock_components = get_mock_ui_components()
        mock_persona_dict = get_mock_persona()
        mock_color_dict = get_mock_color_scheme()

        # Convert dicts to Pydantic models
        persona = PersonaProfile(**mock_persona_dict)
        color_scheme = ColorScheme(**mock_color_dict)

        # Run color scheme through contrast validator to ensure readability
        theme_gen = ThemeGenerator(mock_mode=True)  # Don't need LLM, just using contrast methods
        color_scheme = theme_gen._ensure_readable_contrast(color_scheme)
        print(f"✓ Applied contrast validation to mock theme")

        # Convert UI components to widgets directly
        builder = DashboardBuilder()

        # Build widgets from components
        widgets = []
        for i, component in enumerate(mock_components):
            widget = builder._convert_ui_component_to_widget(component, priority=i+1)
            if widget:
                widgets.append(widget)

        # Create dashboard JSON manually
        from fabric_dashboard.models.schemas import DashboardJSON
        from datetime import datetime

        dashboard_json = DashboardJSON(
            id=f"test-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            generated_at=datetime.now(),
            widgets=widgets,
            theme=color_scheme,
            persona=persona,
        )

        # Convert to dict for JSON response
        dashboard_dict = dashboard_json.model_dump(mode='json')

        print(f"✓ Test dashboard generated with {len(dashboard_dict['widgets'])} widgets:")
        for widget in dashboard_dict['widgets']:
            print(f"  - {widget['type']}: {widget['data'].get('title', 'N/A')}")

        return JSONResponse(content=dashboard_dict)

    except Exception as e:
        print(f"✗ Error generating test dashboard: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "message": "Failed to generate test dashboard"}
        )


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
        # Use mock mode for faster generation without real API calls
        pipeline = PipelineService(mock_mode=True)

        # Define progress callback to send updates via WebSocket
        async def send_progress(data: dict):
            """Send progress update to frontend."""
            await websocket.send_text(json.dumps(data))
            print(f"  → {data.get('step')}: {data.get('percent')}% - {data.get('message')}")

        # Run the actual pipeline (returns both HTML and JSON)
        html, dashboard_json = await pipeline.generate_dashboard(
            persona=persona,
            progress_callback=send_progress,
        )

        # Convert DashboardJSON to dict for JSON serialization
        dashboard_dict = dashboard_json.model_dump(mode='json')

        # LAYER 3: Verify theme in WebSocket message
        print("")
        print("🔍 LAYER 3: THEME IN WEBSOCKET MESSAGE")
        print(f"  Has 'theme' key: {'theme' in dashboard_dict}")
        if 'theme' in dashboard_dict:
            theme = dashboard_dict['theme']
            print(f"  Theme primary: {theme.get('primary')}")
            print(f"  Theme bg type: {theme.get('background_theme', {}).get('type')}")
            bg_theme = theme.get('background_theme', {})
            if bg_theme.get('gradient'):
                print(f"  Gradient colors: {bg_theme['gradient'].get('colors')}")
            elif bg_theme.get('color'):
                print(f"  BG color: {bg_theme.get('color')}")
        print("")

        # Send complete message with dashboard data
        await websocket.send_text(json.dumps({
            "type": "complete",
            "html": html,  # Backward compatibility
            "dashboard": dashboard_dict,  # New JSON format
            "persona": persona,
        }))

        widget_count = len(dashboard_dict["widgets"])
        print(f"✓ Dashboard generated for {persona} ({widget_count} widgets, {len(html):,} chars HTML)")

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
