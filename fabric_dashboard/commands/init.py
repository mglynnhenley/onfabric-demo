"""Initialize fabric_dashboard configuration."""

import click
from pydantic import ValidationError

from fabric_dashboard.models.schemas import Config
from fabric_dashboard.utils import config as config_utils
from fabric_dashboard.utils import logger


@click.command(name="init")
@click.option(
    "--anthropic-key",
    help="Anthropic API key (or set ANTHROPIC_API_KEY env var)",
    type=str,
)
@click.option(
    "--perplexity-key",
    help="Perplexity API key (or set PERPLEXITY_API_KEY env var)",
    type=str,
)
@click.option(
    "--days-back",
    help="Number of days of data to analyze (default: 30)",
    type=int,
    default=30,
)
@click.option(
    "--force",
    is_flag=True,
    help="Overwrite existing configuration",
)
def init_command(
    anthropic_key: str | None,
    perplexity_key: str | None,
    days_back: int,
    force: bool,
) -> None:
    """
    Initialize configuration for Fabric Dashboard.

    This command will prompt you for your API keys and save them to
    ~/.fabric-dashboard/config.yaml

    You can also set environment variables:
    - ANTHROPIC_API_KEY
    - PERPLEXITY_API_KEY
    """
    logger.print_header("Fabric Dashboard Setup")

    # Check if config already exists
    existing_config = config_utils.load_config()
    if existing_config and not force:
        logger.warning(
            "Configuration already exists at ~/.fabric-dashboard/config.yaml"
        )
        logger.info("Use --force to overwrite, or update specific values manually")
        logger.muted("\nCurrent configuration:")
        logger.print_config_summary(existing_config.model_dump())
        return

    logger.info("Let's set up your Fabric Dashboard configuration.\n")

    # Prompt for Anthropic API key if not provided
    if not anthropic_key:
        anthropic_key = click.prompt(
            "Anthropic API key (starts with sk-ant-)",
            type=str,
            hide_input=True,
        )

    # Prompt for Perplexity API key if not provided
    if not perplexity_key:
        perplexity_key = click.prompt(
            "Perplexity API key (starts with pplx-)",
            type=str,
            hide_input=True,
        )

    # Validate and create config
    try:
        # Ensure we have both keys (Click should prevent None, but type checker needs assurance)
        if not anthropic_key or not perplexity_key:
            logger.error("\n✗ Both API keys are required")
            raise click.Abort()

        new_config = Config(
            anthropic_api_key=anthropic_key,
            perplexity_api_key=perplexity_key,
            days_back=days_back,
        )

        # Save configuration
        config_utils.save_config(new_config)

        logger.success("\n✓ Configuration saved successfully!")
        logger.info(f"Config location: {config_utils.CONFIG_FILE}\n")

        # Show summary (with masked keys)
        logger.print_config_summary(new_config.model_dump())

        logger.print_footer()
        logger.info("\nNext steps:")
        logger.info("  1. Ensure Fabric MCP is running")
        logger.info("  2. Run: fabric-dashboard generate")
        logger.muted("\nFor help: fabric-dashboard --help")

    except ValidationError as e:
        logger.error("\n✗ Invalid configuration:")
        for error in e.errors():
            field = " → ".join(str(x) for x in error["loc"])
            logger.error(f"  {field}: {error['msg']}")
        raise click.Abort()
    except Exception as e:
        logger.error(f"\n✗ Failed to save configuration: {e}")
        raise click.Abort()
