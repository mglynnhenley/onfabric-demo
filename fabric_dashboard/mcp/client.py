"""Base MCP client for fabric_dashboard."""

from typing import Any, Optional

from fabric_dashboard.mcp.token_storage import TokenStorage
from fabric_dashboard.utils import logger


class MCPClient:
    """Base Model Context Protocol client."""

    def __init__(self, server_name: str, connection_params: Optional[dict[str, Any]] = None):
        """
        Initialize MCP client.

        Args:
            server_name: Name of the MCP server to connect to.
            connection_params: Optional connection parameters.
        """
        self.server_name = server_name
        self.connection_params = connection_params or {}
        self._connected = False
        self.access_token: Optional[str] = None
        self.token_type: str = "Bearer"

    def is_authenticated(self) -> bool:
        """
        Check if client has valid authentication token.

        Returns:
            True if access token is loaded, False otherwise.
        """
        return self.access_token is not None

    def connect(self) -> bool:
        """
        Connect to MCP server.

        Returns:
            True if connection successful, False otherwise.
        """
        try:
            logger.info(f"Connecting to MCP server: {self.server_name}")

            # Load OAuth token
            storage = TokenStorage()
            token = storage.load_token()

            if not token:
                logger.error("No OAuth token found. Please run 'fabric-dashboard auth' first.")
                return False

            # Store token for API calls
            self.access_token = token.get("access_token")
            self.token_type = token.get("token_type", "Bearer")

            if not self.access_token:
                logger.error("Invalid token: missing access_token")
                return False

            logger.muted(f"Loaded OAuth token: {self.access_token[:8]}...")

            # TODO: Use access_token to establish real MCP connection
            # For now, just mark as connected
            self._connected = True

            logger.success(f"Connected to {self.server_name} (OAuth authenticated)")
            return True

        except Exception as e:
            logger.error(f"Failed to connect to MCP server: {e}")
            self._connected = False
            return False

    def disconnect(self) -> None:
        """Disconnect from MCP server."""
        if self._connected:
            logger.info(f"Disconnecting from {self.server_name}")
            self._connected = False
            self.access_token = None

    def is_connected(self) -> bool:
        """Check if connected to MCP server."""
        return self._connected

    def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> Any:
        """
        Call an MCP tool.

        Args:
            tool_name: Name of the tool to call.
            arguments: Tool arguments.

        Returns:
            Tool result.

        Raises:
            RuntimeError: If not connected to MCP server.
        """
        if not self._connected:
            raise RuntimeError(f"Not connected to MCP server: {self.server_name}")

        if not self.is_authenticated():
            raise RuntimeError("Not authenticated. Please run 'fabric-dashboard auth' first.")

        logger.muted(f"Calling MCP tool: {tool_name}")

        # TODO: Implement actual tool calling with OAuth token in headers
        # Headers should include: Authorization: Bearer {self.access_token}
        raise NotImplementedError("MCP tool calling not yet implemented")

    def __enter__(self) -> "MCPClient":
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
