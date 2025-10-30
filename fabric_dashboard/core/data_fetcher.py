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

    def _load_mock_data(self) -> Optional[UserData]:
        """
        Load user data from mock JSON fixture (OnFabric format).

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

            # OnFabric format: {"items": [...]}
            items = raw_data.get("items", [])

            if not items:
                logger.warning("No items found in mock data")
                return None

            # Generate summary from items
            total_interactions = len(items)
            providers = list(set(item.get("provider", "unknown") for item in items))

            # Extract date range from 'asat' field
            dates = [item.get("asat") for item in items if item.get("asat")]
            if dates:
                dates_parsed = [datetime.fromisoformat(d.replace("Z", "+00:00")) for d in dates]
                date_range_start = min(dates_parsed)
                date_range_end = max(dates_parsed)
                days_analyzed = (date_range_end - date_range_start).days + 1
            else:
                date_range_start = datetime.now(timezone.utc)
                date_range_end = datetime.now(timezone.utc)
                days_analyzed = 1

            summary = DataSummary(
                total_interactions=total_interactions,
                date_range_start=date_range_start,
                date_range_end=date_range_end,
                days_analyzed=days_analyzed,
                platforms=providers,
                top_themes=[],  # Will be populated by PatternDetector
            )

            # Create default persona (will be refined by PatternDetector)
            persona = PersonaProfile(
                writing_style="analytical yet accessible",
                interests=["general"],  # Will be populated by PatternDetector
                activity_level="moderate",
                professional_context=None,
                tone_preference="balanced and approachable",
                age_range=None,
                content_depth_preference="balanced",
            )

            # Build UserData with OnFabric items as-is
            user_data = UserData(
                connection_id=raw_data.get("provider_connection_id", items[0].get("provider_connection_id", "mock_connection")) if items else "mock_connection",
                interactions=items,  # OnFabric items with their original structure
                summary=summary,
                persona=persona,
            )

            logger.success(f"Loaded {total_interactions} OnFabric interactions from {len(providers)} provider(s)")
            return user_data

        except Exception as e:
            logger.error(f"Failed to load mock data: {e}")
            return None

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
                    # Parse date and make timezone-aware if needed
                    thread_date = datetime.fromisoformat(thread_date_str.replace("Z", "+00:00"))
                    if thread_date.tzinfo is None:
                        thread_date = thread_date.replace(tzinfo=timezone.utc)
                    if thread_date >= cutoff_date:
                        filtered_threads.append(thread)

            # Extract date range from filtered threads
            if filtered_threads:
                dates = []
                for t in filtered_threads:
                    if t.get("asat"):
                        dt = datetime.fromisoformat(t["asat"].replace("Z", "+00:00"))
                        if dt.tzinfo is None:
                            dt = dt.replace(tzinfo=timezone.utc)
                        dates.append(dt)

                if dates:
                    date_range_start = min(dates)
                    date_range_end = max(dates)
                    days_analyzed = (date_range_end - date_range_start).days + 1
                else:
                    date_range_start = datetime.now(timezone.utc)
                    date_range_end = datetime.now(timezone.utc)
                    days_analyzed = 1
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
