# Retrieve Unread Emails Server

Simple MCP server for reading unread emails via Gmail IMAP.

## Testing with MCP Inspector

```bash
source .env
npx @modelcontextprotocol/inspector python3 02_retrieve_unread/server.py
```

## Using with Claude Desktop

```json
{
  "mcpServers": {
    "inbox": {
      "command": "python",
      "args": ["/absolute/path/to/02_retrieve_unread/server.py"],
      "env": {
        "GMAIL_USER": "your-email@gmail.com",
        "GMAIL_APP_PASSWORD": "your-app-password"
      }
    }
  }
}
```

After updating the config, restart Claude Desktop.

## Tools

**get_unread_emails**
- Retrieves unread emails from Gmail inbox via IMAP
- Parameters:
  - `limit` (number, optional): Maximum number of emails to retrieve (default: 10)
- Returns: List of unread emails with sender, date, subject, and body preview

**create_draft_replies**
- Creates draft replies for all unread emails in your inbox
- Parameters: None
- Returns: Count of drafts created and list of recipients
- The draft text is a placeholder that you can edit in Gmail before sending
