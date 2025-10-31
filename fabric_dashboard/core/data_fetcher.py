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
            # Use threads for detailed, granular user behavior data
            # To use summaries instead: self._fetch_from_api_summaries(days_back)
            return self._fetch_from_api_threads(days_back)

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

    def _fetch_from_api_summaries(self, days_back: int) -> Optional[UserData]:
        """
        Fetch user data from OnFabric API using summaries only.
        Summaries contain rich, pre-analyzed weekly behavioral insights from multiple providers.

        Args:
            days_back: Number of days of data to fetch.

        Returns:
            UserData model or None if fetch fails.
        """
        if not self.api_client:
            logger.error("API client not initialized")
            return None

        logger.info(f"Fetching summaries from OnFabric API (last {days_back} days, ~{days_back//7} weeks)")

        try:
            tapestry_id = self.api_client.tapestry_id

            # Fetch summaries from multiple providers
            # Fetch more summaries to cover 2 months (page_size=20 for ~8 weeks)
            providers = ["google", "pinterest", "instagram"]
            all_summaries = []

            for provider in providers:
                try:
                    summaries = self.api_client.get_summaries(tapestry_id, provider=provider, page_size=20)
                    if summaries:
                        all_summaries.extend(summaries)
                        logger.muted(f"Retrieved {len(summaries)} {provider} summaries")
                except Exception as e:
                    logger.warning(f"Failed to fetch {provider} summaries: {e}")

            logger.info(f"Retrieved {len(all_summaries)} total summaries from {len(providers)} providers")

            # Build raw_data dict with summaries only
            raw_data = {
                "summaries": all_summaries,
                "tapestry_id": tapestry_id
            }

            # Transform to UserData model
            return self._transform_api_data(raw_data, days_back)

        except Exception as e:
            logger.error(f"Failed to fetch summaries from OnFabric API: {e}")
            return None

    def _fetch_from_api_threads(self, days_back: int) -> Optional[UserData]:
        """
        Fetch user data from OnFabric API using threads (individual interactions).
        Threads contain granular, detailed user behavior data for rich pattern detection.

        Args:
            days_back: Number of days of data to fetch.

        Returns:
            UserData model or None if fetch fails.
        """
        if not self.api_client:
            logger.error("API client not initialized")
            return None

        logger.info(f"Fetching threads from OnFabric API (last {days_back} days)")

        try:
            tapestry_id = self.api_client.tapestry_id

            # Fetch threads from multiple providers
            # Instagram gets more threads for richer historical data
            provider_configs = [
                ("google", 50),
                ("pinterest", 50),
                ("instagram", 100),  # Fetch more Instagram threads for deeper history
            ]
            all_threads = []

            for provider, page_size in provider_configs:
                try:
                    threads = self.api_client.get_threads(tapestry_id, provider=provider, page_size=page_size)
                    if threads:
                        all_threads.extend(threads)
                        logger.muted(f"Retrieved {len(threads)} {provider} threads")
                except Exception as e:
                    logger.warning(f"Failed to fetch {provider} threads: {e}")

            logger.info(f"Retrieved {len(all_threads)} total threads from {len(provider_configs)} providers")

            # Build raw_data dict with threads
            raw_data = {
                "threads": all_threads,
                "tapestry_id": tapestry_id
            }

            # Transform to UserData model using thread transformation logic
            return self._transform_thread_data(raw_data, days_back)

        except Exception as e:
            logger.error(f"Failed to fetch threads from OnFabric API: {e}")
            return None

    def _parse_thread_date(self, date_str: str) -> datetime:
        """Parse thread date string and ensure timezone-aware."""
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt

    def _transform_thread_data(self, raw_data: dict[str, Any], days_back: int) -> Optional[UserData]:
        """
        Transform raw thread data from API into UserData model.
        Threads contain individual granular interactions with 'asat' timestamp.

        Args:
            raw_data: Raw response from API with threads.
            days_back: Number of days to filter data.

        Returns:
            UserData model or None if transformation fails.
        """
        try:
            threads = raw_data.get("threads", [])

            # Filter threads by date
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_back)
            filtered_threads = []
            dates = []

            for thread in threads:
                # Threads have 'asat' timestamp
                asat_str = thread.get("asat")

                if asat_str:
                    asat = self._parse_thread_date(asat_str)

                    # Include thread if within date range
                    if asat >= cutoff_date:
                        filtered_threads.append(thread)
                        dates.append(asat)

            # Extract date range from collected dates
            if dates:
                date_range_start = min(dates)
                date_range_end = max(dates)
                days_analyzed = (date_range_end - date_range_start).days + 1
            else:
                date_range_start = datetime.now(timezone.utc)
                date_range_end = datetime.now(timezone.utc)
                days_analyzed = 1

            # Extract providers from threads
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
                f"Transformed {len(filtered_threads)} threads from "
                f"{len(providers)} provider(s)"
            )
            return user_data

        except Exception as e:
            logger.error(f"Failed to transform thread data: {e}")
            return None

    def _transform_api_data(self, raw_data: dict[str, Any], days_back: int) -> Optional[UserData]:
        """
        Transform raw API response into UserData model.
        Uses summaries (pre-analyzed weekly insights) instead of raw threads for richer persona detection.

        Args:
            raw_data: Raw response from API with threads and summaries.
            days_back: Number of days to filter data.

        Returns:
            UserData model or None if transformation fails.
        """
        try:
            summaries = raw_data.get("summaries", [])

            # Use summaries as interactions - they contain rich, pre-analyzed behavioral insights
            # Each summary covers a week of activity with AI-generated analysis
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_back)
            filtered_summaries = []
            dates = []

            for summary in summaries:
                # Summaries have from_date and to_date instead of asat
                from_date_str = summary.get("from_date")
                to_date_str = summary.get("to_date")

                if from_date_str and to_date_str:
                    from_date = self._parse_thread_date(from_date_str)
                    to_date = self._parse_thread_date(to_date_str)

                    # Include summary if it overlaps with our date range
                    if to_date >= cutoff_date:
                        filtered_summaries.append(summary)
                        dates.append(from_date)
                        dates.append(to_date)

            # Extract date range from collected dates
            if dates:
                date_range_start = min(dates)
                date_range_end = max(dates)
                days_analyzed = (date_range_end - date_range_start).days + 1
            else:
                date_range_start = datetime.now(timezone.utc)
                date_range_end = datetime.now(timezone.utc)
                days_analyzed = 1

            # Extract providers from summaries
            providers = list(set(s.get("provider", "unknown") for s in filtered_summaries))

            # Build summary
            summary = DataSummary(
                total_interactions=len(filtered_summaries),
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
                interactions=filtered_summaries,
                summary=summary,
                persona=persona,
            )

            logger.success(
                f"Transformed {len(filtered_summaries)} summaries from "
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
