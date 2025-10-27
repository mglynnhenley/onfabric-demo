# Fabric Dashboard - Technical Specification

**Version**: 1.0
**Date**: 2025-01-15
**Architecture**: Python + LangChain + Anthropic Claude + Perplexity

---

## Executive Summary

Build a CLI tool that generates personalized HTML dashboards by:
1. Analyzing user data from onfabric MCP
2. Using **separate Claude API calls** for each function:
   - Pattern detection
   - Theme generation
   - Individual widget generation (parallel)
   - Final HTML assembly
3. Enriching with live data via Perplexity API
4. Generating a beautiful, self-contained HTML dashboard

**Key Principle**: One LLM call per discrete function. Maximize modularity and parallelization.

---

## System Architecture

### High-Level Flow

```
CLI Command
    ↓
[1] Data Fetcher → onfabric MCP or mock data
    ↓
[2] Pattern Detector → Claude Call #1 (detect patterns)
    ↓
[3] Theme Generator → Claude Call #2 (generate theme)
    ↓
[4] Search Enricher → Perplexity API (parallel, 2-3 patterns)
    ↓
[5] Widget Generator → Claude Calls #3-N (parallel, one per widget)
    ↓
[6] Dashboard Assembler → Claude Call #N+1 (assemble final HTML)
    ↓
Output: dashboard-{timestamp}.html
```

### Parallelization Strategy

```
After Step 3 (Theme Generated):
    ├─ Perplexity Search (parallel)
    │   ├─ Pattern 1: Query 1, Query 2
    │   ├─ Pattern 2: Query 1, Query 2
    │   └─ Pattern 3: Query 1, Query 2
    │
    └─ Widget Generation (parallel, after search completes)
        ├─ Widget 1 HTML (Claude)
        ├─ Widget 2 HTML (Claude)
        ├─ Widget 3 HTML (Claude)
        ├─ Widget 4 HTML (Claude)
        └─ Widget 5 HTML (Claude)
            ↓
        [Combine] Dashboard Assembly (Claude)
```

**Expected Time**:
- Sequential: ~15-20 seconds
- With parallelization: ~8-10 seconds

---

## Component Specifications

### 1. Data Fetcher

**Purpose**: Fetch user data from onfabric MCP or load mock data

**Inputs**:
- `days_back`: int (default: 30)
- `mock`: bool (default: False)

**Outputs**:
- `UserData` (Pydantic model)

**LLM Calls**: 0

**Implementation**:
```python
class DataFetcher:
    async def fetch(self, days_back: int = 30, mock: bool = False) -> UserData:
        if mock:
            return self._load_mock_data()

        # Connect to onfabric MCP
        client = await self._create_onfabric_client()

        # Get connections
        connections = await client.get_connections()

        # Query threads for each connection
        threads = []
        for conn in connections:
            threads.extend(
                await client.query_threads(
                    connection_id=conn.id,
                    from_date=self._get_date(days_back),
                    to_date=datetime.now().isoformat()
                )
            )

        return UserData(
            connections=connections,
            threads=threads,
            summary=self._create_summary(connections, threads)
        )
```

**Error Handling**:
- MCP connection failure → fallback to mock data
- Empty data → return minimal UserData with placeholder content

---

### 2. Pattern Detector

**Purpose**: Analyze user data and detect behavioral patterns

**Inputs**:
- `user_data`: UserData

**Outputs**:
- `List[Pattern]` (Pydantic models)

**LLM Calls**: 1 (Claude Sonnet 4)

**Prompt Strategy**:
```python
SYSTEM: You are a behavioral pattern analyst. Analyze digital activity
        data and identify meaningful patterns. Be creative with pattern
        types and widget concepts.

USER: Analyze this data and identify 4-6 patterns:

      {user_data_json}

      For each pattern:
      1. Type (invent creative names, not generic)
      2. Confidence (0.0-1.0)
      3. Description
      4. Widget concept (invent unique widget type)
      5. Visualization type - be creative! Examples: clock, feed, radar,
         timeline, heatmap, graph, network, constellation, spiral, wave.
         Invent new visualization types!
      6. Layout size (must be one of: hero/large/medium/small)
      7. 2 search queries to enrich pattern

      {format_instructions}
```

**Pydantic Schema**:
```python
class WidgetConcept(BaseModel):
    name: str  # e.g., "Night Owl Chronometer", "Curiosity Compass"
    icon: str  # emoji
    visualization_type: str  # clock/feed/radar/etc
    layout_size: str  # hero/large/medium/small
    description: str

class Pattern(BaseModel):
    type: str
    name: str
    confidence: float = Field(ge=0.0, le=1.0)
    description: str
    data: dict[str, Any]
    widget_concept: WidgetConcept
    search_queries: list[str] = Field(min_length=2, max_length=2)

class PatternDetectionResult(BaseModel):
    patterns: list[Pattern]
```

**Implementation**:
```python
class PatternDetector:
    def __init__(self, api_key: str):
        self.llm = ChatAnthropic(
            model="claude-sonnet-4-5",
            api_key=api_key,
            temperature=1.0,
            max_tokens=4000
        )
        self.parser = PydanticOutputParser(pydantic_object=PatternDetectionResult)

    async def detect(self, user_data: UserData) -> list[Pattern]:
        prompt = self._build_prompt(user_data)
        chain = prompt | self.llm | self.parser
        result = await chain.ainvoke({"user_data": user_data.model_dump()})
        return result.patterns
```

**Error Handling**:
```python
from tenacity import retry, stop_after_attempt, wait_exponential

class PatternDetector:
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def detect(self, user_data: UserData) -> list[Pattern]:
        try:
            prompt = self._build_prompt(user_data)
            chain = prompt | self.llm | self.parser
            result = await chain.ainvoke({"user_data": user_data.model_dump()})
            return result.patterns
        except Exception as e:
            # Fallback: generate generic patterns
            return self._generate_fallback_patterns(user_data)

    def _generate_fallback_patterns(self, user_data: UserData) -> list[Pattern]:
        """Generate basic patterns when LLM fails"""
        return [
            Pattern(
                type="Activity Level",
                name="Active User",
                confidence=0.9,
                description=f"You have {user_data.summary.total_interactions} interactions.",
                data={"total": user_data.summary.total_interactions},
                widget_concept=WidgetConcept(
                    name="Activity Summary",
                    icon="📊",
                    visualization_type="stats",
                    layout_size="large",
                    description="Overview of your activity"
                )
            )
        ]
```

---

### 3. Theme Generator

**Purpose**: Generate personalized color scheme based on user behavior

**Inputs**:
- `user_data`: UserData
- `patterns`: List[Pattern]

**Outputs**:
- `Theme` (Pydantic model)

**LLM Calls**: 1 (Claude Sonnet 4)

**Prompt Strategy**:
```python
SYSTEM: You are a design expert who creates personalized color schemes
        based on user behavior patterns. Colors must be modern, accessible
        (WCAG AA), and work on dark backgrounds.

USER: Generate a personalized theme for this user:

      Patterns: {patterns_summary}
      Activity Summary: {user_data_summary}

      Consider:
      - Time patterns (night owl vs morning person)
      - Content type (tech, creative, news, social)
      - Activity level (high energy vs contemplative)

      Requirements:
      - Primary, secondary, highlight colors
      - Background gradient (3 colors)
      - Text color with good contrast
      - Modern palette (avoid pure saturated colors)

      {format_instructions}
```

**Pydantic Schema**:
```python
class Theme(BaseModel):
    primary: str = Field(pattern=r"^#[0-9a-fA-F]{6}$")
    secondary: str = Field(pattern=r"^#[0-9a-fA-F]{6}$")
    highlight: str = Field(pattern=r"^#[0-9a-fA-F]{6}$")
    background: list[str] = Field(min_length=3, max_length=3)
    text: str = Field(pattern=r"^#[0-9a-fA-F]{6}$")
    rationale: str
    mood: str  # e.g., "energetic", "calm", "professional"
```

**Implementation**:
```python
class ThemeGenerator:
    def __init__(self, api_key: str):
        self.llm = ChatAnthropic(
            model="claude-sonnet-4-5",
            api_key=api_key,
            temperature=0.8,
            max_tokens=1000
        )
        self.parser = PydanticOutputParser(pydantic_object=Theme)

    async def generate(self, user_data: UserData, patterns: list[Pattern]) -> Theme:
        prompt = self._build_prompt(user_data, patterns)
        chain = prompt | self.llm | self.parser
        return await chain.ainvoke({
            "patterns": [p.model_dump() for p in patterns],
            "summary": user_data.summary.model_dump()
        })
```

**Error Handling**:
- Invalid hex colors → retry with validation reminder
- Parse error → use default theme based on patterns

---

### 4. Search Enricher

**Purpose**: Execute searches via Perplexity API to enrich patterns with live data

**Inputs**:
- `patterns`: List[Pattern]
- `max_patterns`: int (default: 3)

**Outputs**:
- `List[EnrichedPattern]`

**LLM Calls**: 0 (Perplexity API only)

**API Strategy**:
```python
# Perplexity API call per query
POST https://api.perplexity.ai/chat/completions
{
  "model": "sonar",
  "messages": [
    {"role": "user", "content": "{search_query}"}
  ]
}
```

**Implementation**:
```python
class SearchEnricher:
    def __init__(self, api_key: str, cache_dir: Path):
        self.api_key = api_key
        self.cache = DiskCache(cache_dir)
        self.client = httpx.AsyncClient()

    async def enrich(
        self,
        patterns: list[Pattern],
        max_patterns: int = 3
    ) -> list[EnrichedPattern]:
        # Sort by confidence, take top N
        top_patterns = sorted(patterns, key=lambda p: p.confidence, reverse=True)[:max_patterns]

        # Build task map to track which pattern each search belongs to
        task_map = []
        for pattern in top_patterns:
            for query in pattern.search_queries:
                task_map.append((pattern, self._search(query)))

        # Execute all searches in parallel, handling exceptions
        results = await asyncio.gather(
            *[task for _, task in task_map],
            return_exceptions=True
        )

        # Group results by pattern, filtering out exceptions
        enriched_dict = {}
        for (pattern, _), result in zip(task_map, results):
            if pattern not in enriched_dict:
                enriched_dict[pattern] = []
            if not isinstance(result, Exception):
                enriched_dict[pattern].append(result)

        # Convert to EnrichedPattern list
        enriched = [
            EnrichedPattern(pattern=pattern, search_results=results)
            for pattern, results in enriched_dict.items()
        ]

        return enriched

    async def _search(self, query: str) -> SearchResult:
        """Search with error handling"""
        try:
            # Check cache (30min TTL)
            cached = await self.cache.get(query)
            if cached:
                return cached

            # Execute search
            response = await self.client.post(
                "https://api.perplexity.ai/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"model": "sonar", "messages": [{"role": "user", "content": query}]},
                timeout=10.0
            )

            result = SearchResult(
                query=query,
                answer=response.json()["choices"][0]["message"]["content"],
                citations=response.json().get("citations", []),
                timestamp=datetime.now().isoformat()
            )

            await self.cache.set(query, result, ttl=1800)
            return result
        except Exception as e:
            # Return empty result on error
            return SearchResult(
                query=query,
                answer="",
                citations=[],
                timestamp=datetime.now().isoformat()
            )
```

**Error Handling**:
- Individual search failures are caught and return empty SearchResult
- Uses `return_exceptions=True` in gather() to prevent one failure from stopping all searches
- Task mapping ensures results align with patterns even if some searches fail
- Rate limit → use cached results only
- Timeout → returns empty search result
- Network error → returns empty search result

---

### 5. Widget Generator (PARALLEL)

**Purpose**: Generate individual widget HTML snippets

**Inputs**:
- `enriched_pattern`: EnrichedPattern
- `theme`: Theme

**Outputs**:
- `WidgetHTML` (string)

**LLM Calls**: 1 per widget (parallel execution)

**Prompt Strategy**:
```python
SYSTEM: You are a web developer creating beautiful, interactive widget
        components. Generate self-contained HTML+CSS for a single widget.

USER: Create a widget for this pattern:

      Widget Concept: {pattern.widget_concept.name}
      Visualization: {pattern.widget_concept.visualization_type}
      Layout Size: {pattern.widget_concept.layout_size}

      Pattern Data: {pattern.data}
      Live Search Results: {pattern.search_results}

      Theme Colors:
      - Primary: {theme.primary}
      - Secondary: {theme.secondary}
      - Highlight: {theme.highlight}

      Requirements:
      1. Return only the widget HTML (no <html>, <head>, <body>)
      2. Use inline styles or <style> scoped to widget
      3. Widget must be self-contained <div class="widget">
      4. Implement the visualization type creatively
      5. Integrate search results naturally
      6. Add hover effects and animations
      7. Include "LIVE" badge if using search data
      8. Mobile-responsive

      Be creative! Make this widget unique and beautiful.
```

**Implementation**:
```python
class WidgetGenerator:
    def __init__(self, api_key: str):
        self.llm = ChatAnthropic(
            model="claude-sonnet-4-5",
            api_key=api_key,
            temperature=1.0,
            max_tokens=4000
        )

    async def generate(self, enriched_pattern: EnrichedPattern, theme: Theme) -> str:
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.SYSTEM_PROMPT),
            ("user", self.USER_PROMPT)
        ])

        chain = prompt | self.llm | StrOutputParser()

        html = await chain.ainvoke({
            "widget_concept": enriched_pattern.pattern.widget_concept.model_dump(),
            "pattern_data": enriched_pattern.pattern.data,
            "search_results": [r.model_dump() for r in enriched_pattern.search_results],
            "theme": theme.model_dump()
        })

        return self._clean_html(html)

    def _clean_html(self, html: str) -> str:
        # Remove markdown code blocks if present
        if "```html" in html:
            html = html.split("```html")[1].split("```")[0]
        return html.strip()
```

**Parallel Execution**:
```python
# In main generate flow:
widget_tasks = [
    widget_generator.generate(enriched_pattern, theme)
    for enriched_pattern in enriched_patterns
]

widget_htmls = await asyncio.gather(*widget_tasks)
```

**Error Handling**:
- Invalid HTML → retry with validation reminder
- Timeout → use fallback template
- Parse error → skip widget, continue with others

---

### 6. Dashboard Assembler

**Purpose**: Combine all widgets into final HTML dashboard

**Inputs**:
- `widget_htmls`: List[str]
- `theme`: Theme
- `patterns`: List[Pattern]
- `user_data`: UserData

**Outputs**:
- Complete HTML document (string)

**LLM Calls**: 1 (Claude Sonnet 4)

**Prompt Strategy**:
```python
SYSTEM: You are assembling a complete HTML dashboard from individual
        widget components. Create the page structure, header, footer,
        and layout system.

USER: Assemble these widgets into a beautiful dashboard:

      WIDGETS (pre-generated HTML):
      {widget_htmls}

      THEME:
      {theme}

      METADATA:
      - Total patterns: {len(patterns)}
      - Date range: {user_data.summary.date_range}
      - Generated: {datetime.now()}

      Requirements:
      1. Complete <!DOCTYPE html> document
      2. <head> with meta tags, title, viewport
      3. Global CSS for layout (CSS Grid, 12-column)
      4. Header with title, metadata
      5. Main content area with widget grid
      6. Footer with credits
      7. Embedded JavaScript for:
         - Real-time clock
         - Hover interactions
         - LIVE badge pulsing
      8. Responsive breakpoints
      9. Use theme colors for backgrounds, gradients
      10. Arrange widgets by layout_size (hero → large → medium → small)

      Return complete, production-ready HTML.
```

**Implementation**:
```python
class DashboardAssembler:
    def __init__(self, api_key: str):
        self.llm = ChatAnthropic(
            model="claude-sonnet-4-5",
            api_key=api_key,
            temperature=0.7,
            max_tokens=8000
        )

    async def assemble(
        self,
        widget_htmls: list[str],
        theme: Theme,
        patterns: list[Pattern],
        user_data: UserData
    ) -> str:
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.SYSTEM_PROMPT),
            ("user", self.USER_PROMPT)
        ])

        chain = prompt | self.llm | StrOutputParser()

        html = await chain.ainvoke({
            "widgets": "\n\n".join(widget_htmls),
            "theme": theme.model_dump(),
            "num_patterns": len(patterns),
            "date_range": user_data.summary.date_range,
            "generated_at": datetime.now().isoformat()
        })

        return self._clean_html(html)
```

**Error Handling**:
- Invalid HTML → use fallback template with widgets inserted
- Missing widgets → continue with available widgets
- Parse error → retry once

---

## Data Models (Pydantic)

```python
# src/fabric_dashboard/models/schemas.py

from pydantic import BaseModel, Field
from typing import Any, Literal
from datetime import datetime

class DataSummary(BaseModel):
    total_interactions: int
    providers: list[str]
    date_range: dict[str, str]
    primary_activity_hours: list[int] = []
    top_content_types: list[str] = []

class UserData(BaseModel):
    connections: list[dict[str, Any]]
    threads: list[dict[str, Any]]
    summary: DataSummary

class WidgetConcept(BaseModel):
    name: str
    icon: str
    visualization_type: str
    layout_size: Literal["hero", "large", "medium", "small"]
    description: str

class Pattern(BaseModel):
    type: str
    name: str
    confidence: float = Field(ge=0.0, le=1.0)
    description: str
    data: dict[str, Any]
    widget_concept: WidgetConcept
    search_queries: list[str] = Field(min_length=2, max_length=2)

class Theme(BaseModel):
    primary: str = Field(pattern=r"^#[0-9a-fA-F]{6}$")
    secondary: str = Field(pattern=r"^#[0-9a-fA-F]{6}$")
    highlight: str = Field(pattern=r"^#[0-9a-fA-F]{6}$")
    background: list[str] = Field(min_length=3, max_length=3)
    text: str = Field(pattern=r"^#[0-9a-fA-F]{6}$")
    rationale: str
    mood: str

class SearchResult(BaseModel):
    query: str
    answer: str
    citations: list[str] = []
    timestamp: str

class EnrichedPattern(BaseModel):
    pattern: Pattern
    search_results: list[SearchResult]
```

---

## Project Structure

```
fabric-dashboard/
├── fabric_dashboard/
│   ├── __init__.py
│   ├── cli.py                      # Click CLI entry
│   │
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── init.py                 # Setup command
│   │   └── generate.py             # Main orchestration
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── data_fetcher.py         # [LLM: 0] Fetch onfabric data
│   │   ├── pattern_detector.py     # [LLM: 1] Detect patterns
│   │   ├── theme_generator.py      # [LLM: 1] Generate theme
│   │   ├── search_enricher.py      # [LLM: 0] Perplexity search
│   │   ├── widget_generator.py     # [LLM: N] Generate widgets
│   │   └── dashboard_assembler.py  # [LLM: 1] Assemble HTML
│   │
│   ├── mcp/
│   │   ├── __init__.py
│   │   ├── client.py               # Base MCP client
│   │   └── onfabric.py             # onfabric wrapper
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py               # Config management
│   │   ├── cache.py                # DiskCache wrapper
│   │   ├── logger.py               # Rich console
│   │   └── files.py                # File I/O
│   │
│   └── models/
│       ├── __init__.py
│       └── schemas.py              # All Pydantic models
│
├── tests/
│   ├── fixtures/
│   │   ├── mock_user_data.json
│   │   ├── mock_patterns.json
│   │   └── mock_search_results.json
│   ├── test_pattern_detector.py
│   ├── test_theme_generator.py
│   ├── test_widget_generator.py
│   └── test_integration.py
│
├── pyproject.toml
├── README.md
├── .env.example
└── .gitignore
```

---

## Dependencies

### Installation with uv (Fast!)

```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate  # Windows

# Install all dependencies
uv pip install -r requirements.txt

# Install dev dependencies
uv pip install -r requirements-dev.txt
```

### requirements.txt

```txt
langchain>=0.3.17
langchain-core>=0.3.29
langchain-anthropic>=0.3.7
langchain-mcp>=0.3.0
anthropic>=0.42.0
pydantic>=2.10.5
pydantic-settings>=2.7.1
click>=8.1.8
rich>=13.9.4
httpx>=0.28.1
diskcache>=5.6.3
python-dotenv>=1.0.1
tenacity>=8.2.0
```

### requirements-dev.txt

```txt
pytest>=8.3.4
pytest-asyncio>=0.25.2
black>=24.10.0
ruff>=0.8.6
```

---

## Configuration

### Config File Location
`~/.fabric-dashboard/config.yaml`

### Schema
```yaml
claude:
  api_key: sk-ant-...
  model: claude-sonnet-4-5

perplexity:
  api_key: pplx-...

onfabric:
  mcp_command: npx -y @onfabric/mcp-server

dashboard:
  days_back: 30
  max_patterns: 6
  max_enriched_patterns: 3
  output_dir: ~/.fabric-dashboard/dashboards

cache:
  dir: ~/.fabric-dashboard/cache
  ttl: 1800  # 30 minutes
```

---

## CLI Commands

### 1. `fabric-dashboard init`

Interactive setup wizard.

**Flow**:
```
🚀 Fabric Dashboard Setup

Enter Claude API key: ••••••••
Enter Perplexity API key: ••••••••
Days of history to analyze (default: 30): 30
Enable mock mode for testing? (y/n): n

✅ Configuration saved to ~/.fabric-dashboard/config.yaml

Next: Run `fabric-dashboard generate`
```

### 2. `fabric-dashboard generate`

Generate dashboard.

**Options**:
- `--mock` - Use mock data
- `--no-search` - Skip search enrichment
- `--output <path>` - Custom output path
- `--debug` - Verbose logging

**Flow**:
```
🚀 Generating Dashboard

📊 Fetching data... ✓ (576 interactions)
🔍 Detecting patterns... ✓ (5 patterns found)
🎨 Generating theme... ✓ (Primary: #6366f1)
🌐 Enriching with search... ✓ (3 patterns enriched)
🎨 Generating widgets...
  ├─ Night Owl Chronometer ✓
  ├─ Curiosity Compass ✓
  ├─ Adventure Radar ✓
  ├─ Learning Path ✓
  └─ Interest Landscape ✓
🏗️  Assembling dashboard... ✓

✅ Dashboard ready!
📄 ~/.fabric-dashboard/dashboards/dashboard-2025-01-15-143052.html
🌐 Opening in browser...

⏱️  Total time: 9.2s
```

---

## Implementation Plan

### Phase 1: Foundation (2-3 hours)

**Goals**: Project setup, basic structure, mock data

**Tasks**:
1. Initialize project
   ```bash
   mkdir fabric-dashboard
   cd fabric-dashboard

   # Create virtual environment with uv
   uv venv
   source .venv/bin/activate

   # Install dependencies
   uv pip install langchain langchain-core langchain-anthropic langchain-mcp \
     click pydantic pydantic-settings rich httpx diskcache python-dotenv tenacity

   # Install dev dependencies
   uv pip install pytest pytest-asyncio black ruff
   ```

2. Create directory structure
   - All directories from project structure above
   - Empty `__init__.py` files

3. Implement data models
   - `models/schemas.py` with all Pydantic models
   - Write tests for model validation

4. Implement utilities
   - `utils/config.py` - Config loading/saving
   - `utils/logger.py` - Rich console wrapper
   - `utils/cache.py` - DiskCache wrapper
   - `utils/files.py` - File I/O helpers

5. Create mock data
   - `tests/fixtures/mock_user_data.json` - Realistic user data
   - `tests/fixtures/mock_patterns.json` - Sample patterns
   - `tests/fixtures/mock_search_results.json` - Sample Perplexity responses

6. CLI skeleton
   - `cli.py` with Click setup
   - `commands/init.py` - Setup command (prompts, save config)
   - Test: `python fabric_dashboard/cli.py` works

7. Make CLI runnable
   ```bash
   # Add to pyproject.toml or setup.py, or simply run:
   python -m fabric_dashboard.cli

   # Or create a simple run script:
   echo '#!/usr/bin/env python' > run.py
   echo 'from fabric_dashboard.cli import main' >> run.py
   echo 'if __name__ == "__main__": main()' >> run.py
   chmod +x run.py
   ```

**Deliverables**:
- ✅ Can run `python run.py` or `python -m fabric_dashboard.cli`
- ✅ Config saved to `~/.fabric-dashboard/config.yaml`
- ✅ Mock data fixtures ready
- ✅ All Pydantic models defined and tested

---

### Phase 2: Data Fetching (1-2 hours)

**Goals**: Fetch data from onfabric MCP or mock

**Tasks**:
1. Implement MCP client
   - `mcp/client.py` - Generic MCP client using langchain-mcp
   - `mcp/onfabric.py` - onfabric-specific methods

2. Implement data fetcher
   - `core/data_fetcher.py`
   - Support both real MCP and mock mode
   - Return structured `UserData` model

3. Test data fetching
   - Unit tests with mock MCP responses
   - Integration test with real onfabric (if available)

4. Add to generate command
   - `commands/generate.py` - Basic orchestrator
   - Fetch data, print summary

**Deliverables**:
- ✅ Can fetch data from onfabric MCP
- ✅ Mock mode works
- ✅ `python run.py generate --mock` shows data summary

---

### Phase 3: Pattern Detection & Theme (1-2 hours)

**Goals**: Implement first 2 LLM calls

**Tasks**:
1. Pattern detector
   - `core/pattern_detector.py`
   - LangChain prompt + Pydantic parser
   - Test with mock data

2. Theme generator
   - `core/theme_generator.py`
   - LangChain prompt + Pydantic parser
   - Test with mock patterns

3. Integration
   - Add to generate command
   - Print detected patterns and theme

4. Testing
   - Unit tests with fixtures
   - Validate Pydantic outputs
   - Test error handling (retry logic)

**Deliverables**:
- ✅ Pattern detection works
- ✅ Theme generation works
- ✅ `python run.py generate --mock --no-search` shows patterns + theme

---

### Phase 4: Search Enrichment (1 hour)

**Goals**: Integrate Perplexity API

**Tasks**:
1. Search enricher
   - `core/search_enricher.py`
   - Perplexity API integration
   - Parallel search execution
   - Cache implementation

2. Testing
   - Mock Perplexity responses
   - Test cache hits/misses
   - Test error handling (rate limits, timeouts)

3. Integration
   - Add to generate command
   - Show enriched patterns

**Deliverables**:
- ✅ Perplexity search works
- ✅ Caching works
- ✅ Parallel execution works
- ✅ Error handling works

---

### Phase 5: Widget Generation (2-3 hours)

**Goals**: Generate individual widgets in parallel

**Tasks**:
1. Widget generator
   - `core/widget_generator.py`
   - LangChain prompt for single widget
   - HTML cleaning/validation

2. Parallel execution
   - Implement `asyncio.gather()` for all widgets
   - Progress tracking (Rich progress bar)

3. Testing
   - Test each widget type (6 different visualizations)
   - Validate HTML output
   - Test error handling

4. Integration
   - Add to generate command
   - Save individual widget HTML for debugging

**Deliverables**:
- ✅ Can generate individual widgets
- ✅ Parallel generation works
- ✅ All 6 visualization types tested
- ✅ HTML validation works

---

### Phase 6: Dashboard Assembly (1-2 hours)

**Goals**: Final HTML assembly

**Tasks**:
1. Dashboard assembler
   - `core/dashboard_assembler.py`
   - LangChain prompt for full HTML
   - Combine widgets into layout

2. HTML validation
   - Basic HTML structure check
   - Ensure all widgets included
   - Validate theme colors applied

3. File output
   - Save to `~/.fabric-dashboard/dashboards/`
   - Timestamp-based naming
   - Open in browser automatically

4. Testing
   - End-to-end test with mock data
   - Visual inspection of output
   - Test different widget combinations

**Deliverables**:
- ✅ Complete HTML dashboard generated
- ✅ Opens in browser
- ✅ All widgets rendered
- ✅ Theme applied correctly

---

### Phase 7: Polish & Error Handling (1-2 hours)

**Goals**: Production-ready error handling

**Tasks**:
1. Error handling
   - Retry logic for LLM calls
   - Fallback templates for failed widgets
   - Graceful degradation (skip failed components)

2. Logging improvements
   - Debug mode with verbose output
   - Error messages with context
   - Performance metrics

3. CLI improvements
   - Better progress indicators
   - Color-coded output
   - Help text and examples

4. Documentation
   - README with examples
   - API key setup instructions
   - Troubleshooting guide

**Deliverables**:
- ✅ Robust error handling
- ✅ Clear error messages
- ✅ Good documentation
- ✅ Demo-ready

---

## Testing Strategy

### Unit Tests
- All Pydantic models
- Each core component in isolation
- Mock LLM responses
- Cache behavior

### Integration Tests
- Full pipeline with mock data
- MCP integration (if available)
- Perplexity API (with real key)

### End-to-End Tests
- Generate dashboard with mock data
- Verify HTML structure
- Visual inspection

### Manual Testing
- Real onfabric data
- Different user profiles
- Edge cases (empty data, API failures)

---

## Performance Targets

### Sequential Execution
```
Data Fetching:       2s
Pattern Detection:   3s
Theme Generation:    1s
Search Enrichment:   4s (parallel)
Widget Generation:   10s (sequential)
Dashboard Assembly:  2s
---------------------------------
Total:              22s
```

### With Parallelization
```
Data Fetching:       2s
Pattern Detection:   3s
Theme Generation:    1s
Search Enrichment:   4s (parallel)
Widget Generation:   3s (parallel, 5 widgets)
Dashboard Assembly:  2s
---------------------------------
Total:              ~15s → Target: <10s with optimization
```

### Optimization Opportunities
1. Stream widget generation (show progress)
2. Cache pattern detection for same data
3. Reduce widget generation tokens
4. Parallel theme + pattern detection

---

## Demo Considerations

### Demo Script
```bash
# Setup (one time)
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# Generate (8-10 seconds)
python run.py generate --mock

# Result: Beautiful HTML opens in browser
```

### Demo Data Requirements
- Rich mock data (diverse patterns)
- Interesting search results
- Visually distinct widgets
- Cohesive theme

### Failure Modes
1. **Slow LLM response**: Show progress, streaming
2. **Invalid HTML**: Fallback template
3. **API rate limit**: Use cached data
4. **Empty data**: Generate demo dashboard

### Success Metrics
- Visual impact ✓
- Speed (<10s) ✓
- Reliability (mock mode) ✓
- Uniqueness (different each time) ✓

---

## Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Claude generates invalid HTML | High | Medium | HTML validation, retry, fallback |
| Perplexity rate limits | Medium | High | Aggressive caching, fallback to no search |
| MCP connection fails | Medium | Medium | Mock mode, clear error messages |
| Slow generation time | Medium | Medium | Parallelization, streaming, caching |
| Empty user data | Low | Low | Mock mode, demo data |

---

## Future Enhancements (Post-Demo)

1. **Serve Mode**: Live server with auto-refresh
2. **Multiple Profiles**: Switch between work/personal
3. **Export Options**: PDF, PNG, shareable link
4. **Custom Widgets**: User-defined widget types
5. **Analytics**: Track dashboard usage
6. **Collaboration**: Share dashboards

---

## Summary

**Total LLM Calls per Generation**:
- Pattern Detection: 1
- Theme Generation: 1
- Widget Generation: 5 (parallel)
- Dashboard Assembly: 1
- **Total**: 8 calls (5 parallel)

**Expected Time**: 8-10 seconds

**Key Advantages**:
- ✅ Modular (each function separate)
- ✅ Parallelizable (widgets in parallel)
- ✅ Debuggable (isolate failures)
- ✅ Flexible (swap LLM for any component)
- ✅ Demo-ready (fast, reliable)
