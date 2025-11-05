# Loading State Systems Diagram - Testing Instructions

## Overview

This document provides comprehensive testing instructions for Task 13 of the loading state implementation plan. The loading overlay component has been implemented and is ready for integration testing.

## Current Implementation Status

**Completed:**
- ✅ TypeScript interfaces (`frontend/src/components/loading/types.ts`)
- ✅ StageDetail component (`frontend/src/components/loading/StageDetail.tsx`)
- ✅ PipelineStage component (`frontend/src/components/loading/PipelineStage.tsx`)
- ✅ LoadingOverlay component (`frontend/src/components/loading/LoadingOverlay.tsx`)
- ✅ Backend WebSocket progress messages (`backend/app/services/pipeline_service.py`)

**Pending:**
- ⚠️ Integration with Landing.tsx (Task 12) - needs to be completed before testing

## Prerequisites

Before testing, ensure:

1. **Backend is configured and ready:**
   - Python virtual environment activated
   - All dependencies installed (`pip install -r requirements.txt`)
   - Demo fixtures exist at: `/fabric_dashboard/tests/fixtures/personas/demo.json` and `demo2.json`

2. **Frontend is configured and ready:**
   - Node modules installed (`npm install`)
   - TypeScript build passes with no errors
   - LoadingOverlay component is imported and integrated in Landing.tsx (Task 12)

---

## Testing Setup

### Step 1: Start the Backend Server

Open a new terminal window:

```bash
cd /Users/matildaglynn/Documents/projects/onfabric_mvp/.worktrees/loading-state-diagram/backend

# Activate Python virtual environment
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# Start the FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using StatReload
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Verify Backend is Running:**
Open browser to `http://localhost:8000/docs` - you should see the FastAPI Swagger documentation.

---

### Step 2: Start the Frontend Dev Server

Open a second terminal window:

```bash
cd /Users/matildaglynn/Documents/projects/onfabric_mvp/.worktrees/loading-state-diagram/frontend

# Start Vite dev server
npm run dev
```

**Expected Output:**
```
VITE v5.x.x ready in xxx ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
➜  press h + enter to show help
```

**Verify Frontend is Running:**
Open browser to `http://localhost:5173` - you should see the landing page.

---

## Testing Checklist

### Test 1: Loading Overlay Appears Immediately

**Action:**
1. Navigate to `http://localhost:5173`
2. Click the "demo" persona button

**Expected Behavior:**
- ⬜ Loading overlay appears within 100ms of clicking the button
- ⬜ Full-screen dark overlay (black/95% opacity) covers the entire viewport
- ⬜ No flash of underlying content
- ⬜ Loading overlay is visible before any data is fetched

**Visual Check:**
- Background should be `bg-black/95`
- Content should be centered vertically and horizontally
- Smooth fade-in animation (opacity transition)

---

### Test 2: All 6 Stages Visible from Start

**Action:**
Continue observing the loading overlay from Test 1

**Expected Behavior:**
- ⬜ All 6 pipeline stages are visible immediately:
  1. 📊 Data Fetch
  2. 🧠 Persona Detection
  3. 🎨 Theme Generation
  4. 🧩 Component Selection
  5. 🔍 API Enrichment
  6. 🏗️ Dashboard Assembly

**Visual Check:**
- Each stage should be in a bordered box
- Stages should be stacked vertically with arrow connectors between them
- Initial status: all stages should show as "pending" (gray, low opacity)
- Text should read "Waiting..." for all stages

---

### Test 3: Stages Progress Through Status States

**Action:**
Continue observing the loading process

**Expected Behavior:**
Each stage should transition through these states in sequence:

**Pending State:**
- ⬜ Border: `border-gray-700`
- ⬜ Background: `bg-gray-900`
- ⬜ Opacity: 40%
- ⬜ Status indicator: Empty circle (gray border)
- ⬜ Detail text: "Waiting..."

**Active State:**
- ⬜ Border: `border-blue-500` with glow shadow
- ⬜ Background: `bg-blue-950/30`
- ⬜ Opacity: 100%
- ⬜ Status indicator: Pulsing blue dot (animates scale 1 → 1.2 → 1)
- ⬜ Detail text: Stage-specific data (see Test 4)

**Complete State:**
- ⬜ Border: `border-green-600`
- ⬜ Background: `bg-gray-800`
- ⬜ Opacity: 100%
- ⬜ Status indicator: Green check mark (✓)
- ⬜ Detail text: Stage-specific data remains visible

**Progression Order:**
- ⬜ Data Fetch becomes active first (Step 1)
- ⬜ Persona Detection becomes active second (Step 2)
- ⬜ Theme Generation becomes active third (Step 3)
- ⬜ Component Selection becomes active fourth (Step 4)
- ⬜ API Enrichment becomes active fifth (Step 5)
- ⬜ Dashboard Assembly becomes active last (Step 6)

**Important:** Previous stages should mark as "complete" before the next stage becomes "active"

---

### Test 4: Real Fixture Data Appears in Each Stage

Watch for the following data to appear as each stage becomes active:

#### Stage 1: Data Fetch (📊)

**WebSocket Step:** `"initializing"` or `"data"`

**Expected Data Display:**
- ⬜ "• X interactions loaded" (where X is a number from demo fixture)
- ⬜ "• Platforms: Instagram, Google Photos" (or similar platform list)

**Example:**
```
• 1,247 interactions loaded
• Platforms: Instagram, Google Photos
```

---

#### Stage 2: Persona Detection (🧠)

**WebSocket Step:** `"patterns"` or `"patterns_complete"`

**Expected Data Display:**
- ⬜ Italic text showing professional context or writing style
- ⬜ List of 4 interests/patterns with bullet points
- ⬜ Data should be from the PersonaProfile in demo fixture

**Example:**
```
"Tech-savvy professional who values aesthetics and functionality"

• Photography & Visual Arts
• Modern Design Trends
• Travel & Exploration
• Creative Technology
```

---

#### Stage 3: Theme Generation (🎨)

**WebSocket Step:** `"theme"` or `"theme_complete"`

**Expected Data Display:**
- ⬜ Color swatch showing primary color (small colored square with border)
- ⬜ "Primary: #HEXCODE" text next to swatch
- ⬜ "• Mood: [mood description]" (e.g., "Modern & Vibrant")
- ⬜ Truncated rationale text in smaller, gray, italic font (first 100 chars)

**Example:**
```
[🟦] Primary: #3B82F6
• Mood: Modern & Vibrant
"A bold blue palette that reflects creativity and professional polish, balanced with warm accents..."
```

---

#### Stage 4: Component Selection (🧩)

**WebSocket Step:** `"widgets"` or `"widgets_complete"`

**Expected Data Display:**
- ⬜ Bulleted list of widget names
- ⬜ Should show 4-6 widget types from demo fixture

**Example:**
```
• WeatherWidget
• CalendarWidget
• MapWidget
• TaskWidget
• StatsWidget
```

---

#### Stage 5: API Enrichment (🔍)

**WebSocket Step:** `"search"`, `"enriching"`, or `"content"`

**Expected Data Display:**
- ⬜ Bulleted list showing API calls being made
- ⬜ Should show: "• Calling [API Name]..."

**Example:**
```
• Calling Perplexity...
• Calling Weather API...
• Calling Mapbox...
```

---

#### Stage 6: Dashboard Assembly (🏗️)

**WebSocket Step:** `"building"`

**Expected Data Display:**
- ⬜ "• X content cards" (where X is the number of cards)
- ⬜ "• Y widgets" (where Y is the number of widgets)

**Example:**
```
• 8 content cards
• 5 widgets
```

---

### Test 5: Progress Bar Moves Smoothly

**Action:**
Watch the progress bar at the top of the loading overlay

**Expected Behavior:**
- ⬜ Progress bar starts at 0% width
- ⬜ Progress bar is blue (`bg-blue-500`)
- ⬜ Progress bar animates smoothly (no jumps or stutters)
- ⬜ Progress bar follows these milestones:
  - 0% - Initializing
  - 30% - Patterns loading
  - 50% - Theme generation
  - 70-85% - Widgets selection
  - 75% - Enrichment
  - 95% - Building
  - 100% - Complete

**Visual Check:**
- Container: `bg-gray-800 rounded-full h-3`
- Animation: CSS transition with `duration: 0.3s` and `ease-out` easing
- Should reach 100% right before dashboard appears

---

### Test 6: Current Step Message Updates

**Action:**
Watch the message text below the progress bar

**Expected Behavior:**
- ⬜ Message updates in real-time as stages progress
- ⬜ Text color: `text-gray-400 text-sm`
- ⬜ Messages should match WebSocket `message` field

**Expected Message Sequence (for demo persona):**
1. "Loading demo data..."
2. "Loading patterns..."
3. "Loading theme..."
4. "Loading widgets..."
5. "Enriching widgets with live data..."
6. "Loading content..."
7. "Assembling dashboard..."
8. "Demo ready!"

---

### Test 7: Dashboard Appears After Completion

**Action:**
Wait for the loading process to complete

**Expected Behavior:**
- ⬜ All 6 stages show as "complete" (green borders, checkmarks)
- ⬜ Progress bar reaches 100%
- ⬜ Message shows "Demo ready!"
- ⬜ After ~1 second delay, loading overlay fades out
- ⬜ Dashboard is revealed underneath with demo fixture content

**Visual Check:**
- Smooth fade-out animation (opacity transition)
- Dashboard should display immediately (no loading gap)
- Dashboard should show content matching the demo fixture

---

### Test 8: Repeat Test with demo2 Persona

**Action:**
1. Refresh the page (`http://localhost:5173`)
2. Click the "demo2" persona button
3. Repeat Tests 1-7

**Expected Behavior:**
- ⬜ All tests should pass with demo2 fixture data
- ⬜ Data displayed should be different from demo persona
- ⬜ Same stage progression and timing
- ⬜ Same visual styling and animations

**Compare:**
- Demo2 should have different interests, theme colors, and widget selections
- Progression speed should be similar (both use fixtures, no LLM calls)

---

## Responsive Design Testing

### Test 9: Mobile View (320px - 768px)

**Action:**
1. Open browser DevTools (F12)
2. Enable device emulation
3. Test on iPhone SE (375px) and iPhone 12 Pro (390px)
4. Run through Tests 1-7 on mobile viewport

**Expected Behavior:**
- ⬜ Loading overlay is fully responsive
- ⬜ Header title adjusts: `text-2xl sm:text-3xl`
- ⬜ Padding adjusts: `px-4 sm:px-6 lg:px-8`
- ⬜ Stage boxes stack vertically (already does this)
- ⬜ Text is readable and doesn't overflow
- ⬜ Progress bar spans full width
- ⬜ No horizontal scrolling

---

### Test 10: Tablet View (768px - 1024px)

**Action:**
Test on iPad (768px) and iPad Pro (1024px)

**Expected Behavior:**
- ⬜ Content is centered with `max-w-2xl`
- ⬜ More padding on sides
- ⬜ Stage boxes have comfortable width
- ⬜ All content is easily readable

---

## Error Handling Testing

### Test 11: WebSocket Connection Issues

**Action:**
1. Stop the backend server while frontend is running
2. Click a persona button
3. Observe behavior

**Expected Behavior:**
- ⬜ Loading overlay should appear
- ⬜ Should show error state (if implemented) OR
- ⬜ Should timeout gracefully
- ⬜ No JavaScript console errors (or only WebSocket connection errors)

**Note:** Error state visualization is listed as a "Next Steps" item in the plan, so graceful degradation is acceptable for now.

---

### Test 12: Browser Console Checks

**Action:**
Open browser console (F12) during normal demo generation

**Expected Behavior:**
- ⬜ No TypeScript errors
- ⬜ No React warnings
- ⬜ No network errors (except expected WebSocket messages)
- ⬜ Clean console output

**Acceptable Console Messages:**
- WebSocket connection established logs
- Progress update logs (if logging is enabled)
- Performance metrics

**Unacceptable Console Messages:**
- Red errors
- React key warnings
- Uncaught exceptions
- Type errors

---

## Performance Testing

### Test 13: Animation Performance

**Action:**
1. Open Chrome DevTools > Performance tab
2. Start recording
3. Click demo persona button
4. Wait for completion
5. Stop recording

**Expected Behavior:**
- ⬜ No frame drops during animations
- ⬜ Smooth 60fps throughout
- ⬜ No layout thrashing
- ⬜ Framer Motion animations use GPU (transform/opacity)

**Visual Check:**
- Pulsing blue dot should animate smoothly
- Progress bar should move smoothly
- Stage transitions should be smooth (fade in/out)

---

### Test 14: Memory Leaks

**Action:**
1. Open Chrome DevTools > Memory tab
2. Take heap snapshot
3. Generate 3-5 dashboards in succession
4. Take another heap snapshot
5. Compare

**Expected Behavior:**
- ⬜ No significant memory growth between snapshots
- ⬜ Old dashboard data is garbage collected
- ⬜ No detached DOM nodes
- ⬜ WebSocket connections are properly closed

---

## Accessibility Testing

### Test 15: Screen Reader Testing

**Action:**
Enable screen reader (VoiceOver on Mac, NVDA on Windows)

**Expected Behavior:**
- ⬜ Loading overlay has `role="status"`
- ⬜ Progress updates announced via `aria-live="polite"`
- ⬜ Stage names are read correctly
- ⬜ Status changes are announced

---

### Test 16: Keyboard Navigation

**Action:**
Navigate using only keyboard

**Expected Behavior:**
- ⬜ Can tab to persona buttons
- ⬜ Can activate with Enter/Space
- ⬜ ESC key is captured (currently just logs, per plan)
- ⬜ Focus is managed properly

---

## Cross-Browser Testing

### Test 17: Chrome/Chromium

**Action:**
Test on latest Chrome

**Expected Behavior:**
- ⬜ All tests pass

---

### Test 18: Firefox

**Action:**
Test on latest Firefox

**Expected Behavior:**
- ⬜ All tests pass
- ⬜ Framer Motion animations work correctly
- ⬜ WebSocket connection works

---

### Test 19: Safari

**Action:**
Test on latest Safari (macOS)

**Expected Behavior:**
- ⬜ All tests pass
- ⬜ Backdrop blur effects work (if used)
- ⬜ WebSocket connection works

---

## Documentation of Issues

### Issue Report Template

When you find an issue during testing, document it as follows:

```markdown
## Issue: [Brief Description]

**Severity:** Critical | High | Medium | Low

**Test:** Test #X - [Test Name]

**Steps to Reproduce:**
1.
2.
3.

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What actually happened]

**Screenshots/Video:**
[Attach if possible]

**Browser/Device:**
[Chrome 120, macOS 14.1, etc.]

**Console Errors:**
[Paste any errors]

**Suggested Fix:**
[If you have ideas]
```

---

## Success Criteria

The loading state implementation is considered successful when:

✅ **All primary tests (1-7) pass** on all three browsers (Chrome, Firefox, Safari)
✅ **Mobile responsive tests (9-10) pass** on at least 2 mobile sizes
✅ **No console errors** during normal operation
✅ **Performance tests (13-14)** show no significant issues
✅ **Accessibility basics (15-16)** are in place
✅ **Both demo and demo2** personas work correctly

---

## Known Limitations (Expected)

These are documented as "Next Steps" in the plan and are NOT failures:

- ⚠️ Error state visualization not yet implemented
- ⚠️ Retry mechanism on WebSocket disconnect not yet implemented
- ⚠️ Cancel button for long-running generations not yet implemented
- ⚠️ Animation customization via props not yet implemented

---

## Testing Timeline

**Estimated Time:** 45-60 minutes

1. Setup (Steps 1-2): 5 minutes
2. Primary Tests (1-8): 20 minutes
3. Responsive Tests (9-10): 10 minutes
4. Error & Performance Tests (11-14): 10 minutes
5. Accessibility Tests (15-16): 5 minutes
6. Cross-Browser Tests (17-19): 10 minutes
7. Documentation: 5 minutes

---

## Next Steps After Testing

1. **Document all issues found** using the Issue Report Template
2. **Create a test summary** with pass/fail for each test
3. **Prioritize fixes** (Critical → High → Medium → Low)
4. **If all critical tests pass:**
   - Tag the commit: `git tag -a loading-state-tested -m "Loading state testing complete"`
   - Proceed to Task 14 (Polish and Refinement)
5. **If critical tests fail:**
   - Fix issues before proceeding
   - Re-test affected areas
   - Update this document with any new findings

---

## Contact & Questions

If you encounter issues not covered in this guide:

1. Check the plan document: `/Users/matildaglynn/Documents/projects/onfabric_mvp/.worktrees/loading-state-diagram/docs/plans/2025-11-03-loading-state-systems-diagram-implementation.md`
2. Review component source code in: `/Users/matildaglynn/Documents/projects/onfabric_mvp/.worktrees/loading-state-diagram/frontend/src/components/loading/`
3. Check backend WebSocket messages in: `/Users/matildaglynn/Documents/projects/onfabric_mvp/.worktrees/loading-state-diagram/backend/app/services/pipeline_service.py`

---

## Appendix: WebSocket Message Format Reference

For debugging purposes, here's the expected WebSocket message format:

```json
{
  "type": "progress",
  "step": "patterns",
  "percent": 30,
  "message": "Analyzing patterns with Claude AI...",
  "data": {
    "patterns": [...],
    "persona": {...},
    // ... stage-specific data
  }
}
```

**Step Values:**
- `"initializing"` → Data Fetch stage
- `"data"` → Data Fetch stage
- `"patterns"` → Persona Detection stage (active)
- `"patterns_complete"` → Persona Detection stage (complete)
- `"theme"` → Theme Generation stage (active)
- `"theme_complete"` → Theme Generation stage (complete)
- `"widgets"` → Component Selection stage (active)
- `"widgets_complete"` → Component Selection stage (complete)
- `"search"` → API Enrichment stage
- `"enriching"` → API Enrichment stage
- `"content"` → API Enrichment stage
- `"content_complete"` → API Enrichment stage (complete)
- `"building"` → Dashboard Assembly stage
- `"complete"` → All stages complete

---

**Good luck with testing!** This is a manual testing phase - take your time and be thorough. The loading state is a key user-facing feature that sets the tone for the entire dashboard experience.
