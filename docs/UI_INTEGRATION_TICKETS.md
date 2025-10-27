# UI Integration Linear Tickets

## MAT-19: Update generate.py to call UIGenerator

**Priority**: High
**Estimated Time**: 30 minutes
**Dependencies**: Blocks MAT-20

### Goal
Integrate UIGenerator into the existing dashboard generation pipeline so that both blog cards AND interactive UI components are generated.

### Background
Currently, `generate.py` only generates blog-style content cards using ContentWriter. We need to add a parallel step that generates interactive UI widgets (weather, maps, videos, etc.) using the new UIGenerator.

### What You'll Change
**File**: `fabric_dashboard/commands/generate.py`

### Step-by-Step Instructions

#### Step 1: Import UIGenerator
At the top of the file (around line 18), add the import:

```python
from fabric_dashboard.core.ui_generator import UIGenerator
```

#### Step 2: Initialize UIGenerator
In the `generate_dashboard()` function, after initializing ContentWriter (around line 123), add:

```python
ui_generator = UIGenerator(mock_mode=mock)
```

This creates the UI generator in the same mock mode as other components.

#### Step 3: Generate UI Components
After Step 6 where ContentWriter generates cards (around line 290), add a new Step 6b:

```python
# Step 6b: Generate UI components
console.print("[bold]Step 6b/7:[/bold] Generating interactive UI widgets...")

try:
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Selecting UI components...", total=None)

        # Generate UI components from patterns
        ui_result = await ui_generator.generate_components(patterns, persona)
        ui_components = ui_result.components

        progress.update(task, completed=True)

    console.print(f"[green]✓[/green] Generated {len(ui_components)} UI components")
    console.print(f"[dim]  Types: {', '.join(set(c.component_type for c in ui_components))}[/dim]\n")

except Exception as e:
    console.print(f"[red]✗ Failed to generate UI components: {e}[/red]")
    if debug:
        import traceback
        traceback.print_exc()
    # Set empty list on failure - dashboard will still work with just blog cards
    ui_components = []
```

#### Step 4: Pass UI Components to DashboardBuilder
In Step 7 where DashboardBuilder is called (around line 301), modify the call:

**BEFORE:**
```python
dashboard = dashboard_builder.build(
    cards=cards,
    persona=persona,
    color_scheme=color_scheme,
    user_name="User",
    generation_time_seconds=generation_time,
)
```

**AFTER:**
```python
dashboard = dashboard_builder.build(
    cards=cards,
    ui_components=ui_components,  # NEW LINE!
    persona=persona,
    color_scheme=color_scheme,
    user_name="User",
    generation_time_seconds=generation_time,
)
```

#### Step 5: Update Step Numbers
Since you added Step 6b, change "Step 7/7" to "Step 7/8" in the final dashboard building section.

### Testing
Run the generate command:
```bash
fabric-dashboard generate --mock
```

You should see:
- ✅ New "Step 6b/7" output showing UI component generation
- ✅ Message like "Generated 5 UI components"
- ✅ Types listed (e.g., "info-card, video-feed, map-card")

### Acceptance Criteria
- [ ] UIGenerator is imported
- [ ] UIGenerator is initialized with correct mock_mode
- [ ] UI components are generated after blog cards
- [ ] ui_components are passed to DashboardBuilder
- [ ] Progress output shows Step 6b
- [ ] Error handling gracefully handles UI generation failures
- [ ] Test command runs without errors

### Resources
- Reference: `fabric_dashboard/core/ui_generator.py` (already implemented)
- Reference: `fabric_dashboard/commands/generate.py` lines 249-291 for similar pattern

---

## MAT-20: Extend DashboardBuilder to accept UI components

**Priority**: High
**Estimated Time**: 1 hour
**Dependencies**: Depends on MAT-19, Blocks MAT-21-26

### Goal
Modify DashboardBuilder to accept an optional list of UI components and prepare the infrastructure for rendering them alongside blog cards.

### Background
Currently, DashboardBuilder only handles blog-style CardContent. We need to extend it to also accept UIComponentType objects and prepare to render both in a mixed grid layout.

### What You'll Change
**File**: `fabric_dashboard/core/dashboard_builder.py`

### Step-by-Step Instructions

#### Step 1: Import UI Component Types
At the top of the file (around line 7), add imports:

```python
from typing import Optional
from fabric_dashboard.models.ui_components import UIComponentType
```

#### Step 2: Update build() Method Signature
In the `build()` method (around line 25), add the new parameter:

**BEFORE:**
```python
def build(
    self,
    cards: list[CardContent],
    persona: PersonaProfile,
    color_scheme: ColorScheme,
    title: Optional[str] = None,
    user_name: str = "User",
    data_summary: Optional[DataSummary] = None,
    generation_time_seconds: float = 0.0,
) -> Dashboard:
```

**AFTER:**
```python
def build(
    self,
    cards: list[CardContent],
    ui_components: Optional[list[UIComponentType]] = None,  # NEW!
    persona: PersonaProfile,
    color_scheme: ColorScheme,
    title: Optional[str] = None,
    user_name: str = "User",
    data_summary: Optional[DataSummary] = None,
    generation_time_seconds: float = 0.0,
) -> Dashboard:
```

#### Step 3: Handle Empty UI Components
At the start of the build() method (around line 50), add:

```python
# Default to empty list if no UI components provided
if ui_components is None:
    ui_components = []

logger.info(f"Building dashboard with {len(cards)} cards and {len(ui_components)} UI components")
```

#### Step 4: Pass to HTML Generation
Update the `_generate_html()` call (around line 56) to pass ui_components:

**BEFORE:**
```python
html = self._generate_html(cards, persona, color_scheme, title)
```

**AFTER:**
```python
html = self._generate_html(cards, ui_components, persona, color_scheme, title)
```

#### Step 5: Update _generate_html() Signature
Update the method signature (around line 83):

**BEFORE:**
```python
def _generate_html(
    self,
    cards: list[CardContent],
    persona: PersonaProfile,
    color_scheme: ColorScheme,
    title: Optional[str],
) -> str:
```

**AFTER:**
```python
def _generate_html(
    self,
    cards: list[CardContent],
    ui_components: list[UIComponentType],
    persona: PersonaProfile,
    color_scheme: ColorScheme,
    title: Optional[str],
) -> str:
```

#### Step 6: Update _build_cards_grid() Call
Update the call to _build_cards_grid() (around line 109):

**BEFORE:**
```python
cards_html = self._build_cards_grid(cards)
```

**AFTER:**
```python
cards_html = self._build_cards_grid(cards, ui_components)
```

#### Step 7: Update _build_cards_grid() Method Signature
Update the method signature (around line 337):

**BEFORE:**
```python
def _build_cards_grid(self, cards: list[CardContent]) -> str:
```

**AFTER:**
```python
def _build_cards_grid(
    self,
    cards: list[CardContent],
    ui_components: list[UIComponentType]
) -> str:
```

#### Step 8: Add Placeholder for UI Components
Inside `_build_cards_grid()`, after the blog cards loop (around line 352), add:

```python
# TODO: Add UI components to grid (MAT-21-26)
# For now, UI components are passed but not rendered
# Will be implemented in subsequent tickets
```

### Testing
Run the generate command:
```bash
fabric-dashboard generate --mock
```

Should work exactly as before - no visual changes yet, but UI components are now being passed through the system.

### Acceptance Criteria
- [ ] build() accepts ui_components parameter
- [ ] Empty list default works correctly
- [ ] UI components are logged in console
- [ ] _generate_html() receives ui_components
- [ ] _build_cards_grid() receives ui_components
- [ ] No errors when running generate command
- [ ] Dashboard still renders blog cards correctly

### Resources
- Reference: `dashboard_builder.py` lines 337-358 for grid building pattern

---

## MAT-21: Add CDN Libraries and UI Component Infrastructure

**Priority**: High
**Estimated Time**: 45 minutes
**Dependencies**: Depends on MAT-20, Blocks MAT-22-26

### Goal
Add necessary CDN libraries (Mapbox GL JS, etc.) to the HTML head and create the component rendering dispatcher.

### What You'll Change
**File**: `fabric_dashboard/core/dashboard_builder.py`

### Step-by-Step Instructions

#### Step 1: Update _build_head() to Include CDN Libraries
In the `_build_head()` method (around line 132), add CDN links AFTER the Tailwind and Google Fonts, BEFORE the closing `<style>` tag:

```python
<!-- Mapbox GL JS for interactive maps -->
<script src='https://api.mapbox.com/mapbox-gl-js/v3.0.1/mapbox-gl.js'></script>
<link href='https://api.mapbox.com/mapbox-gl-js/v3.0.1/mapbox-gl.css' rel='stylesheet' />
```

#### Step 2: Add Component-Specific CSS
Inside the `<style>` tag (around line 284, before closing `</style>`), add:

```python
/* UI Component Styles */
.ui-component {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
}

.ui-component:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1);
}

/* Weather Widget */
.weather-widget {
    background: linear-gradient(135deg, var(--card) 0%, var(--muted) 100%);
}

/* Map Container */
.map-container {
    height: 400px;
    border-radius: 0.5rem;
    overflow: hidden;
}

/* Video Grid */
.video-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem;
}

/* Event List */
.event-item {
    border-left: 3px solid var(--primary);
    padding-left: 1rem;
}

/* Task Checkbox */
.task-checkbox {
    width: 1.25rem;
    height: 1.25rem;
    cursor: pointer;
}

.task-completed {
    text-decoration: line-through;
    opacity: 0.6;
}
```

#### Step 3: Create Component Renderer Dispatcher
Add a new method after `_build_card()` (around line 418):

```python
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
```

#### Step 4: Add Placeholder Renderer Methods
Add these stub methods after the dispatcher:

```python
def _render_info_card(self, component, idx: int) -> str:
    """Render weather info card. Implementation in MAT-22."""
    return f'<!-- InfoCard {idx} - TODO: MAT-22 -->'

def _render_map_card(self, component, idx: int) -> str:
    """Render interactive map. Implementation in MAT-23."""
    return f'<!-- MapCard {idx} - TODO: MAT-23 -->'

def _render_video_feed(self, component, idx: int) -> str:
    """Render video feed. Implementation in MAT-24."""
    return f'<!-- VideoFeed {idx} - TODO: MAT-24 -->'

def _render_event_calendar(self, component, idx: int) -> str:
    """Render event calendar. Implementation in MAT-25."""
    return f'<!-- EventCalendar {idx} - TODO: MAT-25 -->'

def _render_task_list(self, component, idx: int) -> str:
    """Render task list. Implementation in MAT-26."""
    return f'<!-- TaskList {idx} - TODO: MAT-26 -->'

def _render_content_card(self, component, idx: int) -> str:
    """Render content card. Implementation in MAT-27."""
    return f'<!-- ContentCard {idx} - TODO: MAT-27 -->'
```

### Testing
Run: `fabric-dashboard generate --mock`

Check the generated HTML file - should see:
- ✅ Mapbox script/CSS in `<head>`
- ✅ UI component styles in `<style>`
- ✅ HTML comments showing where components will render

### Acceptance Criteria
- [ ] Mapbox CDN links added to head
- [ ] Component CSS added
- [ ] _build_ui_component() dispatcher created
- [ ] All 6 placeholder renderers created
- [ ] No errors when generating dashboard
- [ ] HTML file contains CDN links

### Resources
- Mapbox GL JS docs: https://docs.mapbox.com/mapbox-gl-js/
- Reference current _build_head() method for structure

---

## MAT-22: Implement InfoCard (Weather) Renderer

**Priority**: High
**Estimated Time**: 1.5 hours
**Dependencies**: Depends on MAT-21

### Goal
Create the HTML renderer for weather info cards with mock data display.

### What You'll Change
**File**: `fabric_dashboard/core/dashboard_builder.py`

### Step-by-Step Instructions

#### Step 1: Replace Placeholder Method
Replace the `_render_info_card()` placeholder with:

```python
def _render_info_card(self, component, idx: int) -> str:
    """
    Render weather information card.

    Args:
        component: InfoCard component.
        idx: Component index.

    Returns:
        HTML for weather widget.
    """
    # Component will be passed to JavaScript for data fetching
    component_id = f"weather-{idx}"

    return f'''<div class="ui-component weather-widget rounded-lg border border-[var(--border)] bg-white shadow-sm overflow-hidden p-6" id="{component_id}">
        <h3 class="text-lg font-semibold text-[var(--foreground)] mb-4">{component.title}</h3>

        <!-- Current Weather -->
        <div class="flex items-center justify-between mb-6">
            <div>
                <div class="text-4xl font-bold text-[var(--foreground)]" id="{component_id}-temp">--°</div>
                <div class="text-sm text-[var(--foreground)] opacity-70" id="{component_id}-location">{component.location}</div>
            </div>
            <div class="text-right">
                <div class="text-xl text-[var(--foreground)]" id="{component_id}-condition">Loading...</div>
                <div class="text-sm text-[var(--foreground)] opacity-70">
                    <span id="{component_id}-feels">Feels like --°</span>
                </div>
            </div>
        </div>

        <!-- Weather Details -->
        <div class="grid grid-cols-2 gap-4 mb-4">
            <div class="text-sm">
                <span class="text-[var(--foreground)] opacity-60">Humidity</span>
                <div class="font-semibold" id="{component_id}-humidity">---%</div>
            </div>
            <div class="text-sm">
                <span class="text-[var(--foreground)] opacity-60">Wind</span>
                <div class="font-semibold" id="{component_id}-wind">-- km/h</div>
            </div>
        </div>

        <!-- 3-Day Forecast (if enabled) -->
        {self._render_weather_forecast(component_id) if component.show_forecast else ''}

        <!-- Hidden data for JavaScript -->
        <script type="application/json" id="{component_id}-data">
            {self._component_to_json(component)}
        </script>
    </div>'''
```

#### Step 2: Add Forecast Helper Method
Add this helper method:

```python
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
```

#### Step 3: Add JSON Helper Method
Add this utility method (can go near the bottom of the class):

```python
def _component_to_json(self, component) -> str:
    """Convert component to JSON for JavaScript consumption."""
    import json
    return json.dumps(component.model_dump(), default=str)
```

#### Step 4: Add Weather Rendering JavaScript
In `_build_drag_drop_script()`, BEFORE the drag-drop code, add:

```python
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
```

### Testing
1. Run: `fabric-dashboard generate --mock`
2. Open generated HTML
3. Look for weather widget showing:
   - ✅ Location name
   - ✅ Temperature (22°C)
   - ✅ Condition ("Sunny")
   - ✅ Humidity, wind speed
   - ✅ 3-day forecast

### Acceptance Criteria
- [ ] InfoCard renders with proper styling
- [ ] Mock weather data displays correctly
- [ ] Forecast shows 3 days
- [ ] Layout is responsive
- [ ] No console errors

### Resources
- Reference: `fabric_dashboard/models/ui_components.py` lines 36-66 for InfoCard schema

---

## MAT-23: Implement MapCard Renderer

**Priority**: High
**Estimated Time**: 2 hours
**Dependencies**: Depends on MAT-21

### Goal
Create an interactive map using Mapbox GL JS with markers.

### What You'll Change
**File**: `fabric_dashboard/core/dashboard_builder.py`

### Step-by-Step Instructions

#### Step 1: Replace Placeholder Method
Replace `_render_map_card()` with:

```python
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
            <p class="text-sm text-[var(--foreground)] opacity-70">{len(component.markers)} location{'' if len(component.markers) == 1 else 's'}</p>
        </div>

        <!-- Map Container -->
        <div id="{component_id}" class="map-container"></div>

        <!-- Hidden data for JavaScript -->
        <script type="application/json" id="{component_id}-data">
            {self._component_to_json(component)}
        </script>
    </div>'''
```

#### Step 2: Add Map Initialization JavaScript
In `_build_drag_drop_script()`, after weather initialization, add:

```python
// Map Component Initialization
document.addEventListener('DOMContentLoaded', function() {
    const mapComponents = document.querySelectorAll('[id^="map-"][id$="-data"]');

    mapComponents.forEach(dataScript => {
        const componentId = dataScript.id.replace('-data', '');
        const container = document.getElementById(componentId);

        if (!container) return;

        try {
            const data = JSON.parse(dataScript.textContent);

            // Initialize Mapbox map
            // Note: Using public Mapbox token (limited to development)
            mapboxgl.accessToken = 'pk.eyJ1IjoiZXhhbXBsZSIsImEiOiJjbGV4YW1wbGUifQ.example';

            const map = new mapboxgl.Map({
                container: componentId,
                style: 'mapbox://styles/mapbox/' + data.style + '-v11',
                center: [data.center_lng, data.center_lat],
                zoom: data.zoom
            });

            // Add navigation controls
            map.addControl(new mapboxgl.NavigationControl());

            // Add markers
            data.markers.forEach(marker => {
                const el = document.createElement('div');
                el.className = 'marker';
                el.style.backgroundColor = 'var(--primary)';
                el.style.width = '20px';
                el.style.height = '20px';
                el.style.borderRadius = '50%';
                el.style.border = '2px solid white';
                el.style.boxShadow = '0 2px 4px rgba(0,0,0,0.3)';

                // Create popup
                const popup = new mapboxgl.Popup({ offset: 25 })
                    .setHTML('<h3 style="margin:0;font-weight:600;">' + marker.title + '</h3>' +
                             (marker.description ? '<p style="margin:4px 0 0 0;font-size:0.875rem;">' + marker.description + '</p>' : ''));

                new mapboxgl.Marker(el)
                    .setLngLat([marker.lng, marker.lat])
                    .setPopup(popup)
                    .addTo(map);
            });

        } catch (e) {
            console.error('Failed to render map component:', e);
            container.innerHTML = '<div class="p-8 text-center text-red-500">Failed to load map</div>';
        }
    });
});
```

### Testing
1. Run: `fabric-dashboard generate --mock`
2. Open HTML - should see:
   - ✅ Interactive map
   - ✅ Markers at correct locations
   - ✅ Click markers to see popups
   - ✅ Pan and zoom work
   - ✅ Map spans full width

### Acceptance Criteria
- [ ] Map renders with Mapbox
- [ ] Markers display correctly
- [ ] Popups show on marker click
- [ ] Navigation controls work
- [ ] Full-width layout (col-span-2)

### Resources
- Mapbox GL JS examples: https://docs.mapbox.com/mapbox-gl-js/example/
- MapCard schema: `ui_components.py` lines 68-91

---

## MAT-24: Implement VideoFeed Renderer

**Priority**: Medium
**Estimated Time**: 1 hour
**Dependencies**: Depends on MAT-21

### Goal
Embed YouTube videos in a grid layout.

### What You'll Change
**File**: `fabric_dashboard/core/dashboard_builder.py`

### Step-by-Step Instructions

#### Step 1: Replace Placeholder
Replace `_render_video_feed()` with:

```python
def _render_video_feed(self, component, idx: int) -> str:
    """
    Render YouTube video feed.

    Args:
        component: VideoFeed component.
        idx: Component index.

    Returns:
        HTML for video grid.
    """
    component_id = f"videos-{idx}"

    # Mock video IDs (in real implementation, these come from YouTube API)
    mock_videos = [
        {'id': 'dQw4w9WgXcQ', 'title': 'Video 1'},
        {'id': 'jNQXAC9IVRw', 'title': 'Video 2'},
        {'id': 'y6120QOlsfU', 'title': 'Video 3'},
    ][:component.max_results]

    videos_html = '\\n'.join([
        f'''<div class="aspect-video">
            <iframe
                width="100%"
                height="100%"
                src="https://www.youtube.com/embed/{video['id']}"
                title="{video['title']}"
                frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen
                class="rounded-lg"
            ></iframe>
        </div>'''
        for video in mock_videos
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
```

### Testing
1. Run: `fabric-dashboard generate --mock`
2. Open HTML - should see:
   - ✅ 3 YouTube video embeds
   - ✅ Videos play when clicked
   - ✅ Responsive grid layout

### Acceptance Criteria
- [ ] Videos embed correctly
- [ ] Grid layout is responsive
- [ ] Videos are playable
- [ ] Search query displayed

### Resources
- YouTube iframe API: https://developers.google.com/youtube/iframe_api_reference

---

## MAT-25: Implement EventCalendar Renderer

**Priority**: Medium
**Estimated Time**: 1.5 hours
**Dependencies**: Depends on MAT-21

### Goal
Display upcoming events in a styled calendar list.

### Implementation
Replace `_render_event_calendar()` with a method that:
1. Creates event cards with date, title, location
2. Styles online vs in-person events differently
3. Links to event URLs
4. Shows mock event data

### Testing
Events should display in chronological order with proper styling.

---

## MAT-26: Implement TaskList Renderer

**Priority**: Medium
**Estimated Time**: 1.5 hours
**Dependencies**: Depends on MAT-21

### Goal
Create interactive task list with checkboxes that persist via localStorage.

### Implementation
1. Render checkboxes + task items
2. Add JavaScript for checkbox interaction
3. Save state to localStorage
4. Restore state on page load
5. Visual feedback for completed tasks (strikethrough)

### Testing
Check/uncheck tasks, refresh page - state should persist.

---

## MAT-27: Implement ContentCard Renderer

**Priority**: Medium
**Estimated Time**: 45 minutes
**Dependencies**: Depends on MAT-21

### Goal
Display single article preview with link.

### Implementation
Simple card with:
- Article title
- Brief overview (2-3 sentences)
- Source name
- Publication date
- "Read More" link

### Testing
Card should look clean and link should work.

---

## MAT-28: Integrate Components into Grid Layout

**Priority**: High
**Estimated Time**: 2 hours
**Dependencies**: Depends on MAT-22-27

### Goal
Mix blog cards and UI components in the same grid.

### Implementation
In `_build_cards_grid()`:
1. Combine blog cards + UI components into single list
2. Render mixed grid with proper col-span
3. Map components get col-span-2
4. Other components get col-span-1
5. Maintain drag-drop for all items

### Testing
Dashboard should show interleaved blog cards and widgets.

---

## MAT-29: End-to-End Testing

**Priority**: High
**Estimated Time**: 1 hour
**Dependencies**: Depends on MAT-28

### Goal
Comprehensive testing of complete integration.

### Test Cases
1. Generate dashboard with mock data
2. Verify all component types render
3. Test interactive features (map, tasks, videos)
4. Check responsive behavior
5. Test drag-and-drop
6. Verify error handling

### Acceptance
All components work together seamlessly.