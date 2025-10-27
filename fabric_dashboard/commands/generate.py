"""Generate command for creating personalized dashboards."""

import asyncio
import webbrowser
from datetime import datetime
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

from fabric_dashboard.core.data_fetcher import DataFetcher
from fabric_dashboard.core.pattern_detector import PatternDetector
from fabric_dashboard.core.theme_generator import ThemeGenerator
from fabric_dashboard.core.search_enricher import SearchEnricher
from fabric_dashboard.core.content_writer import ContentWriter
from fabric_dashboard.core.ui_generator import UIGenerator
from fabric_dashboard.core.dashboard_builder import DashboardBuilder
from fabric_dashboard.models.schemas import CardSize
from fabric_dashboard.utils import logger
from fabric_dashboard.utils.config import get_config

console = Console()


@click.command()
@click.option(
    "--mock",
    is_flag=True,
    help="Use mock data instead of real API calls (for testing)",
)
@click.option(
    "--no-search",
    is_flag=True,
    help="Skip Perplexity search enrichment",
)
@click.option(
    "--output",
    type=click.Path(),
    help="Output directory for dashboard (default: ./dashboards)",
)
@click.option(
    "--debug",
    is_flag=True,
    help="Enable debug mode with verbose logging",
)
@click.option(
    "--days-back",
    type=int,
    default=30,
    help="Number of days of data to analyze (default: 30)",
)
@click.option(
    "--no-open",
    is_flag=True,
    help="Don't auto-open dashboard in browser",
)
def generate(
    mock: bool,
    no_search: bool,
    output: Optional[str],
    debug: bool,
    days_back: int,
    no_open: bool,
):
    """
    Generate a personalized intelligence dashboard.

    This command runs the full pipeline:
    1. Fetch user data from Fabric MCP (or use mock data)
    2. Detect patterns and extract persona profile
    3. Generate persona-matched color scheme
    4. Enrich patterns with live search data (optional)
    5. Write personalized card content
    6. Build final HTML dashboard
    7. Save and open in browser
    """
    # Run async pipeline
    asyncio.run(
        generate_dashboard(
            mock=mock,
            no_search=no_search,
            output_dir=output,
            debug=debug,
            days_back=days_back,
            no_open=no_open,
        )
    )


async def generate_dashboard(
    mock: bool,
    no_search: bool,
    output_dir: Optional[str],
    debug: bool,
    days_back: int,
    no_open: bool,
):
    """
    Main dashboard generation pipeline.

    Args:
        mock: Use mock data instead of real API calls.
        no_search: Skip Perplexity search enrichment.
        output_dir: Output directory path.
        debug: Enable debug logging.
        days_back: Number of days to analyze.
        no_open: Don't auto-open in browser.
    """
    start_time = datetime.now()

    console.print("\n[bold cyan]🎨 Fabric Intelligence Dashboard Generator[/bold cyan]\n")

    # Step 1: Initialize components
    console.print("[bold]Step 1/8:[/bold] Initializing components...")

    try:
        # Initialize all pipeline components
        data_fetcher = DataFetcher(mock_mode=mock)
        pattern_detector = PatternDetector(mock_mode=mock)
        theme_generator = ThemeGenerator(mock_mode=mock)
        search_enricher = SearchEnricher(mock_mode=mock or no_search)
        content_writer = ContentWriter(mock_mode=mock)
        ui_generator = UIGenerator(mock_mode=mock)
        dashboard_builder = DashboardBuilder()

        console.print("[green]✓[/green] Components initialized\n")

    except Exception as e:
        console.print(f"[red]✗ Failed to initialize components: {e}[/red]")
        return

    # Step 2: Fetch user data
    console.print("[bold]Step 2/8:[/bold] Fetching user data...")

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Loading user data...", total=None)

            # Fetch user data (uses mock data in mock mode, or real MCP in production)
            user_data = data_fetcher.fetch_user_data(days_back=days_back)

            progress.update(task, completed=True)

        if user_data:
            console.print(f"[green]✓[/green] Data fetched")
            console.print(f"[dim]  Interactions: {user_data.summary.total_interactions}[/dim]")
            console.print(f"[dim]  Platforms: {', '.join(user_data.summary.platforms)}[/dim]\n")
        else:
            console.print("[red]✗ Failed to fetch user data[/red]")
            return

    except Exception as e:
        console.print(f"[red]✗ Failed to fetch data: {e}[/red]")
        if debug:
            import traceback
            traceback.print_exc()
        return

    # Step 3: Detect patterns and extract persona
    console.print("[bold]Step 3/8:[/bold] Detecting patterns and persona profile...")

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Analyzing user behavior...", total=None)

            # Detect patterns (synchronous call - not async)
            result = pattern_detector.detect_patterns(user_data)
            patterns = result.patterns
            persona = result.persona

            progress.update(task, completed=True)

        console.print(f"[green]✓[/green] Detected {len(patterns)} patterns")
        console.print(f"[dim]  Persona: {persona.writing_style[:50]}...[/dim]\n")

    except Exception as e:
        console.print(f"[red]✗ Failed to detect patterns: {e}[/red]")
        if debug:
            import traceback
            traceback.print_exc()
        return

    # Step 4: Generate color scheme
    console.print("[bold]Step 4/8:[/bold] Generating personalized color scheme...")

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Creating color palette...", total=None)

            # Generate theme from persona and patterns (synchronous call)
            color_scheme = theme_generator.generate_theme(persona, patterns)

            progress.update(task, completed=True)

        console.print(f"[green]✓[/green] Color scheme generated")
        console.print(f"[dim]  Mood: {color_scheme.mood}[/dim]")
        console.print(f"[dim]  Primary: {color_scheme.primary}[/dim]\n")

    except Exception as e:
        console.print(f"[red]✗ Failed to generate theme: {e}[/red]")
        if debug:
            import traceback
            traceback.print_exc()
        return

    # Step 5: Enrich patterns with search data
    console.print("[bold]Step 5/8:[/bold] Enriching patterns with live research...")

    try:
        if no_search or mock:
            console.print("[dim]Skipping search enrichment (--no-search or --mock)[/dim]")
            enriched_patterns = [
                type('EnrichedPattern', (), {
                    'pattern': p,
                    'search_results': []
                })() for p in patterns
            ]
        else:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task("Searching latest insights...", total=None)

                # Enrich patterns with Perplexity search
                enriched_patterns = await search_enricher.enrich_patterns(patterns)

                progress.update(task, completed=True)

        console.print(f"[green]✓[/green] Patterns enriched\n")

    except Exception as e:
        console.print(f"[red]✗ Failed to enrich patterns: {e}[/red]")
        return

    # Step 6: Generate card content
    console.print("[bold]Step 6/8:[/bold] Writing personalized card content...")

    try:
        # Determine card sizes (mix of sizes for better layout)
        # We want 4-8 cards, so let's use the first 4-6 patterns
        num_cards = min(len(enriched_patterns), 6)
        enriched_patterns = enriched_patterns[:num_cards]

        # Mix of card sizes for visual variety
        if num_cards == 4:
            card_sizes = [CardSize.COMPACT, CardSize.SMALL, CardSize.MEDIUM, CardSize.LARGE]
        elif num_cards == 5:
            card_sizes = [CardSize.COMPACT, CardSize.SMALL, CardSize.SMALL, CardSize.MEDIUM, CardSize.LARGE]
        else:  # 6 cards
            card_sizes = [CardSize.COMPACT, CardSize.SMALL, CardSize.SMALL, CardSize.MEDIUM, CardSize.MEDIUM, CardSize.LARGE]

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console,
        ) as progress:
            task = progress.add_task(
                f"Generating {num_cards} cards...",
                total=num_cards
            )

            # Generate all cards in parallel
            cards = await content_writer.generate_cards(
                enriched_patterns, persona, card_sizes
            )

            progress.update(task, completed=num_cards)

        console.print(f"[green]✓[/green] Generated {len(cards)} cards")
        total_words = sum(card.word_count() for card in cards)
        console.print(f"[dim]  Total words: {total_words:,}[/dim]\n")

    except Exception as e:
        console.print(f"[red]✗ Failed to generate cards: {e}[/red]")
        return

    # Step 6b: Generate UI components
    console.print("[bold]Step 6b/8:[/bold] Generating interactive UI widgets...")

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Selecting UI components...", total=None)

            # Generate UI components from patterns
            ui_result = await ui_generator.generate_components(patterns, persona)
            ui_components = ui_result.components

            progress.update(task, completed=True)

        console.print(f"[green]✓[/green] Generated {len(ui_components)} UI components")
        console.print(f"[dim]  Types: {', '.join(set(c.component_type for c in ui_components))}[/dim]\n")

    except Exception as e:
        console.print(f"[red]✗ Failed to generate UI components: {e}[/red]")
        if debug:
            import traceback
            traceback.print_exc()
        # Set empty list on failure - dashboard will still work with just blog cards
        ui_components = []

    # Step 7: Build dashboard and save
    console.print("[bold]Step 7/8:[/bold] Building dashboard...")

    try:
        # Calculate generation time
        generation_time = (datetime.now() - start_time).total_seconds()

        # Build complete dashboard
        dashboard = dashboard_builder.build(
            cards=cards,
            ui_components=ui_components,
            persona=persona,
            color_scheme=color_scheme,
            user_name="User",  # TODO: Get from config or MCP data
            generation_time_seconds=generation_time,
        )

        # Determine output path
        if output_dir:
            output_path = Path(output_dir)
        else:
            output_path = Path.cwd() / "dashboards"

        output_path.mkdir(parents=True, exist_ok=True)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"dashboard_{timestamp}.html"
        file_path = output_path / filename

        # Save HTML to file
        html = dashboard.metadata["html"]
        with open(file_path, "w") as f:
            f.write(html)

        console.print(f"[green]✓[/green] Dashboard built and saved\n")

        # Display summary
        console.print("[bold cyan]📊 Generation Summary[/bold cyan]")
        console.print(f"  • Patterns detected: {len(patterns)}")
        console.print(f"  • Cards generated: {len(cards)}")
        console.print(f"  • Total words: {sum(card.word_count() for card in cards):,}")
        console.print(f"  • Color mood: {color_scheme.mood}")
        console.print(f"  • Generation time: {generation_time:.1f}s")
        console.print(f"  • Output: {file_path}")

        # Open in browser
        if not no_open:
            console.print("\n[dim]Opening dashboard in browser...[/dim]")
            webbrowser.open(f"file://{file_path.absolute()}")

        console.print("\n[bold green]✨ Dashboard generated successfully![/bold green]\n")

    except Exception as e:
        console.print(f"[red]✗ Failed to build dashboard: {e}[/red]")
        import traceback
        if debug:
            traceback.print_exc()
        return


if __name__ == "__main__":
    generate()
