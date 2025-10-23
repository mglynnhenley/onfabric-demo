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

    # Run OAuth Device Code Flow
    flow_manager = OAuthFlowManager()

    # Request device code
    console.print("📱 [bold]Requesting authorization code...[/bold]")
    device_data = flow_manager.request_device_code()

    if not device_data:
        console.print("\n[bold red]❌ Failed to start authorization[/bold red]")
        console.print("Please check your internet connection and try again.\n")
        raise click.Abort()

    # Display user code and instructions
    console.print("\n" + "="*60)
    console.print("[bold cyan]Please authorize Fabric Dashboard:[/bold cyan]\n")
    console.print(f"1. Open your browser and go to:")
    console.print(f"   [bold green]{device_data['verification_uri']}[/bold green]\n")
    console.print(f"2. Enter this code:")
    console.print(f"   [bold yellow]{device_data['user_code']}[/bold yellow]\n")
    console.print(f"3. Log in and authorize the application\n")
    console.print(f"⏱️  Code expires in {device_data['expires_in'] // 60} minutes")
    console.print("="*60 + "\n")

    # Poll for token
    console.print("⏳ Waiting for authorization...")
    console.print("[dim]You can authorize in your browser now...[/dim]\n")

    token = flow_manager.poll_for_token(
        device_code=device_data["device_code"],
        interval=device_data["interval"],
        timeout=device_data["expires_in"]
    )

    if not token:
        console.print("\n[bold red]❌ Authorization failed or timed out[/bold red]")
        console.print("Please try again.\n")
        raise click.Abort()

    # Save token
    storage.save_token(token)

    console.print("\n[bold green]✅ Authentication successful![/bold green]")
    console.print("Your access token has been saved to .env\n")
    console.print("You can now use other commands to access your OnFabric data.\n")

    return 0
