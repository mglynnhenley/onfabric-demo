"""Pattern detection module using Claude for behavioral analysis."""

from typing import Optional

from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from tenacity import retry, stop_after_attempt, wait_exponential

from fabric_dashboard.models.schemas import Pattern, PersonaProfile, UserData
from fabric_dashboard.utils import logger
from fabric_dashboard.utils.config import get_config


class PatternDetectionResult(BaseModel):
    """Result from pattern detection containing patterns and persona."""

    patterns: list[Pattern] = Field(
        min_length=4,
        max_length=5,
        description="4-5 detected behavioral patterns with concise descriptions",
    )
    persona: PersonaProfile = Field(
        description="Extracted user persona profile",
    )


class PatternDetector:
    """Detects behavioral patterns and persona from user data using Claude."""

    def __init__(self, mock_mode: bool = False):
        """
        Initialize pattern detector.

        Args:
            mock_mode: If True, use mock detection instead of real LLM calls.
        """
        self.mock_mode = mock_mode
        self.llm: Optional[ChatAnthropic] = None

        if not mock_mode:
            config = get_config()
            if not config:
                raise RuntimeError("Configuration not found. Run 'fabric-dashboard init' first.")

            self.llm = ChatAnthropic(
                model_name="claude-sonnet-4-5",
                temperature=1.0,  # Higher temperature for creative pattern detection
                api_key=config.anthropic_api_key,
                timeout=60,
                max_tokens=3000,  # Reduced - concise descriptions need less space
                stop=None,
            )

    def detect_patterns(self, user_data: UserData) -> PatternDetectionResult:
        """
        Detect patterns and extract persona from user data.

        Args:
            user_data: User data from Fabric MCP.

        Returns:
            PatternDetectionResult with patterns and persona.
        """
        if self.mock_mode:
            return self._mock_detection(user_data)
        else:
            return self._detect_with_claude(user_data)

    def _mock_detection(self, user_data: UserData) -> PatternDetectionResult:
        """
        Generate mock patterns for testing.

        Args:
            user_data: User data (used for realistic mock generation).

        Returns:
            PatternDetectionResult with mock patterns.
        """
        logger.info("Using mock pattern detection")

        # Use existing persona from user_data if available
        persona = user_data.persona if user_data.persona else PersonaProfile(
            writing_style="analytical and balanced",
            interests=["technology", "design"],
            activity_level="moderate",
            professional_context=None,
            age_range=None,
        )

        # Generate basic patterns
        patterns = [
            Pattern(
                title="Digital Explorer",
                description="Active engagement with technology and digital trends",
                confidence=0.85,
                keywords=["technology", "digital", "innovation"],
                interaction_count=len(user_data.interactions),
            ),
            Pattern(
                title="Curious Learner",
                description="Demonstrates curiosity through diverse search queries",
                confidence=0.78,
                keywords=["learning", "research", "knowledge"],
                interaction_count=len(user_data.interactions) // 2,
            ),
            Pattern(
                title="Content Curator",
                description="Saves and organizes interesting content for later",
                confidence=0.72,
                keywords=["curation", "saving", "organization"],
                interaction_count=len(user_data.interactions) // 3,
            ),
            Pattern(
                title="Community Participant",
                description="Engages with others through comments and discussions",
                confidence=0.68,
                keywords=["community", "engagement", "discussion"],
                interaction_count=len(user_data.interactions) // 4,
            ),
        ]

        logger.success(f"Generated {len(patterns)} mock patterns")
        return PatternDetectionResult(patterns=patterns, persona=persona)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True,
    )
    def _detect_with_claude(self, user_data: UserData) -> PatternDetectionResult:
        """
        Detect patterns using Claude API with retry logic.

        Args:
            user_data: User data from Fabric MCP.

        Returns:
            PatternDetectionResult with detected patterns.

        Raises:
            RuntimeError: If detection fails after retries.
        """
        if not self.llm:
            raise RuntimeError("LLM not initialized")

        logger.info("Detecting patterns with Claude")

        try:
            # Build prompt
            prompt = self._build_prompt()

            # Prepare user data summary for context
            data_context = self._prepare_data_context(user_data)

            # Create structured LLM using with_structured_output()
            structured_llm = self.llm.with_structured_output(PatternDetectionResult)

            # Create chain: prompt -> structured LLM
            chain = prompt | structured_llm

            # Execute
            result = chain.invoke({
                "data_context": data_context,
            })

            logger.success(f"Detected {len(result.patterns)} patterns")
            return result

        except Exception as e:
            logger.error(f"Pattern detection failed: {e}")
            # Fallback to mock detection
            logger.warning("Falling back to mock pattern detection")
            return self._mock_detection(user_data)

    def _build_prompt(self) -> ChatPromptTemplate:
        """
        Build the prompt template for pattern detection.

        Returns:
            ChatPromptTemplate for pattern detection.
        """
        system_message = """You are an expert behavioral analyst specializing in digital footprint analysis.

Your task is to analyze user interaction data and:
1. Identify exactly 4-5 distinct behavioral patterns or interest themes
2. Extract a detailed persona profile including writing style preferences

## CRITICAL: Keep Descriptions Concise
- **Each pattern description must be 2-3 sentences maximum (under 80 words)**
- Focus on the most important insights - what makes this pattern unique and why it matters
- Be punchy and direct - no rambling explanations

## Guidelines for Pattern Detection:
- Look for clusters of related activities, topics, or behaviors
- Identify patterns that reveal interests, habits, or professional focus
- Rank patterns by engagement signals (frequency, depth, consistency)
- Create compelling titles that capture the essence of each pattern
- Write CONCISE descriptions (2-3 sentences) that explain WHY this pattern matters
- Assign confidence scores based on evidence strength (0.0-1.0)

## Guidelines for Persona Extraction:
- Generate a natural, descriptive writing_style (NOT just keywords)
- Examples of good writing_style descriptions:
  * "analytical and data-driven with clear, structured arguments"
  * "narrative and emotionally engaging with vivid storytelling"
  * "provocative and contrarian, challenging conventional wisdom"
  * "accessible and educational, breaking down complex topics"
- Generate a natural tone_preference description
- Identify key interests and professional context
- Assess activity level and content depth preferences

Be creative and insightful. Look beyond surface-level observations. But remember: BREVITY IS KEY."""

        human_message = """Analyze this user's digital activity:

{data_context}

Detect exactly 4-5 distinct behavioral patterns with CONCISE descriptions (2-3 sentences max) and extract their persona profile."""

        return ChatPromptTemplate.from_messages([
            ("system", system_message),
            ("human", human_message),
        ])

    def _prepare_data_context(self, user_data: UserData) -> str:
        """
        Prepare user data context for the LLM prompt.

        Args:
            user_data: User data from Fabric MCP.

        Returns:
            Formatted string with user data context.
        """
        # Extract key information
        summary = user_data.summary
        interactions = user_data.interactions

        # Sample interactions for context (max 20 to avoid token limits)
        sampled = interactions[:20] if len(interactions) > 20 else interactions

        context_parts = [
            f"## Summary Statistics",
            f"- Total interactions: {summary.total_interactions}",
            f"- Date range: {summary.date_range_start.date()} to {summary.date_range_end.date()}",
            f"- Days analyzed: {summary.days_analyzed}",
            f"- Platforms: {', '.join(summary.platforms)}",
            f"- Top themes: {', '.join(summary.top_themes) if summary.top_themes else 'None identified'}",
            "",
            "## Sample Interactions",
        ]

        for i, interaction in enumerate(sampled, 1):
            context_parts.append(f"\n### Interaction {i}")
            context_parts.append(f"Platform: {interaction.get('platform', 'unknown')}")
            context_parts.append(f"Type: {interaction.get('type', 'unknown')}")
            if interaction.get('content'):
                content = interaction['content'][:200]  # Truncate long content
                context_parts.append(f"Content: {content}")
            if interaction.get('query'):
                context_parts.append(f"Query: {interaction['query']}")
            if interaction.get('topics'):
                context_parts.append(f"Topics: {', '.join(interaction['topics'])}")

        return "\n".join(context_parts)
