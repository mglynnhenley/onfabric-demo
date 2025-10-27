# API Enrichment Implementation Plan (v2 - API Pattern)

> **For Claude:** Use `${SUPERPOWERS_SKILLS_ROOT}/skills/collaboration/executing-plans/SKILL.md` to implement this plan task-by-task.

**Goal:** Implement real-time API data enrichment using an `api/` abstraction layer with Protocol-based interfaces for weather, videos, events, and geocoding.

**Architecture:** Create new `api/` folder with Protocol interfaces and concrete implementations for external services (OpenWeatherMap, YouTube, Ticketmaster, Mapbox). Refactor UIGenerator to use dependency injection with these API abstractions. Geocode locations before fetching weather.

**Tech Stack:** Python Protocols (typing), httpx AsyncClient, Pydantic validation, async/await

---

## Current State

**Working:**
- ✅ All 6 UI component types defined
- ✅ UIGenerator selects components using Claude
- ✅ Dashboard renders components with placeholder data
- ✅ Basic API client skeletons exist in `core/api_clients.py`

**Missing:**
- ❌ No proper API abstraction layer
- ❌ APIs use placeholder data only
- ❌ UIGenerator tightly coupled to concrete clients
- ❌ No dependency injection

**Problems to Fix:**
- ❌ Eventbrite API is deprecated (replace with Ticketmaster)
- ❌ OpenWeatherMap needs coordinates (requires geocoding first)
- ❌ YouTube missing required `part` parameter

---

## Architecture Overview

### New Structure
```
fabric_dashboard/
├── api/                          # NEW: API abstraction layer
│   ├── __init__.py              # Export all APIs
│   ├── base.py                  # Shared utilities (retry, error handling)
│   ├── weather.py               # WeatherAPI + OpenWeatherAPI
│   ├── videos.py                # VideoAPI + YouTubeAPI
│   ├── events.py                # EventsAPI + TicketmasterAPI
│   └── geocoding.py             # GeocodingAPI + MapboxAPI
├── core/
│   ├── ui_generator.py          # MODIFY: Use dependency injection
│   ├── api_clients.py           # DELETE: Deprecated
│   └── ...
```

### Abstraction Pattern
```
┌──────────────────────────────┐
│      UIGenerator             │
│  (Business Logic Layer)      │
└──────────┬───────────────────┘
           │
           │ Depends on Protocols
           ▼
┌──────────────────────────────┐
│    API Protocols (Interface) │
│  - WeatherAPI                │
│  - VideoAPI                  │
│  - EventsAPI                 │
│  - GeocodingAPI              │
└──────────┬───────────────────┘
           │
           │ Implemented by
           ▼
┌──────────────────────────────┐
│   Concrete Implementations   │
│  - OpenWeatherAPI            │
│  - YouTubeAPI                │
│  - TicketmasterAPI           │
│  - MapboxAPI                 │
└──────────────────────────────┘
```

---

## Task 1: Create API Base Utilities

**Files:**
- Create: `fabric_dashboard/api/__init__.py`
- Create: `fabric_dashboard/api/base.py`

**Step 1: Create API package init file**

Create `fabric_dashboard/api/__init__.py`:

```python
"""External API abstractions for UI enrichment."""

from fabric_dashboard.api.weather import WeatherAPI, OpenWeatherAPI
from fabric_dashboard.api.videos import VideoAPI, YouTubeAPI
from fabric_dashboard.api.events import EventsAPI, TicketmasterAPI
from fabric_dashboard.api.geocoding import GeocodingAPI, MapboxAPI

__all__ = [
    "WeatherAPI",
    "OpenWeatherAPI",
    "VideoAPI",
    "YouTubeAPI",
    "EventsAPI",
    "TicketmasterAPI",
    "GeocodingAPI",
    "MapboxAPI",
]
```

**Step 2: Create base utilities**

Create `fabric_dashboard/api/base.py`:

```python
"""Shared utilities for API clients."""

import asyncio
from typing import Any, Callable, TypeVar
from fabric_dashboard.utils import logger

T = TypeVar("T")


async def retry_with_backoff(
    coro_func: Callable[..., Any],
    max_attempts: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
) -> T:
    """
    Retry async function with exponential backoff.

    Args:
        coro_func: Async function to retry.
        max_attempts: Maximum retry attempts.
        initial_delay: Initial delay in seconds.
        backoff_factor: Multiplier for each retry.

    Returns:
        Result from successful call.

    Raises:
        Last exception if all retries fail.
    """
    delay = initial_delay

    for attempt in range(max_attempts):
        try:
            return await coro_func()
        except Exception as e:
            if attempt == max_attempts - 1:
                logger.error(f"All {max_attempts} attempts failed: {e}")
                raise

            logger.warning(
                f"Attempt {attempt + 1}/{max_attempts} failed: {e}. "
                f"Retrying in {delay}s..."
            )
            await asyncio.sleep(delay)
            delay *= backoff_factor


class APIError(Exception):
    """Base exception for API errors."""

    def __init__(self, message: str, status_code: int = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class RateLimitError(APIError):
    """Raised when API rate limit is exceeded."""

    pass


class AuthenticationError(APIError):
    """Raised when API authentication fails."""

    pass
```

**Step 3: Test base utilities work**

```bash
python -c "from fabric_dashboard.api.base import retry_with_backoff, APIError; print('Base utilities loaded')"
```

Expected: `Base utilities loaded`

**Step 4: Commit base setup**

```bash
git add fabric_dashboard/api/
git commit -m "feat: create API abstraction base utilities"
```

---

## Task 2: Create Geocoding API

**Files:**
- Create: `fabric_dashboard/api/geocoding.py`

**Why First?** Weather API needs geocoding to convert locations → coordinates

**Step 1: Write geocoding API with Protocol and implementation**

Create `fabric_dashboard/api/geocoding.py`:

```python
"""Geocoding API for converting locations to coordinates."""

from typing import Optional, Protocol
import httpx
from fabric_dashboard.utils import logger
from fabric_dashboard.api.base import retry_with_backoff, APIError


# ============================================================================
# PROTOCOL (Interface)
# ============================================================================


class GeocodingAPI(Protocol):
    """Protocol for geocoding services."""

    async def geocode(self, location: str) -> dict:
        """
        Convert location name to coordinates.

        Args:
            location: Location string (e.g., "San Francisco, CA").

        Returns:
            Dict with lat, lng, formatted_address.
        """
        ...


# ============================================================================
# MAPBOX IMPLEMENTATION
# ============================================================================


class MapboxAPI:
    """Mapbox Geocoding API implementation."""

    BASE_URL = "https://api.mapbox.com/search/geocode/v6/forward"

    def __init__(
        self,
        api_key: Optional[str] = None,
        http_client: Optional[httpx.AsyncClient] = None,
        mock_mode: bool = False,
    ):
        """
        Initialize Mapbox API client.

        Args:
            api_key: Mapbox access token.
            http_client: Shared HTTP client (optional).
            mock_mode: Use mock data instead of real API.
        """
        self.api_key = api_key
        self.client = http_client or httpx.AsyncClient()
        self.mock_mode = mock_mode

        if not mock_mode and not api_key:
            logger.warning("No Mapbox API key provided, using mock mode")
            self.mock_mode = True

    async def geocode(self, location: str) -> dict:
        """
        Geocode location string to coordinates.

        Args:
            location: Location to geocode.

        Returns:
            Dict with lat, lng, formatted_address.
        """
        if self.mock_mode:
            return self._mock_geocode(location)

        try:
            async def _fetch():
                response = await self.client.get(
                    self.BASE_URL,
                    params={
                        "q": location,
                        "access_token": self.api_key,
                        "limit": 1,
                    },
                    timeout=10.0,
                )
                response.raise_for_status()
                return response.json()

            data = await retry_with_backoff(_fetch, max_attempts=2)

            # Parse GeoJSON FeatureCollection
            features = data.get("features", [])
            if not features:
                raise APIError(f"No results found for location: {location}")

            feature = features[0]
            coords = feature["geometry"]["coordinates"]

            return {
                "lat": coords[1],  # GeoJSON is [lng, lat]
                "lng": coords[0],
                "formatted_address": feature["properties"].get(
                    "full_address", location
                ),
            }

        except Exception as e:
            logger.error(f"Mapbox geocoding failed for '{location}': {e}")
            # Fallback to mock on error
            return self._mock_geocode(location)

    def _mock_geocode(self, location: str) -> dict:
        """Generate mock geocoding result."""
        # Default to San Francisco coordinates
        return {
            "lat": 37.7749,
            "lng": -122.4194,
            "formatted_address": location,
        }
```

**Step 2: Test geocoding API**

```bash
python -c "
from fabric_dashboard.api.geocoding import MapboxAPI
import asyncio

async def test():
    api = MapboxAPI(mock_mode=True)
    result = await api.geocode('San Francisco')
    print(f'Geocoded: {result}')

asyncio.run(test())
"
```

Expected: `Geocoded: {'lat': 37.7749, 'lng': -122.4194, ...}`

**Step 3: Commit geocoding API**

```bash
git add fabric_dashboard/api/geocoding.py
git commit -m "feat: add Mapbox geocoding API abstraction"
```

---

## Task 3: Create Weather API (with geocoding dependency)

**Files:**
- Create: `fabric_dashboard/api/weather.py`

**Step 1: Write weather API Protocol and OpenWeatherMap implementation**

Create `fabric_dashboard/api/weather.py`:

```python
"""Weather API for current conditions and forecasts."""

import random
from datetime import datetime, timedelta, timezone
from typing import Optional, Protocol
import httpx
from fabric_dashboard.utils import logger
from fabric_dashboard.api.base import retry_with_backoff, APIError


# ============================================================================
# PROTOCOL (Interface)
# ============================================================================


class WeatherAPI(Protocol):
    """Protocol for weather services."""

    async def get_current_weather(
        self, lat: float, lon: float, units: str = "metric"
    ) -> dict:
        """
        Get current weather for coordinates.

        Args:
            lat: Latitude.
            lon: Longitude.
            units: 'metric' or 'imperial'.

        Returns:
            Dict with temperature, feels_like, condition, etc.
        """
        ...

    async def get_forecast(
        self, lat: float, lon: float, days: int = 3, units: str = "metric"
    ) -> list[dict]:
        """
        Get multi-day weather forecast.

        Args:
            lat: Latitude.
            lon: Longitude.
            days: Number of days (max 8).
            units: 'metric' or 'imperial'.

        Returns:
            List of forecast dicts.
        """
        ...


# ============================================================================
# OPENWEATHERMAP IMPLEMENTATION
# ============================================================================


class OpenWeatherAPI:
    """OpenWeatherMap One Call API 3.0 implementation."""

    BASE_URL = "https://api.openweathermap.org/data/3.0/onecall"

    def __init__(
        self,
        api_key: Optional[str] = None,
        http_client: Optional[httpx.AsyncClient] = None,
        mock_mode: bool = False,
    ):
        """
        Initialize OpenWeatherMap API client.

        Args:
            api_key: OpenWeatherMap API key.
            http_client: Shared HTTP client (optional).
            mock_mode: Use mock data instead of real API.
        """
        self.api_key = api_key
        self.client = http_client or httpx.AsyncClient()
        self.mock_mode = mock_mode

        if not mock_mode and not api_key:
            logger.warning("No OpenWeatherMap API key, using mock mode")
            self.mock_mode = True

    async def get_current_weather(
        self, lat: float, lon: float, units: str = "metric"
    ) -> dict:
        """
        Fetch current weather from OpenWeatherMap.

        Args:
            lat: Latitude.
            lon: Longitude.
            units: Temperature units.

        Returns:
            Normalized weather dict.
        """
        if self.mock_mode:
            return self._mock_current_weather(units)

        try:
            async def _fetch():
                response = await self.client.get(
                    self.BASE_URL,
                    params={
                        "lat": lat,
                        "lon": lon,
                        "appid": self.api_key,
                        "units": units,
                        "exclude": "minutely,hourly,daily,alerts",  # Current only
                    },
                    timeout=10.0,
                )
                response.raise_for_status()
                return response.json()

            data = await retry_with_backoff(_fetch, max_attempts=2)

            # Normalize to internal format
            current = data["current"]
            return {
                "temperature": round(current["temp"], 1),
                "feels_like": round(current["feels_like"], 1),
                "condition": current["weather"][0]["description"].title(),
                "icon": current["weather"][0]["icon"],
                "humidity": current["humidity"],
                "wind_speed": round(current["wind_speed"], 1),
                "units": units,
                "temp_unit": "°C" if units == "metric" else "°F",
            }

        except Exception as e:
            logger.error(f"OpenWeatherMap current weather failed: {e}")
            return self._mock_current_weather(units)

    async def get_forecast(
        self, lat: float, lon: float, days: int = 3, units: str = "metric"
    ) -> list[dict]:
        """
        Fetch weather forecast from OpenWeatherMap.

        Args:
            lat: Latitude.
            lon: Longitude.
            days: Number of days (max 8).
            units: Temperature units.

        Returns:
            List of forecast dicts.
        """
        if self.mock_mode:
            return self._mock_forecast(days, units)

        try:
            async def _fetch():
                response = await self.client.get(
                    self.BASE_URL,
                    params={
                        "lat": lat,
                        "lon": lon,
                        "appid": self.api_key,
                        "units": units,
                        "exclude": "minutely,hourly,current,alerts",  # Daily only
                    },
                    timeout=10.0,
                )
                response.raise_for_status()
                return response.json()

            data = await retry_with_backoff(_fetch, max_attempts=2)

            # Normalize daily forecast
            forecasts = []
            for day_data in data.get("daily", [])[:days]:
                date = datetime.fromtimestamp(day_data["dt"], tz=timezone.utc)
                forecasts.append({
                    "date": date.isoformat(),
                    "day_name": date.strftime("%A"),
                    "temperature_high": round(day_data["temp"]["max"], 1),
                    "temperature_low": round(day_data["temp"]["min"], 1),
                    "condition": day_data["weather"][0]["description"].title(),
                    "icon": day_data["weather"][0]["icon"],
                    "precipitation_chance": int(day_data.get("pop", 0) * 100),
                })

            return forecasts

        except Exception as e:
            logger.error(f"OpenWeatherMap forecast failed: {e}")
            return self._mock_forecast(days, units)

    def _mock_current_weather(self, units: str = "metric") -> dict:
        """Generate mock current weather."""
        temp_unit = "°C" if units == "metric" else "°F"
        base_temp = (
            random.randint(15, 28) if units == "metric" else random.randint(60, 85)
        )

        conditions = ["Clear", "Partly Cloudy", "Cloudy", "Rainy", "Sunny"]
        icons = ["01d", "02d", "03d", "10d", "01d"]
        idx = random.randint(0, len(conditions) - 1)

        return {
            "temperature": base_temp,
            "feels_like": base_temp - random.randint(0, 3),
            "condition": conditions[idx],
            "icon": icons[idx],
            "humidity": random.randint(40, 80),
            "wind_speed": round(random.uniform(5, 20), 1),
            "units": units,
            "temp_unit": temp_unit,
        }

    def _mock_forecast(self, days: int, units: str = "metric") -> list[dict]:
        """Generate mock forecast."""
        forecasts = []
        base_temp = (
            random.randint(15, 28) if units == "metric" else random.randint(60, 85)
        )
        conditions = ["Clear", "Partly Cloudy", "Cloudy", "Rainy", "Sunny"]
        icons = ["01d", "02d", "03d", "10d", "01d"]

        for i in range(days):
            date = datetime.now(timezone.utc) + timedelta(days=i + 1)
            idx = random.randint(0, len(conditions) - 1)
            temp_var = random.randint(-5, 5)

            forecasts.append({
                "date": date.isoformat(),
                "day_name": date.strftime("%A"),
                "temperature_high": base_temp + temp_var + 2,
                "temperature_low": base_temp + temp_var - 2,
                "condition": conditions[idx],
                "icon": icons[idx],
                "precipitation_chance": random.randint(0, 60),
            })

        return forecasts
```

**Step 2: Test weather API**

```bash
python -c "
from fabric_dashboard.api.weather import OpenWeatherAPI
import asyncio

async def test():
    api = OpenWeatherAPI(mock_mode=True)
    weather = await api.get_current_weather(37.7749, -122.4194)
    print(f'Weather: {weather[\"temperature\"]}°{weather[\"temp_unit\"]} - {weather[\"condition\"]}')

    forecast = await api.get_forecast(37.7749, -122.4194, days=3)
    print(f'Forecast: {len(forecast)} days')

asyncio.run(test())
"
```

Expected: `Weather: 22°C - Sunny` and `Forecast: 3 days`

**Step 3: Commit weather API**

```bash
git add fabric_dashboard/api/weather.py
git commit -m "feat: add OpenWeatherMap API with coordinate-based calls"
```

---

## Task 4: Create Video API

**Files:**
- Create: `fabric_dashboard/api/videos.py`

**Step 1: Write YouTube API with proper parameters**

Create `fabric_dashboard/api/videos.py`:

```python
"""Video API for YouTube video search."""

import random
from datetime import datetime, timedelta, timezone
from typing import Optional, Protocol
import httpx
from fabric_dashboard.utils import logger
from fabric_dashboard.api.base import retry_with_backoff, APIError


# ============================================================================
# PROTOCOL (Interface)
# ============================================================================


class VideoAPI(Protocol):
    """Protocol for video search services."""

    async def search_videos(
        self,
        query: str,
        max_results: int = 3,
        duration: str = "any",
        order_by: str = "relevance",
    ) -> list[dict]:
        """
        Search for videos matching query.

        Args:
            query: Search query.
            max_results: Number of results (1-50).
            duration: 'any', 'short', 'medium', 'long'.
            order_by: 'relevance', 'date', 'viewCount'.

        Returns:
            List of video dicts with video_id, title, etc.
        """
        ...


# ============================================================================
# YOUTUBE IMPLEMENTATION
# ============================================================================


class YouTubeAPI:
    """YouTube Data API v3 implementation."""

    BASE_URL = "https://www.googleapis.com/youtube/v3/search"

    def __init__(
        self,
        api_key: Optional[str] = None,
        http_client: Optional[httpx.AsyncClient] = None,
        mock_mode: bool = False,
    ):
        """
        Initialize YouTube API client.

        Args:
            api_key: YouTube Data API v3 key.
            http_client: Shared HTTP client (optional).
            mock_mode: Use mock data instead of real API.
        """
        self.api_key = api_key
        self.client = http_client or httpx.AsyncClient()
        self.mock_mode = mock_mode

        if not mock_mode and not api_key:
            logger.warning("No YouTube API key, using mock mode")
            self.mock_mode = True

    async def search_videos(
        self,
        query: str,
        max_results: int = 3,
        duration: str = "any",
        order_by: str = "relevance",
    ) -> list[dict]:
        """
        Search YouTube for videos.

        Args:
            query: Search query.
            max_results: Number of results.
            duration: Video length filter.
            order_by: Sort order.

        Returns:
            List of video dicts.
        """
        if self.mock_mode:
            return self._mock_videos(query, max_results, duration)

        try:
            params = {
                "part": "snippet",  # REQUIRED by YouTube API
                "q": query,
                "type": "video",
                "maxResults": min(max_results, 50),
                "order": order_by,
                "key": self.api_key,
            }

            # Add duration filter if specified
            if duration != "any":
                params["videoDuration"] = duration

            async def _fetch():
                response = await self.client.get(
                    self.BASE_URL,
                    params=params,
                    timeout=10.0,
                )
                response.raise_for_status()
                return response.json()

            data = await retry_with_backoff(_fetch, max_attempts=2)

            # Normalize to internal format
            videos = []
            for item in data.get("items", []):
                video_id = item["id"]["videoId"]
                snippet = item["snippet"]

                videos.append({
                    "video_id": video_id,
                    "title": snippet["title"],
                    "channel_name": snippet["channelTitle"],
                    "thumbnail_url": snippet["thumbnails"]["high"]["url"],
                    "published_at": snippet["publishedAt"],
                    "url": f"https://www.youtube.com/watch?v={video_id}",
                })

            return videos

        except Exception as e:
            logger.error(f"YouTube API search failed for '{query}': {e}")
            return self._mock_videos(query, max_results, duration)

    def _mock_videos(
        self, query: str, max_results: int, duration: str
    ) -> list[dict]:
        """Generate mock video data."""
        duration_lengths = {
            "short": ["5:23", "3:45", "7:12"],
            "medium": ["12:34", "15:20", "18:45"],
            "long": ["45:30", "1:02:15", "52:40"],
            "any": ["5:23", "15:20", "45:30"],
        }
        durations = duration_lengths.get(duration, duration_lengths["any"])

        videos = []
        for i in range(max_results):
            video_id = f"mock_{random.randint(1000, 9999)}"
            videos.append({
                "video_id": video_id,
                "title": f"{query.title()} - Tutorial Part {i + 1}",
                "channel_name": random.choice([
                    "Tech Explained",
                    "Learning Hub",
                    "Expert Tutorials",
                    "Digital Mastery",
                ]),
                "thumbnail_url": f"https://i.ytimg.com/vi/{video_id}/mqdefault.jpg",
                "duration": random.choice(durations),
                "view_count": random.randint(10000, 1000000),
                "published_at": (
                    datetime.now(timezone.utc) - timedelta(days=random.randint(1, 90))
                ).isoformat(),
                "url": f"https://www.youtube.com/watch?v={video_id}",
            })

        return videos
```

**Step 2: Test YouTube API**

```bash
python -c "
from fabric_dashboard.api.videos import YouTubeAPI
import asyncio

async def test():
    api = YouTubeAPI(mock_mode=True)
    videos = await api.search_videos('python tutorial', max_results=3)
    print(f'Found {len(videos)} videos')
    print(f'First: {videos[0][\"title\"]}')

asyncio.run(test())
"
```

Expected: `Found 3 videos` and a title

**Step 3: Commit video API**

```bash
git add fabric_dashboard/api/videos.py
git commit -m "feat: add YouTube API with proper parameters"
```

---

## Task 5: Create Events API (Ticketmaster)

**Files:**
- Create: `fabric_dashboard/api/events.py`

**Step 1: Write Ticketmaster API implementation**

Create `fabric_dashboard/api/events.py`:

```python
"""Events API for discovering upcoming events."""

import random
from datetime import datetime, timedelta, timezone
from typing import Optional, Protocol
import httpx
from fabric_dashboard.utils import logger
from fabric_dashboard.api.base import retry_with_backoff, APIError


# ============================================================================
# PROTOCOL (Interface)
# ============================================================================


class EventsAPI(Protocol):
    """Protocol for event discovery services."""

    async def search_events(
        self,
        query: str,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
        radius_miles: int = 25,
        max_results: int = 10,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> list[dict]:
        """
        Search for events by query and location.

        Args:
            query: Search keywords.
            lat: Latitude for location search.
            lon: Longitude for location search.
            radius_miles: Search radius in miles.
            max_results: Maximum number of results.
            start_date: Start date filter (ISO format).
            end_date: End date filter (ISO format).

        Returns:
            List of event dicts.
        """
        ...


# ============================================================================
# TICKETMASTER IMPLEMENTATION
# ============================================================================


class TicketmasterAPI:
    """Ticketmaster Discovery API implementation."""

    BASE_URL = "https://app.ticketmaster.com/discovery/v2/events.json"

    def __init__(
        self,
        api_key: Optional[str] = None,
        http_client: Optional[httpx.AsyncClient] = None,
        mock_mode: bool = False,
    ):
        """
        Initialize Ticketmaster API client.

        Args:
            api_key: Ticketmaster API key.
            http_client: Shared HTTP client (optional).
            mock_mode: Use mock data instead of real API.
        """
        self.api_key = api_key
        self.client = http_client or httpx.AsyncClient()
        self.mock_mode = mock_mode

        if not mock_mode and not api_key:
            logger.warning("No Ticketmaster API key, using mock mode")
            self.mock_mode = True

    async def search_events(
        self,
        query: str,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
        radius_miles: int = 25,
        max_results: int = 10,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> list[dict]:
        """
        Search Ticketmaster for events.

        Args:
            query: Search keywords.
            lat: Latitude for location-based search.
            lon: Longitude for location-based search.
            radius_miles: Search radius.
            max_results: Max events to return.
            start_date: Start date filter.
            end_date: End date filter.

        Returns:
            List of normalized event dicts.
        """
        if self.mock_mode:
            return self._mock_events(query, max_results)

        try:
            params = {
                "apikey": self.api_key,
                "keyword": query,
                "size": min(max_results, 200),
                "sort": "date,asc",
            }

            # Location-based search
            if lat is not None and lon is not None:
                params["latlong"] = f"{lat},{lon}"
                params["radius"] = radius_miles
                params["unit"] = "miles"

            # Date range filters
            if start_date:
                params["startDateTime"] = start_date
            if end_date:
                params["endDateTime"] = end_date

            async def _fetch():
                response = await self.client.get(
                    self.BASE_URL,
                    params=params,
                    timeout=10.0,
                )
                response.raise_for_status()
                return response.json()

            data = await retry_with_backoff(_fetch, max_attempts=2)

            # Normalize to internal format
            events = []
            for event in data.get("_embedded", {}).get("events", []):
                # Extract venue info
                venues = event.get("_embedded", {}).get("venues", [])
                venue_name = venues[0]["name"] if venues else "TBD"
                city = venues[0].get("city", {}).get("name", "TBD") if venues else "TBD"

                # Extract date/time
                start = event["dates"]["start"]
                date = start.get("localDate", "TBD")
                time = start.get("localTime")

                events.append({
                    "name": event["name"],
                    "date": date,
                    "time": time,
                    "url": event["url"],
                    "venue": venue_name,
                    "city": city,
                    "is_virtual": False,  # Ticketmaster doesn't clearly indicate virtual
                })

            return events

        except Exception as e:
            logger.error(f"Ticketmaster API search failed for '{query}': {e}")
            return self._mock_events(query, max_results)

    def _mock_events(self, query: str, max_results: int) -> list[dict]:
        """Generate mock event data."""
        today = datetime.now(timezone.utc)

        event_types = [
            "Workshop", "Meetup", "Conference", "Concert", "Festival", "Talk"
        ]
        venues = [
            "TechHub", "Convention Center", "Community Hall", "Auditorium"
        ]
        cities = [
            "San Francisco", "New York", "Austin", "Seattle", "Boston"
        ]

        events = []
        for i in range(max_results):
            event_date = today + timedelta(days=random.randint(3, 90))
            event_type = random.choice(event_types)

            events.append({
                "name": f"{query.title()} {event_type} {i + 1}",
                "date": event_date.strftime("%Y-%m-%d"),
                "time": f"{random.randint(10, 19)}:00:00",
                "url": f"https://example.com/event-{i}",
                "venue": random.choice(venues),
                "city": random.choice(cities),
                "is_virtual": random.choice([True, False]),
            })

        return events
```

**Step 2: Test Ticketmaster API**

```bash
python -c "
from fabric_dashboard.api.events import TicketmasterAPI
import asyncio

async def test():
    api = TicketmasterAPI(mock_mode=True)
    events = await api.search_events('tech conference', max_results=5)
    print(f'Found {len(events)} events')
    print(f'First: {events[0][\"name\"]} on {events[0][\"date\"]}')

asyncio.run(test())
"
```

Expected: `Found 5 events` and event details

**Step 3: Commit events API**

```bash
git add fabric_dashboard/api/events.py
git commit -m "feat: add Ticketmaster API for event discovery"
```

---

## Task 6: Update API Package Exports

**Files:**
- Modify: `fabric_dashboard/api/__init__.py`

**Step 1: Verify all APIs are exported**

Check `fabric_dashboard/api/__init__.py` contains all imports:

```python
"""External API abstractions for UI enrichment."""

from fabric_dashboard.api.weather import WeatherAPI, OpenWeatherAPI
from fabric_dashboard.api.videos import VideoAPI, YouTubeAPI
from fabric_dashboard.api.events import EventsAPI, TicketmasterAPI
from fabric_dashboard.api.geocoding import GeocodingAPI, MapboxAPI

__all__ = [
    "WeatherAPI",
    "OpenWeatherAPI",
    "VideoAPI",
    "YouTubeAPI",
    "EventsAPI",
    "TicketmasterAPI",
    "GeocodingAPI",
    "MapboxAPI",
]
```

**Step 2: Test package imports work**

```bash
python -c "
from fabric_dashboard.api import (
    OpenWeatherAPI,
    YouTubeAPI,
    TicketmasterAPI,
    MapboxAPI,
)
print('All API imports successful')
"
```

Expected: `All API imports successful`

**Step 3: Commit if changes made**

```bash
git add fabric_dashboard/api/__init__.py
git commit -m "feat: finalize API package exports"
```

---

## Task 7: Refactor UIGenerator to Use APIs

**Files:**
- Modify: `fabric_dashboard/core/ui_generator.py`
- Modify: `fabric_dashboard/models/ui_components.py`

**Step 1: Add enriched_data fields to component schemas**

In `fabric_dashboard/models/ui_components.py`, update component classes:

```python
# Add to InfoCard (around line 60):
    enriched_data: Optional[dict] = Field(
        default=None, description="Enriched weather data from API"
    )

# Add to VideoFeed (around line 110):
    enriched_videos: Optional[list[dict]] = Field(
        default=None, description="Enriched video data from YouTube API"
    )

# Add to EventCalendar (around line 150):
    enriched_events: Optional[list[dict]] = Field(
        default=None, description="Enriched event data from Ticketmaster API"
    )
```

**Step 2: Update UIGenerator __init__ for dependency injection**

In `fabric_dashboard/core/ui_generator.py`, replace __init__ method (around line 60):

```python
def __init__(
    self,
    weather_api: Optional[Any] = None,  # WeatherAPI type
    videos_api: Optional[Any] = None,   # VideoAPI type
    events_api: Optional[Any] = None,   # EventsAPI type
    geocoding_api: Optional[Any] = None,  # GeocodingAPI type
    mock_mode: bool = False,
):
    """
    Initialize UI Generator with API dependencies.

    Args:
        weather_api: Weather API implementation.
        videos_api: Video API implementation.
        events_api: Events API implementation.
        geocoding_api: Geocoding API implementation.
        mock_mode: Use mock data for testing.
    """
    self.mock_mode = mock_mode

    # Initialize APIs (create defaults if not provided)
    if weather_api is None:
        from fabric_dashboard.api import OpenWeatherAPI
        from fabric_dashboard.utils.config import get_config

        config = get_config()
        weather_api = OpenWeatherAPI(
            api_key=config.openweathermap_api_key,
            mock_mode=mock_mode,
        )

    if videos_api is None:
        from fabric_dashboard.api import YouTubeAPI
        from fabric_dashboard.utils.config import get_config

        config = get_config()
        videos_api = YouTubeAPI(
            api_key=config.youtube_api_key,
            mock_mode=mock_mode,
        )

    if events_api is None:
        from fabric_dashboard.api import TicketmasterAPI
        from fabric_dashboard.utils.config import get_config

        config = get_config()
        events_api = TicketmasterAPI(
            api_key=config.ticketmaster_api_key,
            mock_mode=mock_mode,
        )

    if geocoding_api is None:
        from fabric_dashboard.api import MapboxAPI
        from fabric_dashboard.utils.config import get_config

        config = get_config()
        geocoding_api = MapboxAPI(
            api_key=config.mapbox_api_key,
            mock_mode=mock_mode,
        )

    self.weather = weather_api
    self.videos = videos_api
    self.events = events_api
    self.geocoding = geocoding_api

    # Initialize LLM client (existing code)
    # ... rest of existing __init__ code
```

**Step 3: Implement enrichment methods**

In `fabric_dashboard/core/ui_generator.py`, replace `_enrich_components` and add enrichment methods (around line 441):

```python
async def _enrich_components(
    self, components: list[UIComponentType]
) -> list[UIComponentType]:
    """
    Enrich components with real API data.

    Dispatches each component to appropriate enrichment method,
    running all in parallel for performance.

    Args:
        components: Components from LLM selection.

    Returns:
        Components with enriched data.
    """
    logger.info(f"Enriching {len(components)} components with API data")

    # Create enrichment tasks for parallel execution
    tasks = []
    for comp in components:
        if comp.component_type == "info-card":
            tasks.append(self._enrich_weather(comp))
        elif comp.component_type == "video-feed":
            tasks.append(self._enrich_videos(comp))
        elif comp.component_type == "event-calendar":
            tasks.append(self._enrich_events(comp))
        elif comp.component_type == "map-card":
            tasks.append(self._enrich_map(comp))
        else:
            # No enrichment needed (task-list, content-card)
            async def return_as_is():
                return comp
            tasks.append(return_as_is())

    # Execute all enrichments in parallel
    try:
        enriched = await asyncio.gather(*tasks, return_exceptions=False)
        logger.success(f"Successfully enriched {len(enriched)} components")
        return enriched
    except Exception as e:
        logger.error(f"Enrichment failed: {e}")
        # Return original components on failure
        return components


async def _enrich_weather(self, component: InfoCard) -> InfoCard:
    """
    Enrich weather component with real API data.

    Strategy: Geocode location first, then fetch weather.

    Args:
        component: InfoCard to enrich.

    Returns:
        InfoCard with enriched_data populated.
    """
    try:
        logger.info(f"Enriching weather for {component.location}")

        # Step 1: Geocode location to coordinates
        coords = await self.geocoding.geocode(component.location)

        # Step 2: Fetch current weather
        current = await self.weather.get_current_weather(
            lat=coords["lat"],
            lon=coords["lon"],
            units=component.units,
        )

        # Step 3: Fetch forecast if requested
        forecast = []
        if component.show_forecast:
            forecast = await self.weather.get_forecast(
                lat=coords["lat"],
                lon=coords["lon"],
                days=3,
                units=component.units,
            )

        # Step 4: Return enriched component
        enriched_data = {
            "current": current,
            "forecast": forecast,
            "location": coords["formatted_address"],
        }

        return component.model_copy(update={"enriched_data": enriched_data})

    except Exception as e:
        logger.warning(f"Weather enrichment failed for {component.location}: {e}")
        return component


async def _enrich_videos(self, component: VideoFeed) -> VideoFeed:
    """
    Enrich video component with YouTube search results.

    Args:
        component: VideoFeed to enrich.

    Returns:
        VideoFeed with enriched_videos populated.
    """
    try:
        logger.info(f"Enriching videos for query: {component.search_query}")

        videos = await self.videos.search_videos(
            query=component.search_query,
            max_results=component.max_results,
            duration=component.video_duration,
            order_by=component.order_by,
        )

        return component.model_copy(update={"enriched_videos": videos})

    except Exception as e:
        logger.warning(f"Video enrichment failed for '{component.search_query}': {e}")
        return component


async def _enrich_events(self, component: EventCalendar) -> EventCalendar:
    """
    Enrich event calendar with Ticketmaster results.

    Args:
        component: EventCalendar to enrich.

    Returns:
        EventCalendar with enriched_events populated.
    """
    try:
        logger.info(f"Enriching events for query: {component.search_query}")

        # Geocode location if provided
        lat, lon = None, None
        if component.location:
            coords = await self.geocoding.geocode(component.location)
            lat, lon = coords["lat"], coords["lon"]

        # Search for events
        events = await self.events.search_events(
            query=component.search_query,
            lat=lat,
            lon=lon,
            radius_miles=25,
            max_results=component.max_events,
        )

        return component.model_copy(update={"enriched_events": events})

    except Exception as e:
        logger.warning(f"Event enrichment failed for '{component.search_query}': {e}")
        return component


async def _enrich_map(self, component: MapCard) -> MapCard:
    """
    Enrich map component (currently minimal - coordinates already from LLM).

    Args:
        component: MapCard to enrich.

    Returns:
        MapCard (unchanged for now).
    """
    try:
        logger.info(f"Map component already has {len(component.markers)} markers")
        # Map coordinates already populated by LLM
        # Could add POI enrichment in future
        return component

    except Exception as e:
        logger.warning(f"Map enrichment failed: {e}")
        return component
```

**Step 4: Add asyncio import at top of file**

At top of `fabric_dashboard/core/ui_generator.py`, ensure asyncio is imported:

```python
import asyncio
from typing import Optional
```

**Step 5: Run tests to verify refactor**

```bash
python -m pytest fabric_dashboard/tests/test_ui_generator.py -v
```

Expected: Existing tests should still pass (they use mock mode)

**Step 6: Commit UIGenerator refactor**

```bash
git add fabric_dashboard/core/ui_generator.py fabric_dashboard/models/ui_components.py
git commit -m "refactor: update UIGenerator to use API abstraction layer"
```

---

## Task 8: Add API Key Configuration

**Files:**
- Modify: `fabric_dashboard/utils/config.py`
- Create: `.env.example`

**Step 1: Add API key fields to Config schema**

In `fabric_dashboard/utils/config.py`, find the `Config` class and add new fields:

```python
class Config(BaseModel):
    """Configuration for fabric_dashboard."""

    # Existing fields
    anthropic_api_key: str = Field(...)
    perplexity_api_key: Optional[str] = Field(None)

    # NEW: External API keys for UI enrichment
    openweathermap_api_key: Optional[str] = Field(
        None,
        description="OpenWeatherMap API key for weather widgets",
    )
    youtube_api_key: Optional[str] = Field(
        None,
        description="YouTube Data API v3 key for video feeds",
    )
    ticketmaster_api_key: Optional[str] = Field(
        None,
        description="Ticketmaster API key for event discovery",
    )
    mapbox_api_key: Optional[str] = Field(
        None,
        description="Mapbox API token for geocoding and maps",
    )

    # ... rest of existing Config fields
```

**Step 2: Create .env.example file**

Create `.env.example` at project root:

```bash
# ============================================================================
# Fabric Dashboard - Environment Variables
# ============================================================================

# Required: Claude API key
ANTHROPIC_API_KEY=sk-ant-...

# Optional: Perplexity API key for search enrichment
PERPLEXITY_API_KEY=pplx-...

# ============================================================================
# Optional: External APIs for UI Component Enrichment
# ============================================================================

# OpenWeatherMap API (weather widgets)
# Free tier: 1,000 calls/day
# Sign up: https://openweathermap.org/api
# Get key: https://home.openweathermap.org/api_keys
OPENWEATHERMAP_API_KEY=

# YouTube Data API v3 (video feeds)
# Free tier: 10,000 units/day (100 searches)
# Enable: https://console.cloud.google.com/apis/library/youtube.googleapis.com
# Get key: https://console.cloud.google.com/apis/credentials
YOUTUBE_API_KEY=

# Ticketmaster Discovery API (event calendars)
# Free tier: 5,000 requests/day
# Sign up: https://developer.ticketmaster.com/products-and-docs/apis/getting-started/
# Get key: https://developer-acct.ticketmaster.com/user/register
TICKETMASTER_API_KEY=

# Mapbox API (geocoding & maps)
# Free tier: 100,000 requests/month for geocoding
# Sign up: https://account.mapbox.com/
# Get token: https://account.mapbox.com/access-tokens/
MAPBOX_API_KEY=
```

**Step 3: Test configuration loading**

```bash
python -c "
from fabric_dashboard.utils.config import get_config
config = get_config()
print(f'OpenWeather key: {\"set\" if config.openweathermap_api_key else \"not set\"}')
print(f'YouTube key: {\"set\" if config.youtube_api_key else \"not set\"}')
print(f'Ticketmaster key: {\"set\" if config.ticketmaster_api_key else \"not set\"}')
print(f'Mapbox key: {\"set\" if config.mapbox_api_key else \"not set\"}')
"
```

Expected: Shows "not set" for new keys (or "set" if you added them)

**Step 4: Commit configuration updates**

```bash
git add fabric_dashboard/utils/config.py .env.example
git commit -m "feat: add external API key configuration"
```

---

## Task 9: Update Dashboard Builder to Use Enriched Data

**Files:**
- Modify: `fabric_dashboard/core/dashboard_builder.py`

**Step 1: Update weather widget rendering**

In `fabric_dashboard/core/dashboard_builder.py`, find `_render_info_card` (line ~540) and update to use enriched data:

```python
def _render_info_card(self, component, idx: int) -> str:
    """
    Render weather information card.

    Uses enriched_data if available, otherwise shows placeholder.
    """
    component_id = f"weather-{idx}"

    # Extract enriched data if available
    temp = "--"
    temp_unit = ""
    condition = "Loading..."
    feels_like = "--"
    humidity = "---"
    wind_speed = "-- km/h"

    if component.enriched_data:
        current = component.enriched_data.get("current", {})
        temp = current.get("temperature", "--")
        temp_unit = current.get("temp_unit", "°")
        condition = current.get("condition", "Unknown")
        feels_like = current.get("feels_like", "--")
        humidity = f"{current.get('humidity', '--')}%"
        wind_speed = f"{current.get('wind_speed', '--')} km/h"

    # Rest of HTML rendering stays the same, but use extracted values
    return f'''<div class="ui-component weather-widget ...">
        <h3>{component.title}</h3>
        <div class="text-4xl">{temp}{temp_unit}</div>
        <div>{condition}</div>
        <div>Feels like {feels_like}{temp_unit}</div>
        <div>Humidity: {humidity}</div>
        <div>Wind: {wind_speed}</div>
        ...
    </div>'''
```

**Step 2: Update video feed rendering**

Find `_render_video_feed` (line ~621) and update:

```python
def _render_video_feed(self, component, idx: int) -> str:
    """Render video feed with enriched YouTube results."""
    component_id = f"videos-{idx}"

    # Use enriched videos if available
    if component.enriched_videos:
        videos = component.enriched_videos[:component.max_results]
        videos_html = '\n'.join([
            f'''<div class="aspect-video">
            <iframe
                width="100%"
                height="100%"
                src="https://www.youtube.com/embed/{video['video_id']}"
                title="{video['title']}"
                frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen
            ></iframe>
        </div>'''
            for video in videos
        ])
    else:
        # Fallback to mock videos
        videos_html = "<!-- Mock videos placeholder -->"

    return f'''<div class="ui-component ...">
        <h3>{component.title}</h3>
        <div class="video-grid">{videos_html}</div>
    </div>'''
```

**Step 3: Update event calendar rendering**

Find `_render_event_calendar` (line ~667) and update to use `component.enriched_events` if available (similar pattern).

**Step 4: Test dashboard rendering**

```bash
python -m pytest fabric_dashboard/tests/test_dashboard_builder.py -v
```

Expected: Tests pass

**Step 5: Commit dashboard builder updates**

```bash
git add fabric_dashboard/core/dashboard_builder.py
git commit -m "feat: update dashboard to render enriched API data"
```

---

## Task 10: Delete Deprecated API Clients

**Files:**
- Delete: `fabric_dashboard/core/api_clients.py`

**Step 1: Verify nothing imports from api_clients.py**

```bash
grep -r "from fabric_dashboard.core.api_clients import" fabric_dashboard/
```

Expected: No matches (or only commented code)

**Step 2: Delete old API clients file**

```bash
git rm fabric_dashboard/core/api_clients.py
```

**Step 3: Commit deletion**

```bash
git commit -m "refactor: remove deprecated api_clients.py (replaced by api/)"
```

---

## Task 11: End-to-End Testing

**Files:**
- Manual testing

**Step 1: Test with mock mode**

```bash
python -m fabric_dashboard generate --mock --no-open
```

Expected:
- ✅ Dashboard generates successfully
- ✅ No errors in output
- ✅ HTML file created

**Step 2: Open dashboard and verify components**

Open the generated HTML file in browser and check:
- ✅ Weather widget shows mock temperature
- ✅ Video feed shows mock videos
- ✅ Event calendar shows mock events
- ✅ No JavaScript errors in console

**Step 3: Test with real API keys (if available)**

If you have API keys, add them to `.env`:

```bash
# Add keys to .env
OPENWEATHERMAP_API_KEY=your_key
YOUTUBE_API_KEY=your_key
TICKETMASTER_API_KEY=your_key
MAPBOX_API_KEY=your_key
```

Run without mock mode:

```bash
python -m fabric_dashboard generate --no-mock --no-open
```

Expected:
- ✅ Dashboard generates
- ✅ Weather shows REAL temperature
- ✅ Videos show REAL YouTube results
- ✅ Events show REAL Ticketmaster events

**Step 4: Test error handling**

Remove one API key from `.env` and run:

```bash
python -m fabric_dashboard generate --no-mock --no-open
```

Expected:
- ✅ Dashboard still generates
- ⚠️ Warning logged for missing API key
- ✅ Component falls back to mock data

**Step 5: Run full test suite**

```bash
python -m pytest fabric_dashboard/tests/ -v
```

Expected: All tests pass

---

## Task 12: Update Documentation

**Files:**
- Modify: `UI_GENERATOR_STATUS.md`
- Modify: `README.md`

**Step 1: Update UI_GENERATOR_STATUS.md**

Mark Phase 3 as complete:

```markdown
### Phase 3: API Enrichment ✅ **COMPLETE**

**Implemented:**
- [x] New `api/` abstraction layer with Protocols
- [x] Weather enrichment (OpenWeatherMap with geocoding)
- [x] Video enrichment (YouTube Data API v3)
- [x] Events enrichment (Ticketmaster Discovery API)
- [x] Geocoding API (Mapbox forward geocoding)
- [x] Parallel async enrichment with error handling
- [x] Dashboard rendering updated for enriched data
- [x] Configuration support for API keys
- [x] Graceful fallback to mock data on errors

**Architecture:**
- Used simplified Protocol-based abstraction
- Dependency injection in UIGenerator
- Testable, swappable implementations
```

**Step 2: Update MVP completion**

```markdown
## 🎯 MVP Success Criteria

| Criterion | Status |
|-----------|--------|
| Component selection works | ✅ DONE |
| All 6 types generate | ✅ DONE |
| API enrichment works | ✅ DONE |
| Components in output | ✅ DONE |
| Frontend renders | ✅ DONE |
| Real data demo | ✅ DONE |

**MVP Completion**: **6/6** (100%)
```

**Step 3: Add API setup to README.md**

Add new section:

```markdown
## External API Setup (Optional)

UI components can be enriched with real-time data from external APIs:

### Weather Widgets (OpenWeatherMap)
1. Sign up: https://openweathermap.org/api
2. Get free API key (1,000 calls/day)
3. Add to `.env`: `OPENWEATHERMAP_API_KEY=your_key`

### Video Feeds (YouTube Data API v3)
1. Enable API: https://console.cloud.google.com/apis/library/youtube.googleapis.com
2. Create credentials (10,000 units/day = ~100 searches)
3. Add to `.env`: `YOUTUBE_API_KEY=your_key`

### Event Calendars (Ticketmaster)
1. Sign up: https://developer.ticketmaster.com/
2. Get free API key (5,000 requests/day)
3. Add to `.env`: `TICKETMASTER_API_KEY=your_key`

### Maps & Geocoding (Mapbox)
1. Sign up: https://account.mapbox.com/
2. Get token (100K requests/month free)
3. Add to `.env`: `MAPBOX_API_KEY=your_token`

**Note**: All APIs work in mock mode without keys. Real data requires API keys.
```

**Step 4: Commit documentation**

```bash
git add UI_GENERATOR_STATUS.md README.md
git commit -m "docs: update Phase 3 completion and API setup guide"
```

---

## Success Criteria

✅ **Phase 3 complete when:**
- [ ] All 4 API modules created in `api/` folder
- [ ] UIGenerator uses dependency injection
- [ ] Weather enrichment uses geocoding + coordinates
- [ ] YouTube API includes `part` parameter
- [ ] Ticketmaster replaces Eventbrite
- [ ] Dashboard renders enriched data (not just placeholders)
- [ ] Mock mode still works for testing
- [ ] Configuration supports all API keys
- [ ] End-to-end test passes with mock data
- [ ] Documentation updated

---

## Estimated Time

- **Task 1** (Base utilities): 10 minutes
- **Task 2** (Geocoding): 15 minutes
- **Task 3** (Weather): 20 minutes
- **Task 4** (Videos): 15 minutes
- **Task 5** (Events/Ticketmaster): 20 minutes
- **Task 6** (Package exports): 5 minutes
- **Task 7** (UIGenerator refactor): 30 minutes
- **Task 8** (Configuration): 10 minutes
- **Task 9** (Dashboard builder): 20 minutes
- **Task 10** (Cleanup): 5 minutes
- **Task 11** (Testing): 30 minutes
- **Task 12** (Documentation): 15 minutes

**Total: ~3-3.5 hours**

---

## Notes

- Protocol-based abstraction = lightweight, no ABC overhead
- All APIs support mock mode for development
- Geocoding happens before weather calls (coordinates required)
- Ticketmaster has better coverage and docs than deprecated Eventbrite
- Error handling ensures components always render (graceful degradation)
- Dependency injection makes testing easy (mock the APIs)
- Parallel enrichment (`asyncio.gather`) improves performance
