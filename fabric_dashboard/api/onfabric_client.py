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
