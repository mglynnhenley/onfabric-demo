"""Data models for fabric_dashboard using Pydantic v2."""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field, field_validator


# ============================================================================
# ENUMS & CONSTANTS
# ============================================================================


class CardSize(str, Enum):
    """Card size categories for bento grid layout."""

    LARGE = "large"  # col-span-8, 400-500 words
    MEDIUM = "medium"  # col-span-6, 250-300 words
    SMALL = "small"  # col-span-4, 150-200 words
    COMPACT = "compact"  # col-span-3, 100-150 words


# ============================================================================
# USER DATA & PERSONA
# ============================================================================


class PersonaProfile(BaseModel):
    """Extracted user persona from Fabric MCP data."""

    writing_style: str = Field(
        min_length=1,
        description="LLM-generated writing style description (e.g., 'analytical and data-driven', 'narrative and emotional', 'provocative and contrarian')",
    )
    interests: list[str] = Field(
        default_factory=list,
        description="List of detected interests/themes",
        min_length=1,
    )
    activity_level: Literal["low", "moderate", "high"] = Field(
        default="moderate", description="User's digital activity level"
    )
    professional_context: Optional[str] = Field(
        None,
        description="Professional context (e.g., 'startup founder', 'corporate exec', 'creative professional')",
    )
    tone_preference: str = Field(
        default="balanced and approachable",
        min_length=1,
        description="LLM-generated tone preference (e.g., 'formal and professional', 'casual and conversational', 'balanced and approachable', 'witty and irreverent')",
    )
    age_range: Optional[str] = Field(
        None, description="Estimated age range (e.g., '25-34', '35-44')"
    )
    content_depth_preference: Literal["quick_insights", "balanced", "deep_dives"] = (
        Field(default="balanced", description="Preferred content depth")
    )


class DataSummary(BaseModel):
    """Summary statistics from user data."""

    total_interactions: int = Field(ge=0, description="Total number of interactions")
    date_range_start: datetime = Field(description="Start of data collection period")
    date_range_end: datetime = Field(description="End of data collection period")
    days_analyzed: int = Field(ge=1, description="Number of days analyzed")
    platforms: list[str] = Field(
        description="List of connected platforms (instagram, google, pinterest)"
    )
    top_themes: list[str] = Field(
        default_factory=list,
        description="Most common themes/topics",
    )


class UserData(BaseModel):
    """Raw user data from Fabric MCP."""

    connection_id: str = Field(description="Fabric MCP connection ID")
    interactions: list[dict[str, Any]] = Field(
        default_factory=list, description="Raw interaction data"
    )
    summary: DataSummary = Field(description="Summary statistics")
    persona: Optional[PersonaProfile] = Field(
        None, description="Extracted persona profile"
    )


# ============================================================================
# COLOR SCHEME & THEMING
# ============================================================================


class FontScheme(BaseModel):
    """Font configuration for dashboard theming."""

    heading: str = Field(description="Heading font family (e.g., 'EB Garamond')")
    body: str = Field(description="Body font family (e.g., 'Manrope')")
    mono: str = Field(description="Monospace font family (e.g., 'IBM Plex Mono')")
    heading_url: str = Field(description="Google Fonts URL for heading font")
    body_url: str = Field(description="Google Fonts URL for body font")
    mono_url: str = Field(description="Google Fonts URL for mono font")


class GradientConfig(BaseModel):
    """Gradient background configuration."""

    type: str = Field(description="Gradient type: 'linear', 'radial', or 'mesh'")
    colors: List[str] = Field(description="List of hex colors for gradient")
    direction: Optional[str] = Field(
        None, description="Gradient direction (e.g., 'to-br', 'to-r')"
    )


class PatternConfig(BaseModel):
    """Pattern background configuration."""

    type: str = Field(
        description="Pattern type: 'dots', 'grid', 'noise', or 'geometric'"
    )
    color: str = Field(description="Pattern color (hex)")
    opacity: float = Field(ge=0.0, le=1.0, description="Pattern opacity (0.0-1.0)")
    scale: float = Field(ge=0.1, le=5.0, description="Pattern scale factor")


class AnimationConfig(BaseModel):
    """CSS animation configuration for backgrounds."""

    name: Literal[
        "float",
        "pulse",
        "drift",
        "wave",
        "rotate-slow",
        "gradient-shift",
        "glitch",
        "breathe",
        "shimmer",
        "none",
    ] = Field(description="Animation name from predefined CSS keyframes library")
    duration: str = Field(
        default="20s", description="Animation duration (e.g., '20s', '30s')"
    )
    timing: str = Field(
        default="ease-in-out",
        description="Animation timing function (e.g., 'ease-in-out', 'linear')",
    )


class BackgroundTheme(BaseModel):
    """Complete background theming configuration."""

    type: str = Field(
        description="Background type: 'solid', 'gradient', 'pattern', or 'animated'"
    )
    color: Optional[str] = Field(None, description="Solid background color (hex)")
    gradient: Optional[GradientConfig] = Field(None, description="Gradient configuration")
    pattern: Optional[PatternConfig] = Field(None, description="Pattern configuration")
    animation: Optional[AnimationConfig] = Field(
        None, description="CSS animation configuration"
    )
    card_background: str = Field(description="Card background color or rgba value")
    card_backdrop_blur: bool = Field(
        default=False, description="Enable backdrop blur for glass effect"
    )


class ColorScheme(BaseModel):
    """Persona-matched color palette for dashboard theming."""

    # Primary palette
    primary: str = Field(
        pattern=r"^#[0-9a-fA-F]{6}$", description="Main brand color (hex)"
    )
    secondary: str = Field(
        pattern=r"^#[0-9a-fA-F]{6}$", description="Supporting color (hex)"
    )
    accent: str = Field(
        pattern=r"^#[0-9a-fA-F]{6}$", description="Highlights and CTAs (hex)"
    )

    # Theming
    background_theme: BackgroundTheme = Field(
        description="Complete background theming configuration"
    )
    fonts: FontScheme = Field(description="Font scheme for typography")

    # Text
    foreground: str = Field(
        pattern=r"^#[0-9a-fA-F]{6}$", description="Primary text color (hex)"
    )
    muted: str = Field(
        pattern=r"^#[0-9a-fA-F]{6}$", description="Secondary text color (hex)"
    )

    # Semantic colors
    success: str = Field(
        pattern=r"^#[0-9a-fA-F]{6}$", description="Success state (hex)"
    )
    warning: str = Field(
        pattern=r"^#[0-9a-fA-F]{6}$", description="Warning state (hex)"
    )
    destructive: str = Field(
        pattern=r"^#[0-9a-fA-F]{6}$", description="Error/destructive state (hex)"
    )

    # Metadata
    mood: str = Field(
        description="Color mood (e.g., 'energetic', 'calm', 'professional', 'creative')"
    )
    rationale: str = Field(
        description="Explanation of why these colors match the persona"
    )

    @field_validator("mood")
    @classmethod
    def validate_mood(cls, v: str) -> str:
        """Ensure mood is not empty."""
        if not v or not v.strip():
            raise ValueError("mood cannot be empty")
        return v.strip()


# ============================================================================
# PATTERNS & CONTENT
# ============================================================================


class Pattern(BaseModel):
    """A detected behavioral pattern or interest theme."""

    title: str = Field(min_length=1, description="Pattern title")
    description: str = Field(
        min_length=10, description="Detailed pattern description"
    )
    confidence: float = Field(
        ge=0.0, le=1.0, description="Confidence score (0.0-1.0)"
    )
    keywords: list[str] = Field(
        default_factory=list,
        description="Related keywords/topics",
        max_length=15,
    )
    interaction_count: int = Field(
        ge=0, description="Number of interactions supporting this pattern"
    )


class SearchResult(BaseModel):
    """Result from Perplexity API search."""

    query: str = Field(description="Search query sent to Perplexity")
    content: str = Field(description="Search result content")
    sources: list[str] = Field(
        default_factory=list, description="Source URLs", max_length=10
    )
    relevance_score: float = Field(
        ge=0.0, le=1.0, default=1.0, description="Relevance score (0.0-1.0)"
    )
    fetched_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="When this was fetched",
    )


class EnrichedPattern(BaseModel):
    """Pattern enriched with live search data from Perplexity."""

    pattern: Pattern = Field(description="Original detected pattern")
    search_results: list[SearchResult] = Field(
        default_factory=list,
        description="Search results enriching this pattern",
        max_length=5,
    )
    enriched_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="When enrichment occurred",
    )


class CardContent(BaseModel):
    """Generated content for a dashboard card."""

    title: str = Field(min_length=1, max_length=150, description="Card title")
    description: str = Field(
        min_length=1, max_length=300, description="Card subtitle/tagline"
    )
    body: str = Field(min_length=50, description="Main content in Markdown format")
    reading_time_minutes: int = Field(
        ge=1, le=15, description="Estimated reading time in minutes"
    )
    sources: list[str] = Field(
        default_factory=list, description="Source URLs cited", max_length=10
    )
    size: CardSize = Field(description="Card size category")
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        default=1.0,
        description="Pattern confidence (affects card positioning)",
    )
    pattern_title: str = Field(
        description="Title of the pattern this card is based on"
    )

    def word_count(self) -> int:
        """Calculate word count from body text."""
        return len(self.body.split())

    def model_post_init(self, __context) -> None:
        """Validate word count matches card size after initialization."""
        word_count = self.word_count()

        # Define expected ranges (with 20% tolerance)
        size_ranges = {
            CardSize.LARGE: (320, 600),  # 400-500 ±20%
            CardSize.MEDIUM: (200, 360),  # 250-300 ±20%
            CardSize.SMALL: (120, 240),  # 150-200 ±20%
            CardSize.COMPACT: (80, 180),  # 100-150 ±20%
        }

        min_words, max_words = size_ranges[self.size]

        if not (min_words <= word_count <= max_words):
            raise ValueError(
                f"Word count {word_count} doesn't match {self.size.value} card size "
                f"(expected {min_words}-{max_words} words)"
            )


# ============================================================================
# DASHBOARD
# ============================================================================


class Dashboard(BaseModel):
    """Complete dashboard with all cards and metadata."""

    user_name: str = Field(min_length=1, description="User's display name")
    generated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="When this dashboard was generated",
    )
    color_scheme: ColorScheme = Field(
        description="Persona-matched color scheme for theming"
    )
    cards: list[CardContent] = Field(
        description="Dashboard cards (3-10 cards)", min_length=3, max_length=10
    )
    persona: PersonaProfile = Field(description="User's persona profile")
    data_summary: DataSummary = Field(description="Summary of analyzed data")
    generation_time_seconds: float = Field(
        ge=0.0, description="Time taken to generate dashboard"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )

    @field_validator("cards")
    @classmethod
    def validate_card_count(cls, v: list[CardContent]) -> list[CardContent]:
        """Ensure we have 3-10 cards."""
        if not (3 <= len(v) <= 10):
            raise ValueError(f"Dashboard must have 3-10 cards, got {len(v)}")
        return v


# ============================================================================
# JSON DASHBOARD (NEW FORMAT)
# ============================================================================


class Widget(BaseModel):
    """Widget definition for JSON dashboard output."""

    id: str = Field(description="Unique widget identifier")
    type: str = Field(
        description="Widget type (e.g., 'stat-card', 'article-card', 'chart-card')"
    )
    size: str = Field(description="Widget size: 'small', 'medium', or 'large'")
    priority: int = Field(ge=1, description="Display priority (1 = highest)")
    data: Dict[str, Any] = Field(description="Widget-specific data")


class DashboardJSON(BaseModel):
    """Dashboard in JSON format for frontend rendering."""

    id: str = Field(description="Unique dashboard identifier")
    generated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="When this dashboard was generated",
    )
    widgets: List[Widget] = Field(
        description="List of widgets to display", min_length=1
    )
    theme: ColorScheme = Field(description="Complete theme configuration")
    persona: PersonaProfile = Field(description="User's persona profile")


# ============================================================================
# CONFIGURATION
# ============================================================================


class Config(BaseModel):
    """Application configuration."""

    # API Keys
    anthropic_api_key: str = Field(description="Anthropic API key for Claude")
    perplexity_api_key: str = Field(description="Perplexity API key")

    # External API keys for UI enrichment (optional)
    openweathermap_api_key: Optional[str] = Field(
        None,
        description="OpenWeatherMap API key for weather widgets",
    )
    youtube_api_key: Optional[str] = Field(
        None,
        description="YouTube Data API v3 key for video feeds",
    )
    ticketmaster_api_key: Optional[str] = Field(
        None,
        description="Ticketmaster API key for event discovery",
    )
    mapbox_api_key: Optional[str] = Field(
        None,
        description="Mapbox API token for geocoding and maps",
    )

    # Generation settings
    days_back: int = Field(
        default=30, ge=1, le=365, description="Days of data to analyze"
    )
    max_patterns: int = Field(
        default=8, ge=4, le=8, description="Maximum number of patterns to detect"
    )
    enable_search: bool = Field(
        default=True, description="Enable Perplexity search enrichment"
    )

    # Output settings
    output_dir: str = Field(
        default="~/.fabric-dashboard/dashboards", description="Output directory path"
    )
    auto_open_browser: bool = Field(
        default=True, description="Auto-open dashboard in browser"
    )

    # Debug settings
    debug: bool = Field(default=False, description="Enable debug mode")
    mock_mode: bool = Field(
        default=False, description="Use mock data instead of live APIs"
    )
