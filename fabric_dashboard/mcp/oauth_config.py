"""OAuth configuration for OnFabric MCP authentication."""

from typing import List


class OAuthConfig:
    """OAuth 2.0 configuration for OnFabric MCP - Device Code Flow."""

    def __init__(self):
        """Initialize OAuth configuration for Device Code Flow."""
        # OnFabric OAuth client ID (extracted from Claude's auth flow)
        # This is a public client ID used by OnFabric for MCP access
        self.client_id = "UGZtoLYZap8A94TnLcaF37bkXoIsi2Vn"

        # OnFabric OAuth endpoints (Auth0-based)
        # Device Code Flow endpoints
        self.device_code_url = "https://auth.onfabric.io/oauth/device/code"
        self.token_url = "https://auth.onfabric.io/oauth/token"

        # Verification URI where user enters the code
        # This will be returned by device_code endpoint, but we can predict it
        self.verification_uri = "https://auth.onfabric.io/activate"

        # OAuth scopes for OnFabric MCP access
        # Using standard Auth0 scopes + offline_access for refresh token
        self.scopes: List[str] = ["openid", "profile", "email", "offline_access"]

        # Polling interval (seconds) - will be overridden by server response
        self.default_poll_interval = 5

        # Auth0 audience for API access (if required)
        self.audience = "https://api.onfabric.io"
