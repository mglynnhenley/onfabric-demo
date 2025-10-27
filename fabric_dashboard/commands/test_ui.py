"""Test UI generation command for development and testing."""

import asyncio
import json
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.table import Table

from fabric_dashboard.core.ui_generator import UIGenerator
from fabric_dashboard.models.schemas import Pattern, PersonaProfile

console = Console()


@click.command()
@click.option(
    "--mock",
    is_flag=True,
    default=True,
    help="Use mock mode (default: True)",
)
@click.option(
    "--output",
    type=click.Path(),
    help="Output JSON file path (optional)",
)
@click.option(
    "--verbose",
    is_flag=True,
    help="Show detailed component configurations",
)
def test_ui(
    mock: bool,
    output: Optional[str],
    verbose: bool,
):
    """
    Test UI component generation.

    This command generates UI components from sample patterns
    to test the UI Generator pipeline without running the full
    dashboard generation.

    Example:
        fabric-dashboard test-ui --verbose
        fabric-dashboard test-ui --output ui_result.json
    """
    asyncio.run(test_ui_generation(mock=mock, output_file=output, verbose=verbose))


async def test_ui_generation(
    mock: bool,
    output_file: Optional[str],
    verbose: bool,
):
    """
    Test UI generation pipeline.

    Args:
        mock: Use mock mode.
        output_file: Output JSON file path.
        verbose: Show detailed output.
    """
    console.print("\n[bold cyan]🧪 Testing UI Component Generation[/bold cyan]\n")

    # Step 1: Create sample patterns
    console.print("[bold]Step 1/3:[/bold] Creating sample patterns...")

    sample_patterns = create_sample_patterns()

    console.print(f"[green]✓[/green] Created {len(sample_patterns)} sample patterns\n")

    # Step 2: Create sample persona
    console.print("[bold]Step 2/3:[/bold] Creating sample persona...")

    sample_persona = create_sample_persona()

    console.print(f"[green]✓[/green] Created persona profile")
    console.print(f"[dim]  Style: {sample_persona.writing_style[:50]}...[/dim]")
    console.print(
        f"[dim]  Interests: {', '.join(sample_persona.interests[:3])}[/dim]\n"
    )

    # Step 3: Generate UI components
    console.print("[bold]Step 3/3:[/bold] Generating UI components...")

    try:
        generator = UIGenerator(mock_mode=mock)

        result = await generator.generate_components(sample_patterns, sample_persona)

        console.print(f"[green]✓[/green] Generated {len(result.components)} components\n")

        # Display results
        display_results(result, verbose)

        # Save to file if requested
        if output_file:
            save_results(result, output_file)
            console.print(f"\n[green]✓[/green] Results saved to {output_file}")

        console.print("\n[bold green]✨ UI generation test successful![/bold green]\n")

    except Exception as e:
        console.print(f"[red]✗ UI generation failed: {e}[/red]")
        import traceback

        traceback.print_exc()


def create_sample_patterns() -> list[Pattern]:
    """Create sample patterns for testing."""
    return [
        Pattern(
            title="Tech Enthusiast",
            description="Strong interest in technology, AI, and software development",
            confidence=0.95,
            keywords=["technology", "AI", "machine learning", "python", "coding"],
            interaction_count=150,
        ),
        Pattern(
            title="San Francisco Explorer",
            description="Frequent searches and engagement with San Francisco area activities",
            confidence=0.88,
            keywords=["san francisco", "bay area", "california", "travel", "local"],
            interaction_count=75,
        ),
        Pattern(
            title="Continuous Learner",
            description="Regular consumption of educational content and tutorials",
            confidence=0.82,
            keywords=["learning", "tutorial", "course", "education", "guide"],
            interaction_count=120,
        ),
        Pattern(
            title="Event Networker",
            description="Shows interest in meetups, conferences, and networking events",
            confidence=0.76,
            keywords=["meetup", "conference", "networking", "event", "community"],
            interaction_count=45,
        ),
        Pattern(
            title="Research Reader",
            description="Engages with in-depth articles and research papers",
            confidence=0.73,
            keywords=["research", "paper", "article", "analysis", "study"],
            interaction_count=60,
        ),
    ]


def create_sample_persona() -> PersonaProfile:
    """Create sample persona for testing."""
    return PersonaProfile(
        writing_style="analytical and data-driven with clear arguments",
        interests=["technology", "AI", "travel", "learning", "networking"],
        activity_level="high",
        professional_context="software engineer",
        tone_preference="balanced and professional",
        content_depth_preference="deep_dives",
    )


def display_results(result, verbose: bool):
    """Display generation results in a nice format."""
    # Create summary table
    table = Table(title="Generated Components", show_header=True, header_style="bold cyan")
    table.add_column("#", style="dim", width=3)
    table.add_column("Type", style="magenta", width=15)
    table.add_column("Title", style="cyan", width=25)
    table.add_column("Pattern", style="yellow", width=20)
    table.add_column("Confidence", style="green", width=10)

    for i, component in enumerate(result.components, 1):
        table.add_row(
            str(i),
            component.component_type,
            component.title[:25],
            component.pattern_title[:20],
            f"{component.confidence:.2f}",
        )

    console.print(table)

    # Show detailed configurations if verbose
    if verbose:
        console.print("\n[bold]Component Details:[/bold]\n")

        for i, component in enumerate(result.components, 1):
            console.print(f"[bold cyan]{i}. {component.component_type}[/bold cyan]")
            console.print(f"   Title: {component.title}")
            console.print(f"   Pattern: {component.pattern_title}")
            console.print(f"   Confidence: {component.confidence:.2f}")

            # Show type-specific details
            if component.component_type == "info-card":
                console.print(f"   Location: {component.location}")
                console.print(f"   Units: {component.units}")
                console.print(f"   Show Forecast: {component.show_forecast}")
            elif component.component_type == "map-card":
                console.print(f"   Center: ({component.center_lat:.4f}, {component.center_lng:.4f})")
                console.print(f"   Zoom: {component.zoom}")
                console.print(f"   Markers: {len(component.markers)}")
            elif component.component_type == "video-feed":
                console.print(f"   Search: {component.search_query}")
                console.print(f"   Max Results: {component.max_results}")
                console.print(f"   Duration: {component.video_duration}")
            elif component.component_type == "event-calendar":
                console.print(f"   Search: {component.search_query}")
                console.print(f"   Location: {component.location or 'Any'}")
                console.print(f"   Date Range: {component.date_range_days} days")
            elif component.component_type == "task-list":
                console.print(f"   Tasks: {len(component.tasks)}")
                console.print(f"   Type: {component.list_type}")
                for task in component.tasks[:3]:  # Show first 3 tasks
                    console.print(f"      • {task.text} [{task.priority}]")
            elif component.component_type == "content-card":
                console.print(f"   Article: {component.article_title[:50]}...")
                console.print(f"   Source: {component.source_name}")
                console.print(f"   Search: {component.search_query}")

            console.print()


def save_results(result, output_file: str):
    """Save results to JSON file."""
    output_path = Path(output_file)

    # Convert to dict for JSON serialization
    data = {
        "generated_at": result.generated_at.isoformat(),
        "total_patterns_analyzed": result.total_patterns_analyzed,
        "components": [
            {
                "component_type": c.component_type,
                "title": c.title,
                "pattern_title": c.pattern_title,
                "confidence": c.confidence,
                **{
                    k: v
                    for k, v in c.model_dump().items()
                    if k not in ["component_type", "title", "pattern_title", "confidence"]
                },
            }
            for c in result.components
        ],
    }

    with open(output_path, "w") as f:
        json.dump(data, f, indent=2, default=str)


if __name__ == "__main__":
    test_ui()
