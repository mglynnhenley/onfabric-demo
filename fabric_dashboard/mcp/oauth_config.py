"""OAuth configuration for OnFabric MCP authentication."""

from typing import List


class OAuthConfig:
    """OAuth 2.0 configuration for OnFabric MCP."""

    def __init__(self):
        """Initialize OAuth configuration."""
        # TODO: These values should come from OnFabric documentation
        # For now, using placeholder values that need to be updated
        self.client_id = "fabric-dashboard"  # Replace with actual client ID

        # OnFabric OAuth endpoints (update these URLs)
        self.authorization_url = "https://onfabric.com/oauth/authorize"
        self.token_url = "https://onfabric.com/oauth/token"

        # Local redirect server configuration
        self.redirect_uri = "http://localhost:8080/callback"
        self.redirect_port = 8080

        # OAuth scopes - what permissions we're requesting
        # Update based on what OnFabric MCP access requires
        self.scopes: List[str] = ["mcp:read", "mcp:write"]
