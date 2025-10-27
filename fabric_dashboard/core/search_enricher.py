"""Search enricher module using Perplexity API to add live research data to patterns."""

import asyncio
from typing import Optional

import httpx
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from tenacity import retry, stop_after_attempt, wait_exponential

from fabric_dashboard.models.schemas import EnrichedPattern, Pattern, SearchResult
from fabric_dashboard.utils import logger
from fabric_dashboard.utils.cache import get_cache
from fabric_dashboard.utils.config import get_config


class SearchQueries(BaseModel):
    """Structured output for search query generation."""

    queries: list[str] = Field(
        min_length=2,
        max_length=2,
        description="Exactly 2 search queries designed to find content for writing interesting articles",
    )


class SearchEnricher:
    """Enriches patterns with live research data from Perplexity API."""

    def __init__(self, mock_mode: bool = False):
        """
        Initialize search enricher.

        Args:
            mock_mode: If True, use mock search results instead of real API calls.
        """
        self.mock_mode = mock_mode
        self.api_key: Optional[str] = None
        self.llm: Optional[ChatAnthropic] = None
        self.base_url = "https://api.perplexity.ai"
        self.model = "sonar"
        self.timeout = 20.0  # 20 second timeout per request
        self.cache = get_cache()

        if not mock_mode:
            config = get_config()
            if not config:
                raise RuntimeError("Configuration not found. Run 'fabric-dashboard init' first.")

            self.api_key = config.perplexity_api_key
            if not self.api_key or self.api_key == "placeholder":
                logger.warning("Perplexity API key not configured. Using mock mode.")
                self.mock_mode = True

            # Initialize LLM for query generation
            self.llm = ChatAnthropic(
                model_name="claude-sonnet-4-5",
                temperature=0.7,  # Moderate creativity for query generation
                api_key=config.anthropic_api_key,
                timeout=30,
                max_tokens=1024,
                stop=None,
            )

    async def enrich_patterns(
        self, patterns: list[Pattern], max_queries_per_pattern: int = 2
    ) -> list[EnrichedPattern]:
        """
        Enrich multiple patterns with search results in parallel.

        Args:
            patterns: List of patterns to enrich.
            max_queries_per_pattern: Maximum search queries to generate per pattern (default: 2).

        Returns:
            List of EnrichedPattern objects with search results.
        """
        if self.mock_mode:
            return self._generate_mock_enriched_patterns(patterns)

        logger.info(f"Enriching {len(patterns)} patterns with Perplexity search...")

        # Generate search queries for all patterns (async)
        all_queries = []
        pattern_query_mapping = []  # Track which queries belong to which pattern

        query_tasks = [
            self._generate_search_queries(pattern, max_queries_per_pattern)
            for pattern in patterns
        ]
        all_pattern_queries = await asyncio.gather(*query_tasks, return_exceptions=True)

        for i, pattern in enumerate(patterns):
            queries_result = all_pattern_queries[i]
            if isinstance(queries_result, Exception):
                logger.warning(f"Query generation failed for pattern '{pattern.title}': {queries_result}")
                # Fallback to simple queries
                queries = self._generate_fallback_queries(pattern, max_queries_per_pattern)
            else:
                queries = queries_result

            for query in queries:
                all_queries.append(query)
                pattern_query_mapping.append(pattern)

        logger.info(f"Generated {len(all_queries)} search queries")

        # Execute searches in batches to avoid overwhelming API
        batch_size = 2  # Process 2 searches at a time
        search_results = []

        for i in range(0, len(all_queries), batch_size):
            batch_queries = all_queries[i:i + batch_size]
            batch_patterns = pattern_query_mapping[i:i + batch_size]

            # Execute batch in parallel
            batch_tasks = [
                self._search_with_retry(query, batch_patterns[j])
                for j, query in enumerate(batch_queries)
            ]

            batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)
            search_results.extend(batch_results)

            # Small delay between batches to avoid rate limiting
            if i + batch_size < len(all_queries):
                await asyncio.sleep(1)  # 1 second delay between batches

        # Group results by pattern
        pattern_results: dict[str, list[SearchResult]] = {
            pattern.title: [] for pattern in patterns
        }

        for i, result in enumerate(search_results):
            pattern = pattern_query_mapping[i]
            if isinstance(result, Exception):
                logger.warning(f"Search failed for '{all_queries[i]}': {result}")
                continue
            if result:
                pattern_results[pattern.title].append(result)

        # Build enriched patterns
        enriched_patterns = []
        for pattern in patterns:
            enriched = EnrichedPattern(
                pattern=pattern,
                search_results=pattern_results[pattern.title][:5],  # Max 5 per pattern
            )
            enriched_patterns.append(enriched)

        logger.success(f"Enriched {len(enriched_patterns)} patterns")
        return enriched_patterns

    async def _generate_search_queries(
        self, pattern: Pattern, max_queries: int = 2
    ) -> list[str]:
        """
        Generate intelligent search queries using LLM for a pattern.

        Args:
            pattern: Pattern to generate queries for.
            max_queries: Maximum number of queries to generate (always 2).

        Returns:
            List of search query strings designed to find article-worthy content.
        """
        if self.mock_mode or not self.llm:
            return self._generate_fallback_queries(pattern, max_queries)

        try:
            # Build prompt
            prompt = self._build_query_generation_prompt()

            # Create structured LLM
            structured_llm = self.llm.with_structured_output(SearchQueries)

            # Create chain
            chain = prompt | structured_llm

            # Execute
            result = await asyncio.to_thread(
                chain.invoke,
                {
                    "pattern_title": pattern.title,
                    "pattern_description": pattern.description,
                    "keywords": ", ".join(pattern.keywords) if pattern.keywords else "N/A",
                    "confidence": pattern.confidence,
                }
            )

            logger.info(f"Generated {len(result.queries)} queries for pattern '{pattern.title}'")
            return result.queries

        except Exception as e:
            logger.warning(f"LLM query generation failed for '{pattern.title}': {e}")
            return self._generate_fallback_queries(pattern, max_queries)

    def _generate_fallback_queries(
        self, pattern: Pattern, max_queries: int = 2
    ) -> list[str]:
        """
        Generate simple fallback search queries when LLM is unavailable.

        Args:
            pattern: Pattern to generate queries for.
            max_queries: Maximum number of queries to generate.

        Returns:
            List of simple search query strings.
        """
        queries = []

        # Query 1: Direct pattern title with current year for relevance
        queries.append(f"{pattern.title} latest news trends developments 2025")

        # Query 2: Combine top keywords with insights
        if pattern.keywords and len(pattern.keywords) >= 2:
            top_keywords = " ".join(pattern.keywords[:3])
            queries.append(f"{top_keywords} future trends insights")

        return queries[:max_queries]

    def _build_query_generation_prompt(self) -> ChatPromptTemplate:
        """
        Build the prompt template for search query generation.

        Returns:
            ChatPromptTemplate for query generation.
        """
        system_message = """You are an expert research strategist who designs search queries to find compelling content for article writing.

Your task: Generate exactly 2 search queries that will find the most interesting, insightful, and article-worthy content related to the given pattern.

## Query Design Principles:
- **Depth over breadth**: Seek queries that uncover insights, trends, controversies, or emerging developments
- **Article-worthy angles**: Think like a journalist - what would make someone want to read about this?
- **Specificity**: Be specific enough to find quality sources, but not so narrow that results are limited
- **Complementary perspectives**: The 2 queries should cover different angles (e.g., current trends + future implications, or mainstream view + emerging alternatives)
- **Recency-aware**: When relevant, incorporate signals for fresh, current information
- **Avoid generic terms**: Instead of "trends" alone, use "emerging developments", "recent breakthroughs", "industry shifts", etc.

## Query Examples:
For a pattern about "AI in Healthcare":
- Good: "AI diagnostic tools clinical accuracy studies 2025"
- Good: "healthcare AI implementation challenges patient privacy concerns"
- Bad: "AI healthcare trends" (too generic)
- Bad: "artificial intelligence medical" (too vague)

For a pattern about "Remote Work Culture":
- Good: "hybrid work policies employee productivity research 2025"
- Good: "remote work culture challenges team collaboration solutions"
- Bad: "remote work trends" (too generic)

Your queries should help a writer create content that is:
- Informative and insight-driven
- Relevant to someone with this interest pattern
- Current and forward-looking
- Based on credible sources and research

Return exactly 2 queries."""

        human_message = """Generate 2 search queries for finding article-worthy content about this pattern:

**Pattern Title:** {pattern_title}
**Description:** {pattern_description}
**Keywords:** {keywords}
**Confidence:** {confidence}

Design queries that will find compelling, insightful content for writing an interesting article."""

        return ChatPromptTemplate.from_messages([
            ("system", system_message),
            ("human", human_message),
        ])

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True,
    )
    async def _search_with_retry(self, query: str, pattern: Pattern) -> Optional[SearchResult]:
        """
        Execute a search with retry logic.

        Args:
            query: Search query.
            pattern: Pattern this query is for (used for cache key).

        Returns:
            SearchResult or None if search fails.
        """
        # Check cache first (30min TTL)
        cache_key = f"search:{pattern.title}:{query}"
        cached = self.cache.get(cache_key)
        if cached:
            logger.info(f"Cache hit for query: '{query}'")
            return SearchResult(**cached)

        logger.info(f"Searching Perplexity: '{query}'")

        try:
            result = await self._execute_search(query)

            # Cache successful result (TTL is set in cache initialization)
            if result:
                self.cache.set(cache_key, result.model_dump())

            return result

        except Exception as e:
            logger.error(f"Search failed for '{query}': {e}")
            raise

    async def _execute_search(self, query: str) -> Optional[SearchResult]:
        """
        Execute a single Perplexity API search.

        Args:
            query: Search query.

        Returns:
            SearchResult or None if request fails.
        """
        if not self.api_key:
            raise RuntimeError("Perplexity API key not configured")

        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful research assistant. Provide concise, factual information with sources. Write as if you are a journalist who is an expert on the topic. Suggest new content to read",
                },
                {
                    "role": "user",
                    "content": query,
                },
            ],
            "max_tokens": 500,
            "temperature": 0.2,  # Low temperature for factual content
            "return_citations": True,  # Automatic, but kept for clarity
            "search_recency_filter": "month",  # Prioritize recent content from last month
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()

                data = response.json()

                # Extract content and sources
                content = data.get("choices", [{}])[0].get("message", {}).get("content", "")

                # Extract sources from citations
                sources = []
                citations = data.get("citations", [])
                for citation in citations[:10]:  # Max 10 sources
                    if isinstance(citation, str):
                        sources.append(citation)
                    elif isinstance(citation, dict) and "url" in citation:
                        sources.append(citation["url"])

                if not content:
                    logger.warning(f"Empty content from Perplexity for query: '{query}'")
                    return None

                return SearchResult(
                    query=query,
                    content=content,
                    sources=sources,
                    relevance_score=1.0,
                )

            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:
                    logger.warning(f"Rate limit hit for query: '{query}'")
                    raise  # Will trigger retry
                elif e.response.status_code >= 500:
                    logger.error(f"Perplexity server error: {e}")
                    raise  # Will trigger retry
                else:
                    logger.error(f"HTTP error {e.response.status_code}: {e}")
                    return None

            except httpx.TimeoutException:
                logger.warning(f"Timeout for query: '{query}'")
                raise  # Will trigger retry

            except Exception as e:
                logger.error(f"Unexpected error during search: {e}")
                return None

    def _generate_mock_enriched_patterns(
        self, patterns: list[Pattern]
    ) -> list[EnrichedPattern]:
        """
        Generate mock enriched patterns for testing.

        Args:
            patterns: Patterns to enrich.

        Returns:
            List of EnrichedPattern objects with mock search results.
        """
        logger.info("Using mock search enrichment")

        enriched_patterns = []
        for pattern in patterns:
            # Generate 2 mock search results per pattern
            mock_results = [
                SearchResult(
                    query=f"{pattern.title} latest trends/developments ",
                    content=f"Recent research on {pattern.title} shows significant progress. "
                    f"Key trends include {', '.join(pattern.keywords[:3])} with growing impact across industries. "
                    f"Experts suggest this area will continue evolving rapidly.",
                    sources=[
                        "https://example.com/research-1",
                        "https://example.com/article-2",
                    ],
                    relevance_score=0.95,
                ),
                SearchResult(
                    query=f"{' '.join(pattern.keywords[:3])} trends 2025",
                    content=f"Analysis of {pattern.description[:100]}... indicates strong momentum. "
                    f"Industry leaders highlight practical applications and future potential.",
                    sources=["https://example.com/trends-1"],
                    relevance_score=0.88,
                ),
            ]

            enriched = EnrichedPattern(
                pattern=pattern,
                search_results=mock_results,
            )
            enriched_patterns.append(enriched)

        logger.success(f"Generated {len(enriched_patterns)} mock enriched patterns")
        return enriched_patterns
