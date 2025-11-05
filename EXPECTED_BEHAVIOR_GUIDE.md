# Expected Behavior Guide - Loading State

This is a visual reference guide showing exactly what you should see during dashboard generation.

---

## Timeline Overview

```
0s    Click "demo" button
      ↓
0.1s  Loading overlay appears (black background, fades in)
      ↓
0.2s  All 6 stages visible, all showing "Waiting..." (gray/pending)
      ↓
0.3s  Stage 1 becomes active (blue border, pulsing dot)
      Progress: 0% → 10%
      ↓
0.5s  Stage 1 data appears (interactions, platforms)
      Stage 1 becomes complete (green border, checkmark)
      Stage 2 becomes active
      Progress: 10% → 30%
      ↓
0.8s  Stage 2 data appears (persona interests)
      Stage 2 becomes complete
      Stage 3 becomes active
      Progress: 30% → 50%
      ↓
1.1s  Stage 3 data appears (theme colors, mood)
      Stage 3 becomes complete
      Stage 4 becomes active
      Progress: 50% → 70%
      ↓
1.4s  Stage 4 data appears (widget list)
      Stage 4 becomes complete
      Stage 5 becomes active
      Progress: 70% → 85%
      ↓
1.7s  Stage 5 data appears (API calls)
      Stage 5 becomes complete
      Stage 6 becomes active
      Progress: 85% → 95%
      ↓
2.0s  Stage 6 data appears (card/widget counts)
      Stage 6 becomes complete
      Progress: 95% → 100%
      ↓
2.5s  All stages complete
      Message: "Demo ready!"
      ↓
3.5s  Loading overlay fades out (1 second after completion)
      ↓
3.6s  Dashboard visible
```

**Total Time:** ~3-4 seconds for demo personas (no LLM calls)

---

## Visual States

### Pending Stage (Initial State)

```
┌─────────────────────────────────────────┐
│ 📊  Data Fetch              ⭕         │  ← Gray circle (empty)
│                                         │
│ Waiting...                              │  ← Gray text
│                                         │
└─────────────────────────────────────────┘
   ↑
   Gray border (border-gray-700)
   Low opacity (40%)
   Dark background (bg-gray-900)
```

### Active Stage

```
┌═════════════════════════════════════════┐
│ 📊  Data Fetch              ⚫         │  ← Pulsing blue dot
│                                ↑↓        │     (animates 1→1.2→1)
│ • 1,247 interactions loaded             │
│ • Platforms: Instagram, Google Photos   │  ← Real data appears
│                                         │
└═════════════════════════════════════════┘
   ↑
   Blue border (border-blue-500)
   Glowing shadow (shadow-blue-500/20)
   Full opacity (100%)
   Blue-tinted background (bg-blue-950/30)
```

### Complete Stage

```
┌─────────────────────────────────────────┐
│ 📊  Data Fetch              ✓          │  ← Green checkmark
│                                         │
│ • 1,247 interactions loaded             │
│ • Platforms: Instagram, Google Photos   │  ← Data persists
│                                         │
└─────────────────────────────────────────┘
   ↑
   Green border (border-green-600)
   Full opacity (100%)
   Gray background (bg-gray-800)
```

---

## Progress Bar States

### Initial (0%)
```
┌──────────────────────────────────────────┐
│░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│  ← Empty gray bar
└──────────────────────────────────────────┘
```

### Mid-Progress (50%)
```
┌──────────────────────────────────────────┐
│████████████████████░░░░░░░░░░░░░░░░░░░░│  ← Blue fill (50%)
└──────────────────────────────────────────┘
    ↑
    Smooth animation (300ms ease-out)
```

### Complete (100%)
```
┌──────────────────────────────────────────┐
│████████████████████████████████████████│  ← Blue fill (100%)
└──────────────────────────────────────────┘
```

---

## Stage-Specific Data Examples

### Stage 1: Data Fetch
```
• 1,247 interactions loaded
• Platforms: Instagram, Google Photos
```

### Stage 2: Persona Detection
```
"Tech-savvy professional who values aesthetics and functionality"

• Photography & Visual Arts
• Modern Design Trends
• Travel & Exploration
• Creative Technology
```

### Stage 3: Theme Generation
```
🟦 Primary: #3B82F6
• Mood: Modern & Vibrant
"A bold blue palette that reflects creativity and professional polish..."
```

### Stage 4: Component Selection
```
• WeatherWidget
• CalendarWidget
• MapWidget
• TaskWidget
• StatsWidget
```

### Stage 5: API Enrichment
```
• Calling Perplexity...
• Calling Weather API...
• Calling Mapbox...
```

### Stage 6: Dashboard Assembly
```
• 8 content cards
• 5 widgets
```

---

## Arrow Connectors

Between each stage, you should see a vertical connector:

```
┌─────────────────────┐
│ Stage 1             │
└─────────────────────┘
         │              ← Gray vertical line (w-0.5 h-6 bg-gray-700)
         ↓
┌─────────────────────┐
│ Stage 2             │
└─────────────────────┘
```

---

## Header Section

```
    Generating Your Dashboard               ← Large white title (text-3xl)

    ┌──────────────────────────────────┐
    │████████████████░░░░░░░░░░░░░░░░│    ← Progress bar
    └──────────────────────────────────┘

    Loading patterns...                     ← Current step message (text-gray-400)
```

---

## Color Reference

### State Colors
- **Pending:** Gray (#6B7280 / gray-700)
- **Active:** Blue (#3B82F6 / blue-500)
- **Complete:** Green (#16A34A / green-600)

### Background Colors
- **Overlay:** Black 95% opacity
- **Stage Pending:** Gray 900 (#111827)
- **Stage Active:** Blue 950 30% opacity (#172554 @ 30%)
- **Stage Complete:** Gray 800 (#1F2937)

### Text Colors
- **Title:** White (#FFFFFF)
- **Stage Title:** White (#FFFFFF)
- **Detail Text:** Gray 300 (#D1D5DB)
- **Message:** Gray 400 (#9CA3AF)
- **Rationale:** Gray 400 italic (#9CA3AF)

---

## Animation Reference

### Pulsing Dot (Active Stage Indicator)
```
Animation: scale
Values: 1 → 1.2 → 1
Duration: 2 seconds
Repeat: Infinite
```

### Progress Bar
```
Animation: width
Duration: 300ms
Easing: ease-out
Trigger: On percent change
```

### Stage Fade-In
```
Animation: opacity, translateY
Initial: opacity 0, y +20px
Final: opacity 1, y 0
Duration: 400ms
Delay: index * 100ms (staggered)
```

### Overlay Fade-In
```
Animation: opacity
Initial: 0
Final: 1
Duration: Default framer-motion
```

### Overlay Fade-Out
```
Animation: opacity
Initial: 1
Final: 0
Duration: Default framer-motion
Trigger: 1 second after completion
```

---

## Responsive Breakpoints

### Mobile (< 640px)
- Title: `text-2xl` (smaller)
- Padding: `px-4` (tighter)

### Tablet (640px - 1024px)
- Title: `text-3xl` (larger)
- Padding: `px-6` (more comfortable)

### Desktop (> 1024px)
- Padding: `px-8` (maximum)
- Content max-width: `max-w-2xl` (672px)

---

## What Should NOT Happen

❌ **Flash of underlying content** before overlay appears
❌ **Stages appearing one-by-one** (all 6 should be visible immediately)
❌ **Stages skipping states** (must go pending → active → complete)
❌ **Progress bar jumping** (should be smooth transitions)
❌ **Multiple stages active at once** (only one blue bordered stage at a time)
❌ **Empty stage boxes** after becoming active (data must appear)
❌ **Overlay staying after dashboard loads** (must fade out)
❌ **Console errors** (should be clean)
❌ **Horizontal scrolling** on any viewport size

---

## Timing Expectations

| Event | Expected Time | Tolerance |
|-------|---------------|-----------|
| Overlay appears | < 100ms | ±50ms |
| First stage active | ~300ms | ±100ms |
| Stage transition | ~300-400ms each | ±100ms |
| Total generation | 3-4 seconds | ±1s |
| Overlay fade-out | 1 second after complete | ±200ms |

---

## Accessibility Features

### ARIA Attributes
- Loading overlay: `role="status"`
- Live updates: `aria-live="polite"`
- Label: `aria-label="Dashboard generation in progress"`

### Keyboard Support
- ESC key: Captured (currently logs only)
- Focus management: Proper during overlay display

---

## WebSocket Message Sequence (Demo Persona)

```
1. { step: "initializing", percent: 0, message: "Loading demo data..." }
2. { step: "patterns", percent: 30, message: "Loading patterns..." }
3. { step: "theme", percent: 50, message: "Loading theme..." }
4. { step: "widgets", percent: 70, message: "Loading widgets..." }
5. { step: "enriching", percent: 75, message: "Enriching widgets with live data..." }
6. { step: "content", percent: 85, message: "Loading content..." }
7. { step: "building", percent: 95, message: "Assembling dashboard..." }
8. { step: "complete", percent: 100, message: "Demo ready!" }
```

Each message should include a `data` field with stage-specific information.

---

## Quick Observation Checklist

During a single test run, observe:

1. ✓ Overlay fades in smoothly
2. ✓ All 6 stages visible immediately
3. ✓ Progress bar starts at left, moves right
4. ✓ First stage turns blue (active)
5. ✓ Data appears in first stage
6. ✓ First stage turns green (complete)
7. ✓ Second stage turns blue (active)
8. ✓ Pattern repeats for all 6 stages
9. ✓ Message updates with each stage
10. ✓ Progress bar reaches 100%
11. ✓ All stages show green checkmarks
12. ✓ 1-second pause
13. ✓ Overlay fades out
14. ✓ Dashboard appears

**If all 14 observations are true, the implementation is working correctly.**

---

## Debugging Tips

### If overlay doesn't appear:
- Check: Is `isGenerating` state set to `true`?
- Check: Is LoadingOverlay imported in Landing.tsx?
- Check: Is LoadingOverlay rendered in the component?

### If stages don't update:
- Check: Is WebSocket connection established?
- Check: Is `updateStageFromWebSocket` being called?
- Check: Console logs for WebSocket messages

### If data doesn't appear:
- Check: WebSocket message `data` field content
- Check: Stage mapping in `updateStageFromWebSocket`
- Check: StageDetail component rendering logic

### If animations are choppy:
- Check: CPU usage (should be low)
- Check: GPU acceleration (use will-change CSS)
- Check: Framer Motion is using transform/opacity

---

**This guide should be kept open during testing for quick reference.**
