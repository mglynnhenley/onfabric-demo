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
