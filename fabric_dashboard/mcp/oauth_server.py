"""Local HTTP server for OAuth redirect callback."""

import http.server
import socketserver
import threading
import urllib.parse
from typing import Optional

from fabric_dashboard.utils import logger


class CallbackHandler(http.server.BaseHTTPRequestHandler):
    """HTTP request handler for OAuth callback."""

    def do_GET(self):
        """Handle GET request from OAuth redirect."""
        # Parse the URL query parameters
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)

        # Extract authorization code from callback URL
        if "code" in params:
            # Store code in server instance
            self.server.authorization_code = params["code"][0]

            # Send success response to browser
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            html = """
            <html>
            <head><title>Authentication Successful</title></head>
            <body style="font-family: sans-serif; text-align: center; padding: 50px;">
                <h1>✅ Authentication Successful!</h1>
                <p>You can close this window and return to your terminal.</p>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
        else:
            # Handle error (no code in callback)
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            error = params.get("error", ["Unknown error"])[0]
            html = f"""
            <html>
            <head><title>Authentication Failed</title></head>
            <body style="font-family: sans-serif; text-align: center; padding: 50px;">
                <h1>❌ Authentication Failed</h1>
                <p>Error: {error}</p>
                <p>Please close this window and try again.</p>
            </body>
            </html>
            """
            self.wfile.write(html.encode())

    def log_message(self, format, *args):
        """Suppress default HTTP server logging."""
        # Only log errors, not every request
        if "404" in str(args) or "500" in str(args):
            logger.warning(f"OAuth callback error: {args}")


class LocalRedirectServer:
    """Local HTTP server to receive OAuth callback."""

    def __init__(self, port: int = 8080):
        """
        Initialize local redirect server.

        Args:
            port: Port to run the server on (default: 8080).
        """
        self.port = port
        self.authorization_code: Optional[str] = None
        self._server: Optional[socketserver.TCPServer] = None

    def wait_for_callback(self, timeout: int = 300) -> Optional[str]:
        """
        Start server and wait for OAuth callback.

        Args:
            timeout: Maximum seconds to wait for callback (default: 300 = 5 minutes).

        Returns:
            Authorization code from callback, or None if timeout/error.
        """
        logger.info(f"Starting local redirect server on port {self.port}...")

        try:
            # Create server
            self._server = socketserver.TCPServer(("", self.port), CallbackHandler)

            # Store reference to authorization code in server instance
            self._server.authorization_code = None

            # Run server in background thread with timeout
            def serve():
                logger.muted("Waiting for OAuth callback...")
                # Handle one request (the callback), then stop
                self._server.handle_request()

            server_thread = threading.Thread(target=serve, daemon=True)
            server_thread.start()

            # Wait for callback (or timeout)
            server_thread.join(timeout=timeout)

            # Get the authorization code from server instance
            if hasattr(self._server, "authorization_code"):
                self.authorization_code = self._server.authorization_code

            if self.authorization_code:
                logger.success("Received authorization code from callback")
                return self.authorization_code
            else:
                logger.error("Timeout waiting for OAuth callback")
                return None

        except OSError as e:
            logger.error(f"Failed to start redirect server: {e}")
            logger.info(f"Make sure port {self.port} is not already in use")
            return None
        finally:
            if self._server:
                self._server.server_close()
