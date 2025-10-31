# GitHub Preparation Design

**Date:** 2025-10-31
**Purpose:** Portfolio/demo project preparation for GitHub upload
**Approach:** Foundation-up (clean infrastructure, then documentation)

## Overview

Transform the OnFabric MVP codebase into a polished portfolio project with clear documentation, organized tests, and easy demo capabilities using mock data.

## Goals

1. **Portfolio-ready presentation**: Clean structure, comprehensive README, good first impression
2. **Easy demo experience**: Run with mock data by default, no API keys required
3. **Developer-friendly**: Clear path from demo to real data integration
4. **Organized testing**: Systematized test structure with mock/real data support

## File Structure & Cleanup

### Target Structure
```
onfabric_mvp/
├── backend/              # FastAPI backend
├── frontend/             # React frontend
├── fabric_dashboard/     # Core dashboard logic
│   └── tests/           # All tests consolidated here
│       ├── conftest.py
│       ├── fixtures/
│       │   ├── raw_data/
│       │   ├── enrichment/
│       │   ├── patterns/
│       │   ├── personas/
│       │   └── api_examples/
│       ├── test_schemas.py
│       ├── test_data_fetcher.py
│       ├── test_dashboard_builder.py
│       └── test_utils.py
├── docs/
│   ├── README.md        # Architecture overview
│   └── plans/           # Key design docs only
├── .env.example         # Template with mock & real modes
├── .gitignore           # Comprehensive
└── README.md            # Main entry point
```

### Cleanup Actions

**Immediate deletions:**
- `backend/test_serialization.py` (misplaced test file)
- Draft/interim files from `docs/plans/` (keep only final design docs like `2025-10-31-demo2-fashion-producer-design.md`)

**Git cleanup:**
- Comprehensive `.gitignore` for Python, Node, env files, OS files
- Verify no sensitive data in git history
- Remove any API keys or credentials

## Test Organization

### Current State
```
fixtures/
├── mock_user_data.json
├── mock_google_data.json
├── mock_patterns.json
├── mock_search_results.json
├── onfabric_raw_data_example.json
├── onfabric_api_format_sample.json
└── personas/
    ├── demo.json
    └── demo2.json
```

### Reorganized Structure
```
fixtures/
├── raw_data/                      # OnFabric interaction data
│   ├── instagram_interactions.json
│   ├── google_interactions.json
│   └── user_interactions_mixed.json
├── enrichment/                    # API responses for content enrichment
│   ├── search_results.json
│   └── weather_data.json
├── patterns/                      # Analyzed patterns/topics
│   └── extracted_patterns.json
├── personas/                      # Complete end-to-end test personas
│   ├── demo.json
│   └── demo2.json
└── api_examples/                  # OnFabric API format documentation
    ├── raw_data_format.json
    └── api_response_format.json
```

### Test Documentation
- Each test file includes docstring explaining what it tests
- Add `# How to run:` sections with mock and real data commands
- Example: `pytest fabric_dashboard/tests/test_dashboard_builder.py --mock`
- `conftest.py` manages fixtures and mock mode toggles

## Environment Configuration

### Mock Mode Implementation

**Configuration file:**
```python
# fabric_dashboard/core/config.py
class Settings:
    MOCK_MODE: bool = True  # Default to mock for demo
    ONFABRIC_API_KEY: str | None = None
    WEATHER_API_KEY: str | None = None
    SEARCH_API_KEY: str | None = None
```

### .env.example Structure
```bash
# ========================================
# MOCK MODE (Default)
# ========================================
# Set to false to use real APIs
MOCK_MODE=true

# ========================================
# REAL DATA MODE (Optional)
# ========================================
# OnFabric API (required for real user data)
ONFABRIC_API_KEY=your_key_here
ONFABRIC_API_URL=https://api.onfabric.com

# Content Enrichment APIs (optional)
WEATHER_API_KEY=your_openweather_key
SEARCH_API_KEY=your_search_api_key

# ========================================
# Application Config
# ========================================
BACKEND_PORT=8000
FRONTEND_PORT=3000
```

### Data Fetcher Behavior
- When `MOCK_MODE=true`: Load from `fixtures/personas/demo.json`
- When `MOCK_MODE=false`: Call real OnFabric API
- Tests can override with `@pytest.mark.use_real_data`

## README Structure

### Main README.md

**Sections:**

1. **Project Title & Tagline**
   - OnFabric MVP - Personalized Dashboard Generator
   - Brief description of what it does

2. **Quick Start (Mock Data Demo)**
   ```bash
   # Clone and install
   git clone <repo>
   cd onfabric_mvp
   npm install
   pip install -e .

   # Run with demo data (no API keys needed)
   npm run dev        # Frontend on :3000
   python -m uvicorn backend.app.main:app --reload  # Backend on :8000
   ```

3. **Features**
   - Dynamic UI generation from user interests
   - Persona-driven content curation
   - Custom theming based on user aesthetics
   - Multi-provider data integration (Instagram, Google, Pinterest)

4. **Architecture Overview**
   - Brief explanation: Data → Patterns → Dashboard
   - Link to detailed docs/README.md

5. **Using Real Data**
   - Prerequisites (OnFabric API access)
   - Setup instructions (copy .env.example, fill keys)
   - Data flow explanation

6. **Development**
   - Project structure with descriptions
   - Running tests (mock vs real)
   - Adding new widget types

7. **License**

### docs/README.md (Detailed Architecture)

**Contents:**
- Architecture overview (how dashboard generation works)
- Widget system explained
- Theme system explained
- Data pipeline (OnFabric → Patterns → Cards → Layout)
- How enrichment APIs integrate

## Documentation Cleanup

### Keep in docs/plans/
- Architecture decision records
- Fashion producer design doc (`2025-10-31-demo2-fashion-producer-design.md`)
- Key technical design documents explaining major decisions

### Remove from docs/plans/
- Drafts, WIP documents, scratch files
- Superseded versions of designs
- Meeting notes or brainstorming sessions
- Interim/temporary documents

## Implementation Sequence

**Foundation-up approach:**

1. **Test organization**
   - Reorganize fixtures into new structure
   - Update test imports
   - Add test documentation
   - Create conftest.py with mock mode support

2. **Mock data mode**
   - Add MOCK_MODE to config
   - Update data fetcher to check MOCK_MODE
   - Test mock vs real data switching

3. **Environment setup**
   - Create comprehensive .env.example
   - Update .gitignore
   - Verify no secrets in repo

4. **Documentation**
   - Write main README.md
   - Create docs/README.md with architecture
   - Clean up docs/plans/
   - Remove test_serialization.py

5. **Final verification**
   - Test quick start commands work
   - Verify mock mode runs without any env vars
   - Check all links in documentation
   - Final git cleanup commit

## Success Criteria

- [ ] App runs with `npm run dev` and `python -m uvicorn` with no .env file
- [ ] README quick start is accurate and works
- [ ] Tests are organized and documented
- [ ] No sensitive data or API keys in repo
- [ ] Clear path from mock demo to real data integration
- [ ] Professional portfolio presentation
