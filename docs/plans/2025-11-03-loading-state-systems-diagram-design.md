# Loading State Systems Diagram Design

**Date:** 2025-11-03
**Status:** Design
**Target:** Demo presentation for technical audience

## Overview

Create an interactive loading state that displays a systems diagram showing the 6-stage dashboard generation pipeline. The diagram provides full visibility into the architecture while the backend generates a personalized dashboard, complementing the live demo narration.

## Requirements

### Audience & Context
- **Primary audience**: Technical developers
- **Use case**: Live demo presentation
- **Goal**: Educate viewers on pipeline architecture while dashboard generates
- **Duration**: ~60 seconds during generation (based on pipeline timing with delays)

### Key Features
- Full-page overlay during generation
- Technical flowchart aesthetic (clean boxes and arrows)
- All 6 stages visible simultaneously (no collapsing)
- Progressive detail revelation as each stage executes
- Real fixture data displayed (from demo.json/demo2.json)
- Syncs with WebSocket progress updates

## Architecture

### Approach: React Component Grid

**Rationale**: Component-based architecture provides maintainability and clean state management. CSS Grid handles layout, Framer Motion handles animations. No manual SVG positioning required.

**Tech Stack**:
- React 19 (already in project)
- TypeScript (type safety for stage data)
- Framer Motion (already installed, handles all animations)
- Tailwind CSS (existing styling system)
- Lucide React (existing icon library)

### Component Structure

```
frontend/src/components/
├── LoadingOverlay.tsx       # Main full-page container
├── PipelineStage.tsx         # Individual stage box component
├── StageDetail.tsx           # Stage-specific detail rendering
└── types.ts                  # TypeScript interfaces for state
```

## Design Specification

### Visual Layout

```
┌─────────────────────────────────────────────────────┐
│                 Generating Your Dashboard           │
│            [================================] 45%   │
│         "Analyzing patterns with Claude AI..."      │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌────────────────────────────────────────┐        │
│  │ [📊] Data Fetch               [✓]      │        │
│  │ • 234 interactions loaded              │        │
│  │ • Platforms: Instagram, Google         │        │
│  └────────────────────────────────────────┘        │
│                    ↓                                │
│  ┌────────────────────────────────────────┐        │
│  │ [🧠] Persona Detection        [●]      │ ← Active│
│  │ "Tech-savvy professional in their      │        │
│  │  late 20s-early 30s, deeply engaged    │        │
│  │  with AI safety research..."           │        │
│  │ • AI safety & alignment                │        │
│  │ • Surf culture & travel                │        │
│  └────────────────────────────────────────┘        │
│                    ↓                                │
│  ┌────────────────────────────────────────┐        │
│  │ [🎨] Theme Generation         [○]      │ ← Pending│
│  │ Waiting...                             │        │
│  └────────────────────────────────────────┘        │
│                    ↓                                │
│  ... (3 more stages below)                         │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Six Pipeline Stages

| Stage | Icon | WebSocket Step | Data Displayed |
|-------|------|---------------|----------------|
| **Data Fetch** | 📊 | `data` | Interaction count, platform names |
| **Persona Detection** | 🧠 | `patterns` | Full persona description, interests list |
| **Theme Generation** | 🎨 | `theme` | Mood, primary color swatch, rationale excerpt |
| **Component Selection** | 🧩 | `widgets` | List of selected component types |
| **API Enrichment** | 🔍 | `search`/`enriching` | API names being called (Perplexity, Weather, Mapbox) |
| **Dashboard Assembly** | 🏗️ | `building` | Card count, component count, assembly status |

### Stage Visual States

**Pending (○)**:
- Grayed out opacity (40%)
- Shows "Waiting..." text
- No detail data visible

**Active (●)**:
- Full opacity, colored border (accent color from theme)
- Pulsing dot indicator (subtle scale animation)
- Detail data animates in line-by-line
- Subtle glow effect on border

**Complete (✓)**:
- Full opacity, neutral border
- Green checkmark with scale pop animation
- Detail data remains visible (collapsed summary)
- Brief green flash on completion

### Fixture Data Integration

For demo personas (`demo` and `demo2`), pull data from:
- `fabric_dashboard/tests/fixtures/personas/demo.json`
- `fabric_dashboard/tests/fixtures/personas/demo2.json`

**Persona Stage Displays**:
```typescript
// From demo.json lines 64-79
{
  writing_style: "intellectually curious yet accessible...",
  interests: [
    "AI safety and alignment research",
    "Surf culture and travel",
    "London startup ecosystem",
    // ...
  ],
  professional_context: "Tech founder or researcher in AI safety space...",
  age_range: "28-35"
}
```

Display as natural language paragraph + bullet list of interests.

## State Management

### LoadingState Interface

```typescript
interface LoadingState {
  currentStep: string;           // Current WebSocket step name
  percent: number;               // Overall progress 0-100
  message: string;               // Current status message

  stageStatuses: {
    data: StageStatus;
    patterns: StageStatus;
    theme: StageStatus;
    widgets: StageStatus;
    enrichment: StageStatus;
    building: StageStatus;
  };

  stageData: {
    data?: { interactions: number; platforms: string[] };
    patterns?: { persona: PersonaProfile; patterns: Pattern[] };
    theme?: { mood: string; primary: string; rationale: string };
    widgets?: { widgets: string[] };
    enrichment?: { apis: string[] };
    building?: { cardCount: number; widgetCount: number };
  };
}

type StageStatus = 'pending' | 'active' | 'complete';
```

### WebSocket Message Mapping

Map incoming progress messages from `pipeline_service.py` to stage updates:

| WebSocket Step | Maps To | Action |
|----------------|---------|--------|
| `data` | `stageStatuses.data = 'active'` | Display interaction count, platforms |
| `patterns` | `stageStatuses.patterns = 'active'` | Display persona from `data.persona` |
| `patterns_complete` | `stageStatuses.patterns = 'complete'` | Show pattern count summary |
| `theme` | `stageStatuses.theme = 'active'` | Display theme mood, colors |
| `widgets` | `stageStatuses.widgets = 'active'` | List component types |
| `search` or `enriching` | `stageStatuses.enrichment = 'active'` | Show API calls |
| `building` | `stageStatuses.building = 'active'` | Show assembly progress |
| `complete` | All stages → `'complete'` | Fade out overlay after 1s |

Existing WebSocket messages in `pipeline_service.py` (lines 138-477) already provide all needed data - no backend changes required.

## Animations

### Framer Motion Specifications

**Initial Load**:
```typescript
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ delay: index * 0.1, duration: 0.4 }}
>
```
All stages fade in staggered (0.1s between each).

**Stage Activation**:
- Border color transition: neutral → accent (0.3s ease)
- Scale pulse: 1.0 → 1.02 → 1.0 (2s infinite)
- Status indicator: ○ → ● with opacity pulse

**Detail Content**:
- Text lines fade in with stagger (0.05s between lines)
- Bullet points slide in from left (x: -10 → 0)
- Numbers count up (using Framer Motion's `animate` prop)

**Completion**:
- Status indicator ○ → ✓ with scale pop (scale: 0.8 → 1.2 → 1.0)
- Border flash: accent → green → neutral (0.5s)
- Glow effect fades out

**Progress Bar**:
- Smooth width transition tracking `percent` state
- Duration: 0.3s ease-out

### Arrow Connectors

Simple CSS-based downward arrows between stages:
```css
.arrow {
  width: 2px;
  height: 20px;
  background: var(--border-color);
  margin: 0 auto;
  position: relative;
}

.arrow::after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: -3px;
  border: 4px solid transparent;
  border-top-color: var(--border-color);
}
```

Optional: Pulse/glow when stage below becomes active.

## Integration Points

### Landing.tsx Changes

Add state and WebSocket handler:

```typescript
const [isGenerating, setIsGenerating] = useState(false);
const [loadingProgress, setLoadingProgress] = useState<LoadingState>({
  currentStep: '',
  percent: 0,
  message: '',
  stageStatuses: {
    data: 'pending',
    patterns: 'pending',
    theme: 'pending',
    widgets: 'pending',
    enrichment: 'pending',
    building: 'pending',
  },
  stageData: {},
});

// WebSocket message handler
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);

  if (data.type === 'progress') {
    setIsGenerating(true);

    // Update current step and progress
    setLoadingProgress(prev => ({
      ...prev,
      currentStep: data.step,
      percent: data.percent,
      message: data.message,
    }));

    // Update stage statuses based on step
    updateStageStatus(data.step, data.data);
  }

  if (data.step === 'complete') {
    // Brief delay to show completion, then hide overlay
    setTimeout(() => {
      setIsGenerating(false);
    }, 1000);
  }
};
```

Render overlay:

```typescript
return (
  <>
    <LoadingOverlay
      show={isGenerating}
      progress={loadingProgress}
    />

    {/* Existing landing page content */}
  </>
);
```

### Lifecycle

**Show overlay when**:
1. User clicks "Generate Dashboard" button
2. WebSocket connection established
3. First progress message received (`step !== 'complete'`)

**Hide overlay when**:
1. WebSocket sends `{step: "complete", percent: 100}`
2. After 1s delay (to show final completion state)
3. Dashboard data ready to render

## Technical Considerations

### Performance
- Use `React.memo` for `PipelineStage` to prevent unnecessary rerenders
- Debounce WebSocket updates if messages arrive faster than 100ms
- Lazy load fixture data only when needed

### Accessibility
- Proper ARIA labels for screen readers
- `role="status"` on progress announcements
- Keyboard dismissible (ESC key) if user wants to skip

### Responsive Design
- On mobile, stages stack vertically (same as desktop)
- Reduce font sizes and padding for smaller screens
- Consider horizontal scroll if needed (unlikely with vertical layout)

### Error Handling
- If WebSocket disconnects, show error state
- Timeout after 120s with "Generation taking longer than expected..." message
- Option to cancel and return to landing

## Open Questions

None - design is complete and ready for implementation.

## Next Steps

1. Set up git worktree for isolated development
2. Create implementation plan with specific tasks
3. Build components following this design
4. Test with demo and demo2 personas
5. Verify timing with live demo narration
