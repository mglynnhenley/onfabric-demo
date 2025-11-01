# OnFabric MVP Architecture

Detailed technical documentation for the personalized dashboard generation system.

## Table of Contents

- [System Overview](#system-overview)
- [Data Pipeline](#data-pipeline)
- [Widget System](#widget-system)
- [Theme System](#theme-system)
- [API Integration](#api-integration)

## System Overview

The OnFabric MVP generates personalized dashboards by analyzing user interaction patterns and dynamically constructing UI components that match user interests and aesthetics.

### High-Level Flow

```
┌─────────────────┐
│  User Data      │
│  (OnFabric API) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Pattern         │
│ Extraction      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Content         │
│ Enrichment      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Dashboard       │
│ Generation      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Frontend        │
│ Rendering       │
└─────────────────┘
```

## Data Pipeline

### 1. Data Collection

**Module**: `fabric_dashboard/core/data_fetcher.py`

Fetches user interaction data from OnFabric API or mock fixtures:

- **Mock Mode**: Loads `tests/fixtures/raw_data/user_interactions_mixed.json`
- **Real Mode**: Queries OnFabric API with user credentials

**Data Format**:
```json
{
  "id": "uuid",
  "provider": "instagram|google|pinterest",
  "interaction_type": "posts_viewed|videos_watched|searches",
  "content": "Human-readable description",
  "details": { /* provider-specific data */ },
  "asat": "2025-10-31T12:00:00Z"
}
```

### 2. Pattern Extraction

**Module**: `fabric_dashboard/core/pattern_analyzer.py`

Analyzes interaction data to extract:

- **Topics**: Recurring themes from user activity
- **Confidence**: Statistical confidence in each pattern
- **Keywords**: Representative terms for each topic
- **Time Range**: When user engaged with this topic

**Output Schema**:
```python
{
  "title": "Pattern name",
  "description": "What this pattern represents",
  "confidence": 0.0-1.0,
  "keywords": ["term1", "term2"],
  "interaction_count": int,
  "suggested_card_size": "small|medium|large"
}
```

### 3. Content Enrichment

**Module**: `fabric_dashboard/core/enrichment.py`

Queries external APIs to provide real-time content:

- **Search API**: Find recent articles matching user interests
- **Weather API**: Location-based weather for travel patterns
- **News API**: Current events related to user topics

### 4. Dashboard Generation

**Module**: `fabric_dashboard/core/dashboard_builder.py`

Generates complete dashboard configuration:

```python
{
  "theme": {
    "primary_color": "#hex",
    "accent_color": "#hex",
    "background_type": "gradient|solid|pattern",
    "typography": {"heading": "font", "body": "font"}
  },
  "cards": [
    {
      "id": "uuid",
      "widget_type": "article|calendar|info|map",
      "size": "small|medium|large",
      "content": { /* widget-specific data */ }
    }
  ],
  "layout": "grid|masonry|pin-board"
}
```

## Widget System

### Available Widgets

**ArticleCard** - Content recommendations
- Size: medium, large
- Content: Title, summary, image, link
- Use: Display articles matching user interests

**CalendarCard** - Upcoming events
- Size: small, medium
- Content: Event list with dates/times
- Use: Schedule awareness for users with calendar patterns

**InfoCard** - Key information blocks
- Size: small, medium
- Content: Title, description, icon
- Use: Quick facts or statistics

**MapCard** - Location-based content
- Size: large
- Content: Map with markers, location info
- Use: Travel patterns, location-based interests

### Widget Selection Logic

1. **Pattern Analysis**: Identify dominant user interests
2. **Size Assignment**: Based on pattern confidence and interaction count
3. **Content Matching**: Query enrichment APIs for relevant content
4. **Layout Optimization**: Arrange widgets for visual balance

## Theme System

### Theme Generation

Themes are generated based on:

- **User aesthetics**: Analyzed from saved content, followed accounts
- **Time of day**: Darker themes for evening usage patterns
- **Content type**: Professional topics → minimal themes, creative topics → vibrant themes

### Theme Components

**Colors**:
- Primary: Dominant brand/accent color
- Accent: Highlight color for CTAs
- Background: Gradient or solid based on user aesthetic

**Typography**:
- Heading font: Distinctive, matches user aesthetic
- Body font: Readable, complements heading

**Backgrounds**:
- CSS gradients for depth
- Geometric patterns for interest
- Solid colors for minimalism

### Customization

Users can override theme in frontend:
```typescript
<ThemeProvider theme={customTheme}>
  <Dashboard />
</ThemeProvider>
```

## API Integration

### OnFabric API

**Base URL**: `https://api.onfabric.com`

**Authentication**: Bearer token

**Endpoints**:
- `GET /users/{id}/interactions` - User interaction data
- `GET /users/{id}/patterns` - Pre-analyzed patterns (if available)

**Rate Limits**: 100 requests/minute

### Mock Mode

When `MOCK_MODE=true`:
- No API calls made
- Data loaded from `tests/fixtures/personas/demo.json`
- Simulates full pipeline with realistic data
- Useful for development and demos

### Error Handling

- **API failures**: Graceful degradation, use cached data
- **Missing data**: Generate dashboard from partial patterns
- **Rate limits**: Exponential backoff retry logic

## Testing

### Test Structure

```
fabric_dashboard/tests/
├── conftest.py           # Shared fixtures
├── fixtures/             # Mock data
│   ├── raw_data/         # OnFabric interaction data
│   ├── enrichment/       # API responses
│   ├── patterns/         # Analyzed patterns
│   ├── personas/         # Complete personas
│   └── api_examples/     # API format docs
├── test_schemas.py       # Data model validation
├── test_data_fetcher.py  # API integration tests
├── test_dashboard_builder.py  # Generation logic tests
└── test_utils.py         # Helper function tests
```

### Mock vs Real Testing

**Mock tests** (default):
```bash
pytest fabric_dashboard/tests/ -v
```

**Real API tests**:
```bash
MOCK_MODE=false pytest fabric_dashboard/tests/ -v
```

Tests marked with `@pytest.mark.use_real_data` are skipped in mock mode.

## Deployment Considerations

### Environment Variables

Required for production:
- `MOCK_MODE=false`
- `ONFABRIC_API_KEY` - User data access
- Optional enrichment API keys

### Performance

- Pattern extraction: ~200ms for typical user
- Dashboard generation: ~100ms
- Total pipeline: <500ms

### Scaling

Current bottlenecks:
- OnFabric API rate limits
- Enrichment API quotas
- Frontend rendering for large dashboards (>20 widgets)
