"""Token storage for OAuth credentials."""

import os
from pathlib import Path
from typing import Any, Dict, Optional

from dotenv import load_dotenv, set_key

from fabric_dashboard.utils import logger


class TokenStorage:
    """Handles storing and loading OAuth tokens from .env file."""

    def __init__(self, env_file: Optional[str] = None):
        """
        Initialize token storage.

        Args:
            env_file: Path to .env file. If None, uses .env in project root.
        """
        if env_file is None:
            # Default to .env in project root
            project_root = Path(__file__).parent.parent.parent
            env_file = project_root / ".env"

        self.env_file = Path(env_file)

        # Create .env file if it doesn't exist
        if not self.env_file.exists():
            logger.info(f"Creating .env file at {self.env_file}")
            self.env_file.touch()

    def save_token(self, token: Dict[str, Any]) -> None:
        """
        Save OAuth token to .env file.

        Args:
            token: Token dictionary from OAuth flow.
        """
        logger.info(f"Saving OAuth token to {self.env_file}")

        # Save access token (required)
        if "access_token" in token:
            set_key(str(self.env_file), "ONFABRIC_ACCESS_TOKEN", token["access_token"])

        # Save token type
        if "token_type" in token:
            set_key(str(self.env_file), "ONFABRIC_TOKEN_TYPE", token["token_type"])

        # Save refresh token (if provided)
        if "refresh_token" in token:
            set_key(str(self.env_file), "ONFABRIC_REFRESH_TOKEN", token["refresh_token"])

        # Save expiry (if provided)
        if "expires_in" in token:
            set_key(str(self.env_file), "ONFABRIC_TOKEN_EXPIRES_IN", str(token["expires_in"]))

        logger.success("OAuth token saved successfully")

    def load_token(self) -> Optional[Dict[str, Any]]:
        """
        Load OAuth token from .env file.

        Returns:
            Token dictionary, or None if no token found.
        """
        # Load environment variables from .env file
        load_dotenv(self.env_file)

        # Check if access token exists
        access_token = os.getenv("ONFABRIC_ACCESS_TOKEN")

        if not access_token:
            return None

        # Build token dictionary
        token = {
            "access_token": access_token,
            "token_type": os.getenv("ONFABRIC_TOKEN_TYPE", "Bearer"),
        }

        # Add optional fields if present
        if refresh_token := os.getenv("ONFABRIC_REFRESH_TOKEN"):
            token["refresh_token"] = refresh_token

        if expires_in := os.getenv("ONFABRIC_TOKEN_EXPIRES_IN"):
            try:
                token["expires_in"] = int(expires_in)
            except ValueError:
                logger.warning(f"Invalid expires_in value: {expires_in}")

        logger.muted("Loaded OAuth token from .env")
        return token

    def has_token(self) -> bool:
        """
        Check if OAuth token exists.

        Returns:
            True if token exists, False otherwise.
        """
        load_dotenv(self.env_file)
        return os.getenv("ONFABRIC_ACCESS_TOKEN") is not None
