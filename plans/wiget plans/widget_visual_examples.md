# Widget Visual Examples & Mockups

This document provides visual descriptions and ASCII mockups of what each widget type will look like in the dashboard.

## Layout Strategy

Widgets can be integrated in two ways:

1. **Widget Cards**: Full card replacements (take up full card space in 2-column grid)
2. **Embedded Widgets**: Small widgets embedded within content cards

For the MVP, we'll focus on **Widget Cards** that replace 1-2 of the 4-8 content cards.

---

## Widget Examples

### 1. Map Widget - Travel Pattern

```
┌──────────────────────────────────────────────────────────────┐
│ Your Travel Footprint                              🗺️  ⚙️    │
│ Mapping your recent Mediterranean adventures                 │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│         🗺️ INTERACTIVE MAP                                   │
│    ┌─────────────────────────────────────────┐              │
│    │         ⭐ Santorini                     │              │
│    │                                          │              │
│    │     🇬🇷 Athens ⭐                        │              │
│    │                                          │              │
│    │                                          │              │
│    │  🗺️ Mediterranean Sea                   │              │
│    │                        ⭐ Crete          │              │
│    │                                          │              │
│    │                                          │              │
│    │                                          │              │
│    └─────────────────────────────────────────┘              │
│                                                               │
│  📍 3 destinations • 🗓️ Sep 2025 • ✈️ 2,400 km traveled     │
│                                                               │
│  Markers:                                                     │
│  ⭐ Athens - "Explored ancient history & local cuisine"      │
│  ⭐ Santorini - "Sunset photography paradise"                │
│  ⭐ Crete - "Next destination on your radar"                 │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

**Visual Features**:
- Interactive pan/zoom map with custom markers
- Color-coded pins matching the dashboard theme
- Connecting routes between destinations (optional)
- Hover tooltips with descriptions
- Click to expand full-screen map view

---

### 2. Image Gallery Widget - Fashion Pattern

```
┌──────────────────────────────────────────────────────────────┐
│ Mediterranean Summer Style                         🎨  🔄    │
│ Fashion inspiration from your interests                      │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌────────┐  ┌────────┐  ┌────────┐                        │
│  │        │  │        │  │        │                        │
│  │ Linen  │  │ Beach  │  │ Sunset │                        │
│  │ Dress  │  │ Cover  │  │ Colors │                        │
│  │        │  │        │  │        │                        │
│  └────────┘  └────────┘  └────────┘                        │
│                                                               │
│  ┌────────┐  ┌────────┐  ┌────────┐                        │
│  │        │  │        │  │        │                        │
│  │ Sandal │  │ Woven  │  │  Straw │                        │
│  │ Styles │  │  Bags  │  │  Hats  │                        │
│  │        │  │        │  │        │                        │
│  └────────┘  └────────┘  └────────┘                        │
│                                                               │
│  📸 Curated from Unsplash • 🔍 "mediterranean summer linen"  │
│  Click any image to view full size                           │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

**Visual Features**:
- Masonry grid layout (Pinterest-style)
- Lazy loading images as you scroll
- Hover effects with captions
- Lightbox modal on click
- Dominant color extraction for theme matching

---

### 3. Checklist Widget - Learning Pattern

```
┌──────────────────────────────────────────────────────────────┐
│ Your Surfing Journey                               📋  ➕    │
│ Track your progress as you learn                            │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Progress: ▰▰▰▰▰▰▱▱▱▱ 60%                                    │
│                                                               │
│  🔴 HIGH PRIORITY                                            │
│  ☑️ Book beginner lessons in Taghazout                      │
│     💬 Found great camp with 5⭐ reviews                     │
│                                                               │
│  ☐ Master the pop-up technique                              │
│     💬 Practice on land first, watch tutorial                │
│     🔗 Watch: "Pop-up in 3 steps"                           │
│                                                               │
│  🟡 MEDIUM PRIORITY                                          │
│  ☐ Learn to read wave patterns                              │
│     💬 Study swell direction and timing                      │
│                                                               │
│  ☑️ Research best beginner beaches in Morocco               │
│     💬 Taghazout & Essaouira look perfect                   │
│                                                               │
│  🟢 LOW PRIORITY                                             │
│  ☐ Buy wetsuit for Atlantic waters                          │
│                                                               │
│  + Add new task                                              │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

**Visual Features**:
- Interactive checkboxes with smooth animations
- Priority color coding
- Expandable notes sections
- Progress bar at top
- Add/edit/delete functionality
- Local storage persistence
- Resource links

---

### 4. World Clock Widget - Multi-timezone Pattern

```
┌──────────────────────────────────────────────────────────────┐
│ Your Time Zones                                    🌍  ⏰    │
│ Stay synchronized across continents                          │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐   │
│   │     🇬🇷      │    │     🇺🇸      │    │     🇯🇵      │   │
│   │   ATHENS    │    │  NEW YORK   │    │    TOKYO    │   │
│   │             │    │             │    │             │   │
│   │      12     │    │      12     │    │      12     │   │
│   │    ╱   ╲    │    │    ╱   ╲    │    │    ╱   ╲    │   │
│   │  9       3  │    │  9       3  │    │  9       3  │   │
│   │    ╲   ╱    │    │    ╲   ╱    │    │    ╲   ╱    │   │
│   │       6     │    │       6     │    │       6     │   │
│   │             │    │             │    │             │   │
│   │   16:34:52  │    │   09:34:52  │    │   22:34:52  │   │
│   │   EEST      │    │   EDT       │    │   JST       │   │
│   │   +3 UTC    │    │   -4 UTC    │    │   +9 UTC    │   │
│   └─────────────┘    └─────────────┘    └─────────────┘   │
│                                                               │
│   Time differences:  NYC -7h  •  Tokyo +6h                  │
│   🌞 Athens: Afternoon  •  🌅 NYC: Morning  •  🌙 Tokyo: Night │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

**Visual Features**:
- Live updating analog clocks (CSS animations)
- Color-coded by theme
- Day/night indicators (sun/moon icons)
- Time zone abbreviations
- Relative time differences
- Smooth second-hand sweep

---

### 5. Timeline Widget - Trip Planning Pattern

```
┌──────────────────────────────────────────────────────────────┐
│ Your Mediterranean Journey                         🗓️  📍    │
│ A chronological view of your adventures                     │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────┐                   │
│  │                                       │                   │
│  │  Sep 15 ─────────● ✈️                │                   │
│  │           Santorini                   │                   │
│  │           "Arrived for sunset views"  │                   │
│  │                  │                    │                   │
│  │                  │                    │                   │
│  │  Sep 18 ─────────● 🏛️                 │                   │
│  │           Athens                      │                   │
│  │           "Explored ancient history"  │                   │
│  │                  │                    │                   │
│  │                  │                    │                   │
│  │  Sep 20 ─────────● 🔍                 │                   │
│  │           Research                    │                   │
│  │           "Planning Morocco surf trip"│                   │
│  │                  │                    │                   │
│  │                  │                    │                   │
│  │  Oct 2025 ───────● 🏄                 │                   │
│  │           Taghazout                   │                   │
│  │           "Surf lessons booked"       │                   │
│  │                  │                    │                   │
│  │                  ▼                    │                   │
│  │           Future adventures...        │                   │
│  │                                       │                   │
│  └──────────────────────────────────────┘                   │
│                                                               │
│  4 milestones  •  2 destinations  •  3 weeks                │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

**Visual Features**:
- Vertical timeline with connecting line
- Icon/emoji markers for event types
- Hover to expand full descriptions
- Past events in full color, future in muted
- Scroll animations (events fade in)
- Optional thumbnail images per event

---

### 6. Chart Widget - Activity Analysis Pattern

```
┌──────────────────────────────────────────────────────────────┐
│ Your Interest Landscape                            📊  🔄    │
│ Visualizing your digital footprint                          │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│   Interest Distribution (Radar Chart)                        │
│                                                               │
│                    Travel                                     │
│                      ▲                                        │
│                   95│ ●                                       │
│                     │  │╲                                     │
│        Culture   80 │  │ ╲                                    │
│              ●──────┼──┼──●── Photography                     │
│               ╲     │  │  ╱                                   │
│                ╲    │  │ ╱                                    │
│                 ╲   │  │╱                                     │
│      Surfing ────●──┴──●────── Food                          │
│                 65     78                                     │
│                                                               │
│   Top Interests:                                             │
│   🥇 Travel (95%) - Dominant pattern                         │
│   🥈 Photography (82%) - Growing interest                    │
│   🥉 Culture (80%) - Consistent engagement                   │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

**Visual Features**:
- Interactive Chart.js visualizations
- Multiple chart types (radar, bar, line, pie)
- Animated transitions
- Theme-matched colors
- Hover tooltips with details
- Responsive sizing

---

### 7. Weather Widget - Surf Conditions Pattern

```
┌──────────────────────────────────────────────────────────────┐
│ Surf Conditions                                    🌊  ☀️    │
│ Real-time conditions for your destinations                  │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌────────────────────────────────────────┐                 │
│  │  📍 Taghazout, Morocco                  │                 │
│  │                                         │                 │
│  │         ☀️                              │                 │
│  │       22°C                              │                 │
│  │     Sunny                               │                 │
│  │                                         │                 │
│  │  🌊 Wave Height:  1.2m (Perfect!)       │                 │
│  │  💨 Wind:  15 km/h NW (Offshore)        │                 │
│  │  🌡️ Water Temp:  19°C                   │                 │
│  │  🌅 Best Time:  Early morning           │                 │
│  │                                         │                 │
│  │  5-Day Forecast:                        │                 │
│  │  Tomorrow  Wed    Thu    Fri    Sat    │                 │
│  │    ☀️      ⛅     ☀️     ⛅     ☀️      │                 │
│  │    23°     21°    24°    22°    23°    │                 │
│  │   🌊1.5m  🌊1.3m 🌊1.8m 🌊1.4m 🌊1.2m  │                 │
│  │                                         │                 │
│  │  📊 Surf Rating:  ⭐⭐⭐⭐⭐ Excellent    │                 │
│  │                                         │                 │
│  └────────────────────────────────────────┘                 │
│                                                               │
│  Updated 5 minutes ago • Source: OpenWeather                │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

**Visual Features**:
- Live weather data via API
- Surf-specific metrics (wave height, wind)
- 5-day forecast with icons
- Condition ratings
- Animated weather icons
- Auto-refresh every 15 min

---

### 8. Quote Widget - Inspirational Pattern

```
┌──────────────────────────────────────────────────────────────┐
│ Travel Wisdom                                      💭  ✨    │
│                                                               │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│                                                               │
│                                                               │
│         "The world is a book, and those                      │
│          who do not travel read only                         │
│                one page."                                     │
│                                                               │
│                  — Saint Augustine                           │
│                                                               │
│                                                               │
│                                                               │
│  ───────────────────────────────────────                     │
│                                                               │
│  This resonates with your Mediterranean journey and          │
│  passion for exploration across cultures.                    │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

**Visual Features**:
- Large, elegant typography
- Optional background gradient or image
- Fade-in animation
- Context explanation below quote
- Curated quotes matching user's patterns
- Optional rotation/carousel

---

## Dashboard Integration Examples

### Example 1: Travel-Heavy Dashboard

```
┌─────────────────────────────────────────────────────────────────┐
│  Your Mediterranean Travel Intelligence Dashboard         🌍    │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────────┬──────────────────────────┐
│  🗺️ MAP WIDGET           │  📝 Content Card         │
│  Your Travel Footprint   │  "Hidden Beaches         │
│  [Interactive Map]       │   of the Med"            │
│                          │                          │
│  3 destinations          │  [Markdown content]      │
│  Athens • Santorini      │                          │
│  • Crete                 │                          │
└──────────────────────────┴──────────────────────────┘

┌──────────────────────────┬──────────────────────────┐
│  🎨 GALLERY WIDGET        │  📝 Content Card         │
│  Mediterranean Style     │  "Learning to Surf"      │
│  [6 fashion images]      │                          │
│                          │  [Markdown content]      │
│                          │                          │
└──────────────────────────┴──────────────────────────┘

┌──────────────────────────┬──────────────────────────┐
│  📋 CHECKLIST WIDGET      │  📝 Content Card         │
│  Surfing Journey         │  "Greek Cuisine Guide"   │
│  [Interactive todos]     │                          │
│  ☑ Book lessons          │  [Markdown content]      │
│  ☐ Master pop-up         │                          │
└──────────────────────────┴──────────────────────────┘
```

### Example 2: Multi-Interest Dashboard

```
┌──────────────────────────┬──────────────────────────┐
│  📊 CHART WIDGET          │  🗺️ MAP WIDGET           │
│  Interest Landscape      │  Global Connections      │
│  [Radar chart]           │  [World map]             │
└──────────────────────────┴──────────────────────────┘

┌──────────────────────────┬──────────────────────────┐
│  📝 Content Card          │  🌍 CLOCK WIDGET          │
│  "Tech Trends 2025"      │  Your Time Zones         │
│  [Markdown]              │  Athens • NYC • Tokyo    │
└──────────────────────────┴──────────────────────────┘
```

---

## Responsive Behavior

### Desktop (> 768px)
- 2-column grid
- Full widget interactivity
- Hover effects enabled

### Tablet (768px - 480px)
- 2-column grid (stacked on smaller tablets)
- Touch-friendly controls
- Simplified animations

### Mobile (< 480px)
- 1-column stack
- Full-width widgets
- Touch gestures enabled
- Reduced animation complexity

---

## Animation & Interaction Examples

### Map Widget Interactions
1. **Pan & Zoom**: Click and drag, scroll to zoom
2. **Marker Click**: Opens tooltip with details
3. **Route Animation**: Lines draw between points on load

### Gallery Widget Interactions
1. **Hover**: Image scales slightly, caption fades in
2. **Click**: Opens lightbox with full image
3. **Lazy Load**: Images fade in as they enter viewport

### Checklist Widget Interactions
1. **Checkbox**: Smooth checkmark animation
2. **Add Item**: Slide down from top
3. **Delete Item**: Fade out and collapse
4. **Drag to Reorder**: Smooth position transitions

### Clock Widget Interactions
1. **Second Hand**: Smooth CSS animation sweep
2. **Click Clock**: Toggle between analog/digital
3. **Hover**: Shows detailed timezone info

---

## Technical Implementation Notes

### Widget Card Structure

```html
<div class="dashboard-card widget-card" data-widget-type="map">
  <!-- Card Header -->
  <div class="widget-header">
    <h2>Your Travel Footprint</h2>
    <div class="widget-controls">
      <button class="widget-refresh">🔄</button>
      <button class="widget-settings">⚙️</button>
    </div>
  </div>
  
  <!-- Widget Content -->
  <div class="widget-content">
    <div id="map-container-123" class="map-widget"></div>
  </div>
  
  <!-- Widget Footer (optional) -->
  <div class="widget-footer">
    <span class="widget-meta">3 destinations • 2,400 km</span>
  </div>
</div>
```

### Widget Styling

```css
.widget-card {
  position: relative;
  min-height: 400px;
}

.widget-content {
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.map-widget {
  height: 400px;
  border-radius: 8px;
}

.widget-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid var(--border);
}

.widget-controls button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  padding: 0.5rem;
  transition: opacity 0.2s;
}

.widget-controls button:hover {
  opacity: 0.7;
}
```

---

## Accessibility Considerations

### Keyboard Navigation
- All widgets navigable via Tab key
- Map: Arrow keys for panning, +/- for zoom
- Gallery: Arrow keys for next/prev image
- Checklist: Enter to toggle, Tab to navigate

### Screen Readers
- Descriptive ARIA labels for all interactive elements
- Alt text for gallery images
- Announced state changes (e.g., "Task completed")

### Color Contrast
- All text maintains 4.5:1 contrast ratio minimum
- Interactive elements have clear focus indicators
- Color not the only indicator of state

---

This visual reference should guide the implementation of each widget type to ensure a cohesive, professional, and impressive dashboard experience.

