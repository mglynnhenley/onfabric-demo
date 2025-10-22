# Fabric Intelligence Dashboard

Generate personalized, AI-powered intelligence dashboards from your digital behavior.

## Overview

Fabric Intelligence Dashboard is a beautiful, design-first CLI tool that analyzes your digital activity from Fabric MCP and creates personalized content using Claude and Perplexity AI. It detects patterns in your behavior, generates persona-matched color schemes, and produces rich, insightful dashboard content.

## Features

- **Automated Pattern Detection**: Analyzes your digital behavior to identify interests, trends, and habits
- **Persona-Aware Theming**: Generates custom color schemes that match your personality and usage patterns
- **Live Search Enrichment**: Enhances insights with real-time research from Perplexity AI
- **Personalized Content**: Creates engaging, relevant content written specifically for you
- **Beautiful Design**: Modern, responsive HTML dashboards with Tailwind CSS
- **CLI-First**: Simple, intuitive command-line interface with rich progress indicators

## Architecture

### Pipeline

1. **Data Fetching** (`DataFetcher`): Retrieves user activity from Fabric MCP
2. **Pattern Detection** (`PatternDetector`): Analyzes data to identify behavioral patterns
3. **Theme Generation** (`ThemeGenerator`): Creates persona-matched color schemes
4. **Search Enrichment** (`SearchEnricher`): Enriches patterns with live research from Perplexity
5. **Content Writing** (`ContentWriter`): Generates personalized card content using Claude
6. **Dashboard Building** (`DashboardBuilder`): Assembles final HTML dashboard

### Tech Stack

- **LLMs**: Claude (Anthropic) for pattern detection, theme generation, and content writing
- **Search**: Perplexity AI for real-time research enrichment
- **Framework**: LangChain for LLM orchestration
- **Data**: Fabric MCP for user activity data
- **Validation**: Pydantic v2 for data models
- **CLI**: Click + Rich for beautiful terminal UI
- **Caching**: DiskCache with TTL for API response caching
- **Styling**: Tailwind CSS via CDN

## Installation

### Prerequisites

- Python 3.11+
- `uv` package manager (recommended) or `pip`
- Anthropic API key (for Claude)
- Perplexity API key (for search)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/onfabric/fabric-dashboard.git
   cd fabric-dashboard
   ```

2. **Create virtual environment**
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   uv pip install -e .
   # Or with pip:
   pip install -e .
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys:
   # ANTHROPIC_API_KEY=your_key_here
   # PERPLEXITY_API_KEY=your_key_here
   ```

## External API Setup (Optional)

UI components can be enriched with real-time data from external APIs. **All APIs work in mock mode without keys** - real API keys are only needed for live data.

### Weather Widgets (OpenWeatherMap)
- **Free Tier**: 1,000 calls/day
- **Sign up**: https://openweathermap.org/api
- **Get key**: https://home.openweathermap.org/api_keys
- **Add to `.env`**: `OPENWEATHERMAP_API_KEY=your_key`

### Video Feeds (YouTube Data API v3)
- **Free Tier**: 10,000 units/day (~100 searches)
- **Enable API**: https://console.cloud.google.com/apis/library/youtube.googleapis.com
- **Get key**: https://console.cloud.google.com/apis/credentials
- **Add to `.env`**: `YOUTUBE_API_KEY=your_key`

### Event Calendars (Ticketmaster)
- **Free Tier**: 5,000 requests/day
- **Sign up**: https://developer.ticketmaster.com/products-and-docs/apis/getting-started/
- **Get key**: https://developer-acct.ticketmaster.com/user/register
- **Add to `.env`**: `TICKETMASTER_API_KEY=your_key`

### Maps & Geocoding (Mapbox)
- **Free Tier**: 100,000 requests/month for geocoding
- **Sign up**: https://account.mapbox.com/
- **Get token**: https://account.mapbox.com/access-tokens/
- **Add to `.env`**: `MAPBOX_API_KEY=your_token`

**Note**: Components display mock data when API keys are not configured. This is perfect for development and testing.

## Usage

### Generate Dashboard

```bash
# Generate with real data
fabric-dashboard generate

# Use mock data for testing
fabric-dashboard generate --mock

# Skip search enrichment
fabric-dashboard generate --no-search

# Analyze last 60 days
fabric-dashboard generate --days-back 60

# Custom output directory
fabric-dashboard generate --output ./my-dashboards

# Debug mode
fabric-dashboard generate --debug

# Don't auto-open in browser
fabric-dashboard generate --no-open
```

### Initialize Configuration

```bash
fabric-dashboard init
```

## Development

### Install Development Dependencies

```bash
uv pip install -e ".[dev]"
```

### Run Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest fabric_dashboard/tests/test_pattern_detector.py

# Run with coverage
pytest --cov=fabric_dashboard --cov-report=html

# Run only fast tests (skip slow integration tests)
pytest -m "not slow"
```

### Code Quality

```bash
# Format code with black
black fabric_dashboard/

# Lint with ruff
ruff check fabric_dashboard/

# Type check with mypy
mypy fabric_dashboard/
```

## Project Structure

```
fabric_dashboard/
├── cli.py                  # CLI entry point
├── __init__.py             # Package metadata
├── commands/               # CLI commands
│   ├── generate.py         # Generate dashboard command
│   └── init.py             # Initialize config command
├── core/                   # Core pipeline modules
│   ├── data_fetcher.py     # Fetch user data from Fabric MCP
│   ├── pattern_detector.py # Detect behavioral patterns
│   ├── theme_generator.py  # Generate color schemes
│   ├── search_enricher.py  # Enrich with Perplexity search
│   ├── content_writer.py   # Write personalized content
│   └── dashboard_builder.py # Build HTML dashboard
├── mcp/                    # Fabric MCP client
│   ├── client.py           # MCP base client
│   └── onfabric.py         # OnFabric MCP wrapper
├── models/                 # Data models
│   └── schemas.py          # Pydantic schemas
├── utils/                  # Utilities
│   ├── config.py           # Configuration management
│   ├── logger.py           # Logging utilities
│   ├── cache.py            # Caching utilities
│   └── files.py            # File utilities
└── tests/                  # Test suite
    ├── fixtures/           # Test fixtures
    └── test_*.py           # Test modules
```

## Configuration

Configuration is managed through environment variables (`.env` file) and a YAML config file (`.fabric-dashboard/config.yaml`).

### Environment Variables

- `ANTHROPIC_API_KEY`: Claude API key (required)
- `PERPLEXITY_API_KEY`: Perplexity API key (required for search enrichment)
- `DAYS_BACK`: Number of days of data to analyze (default: 30)
- `DEBUG`: Enable debug mode (default: false)

### Config File

The config file (`.fabric-dashboard/config.yaml`) is created by `fabric-dashboard init` and stores:
- User preferences
- Theme settings
- Cache settings
- API rate limits

## Card Sizes

Dashboards contain cards with different size tiers:

- **COMPACT**: 80-180 words - Quick insights and highlights
- **SMALL**: 120-240 words - Focused analysis on specific topics
- **MEDIUM**: 200-360 words - In-depth exploration of patterns
- **LARGE**: 320-600 words - Comprehensive deep-dives

## License

MIT

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.
