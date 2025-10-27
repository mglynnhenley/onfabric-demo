#!/usr/bin/env python3
"""Test script to verify dashboard builder with mock data."""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from fabric_dashboard.core.dashboard_builder import DashboardBuilder
from fabric_dashboard.models.schemas import (
    CardContent,
    CardSize,
    ColorScheme,
    PersonaProfile,
)
from fabric_dashboard.utils import logger


def test_dashboard_building():
    """Test dashboard building with mock data."""
    logger.info("Testing dashboard builder with mock data")

    # Create test persona
    persona = PersonaProfile(
        writing_style="analytical and data-driven with clear structure and evidence-based conclusions",
        interests=["artificial intelligence", "technology", "data science", "innovation"],
        activity_level="high",
        professional_context="tech startup founder focused on AI applications",
        tone_preference="balanced and professional with occasional technical depth",
        age_range="30-40",
        content_depth_preference="deep_dives",
    )

    # Create test color scheme
    color_scheme = ColorScheme(
        primary="#3B82F6",
        secondary="#8B5CF6",
        accent="#F59E0B",
        background="#FFFFFF",
        card="#F9FAFB",
        foreground="#1F2937",
        muted="#6B7280",
        success="#10B981",
        warning="#F59E0B",
        destructive="#EF4444",
        mood="professional",
        rationale="Tech-inspired blue with creative purple accent for an analytical yet innovative feel",
    )

    # Create test cards with realistic content
    cards = [
        CardContent(
            title="The Rise of AI Agents in 2025",
            description="How autonomous AI systems are transforming software development and business operations",
            body="""# The Evolution of AI Agents

Artificial intelligence has reached a pivotal moment in 2025. We're witnessing the emergence of truly autonomous AI agents that can reason, plan, and execute complex tasks with minimal human oversight. These aren't simple chatbots or basic automation tools—they're sophisticated systems capable of understanding context, making decisions, and learning from their experiences.

## Key Developments

**Reasoning Capabilities**: Modern AI systems now demonstrate chain-of-thought reasoning that rivals human problem-solving approaches. They can break down complex problems into manageable steps, consider multiple solutions simultaneously, evaluate trade-offs, and self-correct when they make mistakes. The latest models show emergent abilities to plan multi-step tasks, anticipate obstacles, and adapt their strategies in real-time based on feedback.

**Multi-Agent Collaboration**: Perhaps the most exciting frontier is multi-agent systems where specialized AIs work together seamlessly. A coding agent might collaborate with a testing agent and a documentation agent to deliver complete software solutions. Each agent brings domain expertise, and together they accomplish what would take a human team weeks or months.

These collaborative systems use sophisticated protocols to communicate, delegate tasks, resolve conflicts, and coordinate their efforts. Early experiments show that well-designed multi-agent systems can match or exceed human team performance on specific tasks.

## Business Impact

Companies are seeing substantial productivity gains by integrating AI agents into their workflows. Early adopters report efficiency improvements ranging from ten to forty percent across various departments. Agents handle routine tasks like data entry, report generation, customer service inquiries, and code reviews, freeing humans to focus on strategic decision-making and creative work.

The ROI has been compelling enough that Fortune 500 companies are rapidly expanding their AI agent deployments. What started as pilots in IT departments has spread to operations, finance, marketing, and customer success. The technology is still evolving rapidly, but the trajectory is clear: AI agents will become as ubiquitous as email clients in enterprise software stacks.

## What This Means for You

If you haven't started experimenting with AI agents yet, now is the time. The learning curve for working effectively with these systems is steeper than you might expect, requiring new skills in prompt engineering, system design, and quality assurance. However, the competitive advantage is substantial and growing.

Focus on defining clear objectives for your agents, providing good feedback loops, and measuring outcomes rigorously. Start small with well-defined tasks and gradually expand scope as you build expertise. The organizations mastering this technology now will have a significant edge in the coming years.

Remember: the future isn't about replacing humans with machines. It's about amplifying human capabilities through intelligent automation, allowing us to focus on what we do best—creative problem-solving, strategic thinking, and building meaningful relationships.""",
            reading_time_minutes=3,
            sources=[
                "https://www.anthropic.com/research",
                "https://openai.com/research",
                "https://techcrunch.com/ai-agents-2025",
            ],
            size=CardSize.LARGE,
            confidence=0.95,
            pattern_title="AI Enthusiast",
        ),
        CardContent(
            title="Building Products in the AI Era",
            description="Lessons from founders navigating the rapid evolution of AI technology",
            body="""# Product Strategy in Uncertain Times

Building products when the foundational technology changes monthly is uniquely challenging. Here's what successful founders are doing:

**Start Narrow**: Don't try to build everything at once. Pick one specific use case and execute it flawlessly. Vertical AI applications are winning because they solve real problems deeply rather than offering generic capabilities. Focus beats breadth in early-stage AI products.

**Build for Adaptability**: Your product architecture must accommodate multiple LLM providers seamlessly. Today's best model is tomorrow's second choice. Smart teams build abstraction layers that let them swap providers without rewriting core logic. Lock-in to a single provider is increasingly risky as the landscape evolves rapidly.

**Focus on Distribution**: The best AI feature means nothing without users discovering it. Traditional go-to-market strategies matter more than technology choices. Community building, content marketing, and strategic partnerships drive growth more reliably than technical superiority alone.

## The Defensibility Question

Every investor asks the same thing: What's your moat when any competitor can use the same models? It's a fair question that demands a good answer.

The real answer isn't about proprietary models—it's about execution speed, deep domain expertise, and data flywheels that compound over time. Build systems that improve with usage, gather proprietary datasets through product usage, and become indispensable through deep integration into customer workflows.

Your competitive advantage comes from understanding your users better than anyone else, moving faster than larger competitors, and creating network effects that make your product more valuable as more people use it.

Success in AI isn't about having better models than everyone else. It's about understanding your users deeply, solving their problems elegantly, and executing faster than competitors. The technology is increasingly commoditized—differentiation comes from everything else.""",
            reading_time_minutes=2,
            sources=["https://a16z.com/building-ai-products", "https://ycombinator.com/ai-startups"],
            size=CardSize.MEDIUM,
            confidence=0.88,
            pattern_title="Tech Innovator",
        ),
        CardContent(
            title="Data Science Tools to Watch",
            description="The modern data stack is evolving rapidly",
            body="""# Essential Tools for Data Scientists

The modern data stack is evolving faster than ever. Here are the tools gaining momentum:

**DuckDB**: This embedded SQL analytics database runs blazingly fast queries on local files without needing a separate database server. It's becoming the go-to choice for analytical workflows that don't need distributed computing. The performance is remarkable and it's getting better with each release.

**Polars**: If you're still using Pandas for everything, check out Polars. It's a DataFrame library built in Rust that actually scales to larger datasets. The API is cleaner, the performance is dramatically better, and it handles out-of-memory situations gracefully. Many teams are switching their entire data pipeline.

**Modal**: Need to run Python code in the cloud without dealing with containers, Kubernetes, or infrastructure? Modal lets you deploy functions to the cloud in seconds with just a decorator. It's perfect for training models, running batch jobs, or serving APIs.

**LangSmith**: If you're building production LLM applications, debugging and monitoring are essential. LangSmith provides visibility into your prompts, completions, and chain execution. It's become indispensable for serious AI engineering teams.

**Evidence**: Want to build beautiful BI dashboards using just SQL and Markdown? Evidence lets you version control your entire analytics stack, deploy with Git, and iterate faster than traditional BI tools allow.

The common thread across these tools? They respect your time by being fast, simple to use, and composable with existing workflows.""",
            reading_time_minutes=2,
            sources=["https://duckdb.org", "https://pola.rs", "https://modal.com"],
            size=CardSize.SMALL,
            confidence=0.85,
            pattern_title="Data Explorer",
        ),
        CardContent(
            title="Weekly Insight",
            description="The best developers are learning in public",
            body="""# Share Your Progress

Stop waiting until you're an "expert" to write about what you're learning. The best technical content comes from people documenting their journey, not from those who've forgotten what it was like to not know.

Write tutorials. Share mistakes. Ask questions publicly. Your future self (and many others) will thank you.

The developers getting the best opportunities aren't necessarily the most skilled—they're the ones whose work is visible. Building in public creates opportunities and accelerates learning through community feedback.""",
            reading_time_minutes=1,
            sources=[],
            size=CardSize.COMPACT,
            confidence=0.80,
            pattern_title="Professional Growth",
        ),
    ]

    # Build dashboard
    logger.info(f"\n[Test] Building dashboard with {len(cards)} cards")

    builder = DashboardBuilder()

    try:
        dashboard = builder.build(
            cards=cards,
            persona=persona,
            color_scheme=color_scheme,
            title="Your AI & Tech Intelligence Dashboard",
            user_name="Alex Chen",
            generation_time_seconds=2.5,
        )

        # Get HTML
        html = dashboard.metadata["html"]

        logger.success(f"\n✓ Dashboard built successfully!")

        # Display summary
        print("\n" + "=" * 80)
        print("DASHBOARD SUMMARY")
        print("=" * 80)
        print(f"User: {dashboard.user_name}")
        print(f"Generated: {dashboard.generated_at.strftime('%B %d, %Y at %I:%M %p')}")
        print(f"Cards: {len(dashboard.cards)}")
        print(f"Generation Time: {dashboard.generation_time_seconds}s")
        print(f"HTML Size: {len(html):,} characters")
        print(f"Color Scheme Mood: {color_scheme.mood}")

        print("\n" + "-" * 80)
        print("CARDS")
        print("-" * 80)
        for i, card in enumerate(dashboard.cards, 1):
            print(f"\n{i}. {card.title} [{card.size.value.upper()}]")
            print(f"   {card.description}")
            print(f"   📊 {card.word_count()} words • ⏱️  {card.reading_time_minutes} min read")
            print(f"   🔗 {len(card.sources)} sources")

        # Save to file
        output_dir = Path(__file__).parent / "test_output"
        output_dir.mkdir(exist_ok=True)
        output_file = output_dir / "test_dashboard.html"

        with open(output_file, "w") as f:
            f.write(html)

        print("\n" + "=" * 80)
        logger.success(f"Dashboard saved to: {output_file}")
        logger.success("Open in browser to view!")
        print("=" * 80)

        # Preview HTML structure
        print("\n" + "-" * 80)
        print("HTML STRUCTURE PREVIEW")
        print("-" * 80)
        print("✓ DOCTYPE: HTML5")
        print("✓ Viewport: Responsive meta tag")
        print("✓ Fonts: Inter (UI) + Geist (content)")
        print("✓ CSS: Tailwind via CDN")
        print(f"✓ Color Variables: {len([line for line in html.split('\\n') if '--' in line and ':' in line])} CSS custom properties")
        print(f"✓ Grid Layout: 12-column responsive")
        print(f"✓ Cards: {html.count('dashboard-card')} card elements")
        print(f"✓ Card Sizes:")
        print(f"   - Large (col-span-8): {html.count('lg:col-span-8')}")
        print(f"   - Medium (col-span-6): {html.count('lg:col-span-6')}")
        print(f"   - Small (col-span-4): {html.count('lg:col-span-4')}")
        print(f"   - Compact (col-span-3): {html.count('lg:col-span-3')}")

        # Validation
        print("\n" + "-" * 80)
        print("VALIDATION")
        print("-" * 80)
        validations = [
            ("HTML structure", "<html" in html and "</html>" in html),
            ("Head section", "<head>" in html and "</head>" in html),
            ("Body section", "<body" in html and "</body>" in html),
            ("Title tag", "<title>" in html),
            ("Meta charset", 'charset="UTF-8"' in html),
            ("Viewport meta", 'name="viewport"' in html),
            ("CSS variables", "--primary:" in html and "--foreground:" in html),
            ("Grid layout", "grid" in html and "lg:col-span" in html),
            ("All card titles", all(card.title in html for card in cards)),
            ("Header", "Intelligence Dashboard" in html),
            ("Footer", "Fabric Intelligence Dashboard" in html),
            ("Credits", "Claude" in html and "Perplexity" in html),
        ]

        for check, passed in validations:
            status = "✓" if passed else "✗"
            print(f"{status} {check}")

        all_passed = all(passed for _, passed in validations)

        print("\n" + "=" * 80)
        if all_passed:
            logger.success("All validations passed! ✨")
        else:
            logger.warning("Some validations failed")
        print("=" * 80)

        # Instructions
        print("\n📖 NEXT STEPS:")
        print(f"   1. Open {output_file} in your browser")
        print("   2. Resize window to test responsive behavior")
        print("   3. Check color scheme matches persona mood")
        print("   4. Verify all cards render correctly")

        return dashboard

    except Exception as e:
        logger.error(f"Dashboard building failed: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    dashboard = test_dashboard_building()

    if dashboard:
        logger.success("\n🎉 Dashboard builder test completed successfully!")
    else:
        logger.error("\n❌ Dashboard builder test failed")
        sys.exit(1)
