"""Dashboard builder module for assembling final HTML output."""

import markdown
import time
from datetime import datetime, timezone
from typing import Optional

from fabric_dashboard.models.schemas import (
    CardContent,
    CardSize,
    ColorScheme,
    Dashboard,
    DashboardJSON,
    DataSummary,
    PersonaProfile,
    Widget,
)
from fabric_dashboard.models.ui_components import UIComponentType
from fabric_dashboard.utils import logger


class DashboardBuilder:
    """Builds complete HTML dashboard from generated content."""

    def __init__(self):
        """Initialize dashboard builder."""
        pass

    def build(
        self,
        cards: list[CardContent],
        ui_components: Optional[list[UIComponentType]] = None,
        persona: PersonaProfile = None,
        color_scheme: ColorScheme = None,
        title: Optional[str] = None,
        user_name: str = "User",
        data_summary: Optional[DataSummary] = None,
        generation_time_seconds: float = 0.0,
    ) -> Dashboard:
        """
        Build complete dashboard from cards, persona, and theme.

        Args:
            cards: List of 4-10 CardContent objects.
            persona: PersonaProfile for personalization.
            color_scheme: ColorScheme for visual theming.
            title: Optional custom title (default: generated from persona).
            user_name: User's display name (default: "User").
            data_summary: Optional data summary (default: minimal summary).
            generation_time_seconds: Time taken to generate (default: 0.0).

        Returns:
            Dashboard model with complete HTML and metadata.
        """
        if not 4 <= len(cards) <= 10:
            raise ValueError(f"Expected 4-10 cards, got {len(cards)}")

        # Default to empty list if no UI components provided
        if ui_components is None:
            ui_components = []

        logger.info(f"Building dashboard with {len(cards)} cards and {len(ui_components)} UI components")

        # Generate HTML
        html = self._generate_html(cards, ui_components, persona, color_scheme, title)

        # Create minimal data summary if not provided
        if data_summary is None:
            data_summary = DataSummary(
                total_interactions=100,  # Placeholder
                date_range_start=datetime.now(timezone.utc),
                date_range_end=datetime.now(timezone.utc),
                days_analyzed=30,
                platforms=["instagram"],
            )

        # Create dashboard model
        dashboard = Dashboard(
            user_name=user_name,
            generated_at=datetime.now(timezone.utc),
            color_scheme=color_scheme,
            cards=cards,
            persona=persona,
            data_summary=data_summary,
            generation_time_seconds=generation_time_seconds,
            metadata={"html": html},  # Store HTML in metadata
        )

        logger.success("Dashboard built successfully")
        return dashboard

    def build_json(
        self,
        cards: list[CardContent],
        ui_components: Optional[list[UIComponentType]] = None,
        persona: PersonaProfile = None,
        color_scheme: ColorScheme = None,
    ) -> DashboardJSON:
        """
        Build dashboard in JSON format for frontend rendering.

        Args:
            cards: List of 4-10 CardContent objects.
            ui_components: Optional list of UI components.
            persona: PersonaProfile for personalization.
            color_scheme: ColorScheme for visual theming.

        Returns:
            DashboardJSON with widgets, theme, and persona.
        """
        if not 4 <= len(cards) <= 10:
            raise ValueError(f"Expected 4-10 cards, got {len(cards)}")

        # Default to empty list if no UI components provided
        if ui_components is None:
            ui_components = []

        logger.info(
            f"Building JSON dashboard with {len(cards)} cards and {len(ui_components)} UI components"
        )

        widgets = []

        # Convert UI components to widgets FIRST (show interactive widgets at top)
        for idx, component in enumerate(ui_components):
            widget = self._convert_ui_component_to_widget(component, idx + 1)
            if widget:
                widgets.append(widget)

        # Convert content cards to widgets LAST (show at bottom)
        for idx, card in enumerate(cards):
            widget = Widget(
                id=f"article-{idx}",
                type="article-card",
                size=self._determine_card_size(card),
                priority=len(ui_components) + idx + 1,
                data={
                    "title": card.title,
                    "excerpt": card.description,
                    "content": card.body,
                    "readingTime": f"{card.reading_time_minutes} min",
                    "sources": [{"title": s, "url": s} for s in card.sources]
                    if card.sources
                    else [],
                },
            )
            widgets.append(widget)

        dashboard_json = DashboardJSON(
            id=f"dash_{int(time.time())}",
            generated_at=datetime.now(timezone.utc),
            widgets=widgets,
            theme=color_scheme,
            persona=persona,
        )

        logger.success("JSON dashboard built successfully")
        return dashboard_json

    def _determine_card_size(self, card: CardContent) -> str:
        """Determine widget size based on content length."""
        if card.reading_time_minutes < 2:
            return "small"
        elif card.reading_time_minutes < 5:
            return "medium"
        else:
            return "large"

    def _convert_ui_component_to_widget(
        self, component: UIComponentType, priority: int
    ) -> Optional[Widget]:
        """Convert UIComponent to Widget format."""
        from fabric_dashboard.models.ui_components import (
            ContentCard,
            EventCalendar,
            InfoCard,
            MapCard,
            TaskList,
            VideoFeed,
        )

        if isinstance(component, InfoCard):
            # Extract enriched weather data (matches _render_info_card pattern)
            if component.enriched_data:
                current = component.enriched_data.get("current", {})
                temp = current.get("temperature", "--")
                temp_unit = current.get("temp_unit", "°")
                condition = current.get("condition", "Unknown")
                location_display = component.enriched_data.get("location", component.location)
            else:
                temp = "--"
                temp_unit = "°"
                condition = "Loading..."
                location_display = component.location

            return Widget(
                id=f"info-{priority}",
                type="info-card",
                size="small",
                priority=priority,
                data={
                    "title": component.title,
                    "value": f"{temp}{temp_unit}",
                    "subtitle": condition,
                    "location": location_display,
                },
            )
        elif isinstance(component, EventCalendar):
            return Widget(
                id=f"calendar-{priority}",
                type="calendar-card",
                size="large",
                priority=priority,
                data={
                    "title": component.title,
                    "query": component.search_query,
                    "events": [
                        {
                            "name": e.get("name", ""),
                            "date": e.get("date", ""),
                            "location": (
                                e.get("venue").get("name")
                                if isinstance(e.get("venue"), dict)
                                else e.get("venue", "")
                            ) if e.get("venue") else "",
                            "url": e.get("url", ""),
                        }
                        for e in (component.enriched_events or [])
                    ],
                },
            )
        elif isinstance(component, MapCard):
            # Use markers field (matches MapCard schema)
            return Widget(
                id=f"map-{priority}",
                type="map-card",
                size="medium",
                priority=priority,
                data={
                    "title": component.title,
                    "center": {
                        "lat": component.center_lat,
                        "lng": component.center_lng,
                    },
                    "zoom": component.zoom,
                    "markers": [
                        {
                            "lat": m.lat,
                            "lng": m.lng,
                            "title": m.title,
                            "description": m.description or "",
                        }
                        for m in component.markers
                    ],
                },
            )
        elif isinstance(component, VideoFeed):
            return Widget(
                id=f"video-{priority}",
                type="video-card",
                size="medium",
                priority=priority,
                data={
                    "title": component.title,
                    "query": component.search_query,
                    "videos": [
                        {
                            "title": v.get("title", ""),
                            "thumbnail": v.get("thumbnail", ""),
                            "url": v.get("url", ""),
                        }
                        for v in (component.enriched_videos or [])
                    ],
                },
            )
        elif isinstance(component, TaskList):
            return Widget(
                id=f"task-{priority}",
                type="task-card",
                size="small",
                priority=priority,
                data={
                    "title": component.title,
                    "tasks": component.tasks or [],
                },
            )
        elif isinstance(component, ContentCard):
            return Widget(
                id=f"content-{priority}",
                type="content-card",
                size="medium",
                priority=priority,
                data={
                    "title": component.article_title,
                    "overview": component.overview,
                    "url": component.url,
                    "sourceName": component.source_name,
                    "publishedDate": component.published_date,
                },
            )

        return None

    def _generate_html(
        self,
        cards: list[CardContent],
        ui_components: list[UIComponentType],
        persona: PersonaProfile,
        color_scheme: ColorScheme,
        title: Optional[str],
    ) -> str:
        """
        Generate complete HTML document.

        Args:
            cards: List of CardContent objects.
            ui_components: List of UI component objects.
            persona: PersonaProfile.
            color_scheme: ColorScheme.
            title: Optional title.

        Returns:
            Complete HTML string.
        """
        # Generate title
        if not title:
            title = self._generate_title(persona)

        # Build HTML sections
        head = self._build_head(title, color_scheme)
        header = self._build_header(title, persona)
        cards_html = self._build_cards_grid(cards, ui_components)
        footer = self._build_footer()

        # Assemble complete document
        html = f"""<!DOCTYPE html>
<html lang="en">
{head}
<body>
    <div style="min-height: 100vh; display: flex; flex-direction: column;">
        {header}
        <main style="flex: 1; padding: 2rem 0;">
            {cards_html}
        </main>
        {footer}
    </div>
    <script>
        {self._build_drag_drop_script()}
    </script>
</body>
</html>"""

        return html

    def _build_head(self, title: str, color_scheme: ColorScheme) -> str:
        """Build HTML head with styles and metadata."""
        css_vars = self._generate_css_variables(color_scheme)

        return f"""<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>

    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Geist:wght@400;500;600&display=swap" rel="stylesheet">

    <!-- Mapbox GL JS for interactive maps -->
    <script src='https://api.mapbox.com/mapbox-gl-js/v3.0.1/mapbox-gl.js'></script>
    <link href='https://api.mapbox.com/mapbox-gl-js/v3.0.1/mapbox-gl.css' rel='stylesheet' />

    <style>
        {css_vars}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: 'Inter', sans-serif;
            background: var(--background);
            color: var(--foreground);
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 1.5rem;
        }}

        .content-text {{
            font-family: 'Geist', sans-serif;
            line-height: 1.75;
        }}

        /* Card hover effects */
        .dashboard-card {{
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: grab;
            position: relative;
        }}

        .dashboard-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
        }}

        .dashboard-card:hover .drag-handle {{
            opacity: 1;
        }}

        .dashboard-card.dragging {{
            opacity: 0.4;
            cursor: grabbing;
            transform: scale(1.05) rotate(2deg);
            box-shadow: 0 25px 50px -12px rgb(0 0 0 / 0.25);
            z-index: 1000;
        }}

        .dashboard-card.drag-over {{
            transform: scale(0.95);
            box-shadow: inset 0 0 0 3px var(--primary);
            background: linear-gradient(135deg, var(--background) 0%, var(--muted) 100%);
        }}

        .dashboard-card.will-move-up {{
            animation: slideUp 0.3s ease-out;
        }}

        .dashboard-card.will-move-down {{
            animation: slideDown 0.3s ease-out;
        }}

        @keyframes slideUp {{
            0% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-10px); }}
            100% {{ transform: translateY(0); }}
        }}

        @keyframes slideDown {{
            0% {{ transform: translateY(0); }}
            50% {{ transform: translateY(10px); }}
            100% {{ transform: translateY(0); }}
        }}

        .drag-handle {{
            position: absolute;
            top: 12px;
            right: 12px;
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: var(--muted);
            border-radius: 8px;
            opacity: 0;
            transition: opacity 0.2s ease, background 0.2s ease;
            cursor: grab;
            z-index: 10;
        }}

        .drag-handle:hover {{
            background: var(--primary);
            opacity: 1 !important;
        }}

        .drag-handle svg {{
            width: 16px;
            height: 16px;
            color: var(--foreground);
        }}

        #cards-grid {{
            transition: all 0.3s ease;
        }}

        /* Markdown content styles */
        .prose {{
            max-width: none;
            color: #374151;
        }}

        .prose h1, .prose h2, .prose h3 {{
            color: #1f2937;
            font-weight: 600;
            margin-top: 0.75em;
            margin-bottom: 0.375em;
            line-height: 1.3;
        }}

        .prose h1 {{ font-size: 1.25em; }}
        .prose h2 {{ font-size: 1.125em; }}
        .prose h3 {{ font-size: 1em; }}

        .prose p {{
            margin-bottom: 0.75em;
            line-height: 1.5;
        }}

        .prose ul, .prose ol {{
            margin: 0.5em 0;
            padding-left: 1.25em;
        }}

        .prose li {{
            margin-bottom: 0.25em;
            line-height: 1.4;
        }}

        .prose strong {{
            color: #1f2937;
            font-weight: 600;
        }}

        .prose a {{
            color: #3b82f6;
            text-decoration: none;
        }}

        .prose a:hover {{
            text-decoration: underline;
        }}

        .prose code {{
            background: #f3f4f6;
            color: #1f2937;
            padding: 0.15em 0.3em;
            border-radius: 0.2rem;
            font-size: 0.875em;
        }}

        /* UI Component Styles */
        .ui-component {{
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
        }}

        .ui-component:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1);
        }}

        /* Weather Widget */
        .weather-widget {{
            background: linear-gradient(135deg, var(--card) 0%, var(--muted) 100%);
        }}

        /* Map Container */
        .map-container {{
            height: 400px;
            border-radius: 0.5rem;
            overflow: hidden;
        }}

        /* Video Grid */
        .video-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
        }}

        /* Event List */
        .event-item {{
            border-left: 3px solid var(--primary);
            padding-left: 1rem;
        }}

        /* Task Checkbox */
        .task-checkbox {{
            width: 1.25rem;
            height: 1.25rem;
            cursor: pointer;
        }}

        .task-completed {{
            text-decoration: line-through;
            opacity: 0.6;
        }}
    </style>
</head>"""

    def _generate_css_variables(self, color_scheme: ColorScheme) -> str:
        """Generate CSS custom properties from color scheme."""
        # Extract background color from background_theme
        bg_color = color_scheme.background_theme.color or "#ffffff"
        card_color = color_scheme.background_theme.card_background

        return f"""
        :root {{
            --primary: {color_scheme.primary};
            --secondary: {color_scheme.secondary};
            --accent: {color_scheme.accent};
            --background: {bg_color};
            --card: {card_color};
            --foreground: {color_scheme.foreground};
            --muted: {color_scheme.muted};
            --success: {color_scheme.success};
            --warning: {color_scheme.warning};
            --destructive: {color_scheme.destructive};
            --border: {self._adjust_color_opacity(color_scheme.foreground, 0.2)};
        }}
        """

    def _adjust_color_opacity(self, hex_color: str, opacity: float) -> str:
        """
        Convert hex color to rgba with opacity.

        Args:
            hex_color: Hex color string (e.g., "#FF5733").
            opacity: Opacity value 0.0-1.0.

        Returns:
            RGBA color string.
        """
        # Remove # if present
        hex_color = hex_color.lstrip("#")

        # Convert to RGB
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)

        return f"rgba({r}, {g}, {b}, {opacity})"

    def _build_header(self, title: str, persona: PersonaProfile) -> str:
        """Build header section."""
        return f"""<header style="border-bottom: 1px solid var(--border); background: var(--background); padding: 1.5rem 0;">
        <div class="container">
            <h1 style="font-size: 2rem; font-weight: 700; color: var(--foreground); margin-bottom: 0.5rem;">{title}</h1>
            <p style="font-size: 0.875rem; color: var(--foreground); opacity: 0.7;">
                Personalized insights based on your activity • Generated {datetime.utcnow().strftime("%B %d, %Y")}
            </p>
        </div>
    </header>"""

    def _build_cards_grid(
        self,
        cards: list[CardContent],
        ui_components: list[UIComponentType]
    ) -> str:
        """
        Build 2-column grid layout for cards with drag and drop support.

        Cards are displayed in a 2-column grid in a generative, mixed order.
        No sorting - maintains order from generation for organic feel.

        Args:
            cards: List of blog-style content cards.
            ui_components: List of interactive UI widgets (not yet rendered).
        """
        # Keep cards in generated order for organic, generative feel
        sorted_cards = cards

        # Render blog cards
        cards_html = []
        for idx, card in enumerate(sorted_cards):
            card_html = self._build_card(card, idx)
            cards_html.append(card_html)

        # Render UI components
        components_html = []
        for idx, component in enumerate(ui_components):
            component_html = self._build_ui_component(component, idx)
            if component_html:  # Skip empty components
                components_html.append(component_html)

        # Combine blog cards and UI components
        all_items = cards_html + components_html

        # Dense 3-column grid layout for generative feel
        grid_html = f"""<div id="cards-grid" style="display: grid; grid-template-columns: 1fr; gap: 0.875rem; padding: 0 1rem; max-width: 1400px; margin: 0 auto;">
    {"".join(all_items)}
</div>
<style>
    @media (min-width: 640px) {{
        #cards-grid {{
            grid-template-columns: repeat(2, 1fr);
        }}
    }}
    @media (min-width: 1024px) {{
        #cards-grid {{
            grid-template-columns: repeat(3, 1fr);
        }}
    }}
</style>"""

        return grid_html

    def _build_card(self, card: CardContent, idx: int) -> str:
        """Build individual card HTML with drag and drop support."""
        # Convert markdown body to HTML
        body_html = markdown.markdown(
            card.body,
            extensions=['extra', 'codehilite']
        )

        # Build sources list - more compact
        sources_html = ""
        if card.sources:
            sources_list = "\n".join(
                f'<li style="margin-bottom: 0.125rem;"><a href="{source}" target="_blank" style="color: #3b82f6; text-decoration: none; font-size: 0.6875rem;">{self._extract_domain(source)}</a></li>'
                for source in card.sources[:3]  # Max 3 sources for compact feel
            )
            sources_html = f"""<div style="margin-top: 0.75rem; padding-top: 0.625rem; border-top: 1px solid #e5e7eb;">
                <p style="font-size: 0.625rem; font-weight: 600; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.375rem;">Sources</p>
                <ul style="list-style: none; padding: 0;">
                    {sources_list}
                </ul>
            </div>"""

        # Reading time badge - smaller
        reading_time_html = f"""<span style="display: inline-flex; align-items: center; padding: 0.125rem 0.5rem; border-radius: 9999px; font-size: 0.6875rem; font-weight: 500; background: #f3f4f6; color: #6b7280;">
            {card.reading_time_minutes} min
        </span>"""

        return f"""<div class="dashboard-card" style="border-radius: 0.375rem; border: 1px solid #e5e7eb; background: #ffffff; box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05); overflow: hidden;" draggable="true" data-card-index="{idx}">
        <!-- Drag Handle -->
        <div class="drag-handle" title="Drag to reorder">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="8" y1="6" x2="21" y2="6"></line>
                <line x1="8" y1="12" x2="21" y2="12"></line>
                <line x1="8" y1="18" x2="21" y2="18"></line>
                <line x1="3" y1="6" x2="3.01" y2="6"></line>
                <line x1="3" y1="12" x2="3.01" y2="12"></line>
                <line x1="3" y1="18" x2="3.01" y2="18"></line>
            </svg>
        </div>

        <div style="padding: 0.875rem;">
            <!-- Card Header -->
            <div style="margin-bottom: 0.625rem;">
                <h2 style="font-size: 1rem; font-weight: 600; color: #1f2937; margin-bottom: 0.25rem; line-height: 1.3;">{card.title}</h2>
                <p style="font-size: 0.75rem; color: #6b7280; margin-bottom: 0.5rem; line-height: 1.4;">{card.description}</p>
                {reading_time_html}
            </div>

            <!-- Card Content -->
            <div class="prose content-text" style="color: #374151; font-size: 0.8125rem; line-height: 1.5;">
                {body_html}
            </div>

            <!-- Sources -->
            {sources_html}
        </div>
    </div>"""

    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL for display."""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            return parsed.netloc or url
        except Exception:
            return url

    def _build_ui_component(self, component: UIComponentType, idx: int) -> str:
        """
        Build HTML for a single UI component.

        Dispatches to component-specific renderers based on type.

        Args:
            component: UI component to render.
            idx: Component index for unique IDs.

        Returns:
            HTML string for the component.
        """
        component_type = component.component_type

        # Dispatch to appropriate renderer
        if component_type == "info-card":
            return self._render_info_card(component, idx)
        elif component_type == "weather-card":
            return self._render_weather_card(component, idx)
        elif component_type == "map-card":
            return self._render_map_card(component, idx)
        elif component_type == "video-feed":
            return self._render_video_feed(component, idx)
        elif component_type == "event-calendar":
            return self._render_event_calendar(component, idx)
        elif component_type == "task-list":
            return self._render_task_list(component, idx)
        elif component_type == "content-card":
            return self._render_content_card(component, idx)
        else:
            logger.warning(f"Unknown component type: {component_type}")
            return ""  # Skip unknown types

    def _render_info_card(self, component, idx: int) -> str:
        """
        Render weather information card with enriched data.

        Args:
            component: InfoCard component.
            idx: Component index.

        Returns:
            HTML for weather widget.
        """
        component_id = f"weather-{idx}"

        # Extract enriched data if available, otherwise use placeholders
        if component.enriched_data:
            current = component.enriched_data.get("current", {})
            temp_display = f"{current.get('temperature', '--')}{current.get('temp_unit', '°')}"
            condition_display = current.get("condition", "Unknown")
            feels_like_display = f"{current.get('feels_like', '--')}{current.get('temp_unit', '°')}"
            humidity_display = f"{current.get('humidity', '--')}%"
            wind_display = f"{current.get('wind_speed', '--')} km/h"
            location_display = component.enriched_data.get("location", component.location)
        else:
            # Fallback to placeholders
            temp_display = "--°"
            condition_display = "Loading..."
            feels_like_display = "--°"
            humidity_display = "---%"
            wind_display = "-- km/h"
            location_display = component.location

        return f'''<div class="ui-component weather-widget rounded-lg border border-[var(--border)] bg-white shadow-sm overflow-hidden p-6" id="{component_id}">
        <h3 class="text-lg font-semibold text-[var(--foreground)] mb-4">{component.title}</h3>

        <!-- Current Weather -->
        <div class="flex items-center justify-between mb-6">
            <div>
                <div class="text-4xl font-bold text-[var(--foreground)]" id="{component_id}-temp">{temp_display}</div>
                <div class="text-sm text-[var(--foreground)] opacity-70" id="{component_id}-location">{location_display}</div>
            </div>
            <div class="text-right">
                <div class="text-xl text-[var(--foreground)]" id="{component_id}-condition">{condition_display}</div>
                <div class="text-sm text-[var(--foreground)] opacity-70">
                    <span id="{component_id}-feels">Feels like {feels_like_display}</span>
                </div>
            </div>
        </div>

        <!-- Weather Details -->
        <div class="grid grid-cols-2 gap-4 mb-4">
            <div class="text-sm">
                <span class="text-[var(--foreground)] opacity-60">Humidity</span>
                <div class="font-semibold" id="{component_id}-humidity">{humidity_display}</div>
            </div>
            <div class="text-sm">
                <span class="text-[var(--foreground)] opacity-60">Wind</span>
                <div class="font-semibold" id="{component_id}-wind">{wind_display}</div>
            </div>
        </div>

        <!-- 3-Day Forecast (if enabled) -->
        {self._render_weather_forecast_with_data(component_id, component) if component.show_forecast else ''}

        <!-- Hidden data for JavaScript -->
        <script type="application/json" id="{component_id}-data">
            {self._component_to_json(component)}
        </script>
    </div>'''

    def _render_weather_card(self, component, idx: int) -> str:
        """
        Render weather card with current conditions and forecast.

        Args:
            component: InfoCard component.
            idx: Component index.

        Returns:
            HTML for weather widget.
        """
        component_id = f"weather-{idx}"

        return f'''<div class="widget weather-card" id="{component_id}">
        <div class="widget-header">
            <h3>{component.title}</h3>
            <span class="widget-badge">{component.location}</span>
        </div>
        <div class="widget-content">
            <div class="weather-current">
                <div class="weather-temp">{component.current_temp}°</div>
                <div class="weather-condition">{component.condition}</div>
                <div class="weather-details">
                    <span>Feels like: {component.feels_like}°</span>
                    <span>Humidity: {component.humidity}%</span>
                    <span>Wind: {component.wind_speed} {component.wind_direction}</span>
                </div>
            </div>
            <div class="weather-forecast">
                {''.join([f'<div class="forecast-day"><span>{day.day}</span><span>{day.high}°/{day.low}°</span><span>{day.condition}</span></div>' for day in component.forecast])}
            </div>
        </div>
        <script type="application/json" id="{component_id}-data">
            {self._component_to_json(component)}
        </script>
    </div>'''

    def _render_map_card(self, component, idx: int) -> str:
        """
        Render interactive map with Mapbox GL JS.

        Args:
            component: MapCard component.
            idx: Component index.

        Returns:
            HTML for map widget.
        """
        component_id = f"map-{idx}"

        # Map spans full width (col-span-2)
        return f'''<div class="ui-component rounded-lg border border-[var(--border)] bg-white shadow-sm overflow-hidden md:col-span-2" id="{component_id}-container">
        <div class="p-4 border-b border-[var(--border)]">
            <h3 class="text-lg font-semibold text-[var(--foreground)]">{component.title}</h3>
            <p class="text-sm text-[var(--foreground)] opacity-70">{len(component.markers)} location{'s' if len(component.markers) != 1 else ''}</p>
        </div>

        <!-- Map Container -->
        <div id="{component_id}" class="map-container"></div>

        <!-- Hidden data for JavaScript -->
        <script type="application/json" id="{component_id}-data">
            {self._component_to_json(component)}
        </script>
    </div>'''

    def _render_video_feed(self, component, idx: int) -> str:
        """
        Render YouTube video feed with enriched data.

        Args:
            component: VideoFeed component.
            idx: Component index.

        Returns:
            HTML for video grid.
        """
        component_id = f"videos-{idx}"

        # Use enriched videos if available, otherwise use mock data
        if component.enriched_videos:
            videos = component.enriched_videos[:component.max_results]
        else:
            # Fallback to mock video IDs
            videos = [
                {'video_id': 'dQw4w9WgXcQ', 'title': 'Video 1'},
                {'video_id': 'jNQXAC9IVRw', 'title': 'Video 2'},
                {'video_id': 'y6120QOlsfU', 'title': 'Video 3'},
            ][:component.max_results]

        videos_html = '\n'.join([
            f'''<div class="aspect-video">
            <iframe
                width="100%"
                height="100%"
                src="https://www.youtube.com/embed/{video['video_id']}"
                title="{video['title']}"
                frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen
                class="rounded-lg"
            ></iframe>
        </div>'''
            for video in videos
        ])

        return f'''<div class="ui-component rounded-lg border border-[var(--border)] bg-white shadow-sm overflow-hidden p-6" id="{component_id}">
        <h3 class="text-lg font-semibold text-[var(--foreground)] mb-4">{component.title}</h3>
        <div class="video-grid">
            {videos_html}
        </div>
        <div class="mt-4 text-xs text-[var(--foreground)] opacity-60">
            Searching: "{component.search_query}"
        </div>
    </div>'''

    def _render_event_calendar(self, component, idx: int) -> str:
        """
        Render upcoming events calendar with enriched data.

        Args:
            component: EventCalendar component.
            idx: Component index.

        Returns:
            HTML for event calendar widget.
        """
        component_id = f"events-{idx}"

        # Use enriched events if available, otherwise use mock data
        if component.enriched_events:
            events = component.enriched_events[:component.max_events]
        else:
            # Fallback to mock events
            from datetime import datetime, timedelta
            today = datetime.now()
            events = [
                {
                    'name': 'AI & Machine Learning Workshop',
                    'date': (today + timedelta(days=3)).strftime('%Y-%m-%d'),
                    'location': 'TechHub SF',
                    'url': 'https://example.com/event1',
                    'is_virtual': False
                },
                {
                    'name': 'Virtual Tech Meetup',
                    'date': (today + timedelta(days=7)).strftime('%Y-%m-%d'),
                    'location': 'Online',
                    'url': 'https://example.com/event2',
                    'is_virtual': True
                },
                {
                    'name': 'Developer Conference 2025',
                    'date': (today + timedelta(days=14)).strftime('%Y-%m-%d'),
                    'location': 'Convention Center',
                    'url': 'https://example.com/event3',
                    'is_virtual': False
                },
            ][:component.max_events]

        # Build event items HTML
        events_html = []
        for event in events:
            # Parse date for display
            try:
                event_date = datetime.strptime(event['date'], '%Y-%m-%d')
                month = event_date.strftime('%b')
                day = event_date.strftime('%d')
                weekday = event_date.strftime('%A')
            except:
                month = 'TBD'
                day = '00'
                weekday = 'TBD'

            # Handle both enriched data (venue/city) and mock data (location)
            if 'venue' in event and 'city' in event:
                location_display = f"{event['venue']}, {event['city']}"
            else:
                location_display = event.get('location', 'TBD')

            # Virtual event badge
            is_virtual = event.get('is_virtual', False)
            virtual_badge = '''<span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800">
                    <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M10 12a2 2 0 100-4 2 2 0 000 4z"/>
                        <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd"/>
                    </svg>
                    Virtual
                </span>''' if is_virtual else ''

            event_html = f'''<div class="event-item p-4 hover:bg-[var(--muted)] hover:bg-opacity-10 rounded-lg transition-colors">
                <div class="flex items-start gap-4">
                    <!-- Date Badge -->
                    <div class="flex-shrink-0 w-16 text-center">
                        <div class="bg-[var(--primary)] text-white rounded-lg p-2">
                            <div class="text-xs font-semibold uppercase">{month}</div>
                            <div class="text-2xl font-bold">{day}</div>
                        </div>
                    </div>

                    <!-- Event Details -->
                    <div class="flex-1 min-w-0">
                        <div class="flex items-start justify-between gap-2 mb-2">
                            <h4 class="font-semibold text-[var(--foreground)] text-base">{event['name']}</h4>
                            {virtual_badge}
                        </div>

                        <div class="flex items-center gap-4 text-sm text-[var(--foreground)] opacity-70 mb-2">
                            <div class="flex items-center gap-1">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                                </svg>
                                <span>{weekday}</span>
                            </div>
                            <div class="flex items-center gap-1">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                                </svg>
                                <span>{location_display}</span>
                            </div>
                        </div>

                        <a href="{event['url']}" target="_blank" class="inline-flex items-center text-sm font-medium text-[var(--primary)] hover:underline">
                            View Details
                            <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
                            </svg>
                        </a>
                    </div>
                </div>
            </div>'''
            events_html.append(event_html)

        return f'''<div class="ui-component rounded-lg border border-[var(--border)] bg-white shadow-sm overflow-hidden p-6" id="{component_id}">
        <div class="mb-4">
            <h3 class="text-lg font-semibold text-[var(--foreground)]">{component.title}</h3>
            <p class="text-sm text-[var(--foreground)] opacity-60 mt-1">Upcoming events in your area</p>
        </div>

        <div class="space-y-3">
            {''.join(events_html)}
        </div>

        <div class="mt-4 pt-4 border-t border-[var(--border)] text-xs text-[var(--foreground)] opacity-60">
            Searching: "{component.search_query}"
        </div>
    </div>'''

    def _render_task_list(self, component, idx: int) -> str:
        """
        Render interactive task list with checkboxes and localStorage persistence.

        Args:
            component: TaskList component.
            idx: Component index.

        Returns:
            HTML for task list widget.
        """
        component_id = f"tasks-{idx}"

        # Priority badge styling
        priority_badges = {
            'high': '<span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-red-100 text-red-800">High</span>',
            'medium': '<span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-yellow-100 text-yellow-800">Medium</span>',
            'low': '<span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800">Low</span>',
        }

        # Build task items HTML
        tasks_html = []
        for task_idx, task in enumerate(component.tasks):
            task_id = f"{component_id}-task-{task_idx}"
            checked_attr = 'checked' if task.completed else ''
            completed_class = 'task-completed' if task.completed else ''
            priority_badge = priority_badges.get(task.priority, priority_badges['medium'])

            task_html = f'''<div class="task-item flex items-start gap-3 p-3 hover:bg-[var(--muted)] hover:bg-opacity-10 rounded-lg transition-colors">
                <input
                    type="checkbox"
                    id="{task_id}"
                    class="task-checkbox mt-1 accent-[var(--primary)]"
                    {checked_attr}
                    data-task-index="{task_idx}"
                />
                <div class="flex-1 min-w-0">
                    <label for="{task_id}" class="cursor-pointer">
                        <span class="text-[var(--foreground)] {completed_class}">{task.text}</span>
                    </label>
                    <div class="mt-1">
                        {priority_badge}
                    </div>
                </div>
            </div>'''
            tasks_html.append(task_html)

        # List type description
        list_type_descriptions = {
            'goals': 'Personal goals to achieve',
            'recommendations': 'Suggested actions based on your patterns',
            'learning': 'Learning objectives and resources',
        }
        description = list_type_descriptions.get(component.list_type, 'Task list')

        return f'''<div class="ui-component rounded-lg border border-[var(--border)] bg-white shadow-sm overflow-hidden p-6" id="{component_id}">
        <div class="mb-4">
            <h3 class="text-lg font-semibold text-[var(--foreground)]">{component.title}</h3>
            <p class="text-sm text-[var(--foreground)] opacity-60 mt-1">{description}</p>
        </div>

        <div class="space-y-2">
            {''.join(tasks_html)}
        </div>

        <!-- Progress indicator -->
        <div class="mt-6 pt-4 border-t border-[var(--border)]">
            <div class="flex items-center justify-between text-sm">
                <span class="text-[var(--foreground)] opacity-70">Progress</span>
                <span class="font-semibold text-[var(--primary)]" id="{component_id}-progress">
                    {sum(1 for t in component.tasks if t.completed)}/{len(component.tasks)} completed
                </span>
            </div>
            <div class="mt-2 h-2 bg-[var(--muted)] rounded-full overflow-hidden">
                <div
                    id="{component_id}-progress-bar"
                    class="h-full bg-[var(--primary)] transition-all duration-300 rounded-full"
                    style="width: {(sum(1 for t in component.tasks if t.completed) / len(component.tasks) * 100):.0f}%"
                ></div>
            </div>
        </div>

        <!-- Hidden data for JavaScript -->
        <script type="application/json" id="{component_id}-data">
            {self._component_to_json(component)}
        </script>
    </div>'''

    def _render_content_card(self, component, idx: int) -> str:
        """
        Render single article/resource recommendation card.

        Args:
            component: ContentCard component.
            idx: Component index.

        Returns:
            HTML for content card widget.
        """
        component_id = f"content-{idx}"

        # Format published date if available
        date_html = ""
        if component.published_date:
            date_html = f'''<div class="flex items-center gap-1 text-sm text-[var(--foreground)] opacity-60">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                </svg>
                <span>{component.published_date}</span>
            </div>'''

        return f'''<div class="ui-component rounded-lg border border-[var(--border)] bg-white shadow-sm overflow-hidden p-6" id="{component_id}">
        <div class="mb-4">
            <h3 class="text-lg font-semibold text-[var(--foreground)] mb-2">{component.title}</h3>
            <div class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-[var(--muted)] text-[var(--foreground)]">
                {component.source_name}
            </div>
        </div>

        <!-- Article Details -->
        <div class="mb-4">
            <h4 class="font-semibold text-base text-[var(--foreground)] mb-2">{component.article_title}</h4>
            <p class="text-sm text-[var(--foreground)] opacity-80 leading-relaxed">{component.overview}</p>
        </div>

        <!-- Footer with Date and Link -->
        <div class="flex items-center justify-between pt-4 border-t border-[var(--border)]">
            {date_html if date_html else '<div></div>'}
            <a href="{component.url}" target="_blank" class="inline-flex items-center text-sm font-medium text-[var(--primary)] hover:underline">
                Read More
                <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
                </svg>
            </a>
        </div>
    </div>'''

    def _render_weather_forecast(self, component_id: str) -> str:
        """Render 3-day forecast section."""
        return f'''<div class="border-t border-[var(--border)] pt-4 mt-4">
        <div class="text-xs font-semibold text-[var(--foreground)] opacity-60 uppercase tracking-wide mb-3">3-Day Forecast</div>
        <div class="grid grid-cols-3 gap-3" id="{component_id}-forecast">
            <!-- Populated by JavaScript -->
            <div class="text-center">
                <div class="text-xs opacity-70">Loading...</div>
            </div>
        </div>
    </div>'''

    def _render_weather_forecast_with_data(self, component_id: str, component) -> str:
        """Render 3-day forecast with enriched data if available."""
        if not component.enriched_data:
            return self._render_weather_forecast(component_id)

        forecast_data = component.enriched_data.get("forecast", [])
        if not forecast_data:
            return self._render_weather_forecast(component_id)

        forecast_html = []
        for day_data in forecast_data[:3]:
            day_name = day_data.get("day_name", "")[:3]  # Mon, Tue, Wed
            high = day_data.get("temperature_high", "--")
            low = day_data.get("temperature_low", "--")

            forecast_html.append(f'''
                <div class="text-center">
                    <div class="text-xs font-medium text-[var(--foreground)] mb-1">{day_name}</div>
                    <div class="text-lg font-semibold text-[var(--foreground)]">{high}°</div>
                    <div class="text-xs text-[var(--foreground)] opacity-70">{low}°</div>
                </div>
            ''')

        return f'''<div class="border-t border-[var(--border)] pt-4 mt-4">
        <div class="text-xs font-semibold text-[var(--foreground)] opacity-60 uppercase tracking-wide mb-3">3-Day Forecast</div>
        <div class="grid grid-cols-3 gap-3">
            {''.join(forecast_html)}
        </div>
    </div>'''

    def _component_to_json(self, component) -> str:
        """Convert component to JSON for JavaScript consumption."""
        import json
        return json.dumps(component.model_dump(), default=str)

    def _build_footer(self) -> str:
        """Build footer section."""
        return f"""<footer style="border-top: 1px solid var(--border); background: var(--background); margin-top: 4rem; padding: 1.5rem 0;">
        <div class="container">
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: space-between; font-size: 0.875rem; color: var(--foreground); opacity: 0.6;">
                <p style="margin: 0;">Generated by Fabric Intelligence Dashboard</p>
                <p style="margin: 0.5rem 0 0 0;">
                    Powered by <a href="https://www.anthropic.com/claude" target="_blank" style="color: var(--primary); text-decoration: none;">Claude</a> &
                    <a href="https://www.perplexity.ai" target="_blank" style="color: var(--primary); text-decoration: none;">Perplexity</a>
                </p>
            </div>
        </div>
        <style>
            @media (min-width: 768px) {{
                footer > div > div {{
                    flex-direction: row;
                }}
                footer > div > div > p:last-child {{
                    margin-top: 0;
                }}
            }}
        </style>
    </footer>"""

    def _generate_title(self, persona: PersonaProfile) -> str:
        """Generate dashboard title from persona."""
        # Use first interest or activity level as title inspiration
        if persona.interests:
            main_interest = persona.interests[0].title()
            return f"Your {main_interest} Intelligence Dashboard"
        else:
            return "Your Personalized Intelligence Dashboard"

    def _build_drag_drop_script(self) -> str:
        """Build JavaScript for drag and drop functionality."""
        return """
        // Weather Component Initialization
        document.addEventListener('DOMContentLoaded', function() {
            // Find all weather components
            const weatherComponents = document.querySelectorAll('[id^="weather-"]');

            weatherComponents.forEach(component => {
                const componentId = component.id;
                const dataScript = document.getElementById(componentId + '-data');

                if (!dataScript) return;

                try {
                    const data = JSON.parse(dataScript.textContent);

                    // For now, show mock data
                    // TODO: Fetch real weather data in future phases
                    const mockData = {
                        temperature: 22,
                        condition: 'Sunny',
                        feels_like: 21,
                        humidity: 65,
                        wind_speed: 12,
                        forecast: [
                            { day: 'Mon', high: 24, low: 18, condition: 'Sunny' },
                            { day: 'Tue', high: 23, low: 17, condition: 'Cloudy' },
                            { day: 'Wed', high: 21, low: 16, condition: 'Rainy' }
                        ]
                    };

                    // Update UI
                    document.getElementById(componentId + '-temp').textContent = mockData.temperature + '°' + (data.units === 'metric' ? 'C' : 'F');
                    document.getElementById(componentId + '-condition').textContent = mockData.condition;
                    document.getElementById(componentId + '-location').textContent = data.location;
                    document.getElementById(componentId + '-feels').textContent = 'Feels like ' + mockData.feels_like + '°';
                    document.getElementById(componentId + '-humidity').textContent = mockData.humidity + '%';
                    document.getElementById(componentId + '-wind').textContent = mockData.wind_speed + ' km/h';

                    // Render forecast if container exists
                    const forecastContainer = document.getElementById(componentId + '-forecast');
                    if (forecastContainer && mockData.forecast) {
                        forecastContainer.innerHTML = mockData.forecast.map(day => `
                            <div class="text-center">
                                <div class="text-xs font-medium">${day.day}</div>
                                <div class="text-lg font-semibold">${day.high}°</div>
                                <div class="text-xs opacity-70">${day.low}°</div>
                            </div>
                        `).join('');
                    }
                } catch (e) {
                    console.error('Failed to render weather component:', e);
                }
            });
        });

        // Map Component Initialization
        document.addEventListener('DOMContentLoaded', function() {
            const mapComponents = document.querySelectorAll('[id^="map-"][id$="-data"]');

            mapComponents.forEach(dataScript => {
                const componentId = dataScript.id.replace('-data', '');
                const container = document.getElementById(componentId);

                if (!container) return;

                try {
                    const data = JSON.parse(dataScript.textContent);

                    // Show placeholder with marker list
                    const markersList = data.markers.map((marker, idx) => `
                        <div class="flex items-start p-3 hover:bg-gray-50 rounded-lg transition-colors">
                            <div class="flex-shrink-0 w-8 h-8 bg-[var(--primary)] text-white rounded-full flex items-center justify-center font-semibold text-sm">
                                ${idx + 1}
                            </div>
                            <div class="ml-3 flex-1">
                                <h4 class="font-semibold text-[var(--foreground)]">${marker.title}</h4>
                                ${marker.description ? '<p class="text-sm text-[var(--foreground)] opacity-70 mt-1">' + marker.description + '</p>' : ''}
                                <p class="text-xs text-[var(--foreground)] opacity-50 mt-1">
                                    ${marker.lat.toFixed(4)}°N, ${marker.lng.toFixed(4)}°W
                                </p>
                            </div>
                        </div>
                    `).join('');

                    container.innerHTML = `
                        <div class="p-6">
                            <div class="bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg p-8 mb-4 text-center">
                                <svg class="w-16 h-16 mx-auto mb-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"></path>
                                </svg>
                                <h4 class="font-semibold text-lg text-gray-800 mb-2">Interactive Map Preview</h4>
                                <p class="text-sm text-gray-600 mb-4">
                                    Add your Mapbox API token to enable the interactive map<br/>
                                    <a href="https://account.mapbox.com/access-tokens/" target="_blank" class="text-blue-600 hover:underline">
                                        Get free token from Mapbox →
                                    </a>
                                </p>
                            </div>
                            <div class="space-y-2">
                                <h5 class="text-sm font-semibold text-[var(--foreground)] opacity-60 uppercase tracking-wide mb-3">
                                    ${data.markers.length} Location${data.markers.length !== 1 ? 's' : ''}
                                </h5>
                                ${markersList}
                            </div>
                        </div>
                    `;

                } catch (e) {
                    console.error('Failed to render map component:', e);
                    container.innerHTML = '<div class="p-8 text-center text-red-500">Failed to load map component</div>';
                }
            });
        });

        // Task List Component Initialization
        document.addEventListener('DOMContentLoaded', function() {
            const taskComponents = document.querySelectorAll('[id^="tasks-"]');

            taskComponents.forEach(component => {
                const componentId = component.id;
                if (!componentId.includes('-data')) { // Skip data script tags
                    const dataScript = document.getElementById(componentId + '-data');

                    if (!dataScript) return;

                    try {
                        const data = JSON.parse(dataScript.textContent);
                        const storageKey = 'task-' + componentId;

                        // Load saved task states from localStorage
                        const savedStates = JSON.parse(localStorage.getItem(storageKey) || '{}');

                        // Get all checkboxes in this component
                        const checkboxes = component.querySelectorAll('.task-checkbox');

                        // Restore saved states
                        checkboxes.forEach((checkbox, idx) => {
                            const taskIndex = checkbox.dataset.taskIndex;
                            if (savedStates[taskIndex] !== undefined) {
                                checkbox.checked = savedStates[taskIndex];

                                // Update text styling
                                const label = checkbox.nextElementSibling.querySelector('span');
                                if (label) {
                                    if (savedStates[taskIndex]) {
                                        label.classList.add('task-completed');
                                    } else {
                                        label.classList.remove('task-completed');
                                    }
                                }
                            }
                        });

                        // Update progress after restoration
                        updateProgress();

                        // Add change listeners to checkboxes
                        checkboxes.forEach(checkbox => {
                            checkbox.addEventListener('change', function(e) {
                                const taskIndex = this.dataset.taskIndex;
                                const isChecked = this.checked;

                                // Update text styling with smooth transition
                                const label = this.nextElementSibling.querySelector('span');
                                if (label) {
                                    if (isChecked) {
                                        label.classList.add('task-completed');
                                    } else {
                                        label.classList.remove('task-completed');
                                    }
                                }

                                // Save to localStorage
                                savedStates[taskIndex] = isChecked;
                                localStorage.setItem(storageKey, JSON.stringify(savedStates));

                                // Update progress
                                updateProgress();
                            });
                        });

                        // Function to update progress bar and counter
                        function updateProgress() {
                            const total = checkboxes.length;
                            const completed = Array.from(checkboxes).filter(cb => cb.checked).length;
                            const percentage = total > 0 ? (completed / total * 100) : 0;

                            const progressText = document.getElementById(componentId + '-progress');
                            const progressBar = document.getElementById(componentId + '-progress-bar');

                            if (progressText) {
                                progressText.textContent = completed + '/' + total + ' completed';
                            }

                            if (progressBar) {
                                progressBar.style.width = percentage.toFixed(0) + '%';
                            }
                        }

                    } catch (e) {
                        console.error('Failed to initialize task list component:', e);
                    }
                }
            });
        });

        let draggedCard = null;
        let draggedOverCard = null;
        let animationTimeout = null;

        // Get all cards
        const cards = document.querySelectorAll('.dashboard-card');

        // Add smooth transition class to all cards
        cards.forEach(card => {
            // Drag start
            card.addEventListener('dragstart', (e) => {
                draggedCard = card;
                
                // Add dragging class after a tiny delay for smooth animation
                setTimeout(() => {
                    card.classList.add('dragging');
                }, 10);
                
                e.dataTransfer.effectAllowed = 'move';
                e.dataTransfer.setData('text/html', card.innerHTML);
                
                // Add visual feedback to all other cards
                cards.forEach(c => {
                    if (c !== card) {
                        c.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
                    }
                });
            });

            // Drag end
            card.addEventListener('dragend', (e) => {
                // Remove dragging state with smooth animation
                card.classList.remove('dragging');
                
                // Remove all drag-related classes from all cards
                cards.forEach(c => {
                    c.classList.remove('drag-over', 'will-move-up', 'will-move-down');
                });
                
                // Clear animation timeout
                if (animationTimeout) {
                    clearTimeout(animationTimeout);
                }
                
                draggedCard = null;
                draggedOverCard = null;
            });

            // Drag over
            card.addEventListener('dragover', (e) => {
                e.preventDefault();
                e.dataTransfer.dropEffect = 'move';
                
                if (draggedCard && card !== draggedCard) {
                    // Remove drag-over from all other cards
                    cards.forEach(c => {
                        if (c !== card) {
                            c.classList.remove('drag-over');
                        }
                    });
                    
                    // Add drag-over to current card
                    card.classList.add('drag-over');
                    draggedOverCard = card;
                    
                    // Add animation hints
                    const grid = document.getElementById('cards-grid');
                    const allCards = Array.from(grid.querySelectorAll('.dashboard-card'));
                    const draggedIndex = allCards.indexOf(draggedCard);
                    const targetIndex = allCards.indexOf(card);
                    
                    // Add movement hints
                    if (draggedIndex < targetIndex) {
                        card.classList.add('will-move-down');
                    } else {
                        card.classList.add('will-move-up');
                    }
                }
            });

            // Drag enter
            card.addEventListener('dragenter', (e) => {
                if (draggedCard && card !== draggedCard) {
                    e.preventDefault();
                }
            });

            // Drag leave
            card.addEventListener('dragleave', (e) => {
                // Only remove if we're actually leaving the card
                if (e.target === card) {
                    card.classList.remove('drag-over', 'will-move-up', 'will-move-down');
                }
            });

            // Drop
            card.addEventListener('drop', (e) => {
                e.preventDefault();
                e.stopPropagation();
                
                card.classList.remove('drag-over', 'will-move-up', 'will-move-down');
                
                if (draggedCard && card !== draggedCard) {
                    // Get the grid container
                    const grid = document.getElementById('cards-grid');
                    
                    // Get all cards as array
                    const allCards = Array.from(grid.querySelectorAll('.dashboard-card'));
                    
                    // Get indices
                    const draggedIndex = allCards.indexOf(draggedCard);
                    const targetIndex = allCards.indexOf(card);
                    
                    // Add exit animation to dragged card
                    draggedCard.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
                    
                    // Swap the cards in the DOM with smooth transition
                    if (draggedIndex < targetIndex) {
                        card.parentNode.insertBefore(draggedCard, card.nextSibling);
                    } else {
                        card.parentNode.insertBefore(draggedCard, card);
                    }
                    
                    // Add a subtle success feedback
                    draggedCard.style.animation = 'none';
                    setTimeout(() => {
                        draggedCard.style.animation = '';
                    }, 10);
                }
            });
        });

        // Prevent default drag behavior on grid
        const grid = document.getElementById('cards-grid');
        if (grid) {
            grid.addEventListener('dragover', (e) => {
                e.preventDefault();
            });
            
            grid.addEventListener('drop', (e) => {
                e.preventDefault();
            });
        }
        """
