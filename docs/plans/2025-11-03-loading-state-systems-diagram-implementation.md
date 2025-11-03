# Loading State Systems Diagram Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create an interactive loading overlay showing the 6-stage dashboard generation pipeline with real-time progress updates and fixture data display.

**Architecture:** React component grid with Framer Motion animations, WebSocket integration for progress updates, CSS Grid for layout. Fix existing TypeScript errors first to ensure clean baseline.

**Tech Stack:** React 19, TypeScript, Framer Motion, Tailwind CSS, Lucide React, WebSocket

---

## Phase 1: Fix TypeScript Baseline Errors

### Task 1: Fix Type Import Syntax Issues

**Files:**
- Modify: `frontend/src/components/dashboard/PinBoardLayout.tsx:12`
- Modify: `frontend/src/components/theme/ThemeProvider.tsx:11`
- Modify: `frontend/src/components/widgets/WidgetRegistry.tsx:9`

**Step 1: Fix PinBoardLayout.tsx import**

Change line 12 from:
```typescript
import { Layout } from 'react-grid-layout';
```

To:
```typescript
import type { Layout } from 'react-grid-layout';
```

**Step 2: Fix ThemeProvider.tsx import**

Change line 11 from:
```typescript
import { ReactNode } from 'react';
```

To:
```typescript
import type { ReactNode } from 'react';
```

**Step 3: Fix WidgetRegistry.tsx import**

Change line 9 from:
```typescript
import { ComponentType } from 'react';
```

To:
```typescript
import type { ComponentType } from 'react';
```

**Step 4: Verify fixes**

Run: `cd frontend && npm run build 2>&1 | grep TS1484`
Expected: No TS1484 errors (type import errors should be gone)

**Step 5: Commit**

```bash
git add frontend/src/components/dashboard/PinBoardLayout.tsx frontend/src/components/theme/ThemeProvider.tsx frontend/src/components/widgets/WidgetRegistry.tsx
git commit -m "fix: use type-only imports for verbatimModuleSyntax compliance"
```

---

### Task 2: Fix Pattern Type Issues

**Files:**
- Modify: `frontend/src/components/Progress.tsx:47-48`
- Read: `frontend/src/types.ts` (to understand Pattern type structure)

**Step 1: Check Pattern type definition**

Read: `frontend/src/types.ts`
Look for: `interface Pattern` or `type Pattern`
Note: Pattern likely has `title` not `name` property

**Step 2: Fix Progress.tsx pattern references**

Change lines 47-48 from:
```typescript
const patternName = pattern?.name || 'Unknown';
// ... more pattern.name references
```

To:
```typescript
const patternName = pattern?.title || 'Unknown';
// ... update all pattern.name to pattern.title
```

**Step 3: Verify fixes**

Run: `cd frontend && npm run build 2>&1 | grep "Property 'name'"`
Expected: No "Property 'name' does not exist on type 'Pattern'" errors

**Step 4: Commit**

```bash
git add frontend/src/components/Progress.tsx
git commit -m "fix: use pattern.title instead of pattern.name"
```

---

### Task 3: Fix PersonaType Issues in Landing.tsx

**Files:**
- Modify: `frontend/src/components/Landing.tsx:272,338`
- Read: `frontend/src/types.ts` (to check PersonaType definition)

**Step 1: Check PersonaType definition**

Read: `frontend/src/types.ts`
Look for: `type PersonaType` or `enum PersonaType`
Expected: Need to add 'demo' and 'demo2' to the type

**Step 2: Add demo personas to PersonaType**

In `frontend/src/types.ts`, update PersonaType from:
```typescript
export type PersonaType = 'fitness-enthusiast' | 'creative-professional' | 'tech-learner';
```

To:
```typescript
export type PersonaType = 'fitness-enthusiast' | 'creative-professional' | 'tech-learner' | 'demo' | 'demo2';
```

**Step 3: Verify fixes**

Run: `cd frontend && npm run build 2>&1 | grep "demo"`
Expected: No type errors for 'demo' or 'demo2'

**Step 4: Commit**

```bash
git add frontend/src/types.ts
git commit -m "fix: add demo and demo2 to PersonaType"
```

---

### Task 4: Fix Unused Variables (Batch 1 - Widget Cards)

**Files:**
- Modify: `frontend/src/components/widgets/ArticleCard.tsx:26`
- Modify: `frontend/src/components/widgets/CalendarCard.tsx:28`
- Modify: `frontend/src/components/widgets/ContentCard.tsx:21,23,26`
- Modify: `frontend/src/components/widgets/InfoCard.tsx:20,22`
- Modify: `frontend/src/components/widgets/MapCard.tsx:34`
- Modify: `frontend/src/components/widgets/StatCard.tsx:22`
- Modify: `frontend/src/components/widgets/TaskCard.tsx:25`
- Modify: `frontend/src/components/widgets/VideoCard.tsx:25`

**Step 1: Fix by prefixing unused variables with underscore**

For each widget file, prefix unused destructured variables with `_`:

ArticleCard.tsx line 26:
```typescript
// From: const { id, size, title, ...
const { id: _id, size: _size, title, ...
```

Repeat pattern for all widget files where id/size are destructured but unused.

**Step 2: Remove unused imports in widget files**

CalendarCard.tsx line 9 - remove unused imports:
```typescript
// From: import { Calendar, ChevronLeft, ChevronRight } from 'lucide-react';
import { Calendar } from 'lucide-react';
```

ContentCard.tsx line 9 - remove unused imports:
```typescript
// From: import { BookOpen, Calendar, Newspaper } from 'lucide-react';
import { BookOpen } from 'lucide-react';
```

InfoCard.tsx line 9 - remove unused weather icon imports (if not used in component).

MapCard.tsx line 8 - remove MapPin if unused.

**Step 3: Fix ContentCard unused destructured props**

ContentCard.tsx line 23, 26:
```typescript
// Prefix unused props with underscore
const { id: _id, size: _size, overview: _overview, sourceName: _sourceName, publishedDate: _publishedDate, ...
```

Remove unused formatDate function on line 26 entirely if it's not used.

**Step 4: Fix StatCard unused import**

StatCard.tsx line 12 - remove useEffect if unused:
```typescript
// From: import { useState, useEffect } from 'react';
import { useState } from 'react';
```

**Step 5: Verify widget fixes**

Run: `cd frontend && npm run build 2>&1 | grep "components/widgets"`
Expected: No unused variable errors in widget files

**Step 6: Commit**

```bash
git add frontend/src/components/widgets/*.tsx
git commit -m "fix: remove unused variables and imports in widget components"
```

---

### Task 5: Fix Unused Variables (Batch 2 - Dashboard Components)

**Files:**
- Modify: `frontend/src/components/BlueprintProgress.tsx:42`
- Modify: `frontend/src/components/Dashboard.tsx:101`
- Modify: `frontend/src/components/Landing.tsx:6,33`
- Modify: `frontend/src/components/dashboard/PinBoardLayout.tsx:219,258`

**Step 1: Fix BlueprintProgress.tsx**

Line 42 - either use `dashboardCards` or prefix with underscore:
```typescript
// If truly unused:
const { dashboardCards: _dashboardCards, ...rest } = props;
```

**Step 2: Fix Dashboard.tsx**

Line 101 - remove unused state if not needed:
```typescript
// Remove this line if isReady/setIsReady are unused:
// const [isReady, setIsReady] = useState(false);
```

**Step 3: Fix Landing.tsx**

Line 6 - remove unused Framer Motion imports:
```typescript
// From: import { motion, useScroll, useTransform, AnimatePresence } from 'framer-motion';
import { motion, useScroll } from 'framer-motion';
```

Line 33 - remove unused scrollYProgress:
```typescript
// Remove or comment out:
// const { scrollYProgress } = useScroll();
```

**Step 4: Fix PinBoardLayout.tsx**

Line 219 - prefix or remove unused itemVariants:
```typescript
// Either remove the definition or prefix with underscore
```

Line 258 - prefix unused idx parameter:
```typescript
// From: .map((item, idx) => ...
.map((item, _idx) => ...
```

**Step 5: Verify dashboard component fixes**

Run: `cd frontend && npm run build 2>&1 | grep -E "(BlueprintProgress|Dashboard|Landing|PinBoardLayout)"`
Expected: No unused variable errors in these files

**Step 6: Commit**

```bash
git add frontend/src/components/BlueprintProgress.tsx frontend/src/components/Dashboard.tsx frontend/src/components/Landing.tsx frontend/src/components/dashboard/PinBoardLayout.tsx
git commit -m "fix: remove unused variables in dashboard components"
```

---

### Task 6: Fix ColorScheme Type Incompatibility

**Files:**
- Read: `frontend/src/types.ts` (to check ColorScheme definition)
- Read: `backend/fabric_dashboard/models/schemas.py` (backend ColorScheme definition)
- Modify: `frontend/src/components/Dashboard.tsx:139` (where error occurs)

**Step 1: Investigate the type mismatch**

The error says two ColorScheme types exist but are unrelated. Check:
- Frontend: `frontend/src/types.ts` - ColorScheme interface
- Backend data: What's coming from WebSocket/API

Look for `background_theme.type` field differences.

**Step 2: Determine root cause**

Most likely: Backend returns `background_theme.type` as a string, but frontend expects specific literal type `"solid" | "pattern" | "gradient" | "animated"`.

**Step 3: Add type assertion or type guard**

In `Dashboard.tsx` around line 139, add type assertion:
```typescript
// Before (line 139):
const theme = dashboardData.theme;

// After - assert or validate the type:
const theme = {
  ...dashboardData.theme,
  background_theme: {
    ...dashboardData.theme.background_theme,
    type: dashboardData.theme.background_theme.type as "solid" | "pattern" | "gradient" | "animated"
  }
} as ColorScheme;
```

OR create a validation function:
```typescript
function validateTheme(theme: any): ColorScheme {
  // Validate background_theme.type is one of the allowed values
  const validTypes = ["solid", "pattern", "gradient", "animated"];
  if (!validTypes.includes(theme.background_theme.type)) {
    console.warn(`Invalid theme type: ${theme.background_theme.type}, defaulting to solid`);
    theme.background_theme.type = "solid";
  }
  return theme as ColorScheme;
}

const theme = validateTheme(dashboardData.theme);
```

**Step 4: Verify fix**

Run: `cd frontend && npm run build 2>&1 | grep "ColorScheme"`
Expected: No ColorScheme type incompatibility errors

**Step 5: Commit**

```bash
git add frontend/src/components/Dashboard.tsx
git commit -m "fix: resolve ColorScheme type incompatibility with type assertion"
```

---

### Task 7: Verify Clean Baseline

**Files:**
- None (verification only)

**Step 1: Run full TypeScript build**

Run: `cd frontend && npm run build`
Expected: Build completes successfully with no errors

**Step 2: If build still fails, list remaining errors**

Run: `cd frontend && npm run build 2>&1 | grep "error TS" | head -20`
Expected: Empty (no errors) or identify remaining issues

**Step 3: Fix any remaining errors**

If errors remain:
1. Identify the error type
2. Apply appropriate fix (remove unused, fix import, add type assertion)
3. Repeat verification

**Step 4: Run dev server to confirm it works**

Run: `cd frontend && npm run dev`
Expected: Dev server starts on http://localhost:5173 without errors

**Step 5: Create baseline commit tag**

```bash
git tag -a baseline-clean -m "Clean TypeScript baseline before loading state implementation"
git log --oneline -5
```

Expected: See all fix commits and new tag

---

## Phase 2: Loading State Implementation

### Task 8: Create TypeScript Interfaces

**Files:**
- Create: `frontend/src/components/loading/types.ts`

**Step 1: Create types file**

Create `frontend/src/components/loading/types.ts`:

```typescript
export type StageStatus = 'pending' | 'active' | 'complete';

export interface StageData {
  data?: {
    interactions: number;
    platforms: string[];
  };
  patterns?: {
    persona: PersonaProfile;
    patterns: Pattern[];
  };
  theme?: {
    mood: string;
    primary: string;
    rationale: string;
  };
  widgets?: {
    widgets: string[];
  };
  enrichment?: {
    apis: string[];
  };
  building?: {
    cardCount: number;
    widgetCount: number;
  };
}

export interface LoadingState {
  currentStep: string;
  percent: number;
  message: string;
  stageStatuses: {
    data: StageStatus;
    patterns: StageStatus;
    theme: StageStatus;
    widgets: StageStatus;
    enrichment: StageStatus;
    building: StageStatus;
  };
  stageData: StageData;
}

export interface PipelineStageConfig {
  id: string;
  title: string;
  icon: string;
  websocketStep: string[];
}
```

**Step 2: Import shared types from main types file**

Add at top:
```typescript
import { Pattern, PersonaProfile } from '../types';
```

**Step 3: Commit**

```bash
git add frontend/src/components/loading/types.ts
git commit -m "feat: add TypeScript interfaces for loading state"
```

---

### Task 9: Create StageDetail Component

**Files:**
- Create: `frontend/src/components/loading/StageDetail.tsx`

**Step 1: Create component file**

Create `frontend/src/components/loading/StageDetail.tsx`:

```typescript
import React from 'react';
import { StageData } from './types';

interface StageDetailProps {
  type: string;
  data?: StageData[keyof StageData];
  status: 'pending' | 'active' | 'complete';
}

export const StageDetail: React.FC<StageDetailProps> = ({ type, data, status }) => {
  if (status === 'pending') {
    return <div className="text-gray-400 text-sm">Waiting...</div>;
  }

  if (!data) return null;

  switch (type) {
    case 'data':
      return <DataStageDetail data={data as StageData['data']} />;
    case 'patterns':
      return <PersonaStageDetail data={data as StageData['patterns']} />;
    case 'theme':
      return <ThemeStageDetail data={data as StageData['theme']} />;
    case 'widgets':
      return <WidgetsStageDetail data={data as StageData['widgets']} />;
    case 'enrichment':
      return <EnrichmentStageDetail data={data as StageData['enrichment']} />;
    case 'building':
      return <BuildingStageDetail data={data as StageData['building']} />;
    default:
      return null;
  }
};

// Sub-components for each stage type
const DataStageDetail: React.FC<{ data?: StageData['data'] }> = ({ data }) => {
  if (!data) return null;
  return (
    <div className="text-sm space-y-1">
      <div>• {data.interactions} interactions loaded</div>
      <div>• Platforms: {data.platforms.join(', ')}</div>
    </div>
  );
};

const PersonaStageDetail: React.FC<{ data?: StageData['patterns'] }> = ({ data }) => {
  if (!data?.persona) return null;
  const persona = data.persona;

  return (
    <div className="text-sm space-y-2">
      <p className="italic text-gray-300">
        {persona.professional_context || persona.writing_style}
      </p>
      <div className="space-y-1">
        {persona.interests.slice(0, 4).map((interest, idx) => (
          <div key={idx}>• {interest}</div>
        ))}
      </div>
    </div>
  );
};

const ThemeStageDetail: React.FC<{ data?: StageData['theme'] }> = ({ data }) => {
  if (!data) return null;
  return (
    <div className="text-sm space-y-1">
      <div className="flex items-center gap-2">
        <div
          className="w-4 h-4 rounded border border-gray-600"
          style={{ backgroundColor: data.primary }}
        />
        <span>Primary: {data.primary}</span>
      </div>
      <div>• Mood: {data.mood}</div>
      {data.rationale && (
        <div className="text-xs text-gray-400 italic">
          {data.rationale.slice(0, 100)}...
        </div>
      )}
    </div>
  );
};

const WidgetsStageDetail: React.FC<{ data?: StageData['widgets'] }> = ({ data }) => {
  if (!data?.widgets) return null;
  return (
    <div className="text-sm space-y-1">
      {data.widgets.map((widget, idx) => (
        <div key={idx}>• {widget}</div>
      ))}
    </div>
  );
};

const EnrichmentStageDetail: React.FC<{ data?: StageData['enrichment'] }> = ({ data }) => {
  if (!data?.apis) return null;
  return (
    <div className="text-sm space-y-1">
      {data.apis.map((api, idx) => (
        <div key={idx}>• Calling {api}...</div>
      ))}
    </div>
  );
};

const BuildingStageDetail: React.FC<{ data?: StageData['building'] }> = ({ data }) => {
  if (!data) return null;
  return (
    <div className="text-sm space-y-1">
      <div>• {data.cardCount} content cards</div>
      <div>• {data.widgetCount} widgets</div>
    </div>
  );
};
```

**Step 2: Commit**

```bash
git add frontend/src/components/loading/StageDetail.tsx
git commit -m "feat: add StageDetail component for rendering stage-specific data"
```

---

### Task 10: Create PipelineStage Component

**Files:**
- Create: `frontend/src/components/loading/PipelineStage.tsx`

**Step 1: Create component file**

Create `frontend/src/components/loading/PipelineStage.tsx`:

```typescript
import React from 'react';
import { motion } from 'framer-motion';
import { Check } from 'lucide-react';
import { StageDetail } from './StageDetail';
import { StageStatus, StageData } from './types';

interface PipelineStageProps {
  id: string;
  title: string;
  icon: string;
  status: StageStatus;
  data?: StageData[keyof StageData];
  index: number;
}

export const PipelineStage: React.FC<PipelineStageProps> = ({
  id,
  title,
  icon,
  status,
  data,
  index,
}) => {
  const getStatusStyles = () => {
    switch (status) {
      case 'active':
        return 'border-blue-500 bg-blue-950/30 shadow-lg shadow-blue-500/20';
      case 'complete':
        return 'border-green-600 bg-gray-800';
      case 'pending':
      default:
        return 'border-gray-700 bg-gray-900 opacity-40';
    }
  };

  const getStatusIndicator = () => {
    switch (status) {
      case 'active':
        return (
          <motion.div
            className="w-3 h-3 bg-blue-500 rounded-full"
            animate={{ scale: [1, 1.2, 1] }}
            transition={{ repeat: Infinity, duration: 2 }}
          />
        );
      case 'complete':
        return (
          <motion.div
            initial={{ scale: 0.8 }}
            animate={{ scale: 1 }}
            className="text-green-500"
          >
            <Check size={16} />
          </motion.div>
        );
      case 'pending':
      default:
        return <div className="w-3 h-3 border-2 border-gray-600 rounded-full" />;
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1, duration: 0.4 }}
      className={`border-2 rounded-lg p-4 transition-all duration-300 ${getStatusStyles()}`}
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-3">
          <span className="text-2xl">{icon}</span>
          <h3 className="font-semibold text-white">{title}</h3>
        </div>
        <div className="flex items-center gap-2">
          {getStatusIndicator()}
        </div>
      </div>

      {/* Detail Content */}
      <div className="mt-3 text-gray-300">
        <StageDetail type={id} data={data} status={status} />
      </div>
    </motion.div>
  );
};
```

**Step 2: Commit**

```bash
git add frontend/src/components/loading/PipelineStage.tsx
git commit -m "feat: add PipelineStage component with animations and status indicators"
```

---

### Task 11: Create LoadingOverlay Component

**Files:**
- Create: `frontend/src/components/loading/LoadingOverlay.tsx`

**Step 1: Create component file with stage config**

Create `frontend/src/components/loading/LoadingOverlay.tsx`:

```typescript
import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { PipelineStage } from './PipelineStage';
import { LoadingState, PipelineStageConfig } from './types';

interface LoadingOverlayProps {
  show: boolean;
  progress: LoadingState;
}

const PIPELINE_STAGES: PipelineStageConfig[] = [
  {
    id: 'data',
    title: 'Data Fetch',
    icon: '📊',
    websocketStep: ['data', 'initializing'],
  },
  {
    id: 'patterns',
    title: 'Persona Detection',
    icon: '🧠',
    websocketStep: ['patterns', 'patterns_complete'],
  },
  {
    id: 'theme',
    title: 'Theme Generation',
    icon: '🎨',
    websocketStep: ['theme', 'theme_complete'],
  },
  {
    id: 'widgets',
    title: 'Component Selection',
    icon: '🧩',
    websocketStep: ['widgets', 'widgets_complete'],
  },
  {
    id: 'enrichment',
    title: 'API Enrichment',
    icon: '🔍',
    websocketStep: ['search', 'enriching', 'content'],
  },
  {
    id: 'building',
    title: 'Dashboard Assembly',
    icon: '🏗️',
    websocketStep: ['building'],
  },
];

export const LoadingOverlay: React.FC<LoadingOverlayProps> = ({ show, progress }) => {
  return (
    <AnimatePresence>
      {show && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black/95 z-50 overflow-y-auto"
        >
          <div className="min-h-screen flex flex-col items-center justify-start py-8 px-4">
            {/* Header */}
            <motion.div
              initial={{ y: -20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              className="text-center mb-8 w-full max-w-2xl"
            >
              <h1 className="text-3xl font-bold text-white mb-4">
                Generating Your Dashboard
              </h1>

              {/* Progress Bar */}
              <div className="w-full bg-gray-800 rounded-full h-3 overflow-hidden mb-2">
                <motion.div
                  className="h-full bg-blue-500"
                  initial={{ width: 0 }}
                  animate={{ width: `${progress.percent}%` }}
                  transition={{ duration: 0.3, ease: 'easeOut' }}
                />
              </div>

              {/* Current Step Message */}
              <p className="text-gray-400 text-sm">
                {progress.message || 'Starting...'}
              </p>
            </motion.div>

            {/* Pipeline Stages */}
            <div className="w-full max-w-2xl space-y-4">
              {PIPELINE_STAGES.map((stage, index) => (
                <React.Fragment key={stage.id}>
                  <PipelineStage
                    id={stage.id}
                    title={stage.title}
                    icon={stage.icon}
                    status={progress.stageStatuses[stage.id as keyof typeof progress.stageStatuses]}
                    data={progress.stageData[stage.id as keyof typeof progress.stageData]}
                    index={index}
                  />

                  {/* Arrow connector (except after last stage) */}
                  {index < PIPELINE_STAGES.length - 1 && (
                    <div className="flex justify-center">
                      <div className="w-0.5 h-6 bg-gray-700" />
                    </div>
                  )}
                </React.Fragment>
              ))}
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};
```

**Step 2: Create index file for clean imports**

Create `frontend/src/components/loading/index.ts`:

```typescript
export { LoadingOverlay } from './LoadingOverlay';
export type { LoadingState } from './types';
```

**Step 3: Commit**

```bash
git add frontend/src/components/loading/LoadingOverlay.tsx frontend/src/components/loading/index.ts
git commit -m "feat: add LoadingOverlay component with pipeline visualization"
```

---

### Task 12: Integrate LoadingOverlay with Landing Component

**Files:**
- Modify: `frontend/src/components/Landing.tsx`

**Step 1: Import LoadingOverlay**

Add at top of `Landing.tsx`:
```typescript
import { LoadingOverlay, LoadingState } from './loading';
```

**Step 2: Add loading state**

After existing state declarations (around line 30-40):
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
```

**Step 3: Create helper function to update stage status**

Add before the component return:
```typescript
const updateStageFromWebSocket = (step: string, data: any) => {
  // Map WebSocket step to stage ID and update status
  const stageMapping: Record<string, keyof LoadingState['stageStatuses']> = {
    'initializing': 'data',
    'data': 'data',
    'patterns': 'patterns',
    'patterns_complete': 'patterns',
    'theme': 'theme',
    'theme_complete': 'theme',
    'widgets': 'widgets',
    'widgets_complete': 'widgets',
    'search': 'enrichment',
    'enriching': 'enrichment',
    'content': 'enrichment',
    'content_complete': 'enrichment',
    'building': 'building',
  };

  const stageId = stageMapping[step];
  if (!stageId) return;

  setLoadingProgress(prev => {
    const newStatuses = { ...prev.stageStatuses };
    const newData = { ...prev.stageData };

    // Mark current stage as active
    newStatuses[stageId] = 'active';

    // Mark previous stages as complete
    const stages: (keyof LoadingState['stageStatuses'])[] = ['data', 'patterns', 'theme', 'widgets', 'enrichment', 'building'];
    const currentIndex = stages.indexOf(stageId);
    for (let i = 0; i < currentIndex; i++) {
      if (newStatuses[stages[i]] !== 'complete') {
        newStatuses[stages[i]] = 'complete';
      }
    }

    // Store stage-specific data
    if (data) {
      if (stageId === 'data' && data.interactions) {
        newData.data = {
          interactions: data.interactions,
          platforms: data.platforms || [],
        };
      } else if (stageId === 'patterns' && data.patterns) {
        newData.patterns = {
          persona: data.persona,
          patterns: data.patterns,
        };
      } else if (stageId === 'theme' && data.mood) {
        newData.theme = {
          mood: data.mood,
          primary: data.primary,
          rationale: data.rationale,
        };
      } else if (stageId === 'widgets' && data.widgets) {
        newData.widgets = {
          widgets: data.widgets,
        };
      } else if (stageId === 'enrichment') {
        // Track API calls
        newData.enrichment = {
          apis: ['Perplexity', 'Weather API', 'Mapbox'],
        };
      } else if (stageId === 'building' && data.cardCount) {
        newData.building = {
          cardCount: data.cardCount,
          widgetCount: data.widgetCount,
        };
      }
    }

    return {
      ...prev,
      stageStatuses: newStatuses,
      stageData: newData,
    };
  });
};
```

**Step 4: Update WebSocket message handler**

Find the existing `ws.onmessage` handler and update it:
```typescript
ws.onmessage = (event) => {
  const message = JSON.parse(event.data);

  if (message.type === 'progress') {
    setIsGenerating(true);

    // Update progress bar and message
    setLoadingProgress(prev => ({
      ...prev,
      currentStep: message.step,
      percent: message.percent,
      message: message.message,
    }));

    // Update stage statuses
    updateStageFromWebSocket(message.step, message.data);
  }

  if (message.step === 'complete') {
    // Mark all stages complete
    setLoadingProgress(prev => ({
      ...prev,
      stageStatuses: {
        data: 'complete',
        patterns: 'complete',
        theme: 'complete',
        widgets: 'complete',
        enrichment: 'complete',
        building: 'complete',
      },
    }));

    // Hide overlay after brief delay
    setTimeout(() => {
      setIsGenerating(false);
    }, 1000);
  }

  // ... rest of existing message handling (dashboardReady, error, etc.)
};
```

**Step 5: Render LoadingOverlay**

In the component return statement, add LoadingOverlay before existing content:
```typescript
return (
  <>
    <LoadingOverlay show={isGenerating} progress={loadingProgress} />

    {/* Existing landing page content */}
    <div className="min-h-screen bg-gray-950 text-white">
      {/* ... existing JSX ... */}
    </div>
  </>
);
```

**Step 6: Commit**

```bash
git add frontend/src/components/Landing.tsx
git commit -m "feat: integrate LoadingOverlay with Landing component and WebSocket"
```

---

### Task 13: Test with Demo Personas

**Files:**
- None (testing only)

**Step 1: Start backend server**

In terminal 1:
```bash
cd backend
source venv/bin/activate  # or however you activate your Python env
uvicorn app.main:app --reload
```

Expected: Backend starts on http://localhost:8000

**Step 2: Start frontend dev server**

In terminal 2:
```bash
cd frontend
npm run dev
```

Expected: Frontend starts on http://localhost:5173

**Step 3: Test with demo persona**

1. Open http://localhost:5173 in browser
2. Click "demo" persona button
3. Observe:
   - Loading overlay appears immediately
   - All 6 stages visible from start
   - Stages progress from pending → active → complete
   - Real fixture data appears in each stage
   - Progress bar moves smoothly
   - Dashboard appears after completion

**Step 4: Test with demo2 persona**

Repeat step 3 with demo2 button.

**Step 5: Document any issues**

If issues found, note them for fixes:
- Animation glitches
- Data not appearing
- WebSocket sync issues
- Timing problems

---

### Task 14: Polish and Refinement

**Files:**
- Modify: `frontend/src/components/loading/LoadingOverlay.tsx`
- Modify: `frontend/src/components/loading/PipelineStage.tsx`

**Step 1: Add responsive design**

In `LoadingOverlay.tsx`, update container classes:
```typescript
<div className="min-h-screen flex flex-col items-center justify-start py-8 px-4 sm:px-6 lg:px-8">
  <div className="text-center mb-8 w-full max-w-2xl">
    <h1 className="text-2xl sm:text-3xl font-bold text-white mb-4">
```

**Step 2: Add keyboard accessibility**

In `LoadingOverlay.tsx`, add escape key handler:
```typescript
React.useEffect(() => {
  if (!show) return;

  const handleEscape = (e: KeyboardEvent) => {
    if (e.key === 'Escape') {
      // Optional: allow dismissing with ESC
      // For now, just log - can expand later
      console.log('User pressed ESC during loading');
    }
  };

  window.addEventListener('keydown', handleEscape);
  return () => window.removeEventListener('keydown', handleEscape);
}, [show]);
```

**Step 3: Add ARIA labels**

Update LoadingOverlay div:
```typescript
<motion.div
  role="status"
  aria-live="polite"
  aria-label="Dashboard generation in progress"
  // ... rest of props
>
```

**Step 4: Optimize animation performance**

In `PipelineStage.tsx`, add `will-change` for better performance:
```typescript
className={`border-2 rounded-lg p-4 transition-all duration-300 will-change-transform ${getStatusStyles()}`}
```

**Step 5: Commit**

```bash
git add frontend/src/components/loading/LoadingOverlay.tsx frontend/src/components/loading/PipelineStage.tsx
git commit -m "polish: add responsive design, accessibility, and performance optimizations"
```

---

### Task 15: Final Testing and Documentation

**Files:**
- Create: `frontend/src/components/loading/README.md`

**Step 1: Create component documentation**

Create `frontend/src/components/loading/README.md`:

```markdown
# Loading State System Diagram

Interactive loading overlay that visualizes the 6-stage dashboard generation pipeline.

## Components

- **LoadingOverlay**: Full-page overlay container with progress bar
- **PipelineStage**: Individual stage box with status indicator and details
- **StageDetail**: Stage-specific data rendering (persona, theme, etc.)

## Usage

```tsx
import { LoadingOverlay, LoadingState } from './components/loading';

const [isGenerating, setIsGenerating] = useState(false);
const [progress, setProgress] = useState<LoadingState>({...});

<LoadingOverlay show={isGenerating} progress={progress} />
```

## WebSocket Integration

Listens for progress messages from `pipeline_service.py`:
- Maps WebSocket `step` field to stage IDs
- Updates stage status (pending/active/complete)
- Displays stage-specific data from `data` field

## Stage Configuration

Edit `PIPELINE_STAGES` in `LoadingOverlay.tsx` to modify stages:
```typescript
const PIPELINE_STAGES = [
  { id: 'data', title: 'Data Fetch', icon: '📊', websocketStep: ['data'] },
  // ...
];
```

## Styling

Uses Tailwind CSS with custom animations via Framer Motion.
Main colors:
- Active: blue-500
- Complete: green-600
- Pending: gray-700
```

**Step 2: Run final build test**

```bash
cd frontend
npm run build
```

Expected: Build succeeds with no errors

**Step 3: Run linter**

```bash
npm run lint
```

Expected: No linting errors in new files

**Step 4: Create final commit**

```bash
git add frontend/src/components/loading/README.md
git commit -m "docs: add loading state component documentation"
```

**Step 5: Tag completion**

```bash
git tag -a loading-state-complete -m "Loading state systems diagram implementation complete"
git log --oneline --graph -10
```

---

## Verification Checklist

Before marking complete, verify:

- [ ] TypeScript build passes with no errors
- [ ] Dev server runs without errors
- [ ] Loading overlay appears on demo generation
- [ ] All 6 stages visible and progress correctly
- [ ] Real fixture data displays in each stage
- [ ] Progress bar animates smoothly
- [ ] Stages transition pending → active → complete
- [ ] Dashboard appears after completion (1s delay)
- [ ] Responsive on mobile screens
- [ ] ESC key handler present (accessibility)
- [ ] No console errors during generation
- [ ] Works for both demo and demo2 personas

## Next Steps

After completion:
1. Use @superpowers:finishing-a-development-branch to merge back to main
2. Consider adding:
   - Error state visualization
   - Retry mechanism on WebSocket disconnect
   - Cancel button for long-running generations
   - Animation customization via props
