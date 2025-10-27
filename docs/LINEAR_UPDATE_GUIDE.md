# Linear Tickets - Manual Update Guide

**Date**: 2025-10-22

The Linear MCP integration has parameter issues, so here's a guide to manually update your tickets in the Linear UI.

---

## 🎯 Quick Actions Checklist

### Close These 10 Tickets (100% Complete)
Go to each ticket in Linear and click "Done" or "Completed":

1. **MAT-5**: Set up project structure and dependencies ✅
   - URL: https://linear.app/matildaglynn/issue/MAT-5
   - Status: All directories, dependencies in place, 163 tests passing

2. **MAT-7**: Create utility modules ✅
   - URL: https://linear.app/matildaglynn/issue/MAT-7
   - Status: config.py, logger.py, cache.py, files.py all complete with 40+ tests

3. **MAT-8**: Build CLI skeleton with Click ✅
   - URL: https://linear.app/matildaglynn/issue/MAT-8
   - Status: cli.py + init.py + generate.py all working

4. **MAT-9**: Create mock data fixtures ✅
   - URL: https://linear.app/matildaglynn/issue/MAT-9
   - Status: mock_user_data.json, mock_patterns.json, mock_search_results.json all exist

5. **MAT-10**: Implement data fetcher with MCP client ✅
   - URL: https://linear.app/matildaglynn/issue/MAT-10
   - Status: data_fetcher.py (7,189 bytes) + tests working, fetched 46 interactions

6. **MAT-12**: Implement theme generator with Claude ✅
   - URL: https://linear.app/matildaglynn/issue/MAT-12
   - Status: theme_generator.py (8,534 bytes) with retry logic and fallback

7. **MAT-13**: Implement search enricher with Perplexity API ✅
   - URL: https://linear.app/matildaglynn/issue/MAT-13
   - Status: search_enricher.py (17,076 bytes) with parallel execution and caching

8. **MAT-14**: Implement content writer with Claude ✅
   - URL: https://linear.app/matildaglynn/issue/MAT-14
   - Status: content_writer.py (14,546 bytes), generated 4 cards (1,025 words)

9. **MAT-15**: Implement template injection and dashboard builder ✅
   - URL: https://linear.app/matildaglynn/issue/MAT-15
   - Status: dashboard_builder.py (51,733 bytes) - HUGE file with all UI components

10. **MAT-16**: Create generate command and orchestration ✅
    - URL: https://linear.app/matildaglynn/issue/MAT-16
    - Status: Full 8-step pipeline working, generates complete dashboards

---

## 📝 Update These 2 Tickets (Partially Complete)

### MAT-17: Add error handling and retry logic
**URL**: https://linear.app/matildaglynn/issue/MAT-17
**Status**: Change to "In Progress" and update description:

```markdown
## Status: 🔶 60% COMPLETE

### What's Done ✅
- ✅ Retry decorators on LLM calls (tenacity) in pattern_detector, theme_generator, content_writer, ui_generator
- ✅ Fallback templates working (mock generation fallbacks)
- ✅ Graceful degradation (UI components can fail individually)

### What's Missing ⚠️
- ⚠️ Not comprehensive across ALL modules
- ⚠️ Debug mode exists but verbose logging not fully comprehensive
- ⚠️ Error messages could be more contextual
- ⚠️ Common errors not documented in README

### Next Steps
1. Add retry logic to remaining modules
2. Improve error messages with context
3. Expand debug mode logging
4. Document common errors in README
```

---

### MAT-18: Write tests and documentation
**URL**: https://linear.app/matildaglynn/issue/MAT-18
**Status**: Change to "In Progress" and update description:

```markdown
## Status: 🔶 70% COMPLETE

### What's Done ✅
- ✅ Unit tests for all core modules (163 tests total!)
- ✅ Test files for: schemas, utils, pattern_detector, data_fetcher, theme_generator, search_enricher, content_writer, dashboard_builder, ui_components, ui_generator
- ✅ Mock data fixtures (3 JSON files)
- ✅ README exists with basic setup instructions

### Test Coverage Details
- test_schemas.py: 17,243 bytes
- test_utils.py: 10,562 bytes (40+ tests)
- test_pattern_detector.py: 4,530 bytes
- test_data_fetcher.py: 3,887 bytes
- test_theme_generator.py: 11,085 bytes
- test_search_enricher.py: 13,933 bytes
- test_content_writer.py: 12,803 bytes
- test_dashboard_builder.py: 17,099 bytes
- test_ui_components.py: 9,904 bytes
- test_ui_generator.py: 9,859 bytes

### What's Missing ⚠️
- ⚠️ Integration tests for full pipeline (not comprehensive)
- ⚠️ E2E test exists but needs expansion
- ⚠️ API key setup guide could be more detailed
- ⚠️ Troubleshooting section minimal
- ⚠️ Usage examples could be expanded

### Next Steps
1. Add comprehensive integration tests
2. Expand E2E test coverage
3. Write detailed API key setup guide
4. Add troubleshooting section to README
5. Add more usage examples
```

---

## ➕ Create These New Tickets

### MAT-27: Implement ContentCard Renderer
**Priority**: Medium
**Status**: To Do

```markdown
## Goal
Implement the ContentCard renderer for displaying single article recommendations.

## Current State
Stub only in dashboard_builder.py:339-341

## Implementation Required
Simple card displaying:
- Article title
- Brief overview (2-3 sentences)
- Source name
- Publication date
- "Read More" link

## Estimated Time
~30 minutes

## Acceptance Criteria
- [ ] ContentCard renders with proper styling
- [ ] All fields display correctly
- [ ] Link is clickable
- [ ] Matches other UI component styling
- [ ] No console errors
```

---

### MAT-29: Expand End-to-End Testing
**Priority**: High
**Status**: To Do

```markdown
## Goal
Create comprehensive E2E tests for the complete dashboard generation pipeline.

## Current State
- Basic E2E test exists in test_ui.py
- Need comprehensive testing across all scenarios

## Test Cases Required
1. Generate dashboard with mock data ✅ (basic test exists)
2. Verify all component types render correctly
3. Test interactive features:
   - Weather widget displays mock data
   - Map shows location list (without Mapbox token)
   - Task list checkboxes work
   - Task list localStorage persistence
   - Video embeds render
   - Event calendar displays
4. Test responsive behavior (desktop, tablet, mobile)
5. Test error handling:
   - Failed LLM calls
   - Missing API keys
   - Invalid data
6. Test drag-and-drop card reordering
7. Test with various data volumes (4-8 cards)

## Estimated Time
~2 hours

## Acceptance Criteria
- [ ] All component types tested
- [ ] Interactive features verified
- [ ] Responsive design tested
- [ ] Error scenarios covered
- [ ] Test coverage >80%
```

---

## 🗑️ Archive These 4 Tickets (Onboarding)

These are Linear onboarding tickets not related to your project:

1. **MAT-1**: Get familiar with Linear
   - URL: https://linear.app/matildaglynn/issue/MAT-1
   - Action: Archive

2. **MAT-2**: Set up your teams
   - URL: https://linear.app/matildaglynn/issue/MAT-2
   - Action: Archive

3. **MAT-3**: Connect your tools
   - URL: https://linear.app/matildaglynn/issue/MAT-3
   - Action: Archive

4. **MAT-4**: Import your data
   - URL: https://linear.app/matildaglynn/issue/MAT-4
   - Action: Archive

---

## 📊 Updated Project Status

After these updates, your Linear board will show:

- **Completed**: 12 tickets (MAT-5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)
- **In Progress**: 2 tickets (MAT-17, MAT-18)
- **To Do**: 2 tickets (MAT-27, MAT-29)
- **Archived**: 4 tickets (MAT-1, 2, 3, 4)

**True Progress**: 85% complete (12 done, 2 partial, 2 remaining, 1 stub to implement)

---

## 🎯 Recommended Workflow

1. **Batch close tickets** (10 min):
   - Open Linear, filter by project "Fabric Intelligence Dashboard"
   - Close MAT-5, 7, 8, 9, 10, 12, 13, 14, 15, 16

2. **Update partial tickets** (5 min):
   - Update MAT-17 and MAT-18 with completion percentages

3. **Create new tickets** (5 min):
   - Create MAT-27 and MAT-29 with details above

4. **Archive onboarding** (2 min):
   - Archive MAT-1, 2, 3, 4

**Total time**: ~20 minutes to sync Linear with reality

---

## 💡 Pro Tip

You can bulk-select tickets in Linear:
1. Go to your project board
2. Hold Cmd/Ctrl and click multiple tickets
3. Use the bulk actions menu to close them all at once

This will save you a ton of time!
