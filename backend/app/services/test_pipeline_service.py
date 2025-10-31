"""Unit tests for PipelineService.

These tests verify the pipeline data flow from backend to frontend
using mock mode - no real AI or API calls are made.
"""

import pytest
from unittest.mock import AsyncMock

from app.services.pipeline_service import PipelineService


@pytest.fixture
def mock_progress_callback():
    """Create a mock progress callback."""
    return AsyncMock()


class TestPipelineService:
    """Test suite for PipelineService."""

    def test_pipeline_service_initialization_mock_mode(self):
        """Test PipelineService initializes in mock mode."""
        service = PipelineService(mock_mode=True)

        assert service.mock_mode is True
        assert service.persona_fixtures_dir.exists()

    def test_pipeline_service_initialization_real_mode(self):
        """Test PipelineService initializes in real mode."""
        service = PipelineService(mock_mode=False)

        assert service.mock_mode is False

    @pytest.mark.asyncio
    async def test_generate_dashboard_mock_mode(self, mock_progress_callback):
        """Test dashboard generation in mock mode.

        This test verifies:
        1. Pipeline completes without errors
        2. Returns valid HTML and dashboard JSON
        3. All components use mock mode (no real AI/API calls)
        4. Progress callbacks are sent
        5. Theme data is present in dashboard JSON
        """
        service = PipelineService(mock_mode=True)

        # Generate dashboard with mock data
        html, dashboard_json = await service.generate_dashboard(
            persona="fitness-enthusiast",
            progress_callback=mock_progress_callback,
        )

        # Verify HTML was generated
        assert html is not None
        assert isinstance(html, str)
        assert len(html) > 0

        # Verify dashboard JSON structure
        assert dashboard_json is not None
        assert hasattr(dashboard_json, "id")
        assert hasattr(dashboard_json, "widgets")
        assert hasattr(dashboard_json, "theme")
        assert hasattr(dashboard_json, "persona")

        # Verify theme data is present and valid
        theme = dashboard_json.theme
        assert theme.primary.startswith("#")
        assert theme.secondary.startswith("#")
        assert theme.accent.startswith("#")
        assert theme.foreground.startswith("#")
        assert theme.muted.startswith("#")
        assert theme.background_theme is not None
        assert theme.fonts is not None

        # Verify fonts are present
        assert theme.fonts.heading
        assert theme.fonts.body
        assert theme.fonts.mono
        assert theme.fonts.heading_url.startswith("http")
        assert theme.fonts.body_url.startswith("http")
        assert theme.fonts.mono_url.startswith("http")

        # Verify background theme
        bg = theme.background_theme
        assert bg.type in ["solid", "gradient", "pattern", "animated"]
        assert bg.card_background

        # Verify widgets were generated
        assert len(dashboard_json.widgets) > 0

        # Verify persona data
        assert dashboard_json.persona is not None
        assert dashboard_json.persona.writing_style
        assert len(dashboard_json.persona.interests) > 0

        # Verify progress callbacks were called
        assert mock_progress_callback.called
        assert mock_progress_callback.call_count >= 5  # At least 5 progress updates

        # Verify "complete" message was sent
        calls = mock_progress_callback.call_args_list
        complete_calls = [
            call for call in calls if call[0][0].get("type") == "progress" and call[0][0].get("step") == "complete"
        ]
        assert len(complete_calls) > 0

    @pytest.mark.asyncio
    async def test_generate_dashboard_without_callback(self):
        """Test dashboard generation works without progress callback."""
        service = PipelineService(mock_mode=True)

        # Should not raise error even without callback
        html, dashboard_json = await service.generate_dashboard(
            persona="creative-professional",
            progress_callback=None,
        )

        assert html is not None
        assert dashboard_json is not None

    @pytest.mark.asyncio
    async def test_theme_data_flow(self, mock_progress_callback):
        """Test that theme data flows correctly from backend to dashboard JSON.

        This specifically tests the theme generation → dashboard JSON flow
        to ensure frontend receives all required theme data.
        """
        service = PipelineService(mock_mode=True)

        _, dashboard_json = await service.generate_dashboard(
            persona="tech-entrepreneur",
            progress_callback=mock_progress_callback,
        )

        # Theme should be included in dashboard JSON
        assert hasattr(dashboard_json, "theme")

        theme = dashboard_json.theme

        # All required color fields
        required_colors = [
            "primary",
            "secondary",
            "accent",
            "foreground",
            "muted",
            "success",
            "warning",
            "destructive",
        ]

        for color_field in required_colors:
            assert hasattr(theme, color_field)
            color_value = getattr(theme, color_field)
            assert color_value.startswith("#")
            assert len(color_value) == 7  # #RRGGBB format

        # Metadata fields
        assert hasattr(theme, "mood")
        assert len(theme.mood) > 0
        assert hasattr(theme, "rationale")

        # Font scheme
        assert hasattr(theme, "fonts")
        assert hasattr(theme.fonts, "heading")
        assert hasattr(theme.fonts, "body")
        assert hasattr(theme.fonts, "mono")

        # Background theme
        assert hasattr(theme, "background_theme")
        assert hasattr(theme.background_theme, "type")
        assert hasattr(theme.background_theme, "card_background")
        assert hasattr(theme.background_theme, "card_backdrop_blur")
