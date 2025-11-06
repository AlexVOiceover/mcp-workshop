# MCP Workshop - Simple Email Server

## 1. Configure Gmail App Password

To send emails via Gmail, you need to create an App Password:

[https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)

## 2. Set Environment Variables

Create a `.env` file or export these variables:

```bash
export GMAIL_USER="your-email@gmail.com"
export GMAIL_APP_PASSWORD="your-app-password"
```

## 3. Test it with MCP Inspector

First, load your environment variables:

```bash
source .env
```

Then run the inspector:

```bash
npx @modelcontextprotocol/inspector python3 servers/email/server.py
```

## Using with Claude Desktop

To use this server with Claude Desktop, add this to your Claude config:

- **MacOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

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
