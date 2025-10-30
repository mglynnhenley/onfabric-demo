# OnFabric API Client Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Replace MCP integration with direct OnFabric API client for simpler architecture and data fetching.

**Architecture:** Simple HTTP client using `requests` library, reads credentials from `.env`, makes direct calls to OnFabric API endpoints (tapestries, threads, summaries), returns raw JSON for LLM analysis.

**Tech Stack:** Python 3.13, requests, python-dotenv, pytest

---

## Task 1: Create API Client Module Structure

**Files:**
- Create: `fabric_dashboard/api/__init__.py`
- Create: `fabric_dashboard/api/onfabric_client.py`
- Create: `fabric_dashboard/tests/test_onfabric_client.py`

**Step 1: Write the failing test**

Create `fabric_dashboard/tests/test_onfabric_client.py`:

```python
"""Tests for OnFabric API client."""

import os
from unittest.mock import patch

import pytest

from fabric_dashboard.api.onfabric_client import OnFabricAPIClient


def test_client_initialization_with_env_vars():
    """Test client initializes with valid env vars."""
    with patch.dict(os.environ, {
        "ONFABRIC_BEARER_TOKEN": "test_token_123",
        "ONFABRIC_TAPESTRY_ID": "test_tapestry_456"
    }):
        client = OnFabricAPIClient()
        assert client.bearer_token == "test_token_123"
        assert client.tapestry_id == "test_tapestry_456"
        assert client.base_url == "https://api.onfabric.io/api/v1"


def test_client_initialization_missing_token():
    """Test client raises error when token missing."""
    with patch.dict(os.environ, {"ONFABRIC_TAPESTRY_ID": "test_tapestry_456"}, clear=True):
        with pytest.raises(ValueError, match="ONFABRIC_BEARER_TOKEN not found"):
            OnFabricAPIClient()
```

**Step 2: Run test to verify it fails**

Run: `python -m pytest fabric_dashboard/tests/test_onfabric_client.py -v`

Expected: FAIL with "ModuleNotFoundError: No module named 'fabric_dashboard.api'"

**Step 3: Write minimal implementation**

Create `fabric_dashboard/api/__init__.py`:

```python
"""API clients for external services."""

from fabric_dashboard.api.onfabric_client import OnFabricAPIClient

__all__ = ["OnFabricAPIClient"]
```

Create `fabric_dashboard/api/onfabric_client.py`:

```python
"""OnFabric API client."""

import os
from typing import Any

import requests
from dotenv import load_dotenv

from fabric_dashboard.utils import logger


class OnFabricAPIClient:
    """Simple HTTP client for OnFabric API."""

    def __init__(self):
        """
        Initialize client with credentials from .env.

        Raises:
            ValueError: If ONFABRIC_BEARER_TOKEN not found in environment.
        """
        load_dotenv()

        self.bearer_token = os.getenv("ONFABRIC_BEARER_TOKEN")
        if not self.bearer_token:
            raise ValueError(
                "ONFABRIC_BEARER_TOKEN not found in .env. "
                "See docs/plans/2025-10-30-onfabric-api-client-design.md for setup."
            )

        self.tapestry_id = os.getenv("ONFABRIC_TAPESTRY_ID")
        self.base_url = "https://api.onfabric.io/api/v1"

        # Setup requests session with auth header
        self.session = requests.Session()
        self.session.headers.update({
            "accept": "application/json",
            "authorization": f"Bearer {self.bearer_token}"
        })

        logger.info("OnFabric API client initialized")
```

**Step 4: Run test to verify it passes**

Run: `python -m pytest fabric_dashboard/tests/test_onfabric_client.py::test_client_initialization_with_env_vars -v`

Expected: PASS

Run: `python -m pytest fabric_dashboard/tests/test_onfabric_client.py::test_client_initialization_missing_token -v`

Expected: PASS

**Step 5: Commit**

```bash
git add fabric_dashboard/api/__init__.py fabric_dashboard/api/onfabric_client.py fabric_dashboard/tests/test_onfabric_client.py
git commit -m "feat: add OnFabric API client initialization with env validation"
```

---

## Task 2: Implement get_tapestries() Method

**Files:**
- Modify: `fabric_dashboard/api/onfabric_client.py`
- Modify: `fabric_dashboard/tests/test_onfabric_client.py`

**Step 1: Write the failing test**

Add to `fabric_dashboard/tests/test_onfabric_client.py`:

```python
import responses


@responses.activate
def test_get_tapestries_success():
    """Test fetching tapestries from API."""
    responses.add(
        responses.GET,
        "https://api.onfabric.io/api/v1/tapestries",
        json=[
            {
                "id": "tapestry_123",
                "fabric_user_id": "user_456",
                "created_at": "2025-10-16T15:14:29.219809",
                "updated_at": "2025-10-16T15:14:29.219809"
            }
        ],
        status=200
    )

    with patch.dict(os.environ, {
        "ONFABRIC_BEARER_TOKEN": "test_token",
        "ONFABRIC_TAPESTRY_ID": "tapestry_123"
    }):
        client = OnFabricAPIClient()
        tapestries = client.get_tapestries()

        assert len(tapestries) == 1
        assert tapestries[0]["id"] == "tapestry_123"


@responses.activate
def test_get_tapestries_api_error():
    """Test get_tapestries handles API errors."""
    responses.add(
        responses.GET,
        "https://api.onfabric.io/api/v1/tapestries",
        json={"error": "Unauthorized"},
        status=401
    )

    with patch.dict(os.environ, {
        "ONFABRIC_BEARER_TOKEN": "invalid_token",
        "ONFABRIC_TAPESTRY_ID": "tapestry_123"
    }):
        client = OnFabricAPIClient()

        with pytest.raises(requests.HTTPError):
            client.get_tapestries()
```

**Step 2: Run test to verify it fails**

Run: `python -m pytest fabric_dashboard/tests/test_onfabric_client.py::test_get_tapestries_success -v`

Expected: FAIL with "AttributeError: 'OnFabricAPIClient' object has no attribute 'get_tapestries'"

**Step 3: Write minimal implementation**

Add to `fabric_dashboard/api/onfabric_client.py`:

```python
    def get_tapestries(self) -> list[dict[str, Any]]:
        """
        Get list of available tapestries for the authenticated user.

        Returns:
            List of tapestry dictionaries.

        Raises:
            requests.HTTPError: If API request fails.
        """
        url = f"{self.base_url}/tapestries"

        logger.muted("Fetching tapestries from OnFabric API")
        response = self.session.get(url)
        response.raise_for_status()

        tapestries = response.json()
        logger.muted(f"Found {len(tapestries)} tapestry(ies)")

        return tapestries
```

**Step 4: Run tests to verify they pass**

Run: `python -m pytest fabric_dashboard/tests/test_onfabric_client.py::test_get_tapestries_success -v`

Expected: PASS

Run: `python -m pytest fabric_dashboard/tests/test_onfabric_client.py::test_get_tapestries_api_error -v`

Expected: PASS

**Step 5: Commit**

```bash
git add fabric_dashboard/api/onfabric_client.py fabric_dashboard/tests/test_onfabric_client.py
git commit -m "feat: add get_tapestries() method with error handling"
```

---

## Task 3: Implement get_threads() Method

**Files:**
- Modify: `fabric_dashboard/api/onfabric_client.py`
- Modify: `fabric_dashboard/tests/test_onfabric_client.py`

**Step 1: Write the failing test**

Add to `fabric_dashboard/tests/test_onfabric_client.py`:

```python
@responses.activate
def test_get_threads_success():
    """Test fetching threads from API."""
    mock_threads = [
        {
            "id": "thread_1",
            "provider": "instagram",
            "content": "Posted photo",
            "asat": "2025-10-27T18:37:28"
        },
        {
            "id": "thread_2",
            "provider": "google",
            "content": "Searched for AI",
            "asat": "2025-10-26T12:00:00"
        }
    ]

    responses.add(
        responses.GET,
        "https://api.onfabric.io/api/v1/tapestries/tapestry_123/threads",
        json=mock_threads,
        status=200
    )

    with patch.dict(os.environ, {
        "ONFABRIC_BEARER_TOKEN": "test_token",
        "ONFABRIC_TAPESTRY_ID": "tapestry_123"
    }):
        client = OnFabricAPIClient()
        threads = client.get_threads("tapestry_123")

        assert len(threads) == 2
        assert threads[0]["id"] == "thread_1"
        assert threads[1]["provider"] == "google"


@responses.activate
def test_get_threads_not_found():
    """Test get_threads handles 404 errors."""
    responses.add(
        responses.GET,
        "https://api.onfabric.io/api/v1/tapestries/invalid_id/threads",
        json={"error": "Tapestry not found"},
        status=404
    )

    with patch.dict(os.environ, {
        "ONFABRIC_BEARER_TOKEN": "test_token",
        "ONFABRIC_TAPESTRY_ID": "tapestry_123"
    }):
        client = OnFabricAPIClient()

        with pytest.raises(requests.HTTPError):
            client.get_threads("invalid_id")
```

**Step 2: Run test to verify it fails**

Run: `python -m pytest fabric_dashboard/tests/test_onfabric_client.py::test_get_threads_success -v`

Expected: FAIL with "AttributeError: 'OnFabricAPIClient' object has no attribute 'get_threads'"

**Step 3: Write minimal implementation**

Add to `fabric_dashboard/api/onfabric_client.py`:

```python
    def get_threads(self, tapestry_id: str) -> list[dict[str, Any]]:
        """
        Get threads for a specific tapestry.

        Args:
            tapestry_id: ID of the tapestry to fetch threads from.

        Returns:
            List of thread dictionaries.

        Raises:
            requests.HTTPError: If API request fails.
        """
        url = f"{self.base_url}/tapestries/{tapestry_id}/threads"

        logger.muted(f"Fetching threads for tapestry {tapestry_id[:8]}...")
        response = self.session.get(url)
        response.raise_for_status()

        threads = response.json()
        logger.muted(f"Retrieved {len(threads)} thread(s)")

        return threads
```

**Step 4: Run tests to verify they pass**

Run: `python -m pytest fabric_dashboard/tests/test_onfabric_client.py::test_get_threads_success -v`

Expected: PASS

Run: `python -m pytest fabric_dashboard/tests/test_onfabric_client.py::test_get_threads_not_found -v`

Expected: PASS

**Step 5: Commit**

```bash
git add fabric_dashboard/api/onfabric_client.py fabric_dashboard/tests/test_onfabric_client.py
git commit -m "feat: add get_threads() method for tapestry data retrieval"
```

---

## Task 4: Implement get_summaries() Method

**Files:**
- Modify: `fabric_dashboard/api/onfabric_client.py`
- Modify: `fabric_dashboard/tests/test_onfabric_client.py`

**Step 1: Write the failing test**

Add to `fabric_dashboard/tests/test_onfabric_client.py`:

```python
@responses.activate
def test_get_summaries_success():
    """Test fetching summaries from API."""
    mock_summaries = [
        {
            "id": "summary_1",
            "provider": "instagram",
            "summary": "Posted 5 photos this week",
            "week_start": "2025-10-21"
        }
    ]

    responses.add(
        responses.GET,
        "https://api.onfabric.io/api/v1/tapestries/tapestry_123/summaries?page_size=10&direction=desc&provider=instagram",
        json=mock_summaries,
        status=200
    )

    with patch.dict(os.environ, {
        "ONFABRIC_BEARER_TOKEN": "test_token",
        "ONFABRIC_TAPESTRY_ID": "tapestry_123"
    }):
        client = OnFabricAPIClient()
        summaries = client.get_summaries(
            "tapestry_123",
            provider="instagram",
            page_size=10,
            direction="desc"
        )

        assert len(summaries) == 1
        assert summaries[0]["provider"] == "instagram"


@responses.activate
def test_get_summaries_custom_params():
    """Test get_summaries with custom parameters."""
    responses.add(
        responses.GET,
        "https://api.onfabric.io/api/v1/tapestries/tapestry_123/summaries?page_size=20&direction=asc&provider=google",
        json=[],
        status=200
    )

    with patch.dict(os.environ, {
        "ONFABRIC_BEARER_TOKEN": "test_token",
        "ONFABRIC_TAPESTRY_ID": "tapestry_123"
    }):
        client = OnFabricAPIClient()
        summaries = client.get_summaries(
            "tapestry_123",
            provider="google",
            page_size=20,
            direction="asc"
        )

        assert summaries == []
```

**Step 2: Run test to verify it fails**

Run: `python -m pytest fabric_dashboard/tests/test_onfabric_client.py::test_get_summaries_success -v`

Expected: FAIL with "AttributeError: 'OnFabricAPIClient' object has no attribute 'get_summaries'"

**Step 3: Write minimal implementation**

Add to `fabric_dashboard/api/onfabric_client.py`:

```python
    def get_summaries(
        self,
        tapestry_id: str,
        provider: str = "instagram",
        page_size: int = 10,
        direction: str = "desc"
    ) -> list[dict[str, Any]]:
        """
        Get weekly summaries for a specific tapestry and provider.

        Args:
            tapestry_id: ID of the tapestry.
            provider: Provider name (e.g., "instagram", "google").
            page_size: Number of summaries to retrieve.
            direction: Sort direction ("asc" or "desc").

        Returns:
            List of summary dictionaries.

        Raises:
            requests.HTTPError: If API request fails.
        """
        url = f"{self.base_url}/tapestries/{tapestry_id}/summaries"
        params = {
            "page_size": page_size,
            "direction": direction,
            "provider": provider
        }

        logger.muted(f"Fetching {provider} summaries for tapestry {tapestry_id[:8]}...")
        response = self.session.get(url, params=params)
        response.raise_for_status()

        summaries = response.json()
        logger.muted(f"Retrieved {len(summaries)} summary(ies)")

        return summaries
```

**Step 4: Run tests to verify they pass**

Run: `python -m pytest fabric_dashboard/tests/test_onfabric_client.py::test_get_summaries_success -v`

Expected: PASS

Run: `python -m pytest fabric_dashboard/tests/test_onfabric_client.py::test_get_summaries_custom_params -v`

Expected: PASS

**Step 5: Commit**

```bash
git add fabric_dashboard/api/onfabric_client.py fabric_dashboard/tests/test_onfabric_client.py
git commit -m "feat: add get_summaries() method with query parameters"
```

---

## Task 5: Add Auto-Discovery for Tapestry ID

**Files:**
- Modify: `fabric_dashboard/api/onfabric_client.py`
- Modify: `fabric_dashboard/tests/test_onfabric_client.py`

**Step 1: Write the failing test**

Add to `fabric_dashboard/tests/test_onfabric_client.py`:

```python
@responses.activate
def test_client_auto_discovers_tapestry_id():
    """Test client auto-discovers tapestry ID when not in env."""
    responses.add(
        responses.GET,
        "https://api.onfabric.io/api/v1/tapestries",
        json=[
            {"id": "discovered_tapestry_123", "fabric_user_id": "user_456"},
            {"id": "second_tapestry_456", "fabric_user_id": "user_456"}
        ],
        status=200
    )

    with patch.dict(os.environ, {"ONFABRIC_BEARER_TOKEN": "test_token"}, clear=True):
        client = OnFabricAPIClient()

        # Should auto-discover and use first tapestry
        assert client.tapestry_id == "discovered_tapestry_123"


@responses.activate
def test_client_auto_discovery_warns_multiple_tapestries():
    """Test client warns when multiple tapestries found."""
    responses.add(
        responses.GET,
        "https://api.onfabric.io/api/v1/tapestries",
        json=[
            {"id": "tapestry_1", "fabric_user_id": "user_456"},
            {"id": "tapestry_2", "fabric_user_id": "user_456"}
        ],
        status=200
    )

    with patch.dict(os.environ, {"ONFABRIC_BEARER_TOKEN": "test_token"}, clear=True):
        with patch("fabric_dashboard.utils.logger.warning") as mock_warning:
            client = OnFabricAPIClient()

            # Should warn about multiple tapestries
            mock_warning.assert_called()
            assert "multiple tapestries" in str(mock_warning.call_args).lower()
```

**Step 2: Run test to verify it fails**

Run: `python -m pytest fabric_dashboard/tests/test_onfabric_client.py::test_client_auto_discovers_tapestry_id -v`

Expected: FAIL (tapestry_id is None, not auto-discovered)

**Step 3: Write minimal implementation**

Update `__init__` method in `fabric_dashboard/api/onfabric_client.py`:

```python
    def __init__(self):
        """
        Initialize client with credentials from .env.

        Auto-discovers tapestry ID if not set in environment.

        Raises:
            ValueError: If ONFABRIC_BEARER_TOKEN not found in environment.
        """
        load_dotenv()

        self.bearer_token = os.getenv("ONFABRIC_BEARER_TOKEN")
        if not self.bearer_token:
            raise ValueError(
                "ONFABRIC_BEARER_TOKEN not found in .env. "
                "See docs/plans/2025-10-30-onfabric-api-client-design.md for setup."
            )

        self.base_url = "https://api.onfabric.io/api/v1"

        # Setup requests session with auth header
        self.session = requests.Session()
        self.session.headers.update({
            "accept": "application/json",
            "authorization": f"Bearer {self.bearer_token}"
        })

        # Get or auto-discover tapestry ID
        self.tapestry_id = os.getenv("ONFABRIC_TAPESTRY_ID")
        if not self.tapestry_id:
            logger.warning("ONFABRIC_TAPESTRY_ID not set, auto-discovering...")
            tapestries = self.get_tapestries()

            if not tapestries:
                raise ValueError("No tapestries found for this account")

            if len(tapestries) > 1:
                logger.warning(
                    f"Found {len(tapestries)} tapestries, using first one. "
                    "Set ONFABRIC_TAPESTRY_ID in .env to specify."
                )

            self.tapestry_id = tapestries[0]["id"]
            logger.info(f"Using tapestry: {self.tapestry_id}")

        logger.info("OnFabric API client initialized")
```

**Step 4: Run tests to verify they pass**

Run: `python -m pytest fabric_dashboard/tests/test_onfabric_client.py::test_client_auto_discovers_tapestry_id -v`

Expected: PASS

Run: `python -m pytest fabric_dashboard/tests/test_onfabric_client.py::test_client_auto_discovery_warns_multiple_tapestries -v`

Expected: PASS

**Step 5: Commit**

```bash
git add fabric_dashboard/api/onfabric_client.py fabric_dashboard/tests/test_onfabric_client.py
git commit -m "feat: add auto-discovery for tapestry ID when not in env"
```

---

## Task 6: Update DataFetcher to Use API Client

**Files:**
- Modify: `fabric_dashboard/core/data_fetcher.py`
- Modify: `fabric_dashboard/tests/test_data_fetcher.py`

**Step 1: Write the failing test**

Add to `fabric_dashboard/tests/test_data_fetcher.py`:

```python
from unittest.mock import Mock, patch


def test_data_fetcher_uses_api_client():
    """Test DataFetcher initializes with OnFabric API client."""
    with patch("fabric_dashboard.core.data_fetcher.OnFabricAPIClient") as mock_client:
        fetcher = DataFetcher(mock_mode=False)

        # Should create API client instead of MCP client
        mock_client.assert_called_once()
        assert fetcher.api_client is not None
        assert not hasattr(fetcher, "mcp_client")


def test_fetch_from_api_calls_client():
    """Test _fetch_from_api method calls API client methods."""
    with patch("fabric_dashboard.core.data_fetcher.OnFabricAPIClient") as mock_client_class:
        mock_client = Mock()
        mock_client.tapestry_id = "test_tapestry_123"
        mock_client.get_threads.return_value = [
            {"id": "thread_1", "content": "Test", "asat": "2025-10-27T12:00:00"}
        ]
        mock_client.get_summaries.return_value = [
            {"id": "summary_1", "summary": "Test summary"}
        ]
        mock_client_class.return_value = mock_client

        fetcher = DataFetcher(mock_mode=False)
        user_data = fetcher.fetch_user_data(days_back=30)

        # Should call API client methods
        mock_client.get_threads.assert_called_once_with("test_tapestry_123")
        mock_client.get_summaries.assert_called_once_with("test_tapestry_123")

        # Should return UserData
        assert user_data is not None
        assert len(user_data.interactions) > 0
```

**Step 2: Run test to verify it fails**

Run: `python -m pytest fabric_dashboard/tests/test_data_fetcher.py::test_data_fetcher_uses_api_client -v`

Expected: FAIL with "ImportError: cannot import name 'OnFabricAPIClient'" or assertion failures

**Step 3: Write minimal implementation**

Update `fabric_dashboard/core/data_fetcher.py`:

```python
"""Data fetching module for Fabric Dashboard."""

import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Optional

from fabric_dashboard.api.onfabric_client import OnFabricAPIClient
from fabric_dashboard.models.schemas import DataSummary, PersonaProfile, UserData
from fabric_dashboard.utils import logger


class DataFetcher:
    """Fetches user data from OnFabric API or mock fixtures."""

    def __init__(self, mock_mode: bool = False):
        """
        Initialize data fetcher.

        Args:
            mock_mode: If True, load from mock fixtures instead of real API.
        """
        self.mock_mode = mock_mode
        self.api_client: Optional[OnFabricAPIClient] = None

        if not mock_mode:
            self.api_client = OnFabricAPIClient()

    def fetch_user_data(self, days_back: int = 30) -> Optional[UserData]:
        """
        Fetch user data either from API or mock fixtures.

        Args:
            days_back: Number of days of historical data to fetch.

        Returns:
            UserData model or None if fetch fails.
        """
        if self.mock_mode:
            return self._load_mock_data()
        else:
            return self._fetch_from_api(days_back)

    # ... keep _load_mock_data() unchanged ...

    def _fetch_from_api(self, days_back: int) -> Optional[UserData]:
        """
        Fetch user data from OnFabric API.

        Args:
            days_back: Number of days of data to fetch.

        Returns:
            UserData model or None if fetch fails.
        """
        if not self.api_client:
            logger.error("API client not initialized")
            return None

        logger.info(f"Fetching user data from OnFabric API (last {days_back} days)")

        try:
            tapestry_id = self.api_client.tapestry_id

            # Fetch raw data from API
            threads = self.api_client.get_threads(tapestry_id)
            summaries = self.api_client.get_summaries(tapestry_id)

            # Combine into raw_data dict
            raw_data = {
                "threads": threads,
                "summaries": summaries,
                "tapestry_id": tapestry_id
            }

            # Transform to UserData model
            return self._transform_api_data(raw_data, days_back)

        except Exception as e:
            logger.error(f"Failed to fetch data from OnFabric API: {e}")
            return None

    def _transform_api_data(self, raw_data: dict[str, Any], days_back: int) -> Optional[UserData]:
        """
        Transform raw API response into UserData model.

        Args:
            raw_data: Raw response from API with threads and summaries.
            days_back: Number of days to filter data.

        Returns:
            UserData model or None if transformation fails.
        """
        try:
            threads = raw_data.get("threads", [])

            # Filter threads by date
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_back)
            filtered_threads = []

            for thread in threads:
                thread_date_str = thread.get("asat")
                if thread_date_str:
                    thread_date = datetime.fromisoformat(thread_date_str.replace("Z", "+00:00"))
                    if thread_date >= cutoff_date:
                        filtered_threads.append(thread)

            # Extract date range from filtered threads
            if filtered_threads:
                dates = [
                    datetime.fromisoformat(t["asat"].replace("Z", "+00:00"))
                    for t in filtered_threads if t.get("asat")
                ]
                date_range_start = min(dates)
                date_range_end = max(dates)
                days_analyzed = (date_range_end - date_range_start).days + 1
            else:
                date_range_start = datetime.now(timezone.utc)
                date_range_end = datetime.now(timezone.utc)
                days_analyzed = 1

            # Extract providers
            providers = list(set(t.get("provider", "unknown") for t in filtered_threads))

            # Build summary
            summary = DataSummary(
                total_interactions=len(filtered_threads),
                date_range_start=date_range_start,
                date_range_end=date_range_end,
                days_analyzed=days_analyzed,
                platforms=providers,
                top_themes=[],  # Will be populated by PatternDetector
            )

            # Create default persona (will be refined by PatternDetector)
            persona = PersonaProfile(
                writing_style="analytical yet accessible",
                interests=["general"],
                activity_level="moderate",
                professional_context=None,
                tone_preference="balanced and approachable",
                age_range=None,
                content_depth_preference="balanced",
            )

            # Build UserData
            user_data = UserData(
                connection_id=raw_data.get("tapestry_id", "unknown"),
                interactions=filtered_threads,
                summary=summary,
                persona=persona,
            )

            logger.success(
                f"Transformed {len(filtered_threads)} interactions from "
                f"{len(providers)} provider(s)"
            )
            return user_data

        except Exception as e:
            logger.error(f"Failed to transform API data: {e}")
            return None

    def __enter__(self) -> "DataFetcher":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        # No cleanup needed for API client
        pass
```

**Step 4: Run tests to verify they pass**

Run: `python -m pytest fabric_dashboard/tests/test_data_fetcher.py::test_data_fetcher_uses_api_client -v`

Expected: PASS

Run: `python -m pytest fabric_dashboard/tests/test_data_fetcher.py::test_fetch_from_api_calls_client -v`

Expected: PASS

**Step 5: Commit**

```bash
git add fabric_dashboard/core/data_fetcher.py fabric_dashboard/tests/test_data_fetcher.py
git commit -m "feat: update DataFetcher to use OnFabric API client instead of MCP"
```

---

## Task 7: Add Environment Configuration Example

**Files:**
- Create: `.env.example`
- Modify: `README.md`

**Step 1: Create .env.example**

Create `.env.example`:

```bash
# OnFabric API Configuration
# Get your bearer token from https://app.onfabric.io
# Instructions: DevTools → Network tab → Find API request → Copy Authorization header
ONFABRIC_BEARER_TOKEN=your_bearer_token_here

# Optional: Tapestry ID (auto-discovered if not set)
# Get via: curl -H "Authorization: Bearer <token>" https://api.onfabric.io/api/v1/tapestries
ONFABRIC_TAPESTRY_ID=your_tapestry_id_here

# Anthropic API Key (for LLM analysis)
ANTHROPIC_API_KEY=your_anthropic_key_here

# Perplexity API Key (for web search enrichment)
PERPLEXITY_API_KEY=your_perplexity_key_here
```

**Step 2: Update README with setup instructions**

Add to `README.md` after installation section:

```markdown
### Configuration

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Get your OnFabric bearer token:
   - Go to https://app.onfabric.io
   - Open browser DevTools (F12 or right-click → Inspect)
   - Navigate to the Network tab
   - Click on Profile, Status, or Connections
   - Find an API request in the Network tab
   - Copy the `Authorization: Bearer <token>` header value
   - Paste the token value into `.env` as `ONFABRIC_BEARER_TOKEN`

3. (Optional) Get your tapestry ID:
   ```bash
   curl -X 'GET' 'https://api.onfabric.io/api/v1/tapestries' \
     -H 'authorization: Bearer <your_token>'
   ```
   Copy the `id` field from the response and add to `.env` as `ONFABRIC_TAPESTRY_ID`.

   If not set, the system will auto-discover and use the first available tapestry.

4. Add your Anthropic and Perplexity API keys to `.env`
```

**Step 3: Verify files created**

Run: `ls -la .env.example`

Expected: File exists

Run: `grep "ONFABRIC_BEARER_TOKEN" README.md`

Expected: Setup instructions found

**Step 4: Commit**

```bash
git add .env.example README.md
git commit -m "docs: add environment configuration example and setup instructions"
```

---

## Task 8: Remove MCP Dependencies

**Files:**
- Delete: `fabric_dashboard/mcp/onfabric.py`
- Modify: `fabric_dashboard/mcp/__init__.py` (if needed)

**Step 1: Verify MCP client is no longer imported**

Run: `grep -r "from fabric_dashboard.mcp.onfabric import" fabric_dashboard/`

Expected: No matches (already removed in Task 6)

Run: `grep -r "FabricMCPClient" fabric_dashboard/`

Expected: Only in old test files or comments

**Step 2: Remove MCP onfabric module**

```bash
git rm fabric_dashboard/mcp/onfabric.py
```

**Step 3: Update MCP __init__.py if needed**

Check `fabric_dashboard/mcp/__init__.py`:

```python
"""MCP client modules."""

from fabric_dashboard.mcp.client import MCPClient

__all__ = ["MCPClient"]
```

Remove `FabricMCPClient` from `__all__` if present.

**Step 4: Run all tests to ensure nothing broke**

Run: `python -m pytest fabric_dashboard/tests/ -v --tb=line -k "not test_fetch_real_mode_fallback"`

Expected: All tests pass (excluding known failing tests from baseline)

**Step 5: Commit**

```bash
git add fabric_dashboard/mcp/
git commit -m "refactor: remove MCP FabricMCPClient in favor of direct API client"
```

---

## Task 9: Integration Test with Real API (Manual)

**Files:**
- Create: `manual_tests/test_onfabric_api_integration.py`

**Step 1: Create manual integration test**

Create `manual_tests/test_onfabric_api_integration.py`:

```python
"""
Manual integration test for OnFabric API client.

REQUIRES:
- Valid ONFABRIC_BEARER_TOKEN in .env
- Valid ONFABRIC_TAPESTRY_ID in .env (or will auto-discover)

Run with:
    python manual_tests/test_onfabric_api_integration.py
"""

from fabric_dashboard.api.onfabric_client import OnFabricAPIClient
from fabric_dashboard.core.data_fetcher import DataFetcher
from fabric_dashboard.utils import logger


def test_api_client_direct():
    """Test API client methods directly."""
    logger.info("Testing OnFabric API client...")

    try:
        client = OnFabricAPIClient()
        logger.success(f"✓ Client initialized with tapestry: {client.tapestry_id}")

        # Test get_tapestries
        tapestries = client.get_tapestries()
        logger.success(f"✓ Found {len(tapestries)} tapestry(ies)")

        # Test get_threads
        threads = client.get_threads(client.tapestry_id)
        logger.success(f"✓ Retrieved {len(threads)} thread(s)")

        if threads:
            logger.info(f"  Sample thread: {threads[0].get('preview', 'No preview')[:50]}...")

        # Test get_summaries
        summaries = client.get_summaries(client.tapestry_id)
        logger.success(f"✓ Retrieved {len(summaries)} summary(ies)")

        return True

    except Exception as e:
        logger.error(f"✗ API client test failed: {e}")
        return False


def test_data_fetcher_integration():
    """Test DataFetcher with API client."""
    logger.info("Testing DataFetcher integration...")

    try:
        fetcher = DataFetcher(mock_mode=False)
        user_data = fetcher.fetch_user_data(days_back=7)

        if user_data:
            logger.success(f"✓ Fetched {user_data.summary.total_interactions} interactions")
            logger.success(f"✓ Date range: {user_data.summary.date_range_start.date()} to {user_data.summary.date_range_end.date()}")
            logger.success(f"✓ Platforms: {', '.join(user_data.summary.platforms)}")
            return True
        else:
            logger.error("✗ DataFetcher returned None")
            return False

    except Exception as e:
        logger.error(f"✗ DataFetcher test failed: {e}")
        return False


if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("OnFabric API Integration Test")
    logger.info("=" * 60)

    test1 = test_api_client_direct()
    print()
    test2 = test_data_fetcher_integration()

    print()
    logger.info("=" * 60)
    if test1 and test2:
        logger.success("✓ All integration tests passed!")
    else:
        logger.error("✗ Some integration tests failed")
    logger.info("=" * 60)
```

**Step 2: Document how to run**

Add to `README.md` in Testing section:

```markdown
### Manual Integration Testing

To test the OnFabric API integration with real credentials:

1. Ensure `.env` has valid `ONFABRIC_BEARER_TOKEN`
2. Run the integration test:
   ```bash
   python manual_tests/test_onfabric_api_integration.py
   ```

This will test:
- API client initialization
- Fetching tapestries, threads, and summaries
- DataFetcher integration
- Data transformation
```

**Step 3: Commit**

```bash
git add manual_tests/test_onfabric_api_integration.py README.md
git commit -m "test: add manual integration test for OnFabric API client"
```

---

## Task 10: Final Verification

**Step 1: Run full test suite**

Run: `python -m pytest fabric_dashboard/tests/test_onfabric_client.py -v`

Expected: All OnFabric API client tests pass

Run: `python -m pytest fabric_dashboard/tests/test_data_fetcher.py -v -k "not fallback"`

Expected: All DataFetcher tests pass (excluding known failing baseline tests)

**Step 2: Verify no MCP imports remain**

Run: `grep -r "from fabric_dashboard.mcp.onfabric" fabric_dashboard/ || echo "Clean!"`

Expected: "Clean!" (no matches)

**Step 3: Check code quality**

Run: `ruff check fabric_dashboard/api/`

Expected: No errors

Run: `mypy fabric_dashboard/api/ --ignore-missing-imports`

Expected: No type errors

**Step 4: Create final commit**

```bash
git add -A
git commit -m "feat: complete OnFabric API client implementation

- Replace MCP integration with direct API calls
- Auto-discover tapestry ID when not configured
- Add comprehensive test coverage
- Update documentation with setup instructions

Closes #<issue-number>
"
```

---

## Dependencies

Add to `requirements.txt` if not already present:

```
requests>=2.31.0
python-dotenv>=1.0.0
```

Add to `requirements-dev.txt`:

```
responses>=0.24.0  # For mocking HTTP requests in tests
```

---

## Success Criteria

- ✅ OnFabricAPIClient implements all 3 methods (tapestries, threads, summaries)
- ✅ Auto-discovers tapestry ID when not in .env
- ✅ DataFetcher uses API client instead of MCP
- ✅ Data transformation preserves existing UserData structure
- ✅ All new tests pass
- ✅ No MCP dependencies remain
- ✅ Documentation updated with setup instructions
- ✅ Manual integration test works with real API

---

## Notes for Implementation

- Follow TDD strictly: test → fail → implement → pass → commit
- Keep each commit small and focused
- Run tests after each change
- Use `responses` library to mock HTTP requests in tests
- Preserve mock_mode functionality for testing without API
- Don't modify existing PatternDetector or DashboardBuilder
- The baseline has 11 failing tests - focus on not introducing new failures
