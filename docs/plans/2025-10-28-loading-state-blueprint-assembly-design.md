# Loading State: Blueprint Assembly Design

**Created:** 2025-10-28
**Purpose:** Demo loading state for OnFabric dashboard (15-20 second presentation to 100-person audience)
**Design System:** Zen Terminal aesthetic (JetBrains Mono + Noto Serif JP, paper background, crimson/terminal-green accents)

## Overview

The Blueprint Assembly loading state visualizes OnFabric's process of collating personal context from multiple sources and orchestrating AI agents to generate a personalized UI. It uses a technical blueprint/architectural construction metaphor that unfolds over 15-20 seconds.

**Key Requirements:**
- Hybrid approach: Technical credibility + visual drama
- Emphasize: Multi-source data fetching + personalization engine
- Duration: 15-20 seconds (extended for educational demo)
- Must adhere to existing Zen Terminal design system
- Engaging for non-technical audience while showing real technical process

## Visual Concept

A technical blueprint overlay appears on the existing Zen Terminal aesthetic. Data sources (Instagram, Google, Pinterest) are represented as labeled nodes with connecting lines. Data flows as particles toward a central "construction zone" where UI components are fabricated. Terminal logs stream technical details synchronized with visual events.

## Four-Act Structure

### Act 1: Grid Foundation (0-3 seconds)
**Visual:**
- Technical blueprint grid lines animate in using SVG stroke animations
- Thicker measurement lines with corner brackets at screen edges
- Coordinate grid labels (A1, A2, B1, etc.) appear at edges
- Dimension callouts showing pixel measurements

**Terminal Log:**
```
▸ Initializing blueprint rendering engine
▸ Drawing construction grid...
✓ Foundation ready
```

**Technical Implementation:**
- SVG overlay with `stroke-dasharray` animation
- Corner brackets positioned at viewport edges
- Grid labels: JetBrains Mono, 10px, `--color-gray`
- Measurement lines: `--color-stroke` at 0.3 opacity

### Act 2: Data Sources Connect (3-8 seconds)
**Visual:**
- Three labeled callout boxes materialize in triangular formation:
  - Top-left (20%, 15%): INSTAGRAM
  - Top-right (80%, 20%): GOOGLE
  - Bottom-center (50%, 75%): PINTEREST
- Each node shows:
  - Source name (uppercase, letter-spaced)
  - Interaction count
  - Date range
  - Status indicator
- Connecting lines draw from each source toward center
- Data particles (8x8px colored dots) flow along lines:
  - Instagram: `--color-crimson`
  - Google: `--color-terminal-green`
  - Pinterest: `--color-charcoal`

**Node Structure:**
```
┌─ INSTAGRAM ─────────┐
│ 847 interactions    │
│ 2024-10-01 → now    │
│ status: ✓ fetched   │
└─────────────────────┘
```

**Terminal Log:**
```
▸ Connecting to OnFabric API endpoints
▸ Fetching Instagram data... 847 interactions
▸ Fetching Google data... 1,203 interactions
▸ Fetching Pinterest data... 456 interactions
✓ Data streams established
```

**Technical Implementation:**
- Nodes: Bordered boxes with clockwise draw animation
- Borders animate using CSS border animation or SVG paths
- Connecting lines: SVG `<path>` with animated `stroke-dashoffset`
- Particles: Framer Motion `motion.div` with custom path easing
- Staggered timing: Each source appears 1-1.5s apart

### Act 3: Analysis & Fabrication (8-15 seconds)
**Visual:**
- Center "construction zone" appears: dashed rectangle frame
- Inside frame:
  - Geometric shapes representing widgets materialize with stagger
  - Pattern labels appear: "Evening consumer", "Visual-focused"
  - Color palette swatches appear with hex codes
  - Widget outlines with measurement labels
  - Assembly process visible through semi-transparent overlays

**Terminal Log:**
```
▸ Running pattern detection algorithms
▸ Detected: Evening content consumer
▸ Detected: Visual-focused interactions
▸ Generating color palette from data entropy
▸ Color sampled: #DC143C (primary accent)
▸ Orchestrating AI agents for UI selection
▸ Fabricating personalized widgets...
✓ Interface components assembled
```

**Technical Implementation:**
- Construction frame: Dashed border rectangle, centered
- Widget shapes: SVG primitives (rect, circle) with stroke animations
- Color swatches: 24x24px squares with hex labels
- Staggered reveals: 0.2-0.4s delays between elements
- Use existing `animate-fade-in` easing

### Act 4: Finalization (15-20 seconds)
**Visual:**
- Blueprint grid lines fade out (opacity: 0.3 → 0)
- Construction frame dissolves
- Data source nodes fade
- Finished dashboard revealed underneath with smooth transition
- Return to clean Zen Terminal aesthetic

**Terminal Log:**
```
▸ Finalizing render...
✓ Your dashboard is ready
```

**Technical Implementation:**
- Synchronized fade-out animations
- Stagger timing: Grid → Nodes → Frame (each 0.5s apart)
- Final fade uses same easing as landing page
- Dashboard components already pre-rendered underneath

## Terminal Integration

**Position & Styling:**
- Keep existing top status bar: `generating.interface()` with progress %
- Terminal log: Fixed overlay, bottom-left corner
- Dimensions: max-width 500px, max-height 300px, scrollable
- Background: `rgba(255, 255, 255, 0.95)` with `border: 1px solid var(--color-stroke)`
- Messages in JetBrains Mono, 13px, line-height 1.8

**Message Synchronization:**
- Each terminal message appears exactly when corresponding visual event triggers
- Messages use existing checkmark/arrow indicators:
  - `▸` for in-progress (terminal green, blinking)
  - `✓` for completed (gray, static)
- Smooth scroll-to-bottom as new messages appear

## Design System Adherence

**Colors (existing palette only):**
- `--color-paper`: Background
- `--color-white`: Node backgrounds, terminal background
- `--color-charcoal`: Primary text
- `--color-gray`: Secondary text, completed states
- `--color-crimson`: Instagram data, emphasis accents
- `--color-terminal-green`: Active states, Google data
- `--color-stroke`: Grid lines, borders

**Typography (existing fonts only):**
- JetBrains Mono: All technical labels, terminal, node details
- Noto Serif JP: None used in loading state (preserve for dashboard)
- Font sizes: 10px (grid labels), 12px (nodes), 13px (terminal), 14px (status)

**Motion (aligned with existing):**
- Primary easing: `cubic-bezier(0.16, 1, 0.3, 1)` (from `animate-fade-in`)
- Staggered reveals with `animation-delay` pattern
- Blink animation for active indicators (existing `animate-blink`)
- Draw animations similar to typing effect timing

**Backgrounds:**
- Maintain existing paper texture overlay
- Maintain subtle grid from Landing/Progress
- Red sun circle remains visible (static)
- Geometric accent elements (square, line) stay with parallax
- Blueprint is additive overlay, not replacement

## Component Architecture

**Component Structure:**
```
<BlueprintProgress>
  ├─ <BlueprintGrid /> (SVG overlay)
  ├─ <DataSourceNodes /> (3 nodes + connecting lines)
  ├─ <ConstructionZone /> (center frame + widgets)
  ├─ <TerminalLog /> (bottom-left overlay)
  └─ <StatusBar /> (top bar, reuse from Progress.tsx)
```

**State Management:**
- Single progress value (0-100) drives all animations
- Timeline mapping:
  - 0-15%: Act 1 (Grid)
  - 15-40%: Act 2 (Data Sources)
  - 40-75%: Act 3 (Fabrication)
  - 75-100%: Act 4 (Finalization)
- Terminal messages keyed to progress thresholds
- Visual elements keyed to same thresholds

**Props Interface:**
```typescript
interface BlueprintProgressProps {
  progress: number; // 0-100
  intelligence: IntelligenceData; // Real data for counts/labels
  onComplete?: () => void;
}
```

## Animation Timing Reference

| Time | Progress % | Event |
|------|-----------|-------|
| 0s | 0% | Grid lines start drawing |
| 1.5s | 8% | Corner brackets appear |
| 3s | 15% | Grid complete, Instagram node appears |
| 4.5s | 23% | Google node appears |
| 6s | 30% | Pinterest node appears |
| 7s | 35% | All data streams flowing |
| 8s | 40% | Construction frame appears |
| 9s | 47% | First widget shapes appear |
| 10s | 53% | Pattern labels appear |
| 11.5s | 60% | Color swatches appear |
| 13s | 68% | Widget assembly completes |
| 15s | 75% | Grid begins fade |
| 16s | 82% | Nodes fade |
| 17s | 88% | Frame dissolves |
| 18s | 94% | Final message |
| 20s | 100% | Dashboard revealed |

## Technical Notes

**Performance Considerations:**
- Use CSS transforms for animations where possible (GPU acceleration)
- Limit particle count to ~30-50 active particles
- Use `will-change` sparingly on animated elements
- SVG path animations more performant than canvas for this use case

**Responsive Behavior:**
- Node positions use percentage-based positioning
- Terminal log stacks to bottom on mobile (full width)
- Grid density reduces on smaller viewports
- Particles reduce in count on mobile

**Accessibility:**
- Loading state should have `role="status"` and `aria-live="polite"`
- Progress percentage announced to screen readers
- Terminal log messages available to assistive tech
- Respect `prefers-reduced-motion` (static version fallback)

## Success Criteria

**For Demo:**
- Audience understands OnFabric fetches from multiple sources
- Audience sees AI/orchestration happening (not just loading spinner)
- Technical credibility maintained (real API calls, real data)
- Visually engaging enough to hold attention for 15-20 seconds
- Smooth transition to dashboard feels earned/built

**Technical:**
- Loading state accurately reflects actual data fetching progress
- No performance issues even with all animations running
- Respects existing design system completely
- Reusable for real production loading (not just demo mock)

## Next Steps

1. Create `BlueprintProgress.tsx` component
2. Build SVG grid system with animation
3. Implement data source nodes with particle system
4. Create construction zone with widget fabrication
5. Integrate terminal log with progress sync
6. Add transition to dashboard reveal
7. Test timing/pacing with real data
8. Add reduced-motion fallback
9. Demo run-through for timing adjustment
