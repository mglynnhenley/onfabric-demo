"""Content writer module using Claude for persona-matched card content generation."""

import asyncio
from typing import Optional

from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from tenacity import retry, stop_after_attempt, wait_exponential

from fabric_dashboard.models.schemas import (
    CardContent,
    CardSize,
    EnrichedPattern,
    PersonaProfile,
)
from fabric_dashboard.utils import logger
from fabric_dashboard.utils.config import get_config


class ContentWriter:
    """Writes persona-matched content for dashboard cards using Claude."""

    def __init__(self, mock_mode: bool = False):
        """
        Initialize content writer.

        Args:
            mock_mode: If True, generate mock content instead of real LLM calls.
        """
        self.mock_mode = mock_mode
        self.llm: Optional[ChatAnthropic] = None

        if not mock_mode:
            config = get_config()
            if not config:
                raise RuntimeError("Configuration not found. Run 'fabric-dashboard init' first.")

            self.llm = ChatAnthropic(
                model_name="claude-sonnet-4-5",
                temperature=0.7,  # Balanced creativity and consistency
                api_key=config.anthropic_api_key,
                timeout=90,  # Longer timeout for content generation
                max_tokens=4096,
                stop=None,
            )

    async def generate_cards(
        self,
        enriched_patterns: list[EnrichedPattern],
        persona: PersonaProfile,
        card_sizes: list[CardSize],
    ) -> list[CardContent]:
        """
        Generate content for multiple cards in parallel.

        Args:
            enriched_patterns: Patterns with search results.
            persona: User's persona profile.
            card_sizes: List of card sizes for each pattern.

        Returns:
            List of CardContent objects (4-8 cards).
        """
        if self.mock_mode:
            return self._generate_mock_cards(enriched_patterns, card_sizes)

        # Generate cards in parallel
        tasks = []
        for i, (enriched_pattern, size) in enumerate(zip(enriched_patterns, card_sizes)):
            task = self._generate_card_with_retry(enriched_pattern, persona, size, i + 1)
            tasks.append(task)

        logger.info(f"Generating {len(tasks)} cards in parallel...")

        # Execute all tasks concurrently
        cards = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out failed generations and replace with fallback
        valid_cards = []
        for i, card in enumerate(cards):
            if isinstance(card, Exception):
                logger.error(f"Card {i + 1} generation failed: {card}")
                # Generate fallback card
                fallback = self._generate_fallback_card(
                    enriched_patterns[i], card_sizes[i]
                )
                valid_cards.append(fallback)
            else:
                valid_cards.append(card)

        logger.success(f"Generated {len(valid_cards)} cards")
        return valid_cards

    def _generate_mock_cards(
        self,
        enriched_patterns: list[EnrichedPattern],
        card_sizes: list[CardSize],
    ) -> list[CardContent]:
        """
        Generate mock cards for testing.

        Args:
            enriched_patterns: Patterns to generate cards for.
            card_sizes: Sizes for each card.

        Returns:
            List of mock CardContent objects.
        """
        logger.info("Using mock card generation")

        cards = []
        for pattern, size in zip(enriched_patterns, card_sizes):
            # Generate mock content based on size
            word_counts = {
                CardSize.LARGE: 450,
                CardSize.MEDIUM: 275,
                CardSize.SMALL: 175,
                CardSize.COMPACT: 125,
            }

            target_words = word_counts[size]
            body = " ".join([f"Word{i}" for i in range(target_words)])

            card = CardContent(
                title=pattern.pattern.title,
                description=pattern.pattern.description[:150],
                body=body,
                reading_time_minutes=max(1, target_words // 200),
                sources=["https://example.com"],
                size=size,
                confidence=pattern.pattern.confidence,
                pattern_title=pattern.pattern.title,
            )
            cards.append(card)

        logger.success(f"Generated {len(cards)} mock cards")
        return cards

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True,
    )
    async def _generate_card_with_retry(
        self,
        enriched_pattern: EnrichedPattern,
        persona: PersonaProfile,
        size: CardSize,
        card_number: int,
    ) -> CardContent:
        """
        Generate a single card with retry logic.

        Args:
            enriched_pattern: Pattern with search results.
            persona: User's persona profile.
            size: Card size.
            card_number: Card number for logging.

        Returns:
            CardContent object.
        """
        if not self.llm:
            raise RuntimeError("LLM not initialized")

        logger.info(f"Generating card {card_number} ({size.value})...")

        try:
            # Build prompt
            prompt = self._build_prompt(size)

            # Prepare context
            context = self._prepare_context(enriched_pattern, persona, size)

            # Create structured LLM
            structured_llm = self.llm.with_structured_output(CardContent)

            # Create chain
            chain = prompt | structured_llm

            # Execute
            result = await chain.ainvoke({"context": context})

            # Set additional fields
            result.confidence = enriched_pattern.pattern.confidence
            result.pattern_title = enriched_pattern.pattern.title

            logger.success(
                f"✓ Card {card_number} generated ({result.word_count()} words)"
            )
            return result

        except Exception as e:
            logger.error(f"Card {card_number} generation failed: {e}")
            raise

    def _build_prompt(self, size: CardSize) -> ChatPromptTemplate:
        """
        Build prompt template for card content generation.

        Args:
            size: Card size (determines word count target).

        Returns:
            ChatPromptTemplate for content generation.
        """
        # Word count targets
        word_targets = {
            CardSize.LARGE: "400-500 words",
            CardSize.MEDIUM: "250-300 words",
            CardSize.SMALL: "150-200 words",
            CardSize.COMPACT: "100-150 words",
        }

        target = word_targets[size]

        system_message = f"""You are an expert content writer creating personalized dashboard cards.

Your task is to write engaging, informative content that matches the user's persona and interests. Make an effort to make it not sound AI generated. The idea is that it reads like a blog post, but doesn't seem personalised. Write as if you are a journalist who is an expert on the topic. You should rather write factually about the sources.

## Content Requirements:

**Length**: {target} (STRICT - this is critical for layout)
**Format**: Markdown paragraphs ONLY - absolutely NO headings/headers
**Style**: Match the user's writing style and tone exactly
**Quality**: High-quality, well-researched, engaging

## Writing Guidelines:

**Match the Persona**:
- Adapt to the user's writing_style (e.g., "analytical and data-driven" → use data, clear arguments)
- Match their tone_preference (e.g., "formal" → professional language, "casual" → conversational)

**Content Structure**:
- **Title**: Short and specific factual title (max 150 chars)
- **Description**: Punchy subtitle/tagline that complements title (max 300 chars)
- **Body**: Flowing prose with multiple paragraphs
  * Use **bold** for emphasis on key terms or names
  * Use *italics* for publication names, quotes, or subtle emphasis
  * Use bullet lists when listing multiple items
  * Create natural paragraph breaks for readability
  * Concrete examples and specific details
  * What has been said by who in a consistent argument

**Writing Style Examples**:
- "analytical and data-driven" → Use statistics, clear structure, evidence-based arguments
- "narrative and engaging" → Tell stories, use vivid language, emotional connection
- "provocative and contrarian" → Challenge assumptions, ask tough questions
- "accessible and educational" → Break down complex ideas, teach clearly

**Sources**:
- Include 2-5 relevant source URLs
- Can be from search results or general knowledge
- Must be real, accessible URLs

**Reading Time**:
- Calculate honestly: ~200 words per minute
- {target} = approximately {self._estimate_reading_time(size)} minutes

## Critical Constraints:

1. **WORD COUNT MUST BE EXACT**: {target} (±20% tolerance)
2. **ABSOLUTELY NO MARKDOWN HEADERS** in the body (no #, ##, ###, etc.)
3. **Body = paragraphs only**, separated by blank lines
4. **Title and description are separate fields** (not part of body)
5. **All fields are required**

REMINDER: The body field should contain ONLY paragraphs and formatting like bold/italics/lists. Do NOT include any headers (# symbols) in the body.

Your response will be automatically validated against a Pydantic schema."""

        human_message = """Write dashboard card content for this pattern:

{context}

Create engaging, persona-matched content that brings this pattern to life."""

        return ChatPromptTemplate.from_messages([
            ("system", system_message),
            ("human", human_message),
        ])

    def _estimate_reading_time(self, size: CardSize) -> int:
        """Estimate reading time based on card size."""
        word_counts = {
            CardSize.LARGE: 450,
            CardSize.MEDIUM: 275,
            CardSize.SMALL: 175,
            CardSize.COMPACT: 125,
        }
        return max(1, word_counts[size] // 200)

    def _prepare_context(
        self,
        enriched_pattern: EnrichedPattern,
        persona: PersonaProfile,
        size: CardSize,
    ) -> str:
        """
        Prepare context for content generation.

        Args:
            enriched_pattern: Pattern with search results.
            persona: User's persona profile.
            size: Card size.

        Returns:
            Formatted context string.
        """
        pattern = enriched_pattern.pattern

        context_parts = [
            "## Pattern Information",
            f"**Title**: {pattern.title}",
            f"**Description**: {pattern.description}",
            f"**Keywords**: {', '.join(pattern.keywords[:10])}",
            f"**Confidence**: {pattern.confidence:.2f}",
            "",
            "## User Persona",
            f"**Writing Style**: {persona.writing_style}",
            f"**Tone Preference**: {persona.tone_preference}",
            f"**Interests**: {', '.join(persona.interests[:5])}",
            f"**Content Depth**: {persona.content_depth_preference}",
        ]

        if persona.professional_context:
            context_parts.append(f"**Professional Context**: {persona.professional_context}")

        # Add search results if available
        if enriched_pattern.search_results:
            context_parts.append("\n## Research Context (from Perplexity)")
            for i, result in enumerate(enriched_pattern.search_results[:3], 1):
                context_parts.append(f"\n### Result {i}")
                context_parts.append(f"Query: {result.query}")
                # Truncate content to avoid token limits
                content_preview = result.content[:500] if len(result.content) > 500 else result.content
                context_parts.append(f"Content: {content_preview}...")
                if result.sources:
                    context_parts.append(f"Sources: {', '.join(result.sources[:3])}")

        context_parts.append(f"\n## Card Size: {size.value}")

        return "\n".join(context_parts)

    def _generate_fallback_card(
        self, enriched_pattern: EnrichedPattern, size: CardSize
    ) -> CardContent:
        """
        Generate a fallback card when LLM generation fails.

        Args:
            enriched_pattern: Pattern to generate fallback for.
            size: Card size.

        Returns:
            Basic CardContent object.
        """
        logger.warning(f"Generating fallback card for: {enriched_pattern.pattern.title}")

        pattern = enriched_pattern.pattern

        # Generate basic content based on size
        word_targets = {
            CardSize.LARGE: 450,
            CardSize.MEDIUM: 275,
            CardSize.SMALL: 175,
            CardSize.COMPACT: 125,
        }

        target_words = word_targets[size]

        # Create simple but valid markdown content
        body_parts = [
            f"## {pattern.title}",
            "",
            pattern.description,
            "",
            "### Key Insights",
            "",
        ]

        # Add keywords as content
        for keyword in pattern.keywords[:5]:
            body_parts.append(f"- **{keyword}**: Relevant topic in this area")

        # Pad to reach target word count
        body_parts.append("")
        body_parts.append("### Overview")
        body_parts.append("")

        current_body = "\n".join(body_parts)
        current_words = len(current_body.split())

        # Add filler content to reach target
        if current_words < target_words:
            filler = "This pattern represents an important aspect of digital behavior and engagement. "
            words_needed = target_words - current_words
            body_parts.append(filler * (words_needed // len(filler.split()) + 1))

        body = "\n".join(body_parts)

        # Truncate to exact target (with tolerance)
        words = body.split()
        if len(words) > target_words * 1.2:
            words = words[:int(target_words * 1.1)]
            body = " ".join(words)

        return CardContent(
            title=pattern.title,
            description=pattern.description[:150],
            body=body,
            reading_time_minutes=self._estimate_reading_time(size),
            sources=[],
            size=size,
            confidence=pattern.confidence,
            pattern_title=pattern.title,
        )
