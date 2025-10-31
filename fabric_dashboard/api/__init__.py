"""External API abstractions for UI enrichment."""

from fabric_dashboard.api.weather import WeatherAPI, OpenWeatherAPI
from fabric_dashboard.api.videos import VideoAPI, YouTubeAPI
from fabric_dashboard.api.events import EventsAPI, TicketmasterAPI
from fabric_dashboard.api.geocoding import GeocodingAPI, MapboxAPI
from fabric_dashboard.api.onfabric_client import OnFabricAPIClient

__all__ = [
    "WeatherAPI",
    "OpenWeatherAPI",
    "VideoAPI",
    "YouTubeAPI",
    "EventsAPI",
    "TicketmasterAPI",
    "GeocodingAPI",
    "MapboxAPI",
    "OnFabricAPIClient",
]
