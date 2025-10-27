"""Rich console logging for fabric_dashboard."""

from typing import Any, Optional

from rich.console import Console
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TaskID,
    TextColumn,
    TimeElapsedColumn,
)
from rich.theme import Theme

# Custom theme for fabric_dashboard
custom_theme = Theme(
    {
        "info": "cyan",
        "success": "bold green",
        "warning": "bold yellow",
        "error": "bold red",
        "muted": "dim",
        "highlight": "bold magenta",
    }
)

# Global console instance
console = Console(theme=custom_theme)


def info(message: str, **kwargs: Any) -> None:
    """Print info message in cyan."""
    console.print(f"ℹ {message}", style="info", **kwargs)


def success(message: str, **kwargs: Any) -> None:
    """Print success message in green."""
    console.print(f"✓ {message}", style="success", **kwargs)


def warning(message: str, **kwargs: Any) -> None:
    """Print warning message in yellow."""
    console.print(f"⚠ {message}", style="warning", **kwargs)


def error(message: str, **kwargs: Any) -> None:
    """Print error message in red."""
    console.print(f"✗ {message}", style="error", **kwargs)


def muted(message: str, **kwargs: Any) -> None:
    """Print muted/dimmed message."""
    console.print(message, style="muted", **kwargs)


def highlight(message: str, **kwargs: Any) -> None:
    """Print highlighted message in magenta."""
    console.print(message, style="highlight", **kwargs)


def print_header(title: str) -> None:
    """Print a formatted header."""
    console.rule(f"[bold]{title}[/bold]", style="info")


def print_footer() -> None:
    """Print a separator line."""
    console.rule(style="muted")


def create_progress() -> Progress:
    """
    Create a Rich progress bar for tracking tasks.

    Returns:
        Progress object with custom columns.
    """
    return Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
        console=console,
    )


def create_simple_progress() -> Progress:
    """
    Create a simple Rich progress bar (spinner + text only).

    Returns:
        Progress object with minimal columns.
    """
    return Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        console=console,
    )


class ProgressTracker:
    """Context manager for progress tracking."""

    def __init__(self, description: str, total: Optional[int] = None):
        """
        Initialize progress tracker.

        Args:
            description: Description of the task.
            total: Total number of steps (None for indeterminate).
        """
        self.description = description
        self.total = total
        self.progress: Optional[Progress] = None
        self.task_id: Optional[TaskID] = None

    def __enter__(self) -> "ProgressTracker":
        """Start progress tracking."""
        if self.total:
            self.progress = create_progress()
        else:
            self.progress = create_simple_progress()

        self.progress.__enter__()
        self.task_id = self.progress.add_task(self.description, total=self.total)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop progress tracking."""
        if self.progress:
            self.progress.__exit__(exc_type, exc_val, exc_tb)

    def update(self, advance: int = 1, description: Optional[str] = None) -> None:
        """
        Update progress.

        Args:
            advance: Number of steps to advance.
            description: New description (optional).
        """
        if self.progress and self.task_id is not None:
            kwargs = {"advance": advance}
            if description:
                kwargs["description"] = description
            self.progress.update(self.task_id, **kwargs)


def print_config_summary(config: dict[str, Any]) -> None:
    """
    Print configuration summary in a formatted way.

    Args:
        config: Configuration dictionary.
    """
    from rich.table import Table

    table = Table(title="Configuration", show_header=False, box=None)
    table.add_column("Key", style="cyan")
    table.add_column("Value", style="white")

    for key, value in config.items():
        # Mask API keys
        if "key" in key.lower() or "token" in key.lower():
            if value:
                masked_value = f"{value[:8]}...{value[-4:]}" if len(value) > 12 else "***"
                table.add_row(key, masked_value)
            else:
                table.add_row(key, "[red]Not set[/red]")
        else:
            table.add_row(key, str(value))

    console.print(table)


def print_dashboard_summary(
    num_cards: int, generation_time: float, output_path: str
) -> None:
    """
    Print dashboard generation summary.

    Args:
        num_cards: Number of cards generated.
        generation_time: Time taken in seconds.
        output_path: Path to output file.
    """
    from rich.panel import Panel

    summary = f"""
[bold green]Dashboard Generated Successfully![/bold green]

📊 Cards: {num_cards}
⏱️  Time: {generation_time:.1f}s
📁 Output: {output_path}
"""
    console.print(Panel(summary.strip(), border_style="green"))
