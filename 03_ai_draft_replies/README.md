# AI Draft Replies Server

Simple MCP server for creating AI-powered draft replies using Claude to analyze conversation context.

## Additional Setup

In addition to Gmail credentials, you'll need an Anthropic API key.

Get your API key at: [https://console.anthropic.com/](https://console.anthropic.com/)

Add to your `.env` file:
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

## Testing with MCP Inspector

```bash
source .env
npx @modelcontextprotocol/inspector python3 03_ai_draft_replies/server.py
```

## Using with Claude Desktop

```json
{
  "mcpServers": {
    "ai-draft-replies": {
      "command": "python",
      "args": ["/absolute/path/to/03_ai_draft_replies/server.py"],
      "env": {
        "GMAIL_USER": "your-email@gmail.com",
        "GMAIL_APP_PASSWORD": "your-app-password",
        "ANTHROPIC_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

After updating the config, restart Claude Desktop.

## Tool

**create_ai_draft_replies**
- Creates AI-powered draft replies for all unread emails
- Parameters:
  - `context_limit` (number, optional): Number of emails to include in thread context (default: 10)
- Uses Claude to analyze conversation history and generate contextual replies
- Returns: Count of drafts created and list of recipients
