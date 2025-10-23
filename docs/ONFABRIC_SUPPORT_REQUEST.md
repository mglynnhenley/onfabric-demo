# OnFabric Support Request - Enable Device Code Flow

## Current Status

✅ **OAuth Device Code Flow implementation is COMPLETE and tested**
❌ **Blocked on**: Client not authorized for Device Code Flow on Auth0

## Error Message

```
403 Forbidden
{
  "error": "unauthorized_client",
  "error_description": "Unauthorized or unknown client"
}
```

## What We Need from OnFabric

Please enable **OAuth 2.0 Device Code Flow** (RFC 8628) for the client:

**Client ID**: `UGZtoLYZap8A94TnLcaF37bkXoIsi2Vn`

This client is currently configured for Authorization Code Flow (used by Claude AI), but we need Device Code Flow enabled for CLI/terminal applications.

## Why Device Code Flow?

Device Code Flow is the **industry standard** for CLI and terminal applications:
- Used by: GitHub CLI, AWS CLI, Azure CLI, Google Cloud CLI
- No localhost server needed
- Works on remote machines/SSH
- Better UX for command-line tools
- Specified in RFC 8628

## What We're Building

**Fabric Dashboard CLI** - A command-line tool that:
- Authenticates users to access their OnFabric MCP data
- Generates personalized AI-powered dashboards
- Runs in terminal environments

## Technical Request

In your Auth0 dashboard, please:

1. Navigate to the client with ID: `UGZtoLYZap8A94TnLcaF37bkXoIsi2Vn`
2. Under "Application Type", ensure it's set to "Native" or "Machine to Machine"
3. Enable "Device Code" grant type
4. Alternatively, create a new client specifically for CLI applications with Device Code enabled

## What Happens After You Enable It

Once enabled, our flow will:

1. **Request device code**:
   ```
   POST https://auth.onfabric.io/oauth/device/code
   Content-Type: application/x-www-form-urlencoded

   client_id=UGZtoLYZap8A94TnLcaF37bkXoIsi2Vn
   scope=openid profile email offline_access
   audience=https://api.onfabric.io
   ```

2. **Get response**:
   ```json
   {
     "device_code": "...",
     "user_code": "ABCD-1234",
     "verification_uri": "https://auth.onfabric.io/activate",
     "interval": 5,
     "expires_in": 600
   }
   ```

3. **User authorizes** in browser at verification_uri

4. **Poll for token**:
   ```
   POST https://auth.onfabric.io/oauth/token

   client_id=UGZtoLYZap8A94TnLcaF37bkXoIsi2Vn
   device_code=...
   grant_type=urn:ietf:params:oauth:grant-type:device_code
   ```

5. **Receive access token** and save to user's environment

## Alternative Solution

If you prefer not to modify the existing client, you can:

**Create a new Auth0 client** specifically for CLI applications with:
- Application Type: Native
- Grant Types: Device Code, Refresh Token
- Allowed Scopes: openid, profile, email, offline_access
- Audience: https://api.onfabric.io (if required for MCP access)

Then provide us with the new `client_id`.

## Our Implementation

We've already implemented the complete Device Code Flow:
- ✅ Device code request
- ✅ User code display with instructions
- ✅ Token polling with proper error handling
- ✅ Token storage and refresh
- ✅ All tests passing

**We're ready to go as soon as Device Code is enabled!**

## Contact

If you have any questions or need more details about our use case, please let me know.

## References

- RFC 8628 (Device Authorization Grant): https://datatracker.ietf.org/doc/html/rfc8628
- Auth0 Device Authorization Flow: https://auth0.com/docs/get-started/authentication-and-authorization-flow/device-authorization-flow
