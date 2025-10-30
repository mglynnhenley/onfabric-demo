# Generative Dashboard Reveal Design

**Date:** 2025-10-30
**Status:** Design Approved
**Implementation Target:** 3 weeks

## Overview

Transform the dashboard loading experience to feel "generative" and AI-crafted by implementing skeleton-to-content morphing animations and AI-generated background imagery. This enhances the perception that the dashboard is being uniquely created for each user.

## Goals

1. Make dashboard generation feel more "AI-powered" and personalized
2. Improve perceived performance with immediate skeleton feedback
3. Add visual "wow" factor through AI-generated backgrounds
4. Maintain fast Time to Interactive (<3s)
5. Give AI more design control over visual presentation

## Design Decisions

### Core Approach: Frontend Animation Orchestrator

**Rationale:** Implement animation choreography entirely in the frontend with zero backend changes to existing dashboard generation. This allows rapid UX validation while keeping the architecture simple.

**Trade-offs:**
- ✅ Zero backend refactoring required
- ✅ Can ship Phase 1 (animations) immediately
- ✅ Easy to toggle with feature flag
- ✅ Tests UX before investing in streaming architecture
- ❌ Not "true" real-time generation (simulated)
- ❌ Backend generates everything before first byte

### Skeleton-to-Content Morphing

**User Experience:**
1. Dashboard loads → All card skeletons appear instantly (0ms)
2. Brief pause (500ms) to let user see layout
3. Cards morph from skeleton → real content with 150ms stagger
4. Background begins generating after last card visible

**Animation Details:**
- Fixed timing (not AI-controlled): 150ms stagger, 600ms duration per card
- Each card type has specialized skeleton placeholder
- Smooth cross-fade with brief overlap (100ms at 50% opacity)
- Respects `prefers-reduced-motion` for accessibility

### AI Design Control

**What AI Controls:**
- ✅ Color palette and typography (existing)
- ✅ Background image prompt generation (new)
- ✅ Theme "mood" classification (new)

**What AI Does NOT Control:**
- ❌ Animation timing/choreography (frontend constants)
- ❌ Layout arrangement (existing pin board logic)
- ❌ Card sizing (existing responsive logic)

**Rationale:** Separation of concerns. Visual identity is AI domain, interaction design is frontend domain.

### Background Generation Strategy

**Timing:** After dashboard is interactive (progressive enhancement)

**Flow:**
1. Backend generates `background_prompt` during theme generation (no added latency)
2. Dashboard JSON includes prompt but not image
3. Frontend shows skeletons → content → interactive dashboard
4. Background API called: `POST /api/generate-background`
5. OpenAI DALL-E 3 generates image (3-8 seconds)
6. Image cross-fades into view at low opacity (0.15-0.3)

**Service:** OpenAI DALL-E 3
- Quality: "standard" ($0.04 per image)
- Size: 1792x1024 (landscape)
- Style: "natural" (or "vivid" for energetic moods)

**Fallback:** If generation fails/times out, dashboard remains functional with existing paper texture background. No degraded experience.

## Architecture

### Component Structure

```
<GenerativeReveal>
  <SkeletonLayout cards={skeletonData} />
  <AnimatedDashboard cards={fullData} />
  <BackgroundLoader theme={theme} />
</GenerativeReveal>
```

### State Management

```typescript
type RevealState =
  | { phase: 'skeleton', data: CardSkeleton[] }
  | { phase: 'revealing', data: DashboardCard[], progress: number }
  | { phase: 'complete', data: DashboardCard[], background?: string }
```

**Lifecycle:**
1. Receive dashboard JSON from `/generate`
2. Extract skeleton metadata, render immediately
3. After 500ms, transition to 'revealing'
4. Stagger card content reveal (150ms between cards)
5. On complete, trigger background generation
6. Cross-fade background when received

### Data Schema Changes

**Backend Theme JSON (Extended):**
```python
{
  "colors": { "primary": "#...", ... },
  "fonts": { "heading": "...", ... },
  "background_prompt": "abstract flowing lines in teal and coral, minimalist, paper texture"
}
```

**New Backend Endpoint:**
```
POST /api/generate-background
Body: { prompt: string, theme_id: string }
Response: { url: string, expires_at: timestamp }
```

### Frontend Components

**New Components:**
- `GenerativeReveal.tsx` - Orchestrates reveal lifecycle
- `SkeletonLayout.tsx` - Renders card skeletons
- `BackgroundLoader.tsx` - Handles DALL-E API call and fade-in
- Skeleton variants: `StatSkeleton`, `MapSkeleton`, `CalendarSkeleton`, etc.

**Modified Components:**
- `Dashboard.tsx` - Wrapped by GenerativeReveal (no internal changes)
- `ThemeProvider.tsx` - Reads expanded theme JSON

### Backend Changes

**Modified:**
- `ThemeGenerator.generate_theme()` - Add background_prompt to LLM output
- LLM prompt enhancement - Include instruction to generate DALL-E prompt

**New:**
- `POST /api/generate-background` endpoint
- OpenAI DALL-E 3 integration
- Prompt sanitization (strip user text, use only AI-generated descriptions)

## Error Handling

### Background Generation Failures

- **Timeout (>10s):** Cancel request, log error, keep texture background
- **API Error:** Silent fallback, optional toast notification
- **Network offline:** Skip generation entirely
- **Content policy violation:** Pre-sanitize prompts, log violations

### Performance Degradation

- **Low-end devices:** Detect via `navigator.hardwareConcurrency < 4`, reduce stagger to 50ms
- **Reduced motion:** Respect `prefers-reduced-motion`, instant reveal
- **Slow dashboard load:** Existing Progress component handles (>5s)

### Theme Data Issues

- **Missing theme:** Fallback to default theme, skip background
- **Invalid background_prompt:** Skip background generation
- **LLM failure:** Use hardcoded default theme

### Race Conditions

- Background arrives before reveal complete → store in state, apply after phase='complete'
- User navigates away mid-reveal → cleanup timers, cancel background fetch
- Multiple rapid generations → cancel in-flight requests

## Testing Strategy

### Unit Tests

- `GenerativeReveal`: State transitions, phase management
- `SkeletonLayout`: Each card type renders correct skeleton
- `BackgroundLoader`: API calls, error handling, timeouts
- `ThemeProvider`: CSS variable injection from expanded theme

### Integration Tests

- Full flow: JSON → skeletons → reveal → background
- Feature flag: Verify old behavior when disabled
- Theme fallback: Missing data doesn't break dashboard
- Background failure: Dashboard usable when DALL-E fails

### E2E Tests (Playwright)

- Visual regression: Screenshots at skeleton, mid-reveal, complete phases
- Animation timing: Verify stagger delays with timeout assertions
- Performance: Measure Time to Interactive (<3s target)
- Reduced motion: Test with emulation enabled

### Manual QA Checklist

- [ ] Skeletons appear instantly (<100ms)
- [ ] Content reveals smoothly with morph effect
- [ ] Background fades in after dashboard interactive
- [ ] Text readable over background (low opacity verified)
- [ ] Works on mobile, tablet, desktop
- [ ] Graceful degradation when background fails
- [ ] Performance acceptable on low-end devices

## Implementation Phases

### Phase 1: Skeleton Animation (Week 1)
**Deliverable:** Dashboard with skeleton-to-content morph, no backend changes

- Create `GenerativeReveal` wrapper component
- Build skeleton components for each card type
- Implement staggered reveal animation with Framer Motion
- Add feature flag: `VITE_GENERATIVE_REVEAL`
- Unit tests for reveal logic

**Success Criteria:**
- Skeletons appear <100ms after JSON received
- Smooth morph effect visible
- Feature flag toggles old/new behavior

### Phase 2: Enhanced Theme Generation (Week 2)
**Deliverable:** Backend generates background prompts

- Extend `ThemeGenerator.generate_theme()` to output `background_prompt`
- Update LLM prompt with DALL-E generation instruction
- Modify frontend `ThemeProvider` to read expanded JSON
- Test theme fallback scenarios
- Integration tests for theme generation

**Success Criteria:**
- All themes include valid background_prompt
- Prompts are contextually relevant to user data
- Graceful fallback when prompt missing

### Phase 3: Background Generation (Week 2-3)
**Deliverable:** Full generative experience with AI backgrounds

- Create `/api/generate-background` endpoint
- Integrate OpenAI DALL-E 3 API
- Build `BackgroundLoader` component
- Implement cross-fade with opacity control (0.15-0.3)
- Add error handling, timeouts, retry logic
- E2E tests for full flow

**Success Criteria:**
- Background generates successfully >95% of time
- Cross-fade is smooth and subtle
- Dashboard remains usable if background fails
- Cost per dashboard ~$0.05

### Phase 4: Polish & Optimization (Week 3)
**Deliverable:** Production-ready feature

- Performance tuning for low-end devices
- Reduced motion support
- Visual regression test suite
- A/B testing instrumentation
- Documentation and runbook

**Success Criteria:**
- Time to Interactive <3s on p50
- No visual regressions detected
- Reduced motion compliance verified
- Monitoring and alerts configured

## Rollout Strategy

**Week 1:** Ship Phase 1 behind feature flag to internal users (n=10)
- Monitor: Animation smoothness, skeleton quality, any jank
- Success: No reported issues, positive feedback

**Week 2:** Enable for 10% of production users
- Monitor: TTI, error rates, background success rate
- Success: TTI <3s p50, error rate <1%, background success >90%

**Week 3:** Full rollout (100%)
- Monitor: All metrics, user engagement (session duration)
- Rollback: If error rate >2% or TTI >5s, disable via feature flag

## Metrics to Track

### Performance
- **Time to Interactive (TTI):** Target <3s p50, <5s p95
- **Skeleton render time:** Target <100ms
- **Background generation time:** Target <8s p95

### Reliability
- **Background success rate:** Target >95%
- **Theme generation success:** Target >99%
- **Error rate:** Target <1%

### Business
- **Cost per dashboard:** Target <$0.06 (theme $0.01 + background $0.05)
- **User engagement:** Session duration before/after comparison
- **Perceived quality:** User feedback survey

### Technical
- **API latency:** DALL-E p95 <10s
- **Cache hit rate:** If implemented, target >20%
- **Memory usage:** No memory leaks during reveal

## Future Enhancements (Out of Scope)

- **True streaming architecture:** WebSocket streams cards as generated
- **Background caching:** Store by theme hash, 24hr TTL
- **Layout control:** AI decides card arrangement priority
- **Animation variety:** Different reveal patterns per mood
- **Video backgrounds:** Animated backgrounds for "energetic" moods
- **User preferences:** Let users toggle backgrounds on/off

## Open Questions

None - design approved for implementation.

## References

- Existing codebase: `frontend/src/components/Dashboard.tsx`
- Theme generation: `fabric_dashboard/core/theme_generator.py`
- OpenAI DALL-E 3 docs: https://platform.openai.com/docs/guides/images
- Framer Motion orchestration: https://www.framer.com/motion/animation/#orchestration
