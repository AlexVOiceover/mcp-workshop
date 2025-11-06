# Send Email Server

Simple MCP server for sending emails via Gmail SMTP.

## Setup

### 1. Configure Gmail App Password

Create an App Password at: [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)

### 2. Set Environment Variables

Create a `.env` file in the root directory:

```bash
export GMAIL_USER="your-email@gmail.com"
export GMAIL_APP_PASSWORD="your-app-password"
```

## Testing with MCP Inspector

Load your environment variables and run the inspector:

```bash
source .env
npx @modelcontextprotocol/inspector python3 01_send_email/server.py
```

## Using with Claude Desktop

Add this to your Claude Desktop config:

**MacOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "email": {
      "command": "python",
      "args": ["/absolute/path/to/01_send_email/server.py"],
      "env": {
        "GMAIL_USER": "your-email@gmail.com",
        "GMAIL_APP_PASSWORD": "your-app-password"
      }
    }
  }
}
```

After updating the config, restart Claude Desktop.

## Tool

**send_email**
- Sends an email via Gmail SMTP
- Parameters:
  - `to` (string, required): Recipient email address
  - `subject` (string, required): Email subject line
  - `body` (string, required): Email body content
