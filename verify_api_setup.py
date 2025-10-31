#!/usr/bin/env python3
"""Verification script for OnFabric API integration.

This script tests the API client setup and connectivity.
Run this after setting up your .env file with ONFABRIC_BEARER_TOKEN.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from fabric_dashboard.api.onfabric_client import OnFabricAPIClient
from fabric_dashboard.core.data_fetcher import DataFetcher
from fabric_dashboard.utils import logger


def verify_api_client():
    """Test OnFabricAPIClient initialization and methods."""
    logger.info("🔍 Verifying OnFabric API client setup...")

    try:
        # Test 1: Initialize client
        logger.info("Test 1: Initializing API client...")
        client = OnFabricAPIClient()
        logger.success(f"✓ Client initialized with tapestry: {client.tapestry_id}")

        # Test 2: Get tapestries
        logger.info("Test 2: Fetching tapestries...")
        tapestries = client.get_tapestries()
        logger.success(f"✓ Found {len(tapestries)} tapestry/tapestries")

        # Test 3: Get threads
        logger.info("Test 3: Fetching threads...")
        threads = client.get_threads(client.tapestry_id)
        logger.success(f"✓ Fetched {len(threads)} thread(s)")

        # Test 4: Get summaries
        logger.info("Test 4: Fetching summaries...")
        summaries = client.get_summaries(client.tapestry_id)
        logger.success(f"✓ Fetched {len(summaries)} summary/summaries")

        return True

    except ValueError as e:
        logger.error(f"✗ Configuration error: {e}")
        logger.info("\n📝 Setup instructions:")
        logger.info("1. Copy .env.example to .env")
        logger.info("2. Get your bearer token from https://app.onfabric.io")
        logger.info("   - Open DevTools (F12) → Network tab")
        logger.info("   - Navigate around the app")
        logger.info("   - Find an API request, copy the Authorization header")
        logger.info("3. Add token to .env: ONFABRIC_BEARER_TOKEN=your_token_here")
        logger.info("4. (Optional) Add tapestry ID: ONFABRIC_TAPESTRY_ID=your_id")
        return False

    except Exception as e:
        logger.error(f"✗ API error: {e}")
        return False


def verify_data_fetcher():
    """Test DataFetcher with API client."""
    logger.info("\n🔍 Verifying DataFetcher integration...")

    try:
        logger.info("Test 5: Fetching user data via DataFetcher...")
        fetcher = DataFetcher(mock_mode=False)
        user_data = fetcher.fetch_user_data(days_back=30)

        if user_data:
            logger.success(f"✓ Fetched {user_data.summary.total_interactions} interactions")
            logger.info(f"  Date range: {user_data.summary.date_range_start.date()} to {user_data.summary.date_range_end.date()}")
            logger.info(f"  Platforms: {', '.join(user_data.summary.platforms)}")
            return True
        else:
            logger.error("✗ DataFetcher returned None")
            return False

    except Exception as e:
        logger.error(f"✗ DataFetcher error: {e}")
        return False


def main():
    """Run all verification tests."""
    logger.info("=" * 60)
    logger.info("OnFabric API Integration Verification")
    logger.info("=" * 60)

    # Test API client
    api_ok = verify_api_client()

    if not api_ok:
        logger.error("\n❌ API client verification failed. Fix issues above and retry.")
        sys.exit(1)

    # Test DataFetcher
    fetcher_ok = verify_data_fetcher()

    if not fetcher_ok:
        logger.error("\n❌ DataFetcher verification failed.")
        sys.exit(1)

    # Success!
    logger.info("\n" + "=" * 60)
    logger.success("✅ All verification tests passed!")
    logger.info("=" * 60)
    logger.info("\n🎉 OnFabric API integration is working correctly.")
    logger.info("You can now generate dashboards with real data using:")
    logger.info("  python -m fabric_dashboard.cli generate")


if __name__ == "__main__":
    main()
