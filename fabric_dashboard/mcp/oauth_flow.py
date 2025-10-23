"""OAuth 2.0 authorization flow manager."""

from typing import Any, Dict, Optional
import webbrowser

from requests_oauthlib import OAuth2Session

from fabric_dashboard.mcp.oauth_config import OAuthConfig
from fabric_dashboard.mcp.oauth_server import LocalRedirectServer
from fabric_dashboard.utils import logger


class OAuthFlowManager:
    """Manages OAuth 2.0 authorization code flow."""

    def __init__(self):
        """Initialize OAuth flow manager with config."""
        self.config = OAuthConfig()

    def get_authorization_url(self) -> str:
        """
        Generate OAuth authorization URL.

        Returns:
            Authorization URL to open in browser.
        """
        # Create OAuth2 session
        oauth = OAuth2Session(
            client_id=self.config.client_id,
            redirect_uri=self.config.redirect_uri,
            scope=self.config.scopes,
        )

        # Generate authorization URL
        authorization_url, state = oauth.authorization_url(
            self.config.authorization_url
        )

        logger.muted(f"Generated authorization URL with state: {state[:8]}...")
        return authorization_url

    def exchange_code_for_token(
        self,
        authorization_code: str,
        client_secret: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Exchange authorization code for access token.

        Args:
            authorization_code: The code received from OAuth callback.
            client_secret: Optional client secret for confidential clients.

        Returns:
            Token dictionary with access_token, or None if exchange fails.
        """
        logger.info("Exchanging authorization code for access token...")

        try:
            # Create OAuth2 session
            oauth = OAuth2Session(
                client_id=self.config.client_id,
                redirect_uri=self.config.redirect_uri,
            )

            # Exchange code for token
            token = oauth.fetch_token(
                self.config.token_url,
                code=authorization_code,
                client_secret=client_secret,  # Only needed if OnFabric requires it
                include_client_id=True,
            )

            logger.success("Successfully obtained access token")
            return token

        except Exception as e:
            logger.error(f"Failed to exchange code for token: {e}")
            return None

    def run_interactive_flow(self) -> Optional[Dict[str, Any]]:
        """
        Run complete interactive OAuth flow.

        This method:
        1. Starts local redirect server
        2. Opens browser to authorization URL
        3. Waits for callback with code
        4. Exchanges code for token

        Returns:
            Token dictionary, or None if flow fails.
        """
        logger.info("Starting OAuth authorization flow...")

        # Step 1: Start local redirect server
        server = LocalRedirectServer(port=self.config.redirect_port)

        # Step 2: Generate and open authorization URL
        auth_url = self.get_authorization_url()

        logger.info("Opening browser for authorization...")
        logger.info(f"If browser doesn't open, visit: {auth_url}")

        try:
            webbrowser.open(auth_url)
        except Exception as e:
            logger.warning(f"Could not auto-open browser: {e}")
            logger.info("Please manually open the URL above")

        # Step 3: Wait for callback
        authorization_code = server.wait_for_callback(timeout=300)

        if not authorization_code:
            logger.error("Failed to receive authorization code")
            return None

        # Step 4: Exchange code for token
        token = self.exchange_code_for_token(authorization_code)

        return token
