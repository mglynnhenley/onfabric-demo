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
