# MCP Workshop - Simple Email Server

### 1. Configure Gmail App Password

To send emails via Gmail, you need to create an App Password:

1. Go to your Google Account settings
2. Enable 2-Factor Authentication (if not already enabled)
3. Go to Security → App Passwords
4. Generate a new app password for "Mail"
5. Save this password - you'll need it below

### 2. Set Environment Variables

Create a `.env` file or export these variables:

```bash
export GMAIL_USER="your-email@gmail.com"
export GMAIL_APP_PASSWORD="your-app-password"
```

### 3. Test it with MCP_Inspector

```bash
npx @modelcontextprotocol/inspector python3 01_send_email/server.py
```

## Using with Claude Desktop

To use this server with Claude Desktop, add this to your Claude config:

**MacOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "email": {
      "command": "python",
      "args": ["/absolute/path/to/servers/email/server.py"],
      "env": {
        "GMAIL_USER": "your-email@gmail.com",
        "GMAIL_APP_PASSWORD": "your-app-password"
      }
    }
  }
}
```

After updating the config, restart Claude Desktop.
