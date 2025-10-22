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
