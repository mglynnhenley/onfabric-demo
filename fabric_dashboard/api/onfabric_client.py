"""OnFabric API client."""

import os
from typing import Any

import requests
from dotenv import load_dotenv

from fabric_dashboard.utils import logger


class OnFabricAPIClient:
    """Simple HTTP client for OnFabric API."""

    bearer_token: str
    tapestry_id: str | None
    base_url: str
    session: requests.Session

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
                    f"Found multiple tapestries ({len(tapestries)}), using first one. "
                    "Set ONFABRIC_TAPESTRY_ID in .env to specify."
                )

            self.tapestry_id = tapestries[0]["id"]
            logger.info(f"Using tapestry: {self.tapestry_id}")

        logger.info("OnFabric API client initialized")

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
