# OnFabric Direct API Client Design

**Date:** 2025-10-30
**Status:** Approved
**Author:** Design Session

## Overview

Replace the MCP integration layer with a direct OnFabric API client for simpler architecture and better control over data fetching.

## Motivation

- **Simpler architecture**: Direct API calls easier to understand and debug than MCP abstraction layer
- **Full control**: Access to all API capabilities without MCP wrapper limitations
- **LLM-centric approach**: Data is passed directly to LLMs for pattern extraction - no need for complex validation layers

## Current Architecture

```
DataFetcher → FabricMCPClient (NotImplementedError) → Falls back to mock data
```

**Issues:**
- MCP client not implemented (raises `NotImplementedError`)
- Always falls back to mock data in production
- Extra abstraction layer adds complexity

## Proposed Architecture

```
DataFetcher → OnFabricAPIClient → OnFabric API → Raw JSON → LLM Analysis
```

**Benefits:**
- Direct HTTP calls to OnFabric API
- Simple, predictable error handling
- No intermediary abstractions
- Reuses existing data transformation logic

## Design

### 1. API Client (`fabric_dashboard/api/onfabric_client.py`)

**Class: `OnFabricAPIClient`**

```python
class OnFabricAPIClient:
    """Simple HTTP client for OnFabric API."""

    def __init__(self):
        """Load credentials from .env, validate, setup session."""

    def get_tapestries() -> list[dict]:
        """GET /api/v1/tapestries"""

    def get_threads(tapestry_id: str) -> list[dict]:
        """GET /api/v1/tapestries/{tapestry_id}/threads"""

    def get_summaries(
        tapestry_id: str,
        provider: str = "instagram",
        page_size: int = 10,
        direction: str = "desc"
    ) -> list[dict]:
        """GET /api/v1/tapestries/{tapestry_id}/summaries"""
```

**Key characteristics:**
- Uses `requests` library for HTTP calls
- Returns raw JSON responses (no Pydantic models)
- Raises exceptions on API errors (fail fast)
- Authorization header: `Bearer {token}` from `.env`
- Base URL: `https://api.onfabric.io/api/v1`

**Error handling:**
- HTTP errors → raise exception with API response details
- Network errors → raise exception with network details
- Invalid credentials → raise exception at init time
- No retries, no fallbacks - fail fast with clear messages

### 2. Data Fetcher Integration

**Update `DataFetcher`:**

```python
class DataFetcher:
    def __init__(self, mock_mode: bool = False):
        self.mock_mode = mock_mode
        if not mock_mode:
            self.api_client = OnFabricAPIClient()  # Replace MCP client

    def fetch_user_data(self, days_back: int = 30) -> Optional[UserData]:
        if self.mock_mode:
            return self._load_mock_data()
        else:
            return self._fetch_from_api(days_back)  # Rename from _fetch_from_mcp

    def _fetch_from_api(self, days_back: int) -> Optional[UserData]:
        """Fetch from OnFabric API, transform to UserData."""
        try:
            tapestry_id = self.api_client.tapestry_id

            # Fetch raw data
            threads = self.api_client.get_threads(tapestry_id)
            summaries = self.api_client.get_summaries(tapestry_id)

            # Combine and transform
            raw_data = {
                "threads": threads,
                "summaries": summaries,
                "tapestry_id": tapestry_id
            }

            return self._transform_api_data(raw_data)

        except Exception as e:
            logger.error(f"Failed to fetch from OnFabric API: {e}")
            return None

    def _transform_api_data(self, raw_data: dict) -> Optional[UserData]:
        """Transform API response to UserData model."""
        # Reuse existing _transform_mcp_data logic with adjustments
        # threads → UserData.interactions
        # Build PersonaProfile and DataSummary from raw data
        # Return UserData model
```

**Data flow:**
1. API returns raw threads and summaries (JSON)
2. Combine into `raw_data` dict
3. Transform to `UserData` model (existing logic)
4. Pass to pattern detector → LLM analyzes → Dashboard renders

**Date filtering:**
- API returns all data
- Python filters threads by date before creating `UserData`
- Filter logic: `thread["date"] >= (now - days_back)`

### 3. Configuration

**Environment variables (`.env`):**
```bash
# OnFabric API Configuration
ONFABRIC_BEARER_TOKEN=your_bearer_token_here
ONFABRIC_TAPESTRY_ID=your_tapestry_id_here
```

**Getting credentials:**

*Bearer token:*
1. Go to https://app.onfabric.io
2. Open DevTools (F12) → Network tab
3. Navigate to Connections/Profile/Status
4. Find API request in Network tab
5. Copy `Authorization: Bearer <token>` header value
6. Paste token into `.env`

*Tapestry ID (Option 1 - Manual):*
```bash
curl -X 'GET' 'https://api.onfabric.io/api/v1/tapestries' \
  -H 'authorization: Bearer <your_token>'
# Returns: [{"id":"tapestry_id",...}]
```

*Tapestry ID (Option 2 - Auto-discovery):*
- If `ONFABRIC_TAPESTRY_ID` not in `.env`, call `get_tapestries()`
- Use first tapestry ID
- Log warning if multiple tapestries found

**Validation:**
```python
# In OnFabricAPIClient.__init__()
load_dotenv()
self.bearer_token = os.getenv("ONFABRIC_BEARER_TOKEN")
self.tapestry_id = os.getenv("ONFABRIC_TAPESTRY_ID")

if not self.bearer_token:
    raise ValueError(
        "ONFABRIC_BEARER_TOKEN not found in .env. "
        "See docs/plans/2025-10-30-onfabric-api-client-design.md for setup."
    )

if not self.tapestry_id:
    logger.warning("ONFABRIC_TAPESTRY_ID not set, auto-discovering...")
    tapestries = self.get_tapestries()
    if tapestries:
        self.tapestry_id = tapestries[0]["id"]
        logger.info(f"Using tapestry: {self.tapestry_id}")
```

### 4. Dependencies

**Add to `requirements.txt`:**
```
requests>=2.31.0
python-dotenv>=1.0.0
```

## Implementation Plan

1. **Create API client module**
   - File: `fabric_dashboard/api/__init__.py`
   - File: `fabric_dashboard/api/onfabric_client.py`
   - Implement `OnFabricAPIClient` class with 3 methods

2. **Update DataFetcher**
   - Replace `FabricMCPClient` with `OnFabricAPIClient`
   - Rename `_fetch_from_mcp` → `_fetch_from_api`
   - Update `_transform_mcp_data` → `_transform_api_data`
   - Adjust data transformation for API response format

3. **Update tests**
   - Create `tests/test_onfabric_client.py`
   - Mock API responses with `responses` library
   - Update `test_data_fetcher.py` for API client

4. **Documentation**
   - Add setup instructions to README
   - Document credential acquisition process
   - Add `.env.example` with placeholder values

5. **Remove MCP dependencies**
   - Delete `fabric_dashboard/mcp/onfabric.py`
   - Remove MCP imports from `data_fetcher.py`
   - Update any references to MCP client

## Migration Notes

**Preserving existing functionality:**
- Mock mode (`--mock` flag) still works - loads from JSON fixtures
- `UserData` model unchanged - same interface for downstream code
- Dashboard generation unchanged - still receives `UserData`

**What gets removed:**
- `fabric_dashboard/mcp/onfabric.py` (FabricMCPClient)
- MCP client initialization in DataFetcher
- MCP-specific error handling

**What stays:**
- Mock data loading (`_load_mock_data`)
- Data transformation logic (adjusted for API format)
- All downstream code (PatternDetector, DashboardBuilder, etc.)

## Open Questions

None - design approved.

## Success Criteria

1. ✅ Can fetch threads from OnFabric API with bearer token
2. ✅ Can fetch summaries from OnFabric API
3. ✅ Transforms API responses into `UserData` model
4. ✅ Dashboard generation works with API-fetched data
5. ✅ Clear error messages when credentials missing/invalid
6. ✅ Mock mode still functional for testing
7. ✅ No MCP dependencies remaining
