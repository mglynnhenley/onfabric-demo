"""CLI command for OnFabric OAuth authentication."""

import click
from rich.console import Console

from fabric_dashboard.mcp.oauth_flow import OAuthFlowManager
from fabric_dashboard.mcp.token_storage import TokenStorage

console = Console()


@click.command()
def auth():
    """
    Authenticate with OnFabric using OAuth 2.0.

    This command:
    1. Opens your browser to OnFabric login page
    2. Waits for you to log in and authorize the app
    3. Saves the access token to your .env file

    After authentication, you can use other commands to access your OnFabric data.
    """
    console.print("\n[bold cyan]🔐 OnFabric OAuth Authentication[/bold cyan]\n")

    # Check if already authenticated
    storage = TokenStorage()
    if storage.has_token():
        console.print("⚠️  You are already authenticated.")

        if not click.confirm("Do you want to re-authenticate?", default=False):
            console.print("\n✅ Keeping existing authentication.\n")
            return 0

        console.print("\n🔄 Re-authenticating...\n")

    # Run OAuth flow
    console.print("[dim]Step 1: Opening browser for authorization...[/dim]")
    console.print("[dim]Step 2: Log in to OnFabric in your browser[/dim]")
    console.print("[dim]Step 3: Authorize Fabric Dashboard to access your data[/dim]")
    console.print("[dim]Step 4: Wait for redirect (this may take a moment)[/dim]\n")

    flow_manager = OAuthFlowManager()
    token = flow_manager.run_interactive_flow()

    if not token:
        console.print("\n[bold red]❌ Authentication failed[/bold red]")
        console.print("Please try again or check your internet connection.\n")
        raise click.Abort()

    # Save token
    storage.save_token(token)

    console.print("\n[bold green]✅ Authentication successful![/bold green]")
    console.print("Your access token has been saved to .env\n")
    console.print("You can now use other commands to access your OnFabric data.\n")

    return 0
