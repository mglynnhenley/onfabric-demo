"""Fabric MCP client wrapper."""

from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from fabric_dashboard.mcp.client import MCPClient
from fabric_dashboard.utils import logger


class FabricMCPClient(MCPClient):
    """Fabric-specific MCP client wrapper."""

    def __init__(self):
        """Initialize Fabric MCP client."""
        super().__init__(server_name="onfabric")

    def get_available_connections(self) -> list[dict[str, Any]]:
        """
        Get list of available user connections.

        Returns:
            List of connection dictionaries with provider and connection info.
        """
        if not self.is_connected():
            raise RuntimeError("Not connected to Fabric MCP")

        logger.muted("Fetching available connections from Fabric MCP")
        # TODO: Implement actual MCP call
        # This would call the get_available_connections_by_provider tool
        raise NotImplementedError("Fabric MCP get_available_connections not yet implemented")

    def query_threads(
        self,
        connection_id: str,
        interaction_types: list[str],
        from_date: datetime,
        to_date: datetime,
    ) -> dict[str, Any]:
        """
        Query threads for a specific connection and date range.

        Args:
            connection_id: UUID of the connection.
            interaction_types: List of interaction types to query.
            from_date: Start date for query.
            to_date: End date for query.

        Returns:
            Dictionary with threads data.
        """
        if not self.is_connected():
            raise RuntimeError("Not connected to Fabric MCP")

        logger.muted(
            f"Querying threads for connection {connection_id[:8]}... "
            f"({len(interaction_types)} interaction types)"
        )

        # TODO: Implement actual MCP call
        # This would call the query_threads tool
        raise NotImplementedError("Fabric MCP query_threads not yet implemented")

    def get_interaction_types(self) -> dict[str, Any]:
        """
        Get available interaction types grouped by provider.

        Returns:
            Dictionary of interaction types by provider.
        """
        if not self.is_connected():
            raise RuntimeError("Not connected to Fabric MCP")

        logger.muted("Fetching interaction types from Fabric MCP")
        # TODO: Implement actual MCP call
        raise NotImplementedError("Fabric MCP get_interaction_types not yet implemented")

    def fetch_user_data(self, days_back: int = 30) -> dict[str, Any]:
        """
        Fetch all available user data from Fabric MCP.

        This is a convenience method that:
        1. Gets available connections
        2. Queries threads for each connection
        3. Aggregates the data

        Args:
            days_back: Number of days of data to fetch.

        Returns:
            Dictionary with aggregated user data.
        """
        if not self.is_connected():
            raise RuntimeError("Not connected to Fabric MCP")

        logger.info(f"Fetching user data from Fabric MCP (last {days_back} days)")

        # Calculate date range
        to_date = datetime.now(timezone.utc)
        from_date = to_date - timedelta(days=days_back)

        # Get connections
        connections = self.get_available_connections()

        if not connections:
            logger.warning("No connections found in Fabric MCP")
            return {
                "connections": [],
                "threads": [],
                "date_range": {"from": from_date.isoformat(), "to": to_date.isoformat()},
            }

        # Query threads for each connection
        all_threads = []
        for connection in connections:
            connection_id = connection.get("connection_id")
            interaction_types = connection.get("interaction_types", [])

            if not interaction_types:
                logger.muted(
                    f"Skipping connection {connection_id[:8]}... (no interaction types)"
                )
                continue

            try:
                threads = self.query_threads(
                    connection_id=connection_id,
                    interaction_types=interaction_types,
                    from_date=from_date,
                    to_date=to_date,
                )
                all_threads.extend(threads.get("threads", []))
            except Exception as e:
                logger.warning(
                    f"Failed to query threads for connection {connection_id[:8]}...: {e}"
                )
                continue

        logger.success(
            f"Fetched {len(all_threads)} threads from {len(connections)} connections"
        )

        return {
            "connections": connections,
            "threads": all_threads,
            "date_range": {"from": from_date.isoformat(), "to": to_date.isoformat()},
            "total_threads": len(all_threads),
        }
