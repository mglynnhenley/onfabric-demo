# OAuth Configuration TODO

Before this can work with real OnFabric:

## 1. Update OAuth Configuration

Update `fabric_dashboard/mcp/oauth_config.py` with real values:

- **client_id**: Get from OnFabric when you register your app
- **authorization_url**: Real OnFabric OAuth authorization endpoint
  - Example: `https://app.onfabric.com/oauth/authorize`
- **token_url**: Real OnFabric OAuth token endpoint
  - Example: `https://api.onfabric.com/oauth/token`
- **scopes**: Correct OAuth scopes for MCP access
  - Check OnFabric docs for required scopes

## 2. Register App with OnFabric

Contact OnFabric or use their developer portal to:

1. Register "Fabric Dashboard" as an OAuth application
2. Provide redirect URI: `http://localhost:8080/callback`
3. Receive your `client_id` (and `client_secret` if needed)
4. Document the required OAuth scopes for MCP access

## 3. Test OAuth Flow

Once real credentials are configured:

```bash
# Run the auth command
fabric-dashboard auth
```

**Expected behavior:**
1. ✅ Browser opens to real OnFabric login page
2. ✅ User logs in successfully
3. ✅ OnFabric redirects to `http://localhost:8080/callback?code=...`
4. ✅ Local server captures authorization code
5. ✅ Code is exchanged for access token
6. ✅ Token is saved to `.env` file
7. ✅ Success message displayed

## 4. Verify Token Usage

Test that saved token works for MCP connections:

```python
from fabric_dashboard.mcp.client import MCPClient

client = MCPClient('onfabric')
success = client.connect()

print(f'Connected: {success}')
print(f'Authenticated: {client.is_authenticated()}')
print(f'Token: {client.access_token[:10]}...' if client.access_token else 'No token')
```

**Expected:**
- `Connected: True`
- `Authenticated: True`
- `Token: abc123...`

## 5. Implement Real MCP Connection

Once OAuth is working, update `MCPClient.connect()` and `call_tool()`:

1. **In `connect()`**: Use access_token to establish real MCP connection
   - Replace TODO comment with actual `langchain-mcp` connection code
   - Pass token to MCP server for authentication

2. **In `call_tool()`**: Add Authorization header to API requests
   ```python
   headers = {
       "Authorization": f"{self.token_type} {self.access_token}"
   }
   ```

## 6. Token Refresh (Optional)

If OnFabric provides refresh tokens:

1. Store `refresh_token` from OAuth response (already done in `TokenStorage`)
2. Implement token refresh logic in `MCPClient`:
   - Detect when access token expires
   - Use refresh token to get new access token
   - Update stored token in `.env`

## Current Status

- ✅ OAuth flow implementation complete
- ✅ Token storage working
- ✅ CLI command functional
- ✅ MCP client loads tokens
- ⏸️ **Blocked on**: Real OnFabric OAuth credentials
- ⏸️ **Next step**: Contact OnFabric for client_id and endpoints
