"""
Pytest configuration and shared fixtures for fabric_dashboard tests.

Provides:
- Mock data fixtures
- Test configuration
- Common test utilities
"""

import os
import json
from pathlib import Path
import pytest


@pytest.fixture
def fixtures_dir():
    """Return path to test fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def mock_user_data(fixtures_dir):
    """Load mock user interaction data."""
    with open(fixtures_dir / "raw_data" / "user_interactions_mixed.json") as f:
        return json.load(f)


@pytest.fixture
def mock_google_data(fixtures_dir):
    """Load mock Google interaction data."""
    with open(fixtures_dir / "raw_data" / "google_interactions.json") as f:
        return json.load(f)


@pytest.fixture
def mock_patterns(fixtures_dir):
    """Load mock extracted patterns."""
    with open(fixtures_dir / "patterns" / "extracted_patterns.json") as f:
        return json.load(f)


@pytest.fixture
def mock_search_results(fixtures_dir):
    """Load mock search/enrichment results."""
    with open(fixtures_dir / "enrichment" / "search_results.json") as f:
        return json.load(f)


@pytest.fixture
def demo_persona(fixtures_dir):
    """Load demo persona for end-to-end tests."""
    with open(fixtures_dir / "personas" / "demo.json") as f:
        return json.load(f)


@pytest.fixture
def demo2_persona(fixtures_dir):
    """Load demo2 (fashion producer) persona for end-to-end tests."""
    with open(fixtures_dir / "personas" / "demo2.json") as f:
        return json.load(f)


@pytest.fixture
def mock_mode():
    """Check if tests should run in mock mode (default: True)."""
    return os.getenv("MOCK_MODE", "true").lower() == "true"


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "use_real_data: mark test to run with real API data"
    )


def pytest_collection_modifyitems(config, items):
    """Skip tests marked with use_real_data when in mock mode."""
    mock_mode = os.getenv("MOCK_MODE", "true").lower() == "true"

    if mock_mode:
        skip_real_data = pytest.mark.skip(reason="Skipped in mock mode")
        for item in items:
            if "use_real_data" in item.keywords:
                item.add_marker(skip_real_data)
