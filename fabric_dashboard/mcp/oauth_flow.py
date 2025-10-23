"""OAuth 2.0 Device Code Flow manager for OnFabric MCP."""

import time
from typing import Any, Dict, Optional

import requests

from fabric_dashboard.mcp.oauth_config import OAuthConfig
from fabric_dashboard.utils import logger


class OAuthFlowManager:
    """Manages OAuth 2.0 Device Code Flow (RFC 8628)."""

    def __init__(self):
        """Initialize OAuth flow manager with config."""
        self.config = OAuthConfig()

    def request_device_code(self) -> Optional[Dict[str, Any]]:
        """
        Request device code from OnFabric.

        Returns:
            Dictionary with device_code, user_code, verification_uri, interval, expires_in
            or None if request fails.
        """
        logger.info("Requesting device code from OnFabric...")

        try:
            response = requests.post(
                self.config.device_code_url,
                data={
                    "client_id": self.config.client_id,
                    "scope": " ".join(self.config.scopes),
                    "audience": self.config.audience,
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )

            if response.status_code == 200:
                data = response.json()
                logger.success("Device code obtained successfully")

                return {
                    "device_code": data["device_code"],
                    "user_code": data["user_code"],
                    "verification_uri": data.get("verification_uri_complete")
                    or data.get("verification_uri"),
                    "interval": data.get("interval", self.config.default_poll_interval),
                    "expires_in": data["expires_in"],
                }
            else:
                logger.error(f"Failed to get device code: {response.status_code}")
                logger.error(f"Response: {response.text}")
                return None

        except Exception as e:
            logger.error(f"Error requesting device code: {e}")
            return None

    def poll_for_token(
        self, device_code: str, interval: int = 5, timeout: int = 600
    ) -> Optional[Dict[str, Any]]:
        """
        Poll for access token until user authorizes.

        Args:
            device_code: The device code from request_device_code().
            interval: Seconds to wait between polls.
            timeout: Maximum seconds to wait for authorization.

        Returns:
            Token dictionary with access_token, or None if failed/declined/timeout.
        """
        logger.info("Polling for authorization...")

        start_time = time.time()

        while True:
            # Check timeout
            if time.time() - start_time > timeout:
                logger.error("Authorization timeout - user did not authorize in time")
                return None

            try:
                response = requests.post(
                    self.config.token_url,
                    data={
                        "client_id": self.config.client_id,
                        "device_code": device_code,
                        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                    },
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                )

                if response.status_code == 200:
                    # Success! User authorized
                    logger.success("Authorization successful!")
                    return response.json()

                # Handle errors
                error_data = response.json()
                error = error_data.get("error")

                if error == "authorization_pending":
                    # User hasn't authorized yet, keep waiting
                    logger.muted("Waiting for user authorization...")
                    time.sleep(interval)
                    continue

                elif error == "slow_down":
                    # Server wants us to slow down polling
                    interval += 5
                    logger.muted(f"Slowing down polling interval to {interval}s")
                    time.sleep(interval)
                    continue

                elif error == "access_denied":
                    # User declined authorization
                    logger.error("User declined authorization")
                    return None

                elif error == "expired_token":
                    # Device code expired
                    logger.error("Device code expired - please try again")
                    return None

                else:
                    # Unknown error
                    logger.error(f"Authorization error: {error}")
                    logger.error(f"Error description: {error_data.get('error_description')}")
                    return None

            except Exception as e:
                logger.error(f"Error polling for token: {e}")
                return None

    def run_interactive_flow(self) -> Optional[Dict[str, Any]]:
        """
        Run complete interactive Device Code Flow.

        This method:
        1. Requests device code
        2. Displays user code and verification URL
        3. Polls for access token
        4. Returns token when authorized

        Returns:
            Token dictionary, or None if flow fails.
        """
        logger.info("Starting OAuth Device Code Flow...")

        # Step 1: Request device code
        device_data = self.request_device_code()

        if not device_data:
            logger.error("Failed to initiate device code flow")
            return None

        # Step 2: Display instructions to user
        # (This will be handled by the auth command with rich formatting)
        logger.info(f"User code: {device_data['user_code']}")
        logger.info(f"Verification URL: {device_data['verification_uri']}")
        logger.info(f"Code expires in: {device_data['expires_in']} seconds")

        # Step 3: Poll for token
        token = self.poll_for_token(
            device_code=device_data["device_code"],
            interval=device_data["interval"],
            timeout=device_data["expires_in"],
        )

        return token
