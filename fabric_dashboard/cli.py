"""Command-line interface for fabric_dashboard."""

import click

from fabric_dashboard import __version__


@click.group()
@click.version_option(version=__version__, prog_name="fabric-dashboard")
@click.pass_context
def cli(ctx: click.Context) -> None:
    """
    Fabric Intelligence Dashboard - Generate personalized AI-powered dashboards.

    A beautiful, design-first dashboard that analyzes your digital behavior
    from Fabric MCP and creates personalized content using Claude and Perplexity.
    """
    # Ensure context object exists
    ctx.ensure_object(dict)


# Import commands after defining cli group to avoid circular imports
from fabric_dashboard.commands import init, generate, test_ui, auth  # noqa: E402

cli.add_command(init.init_command)
cli.add_command(generate.generate)
cli.add_command(test_ui.test_ui)
cli.add_command(auth.auth)


def main() -> None:
    """Entry point for the CLI."""
    cli(obj={})


if __name__ == "__main__":
    main()
