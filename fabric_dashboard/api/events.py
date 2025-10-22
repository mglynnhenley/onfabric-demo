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
