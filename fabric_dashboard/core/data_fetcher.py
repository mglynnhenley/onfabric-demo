"""Data fetching module for Fabric Dashboard."""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from fabric_dashboard.mcp.onfabric import FabricMCPClient
from fabric_dashboard.models.schemas import DataSummary, PersonaProfile, UserData
from fabric_dashboard.utils import logger


class DataFetcher:
    """Fetches user data from Fabric MCP or mock fixtures."""

    def __init__(self, mock_mode: bool = False):
        """
        Initialize data fetcher.

        Args:
            mock_mode: If True, load from mock fixtures instead of real MCP.
        """
        self.mock_mode = mock_mode
        self.mcp_client: Optional[FabricMCPClient] = None

        if not mock_mode:
            self.mcp_client = FabricMCPClient()

    def fetch_user_data(self, days_back: int = 30) -> Optional[UserData]:
        """
        Fetch user data either from MCP or mock fixtures.

        Args:
            days_back: Number of days of historical data to fetch.

        Returns:
            UserData model or None if fetch fails.
        """
        if self.mock_mode:
            return self._load_mock_data()
        else:
            return self._fetch_from_mcp(days_back)

    def _load_mock_data(self) -> Optional[UserData]:
        """
        Load user data from mock JSON fixture.

        Returns:
            UserData model or None if load fails.
        """
        logger.info("Loading mock user data from fixtures")

        fixture_path = Path(__file__).parent.parent / "tests" / "fixtures" / "mock_user_data.json"

        if not fixture_path.exists():
            logger.error(f"Mock data file not found: {fixture_path}")
            return None

        try:
            with open(fixture_path) as f:
                raw_data = json.load(f)

            # Extract persona profile
            persona_data = raw_data.get("persona", {})
            persona = PersonaProfile(
                writing_style=persona_data.get(
                    "writing_style",
                    "analytical yet accessible",
                ),
                interests=persona_data.get("interests", []),
                activity_level=persona_data.get("activity_level", "moderate"),
                professional_context=persona_data.get("professional_context"),
                tone_preference=persona_data.get("tone_preference", "balanced and approachable"),
                age_range=persona_data.get("age_range"),
                content_depth_preference=persona_data.get("content_depth_preference", "balanced"),
            )

            # Extract summary data
            summary_data = raw_data.get("summary", {})
            summary = DataSummary(
                total_interactions=summary_data.get("total_interactions", 0),
                date_range_start=datetime.fromisoformat(
                    summary_data.get("date_range_start", datetime.now(timezone.utc).isoformat()).replace("Z", "+00:00")
                ),
                date_range_end=datetime.fromisoformat(
                    summary_data.get("date_range_end", datetime.now(timezone.utc).isoformat()).replace("Z", "+00:00")
                ),
                days_analyzed=summary_data.get("days_analyzed", 1),
                platforms=summary_data.get("platforms", []),
                top_themes=summary_data.get("top_themes", []),
            )

            # Get interactions as-is (they're already dicts)
            interactions = raw_data.get("interactions", [])

            # Build UserData
            user_data = UserData(
                connection_id=raw_data.get("connection_id", "mock_connection"),
                interactions=interactions,
                summary=summary,
                persona=persona,
            )

            logger.success(f"Loaded {len(interactions)} interactions from mock data")
            return user_data

        except Exception as e:
            logger.error(f"Failed to load mock data: {e}")
            return None

    def _fetch_from_mcp(self, days_back: int) -> Optional[UserData]:
        """
        Fetch user data from Fabric MCP.

        Args:
            days_back: Number of days of data to fetch.

        Returns:
            UserData model or None if fetch fails.
        """
        if not self.mcp_client:
            logger.error("MCP client not initialized")
            return None

        logger.info(f"Fetching user data from Fabric MCP (last {days_back} days)")

        try:
            with self.mcp_client as client:
                raw_data = client.fetch_user_data(days_back=days_back)

                # Transform MCP response into UserData model
                # TODO: Implement actual transformation once MCP integration is complete
                # For now, this will raise NotImplementedError from the MCP client
                return self._transform_mcp_data(raw_data)

        except NotImplementedError:
            logger.warning("MCP integration not yet implemented, falling back to mock data")
            return self._load_mock_data()
        except Exception as e:
            logger.error(f"Failed to fetch data from MCP: {e}")
            return None

    def _transform_mcp_data(self, raw_data: dict[str, Any]) -> Optional[UserData]:
        """
        Transform raw MCP response into UserData model.

        Args:
            raw_data: Raw response from MCP.

        Returns:
            UserData model or None if transformation fails.
        """
        try:
            # This will be implemented once we know the exact MCP response format
            # For now, assume similar structure to mock data
            interactions = raw_data.get("threads", [])

            # Build persona from available data
            persona = PersonaProfile(
                writing_style="balanced and informative",
                interests=[],
                activity_level="moderate",
            )

            # Build summary
            to_date = datetime.now(timezone.utc)
            from_date = raw_data.get("date_range", {}).get("from", to_date.isoformat())

            summary = DataSummary(
                total_interactions=raw_data.get("total_threads", 0),
                date_range_start=datetime.fromisoformat(from_date.replace("Z", "+00:00")),
                date_range_end=to_date,
                days_analyzed=30,
                platforms=[],
                top_themes=[],
            )

            user_data = UserData(
                connection_id=raw_data.get("connection_id", "unknown"),
                interactions=interactions,
                summary=summary,
                persona=persona,
            )

            logger.success(f"Transformed {len(interactions)} interactions from MCP")
            return user_data

        except Exception as e:
            logger.error(f"Failed to transform MCP data: {e}")
            return None

    def __enter__(self) -> "DataFetcher":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if self.mcp_client and not self.mock_mode:
            self.mcp_client.disconnect()
